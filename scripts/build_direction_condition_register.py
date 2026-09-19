"""Build a condition-completeness register for the canonical direction atlas."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


CONDITION_ALIASES = {
    "workload": ("workload_or_benchmark", "workload_or_design_corpus"),
    "hardware": ("hardware_or_process_assumptions", "hardware_or_process"),
    "baseline": ("baselines",),
    "metrics": ("metrics",),
    "limits": ("limits", "limitations"),
    "locator": ("evidence_span", "evidence_locators"),
}


def _has_value(row: dict, names: tuple[str, ...]) -> bool:
    return any(row.get(name) not in (None, "", [], {}) for name in names)


def build(root: Path) -> dict:
    atlas = json.loads((root / "data/long-term-direction-atlas-v1.json").read_text(encoding="utf-8"))
    evidence_rows: dict[str, list[tuple[str, dict]]] = {}
    for path in sorted(root.glob("**/data/adjudicated-*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            evidence_rows.setdefault(row["paper_id"], []).append((str(path.relative_to(root)), row))
    supplementary = {}
    supplementary_paths = [root / "data/direction-condition-extractions-v1.jsonl"]
    supplementary_paths.extend(sorted(root.glob("**/data/source-condition-extractions-v1.jsonl")))
    for supplementary_path in supplementary_paths:
        if not supplementary_path.exists():
            continue
        for line in supplementary_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row["paper_id"] in supplementary:
                raise ValueError(f"Duplicate supplementary condition extraction: {row['paper_id']}")
            supplementary[row["paper_id"]] = row
    primary_assessments = {}
    primary_path = root / "data/primary-condition-assessments-v1.jsonl"
    if primary_path.exists():
        for line in primary_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                primary_assessments[row["paper_id"]] = row

    queue_rows = {}
    queue_path = root / "data/research-work-queue.jsonl"
    if queue_path.exists():
        for line in queue_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                queue_rows[row["paper_id"]] = row

    direction_rows = []
    for direction in atlas["directions"]:
        papers = []
        references = [(evidence, False) for evidence in direction["evidence"]]
        challenge = direction.get("challenge")
        if challenge and challenge.get("paper_id"):
            challenge_queue = queue_rows.get(challenge["paper_id"], {})
            references.append((
                {
                    "paper_id": challenge["paper_id"],
                    "conference_id": challenge_queue.get("conference_id", "unknown"),
                    "edition": challenge_queue.get("analysis_edition"),
                    "evidence_tier": challenge.get("evidence_tier", challenge_queue.get("evidence_tier", "unknown")),
                    "source_direction_id": None,
                },
                True,
            ))
        for evidence, is_challenge in references:
            candidates = evidence_rows.get(evidence["paper_id"], [])
            # Prefer the row with the greatest number of condition fields. This
            # preserves the source path and does not merge unsupported values.
            if candidates:
                path, row = max(
                    candidates,
                    key=lambda item: sum(_has_value(item[1], aliases) for aliases in CONDITION_ALIASES.values()),
                )
                available = {
                    name: _has_value(row, aliases) for name, aliases in CONDITION_ALIASES.items()
                }
                title = row.get("title", evidence["paper_id"])
                record_status = "adjudicated_record_found"
            else:
                path, row = None, {}
                available = {name: False for name in CONDITION_ALIASES}
                title = evidence["paper_id"]
                record_status = "no_adjudicated_record_found"
            missing = [name for name, present in available.items() if not present]
            supplement = supplementary.get(evidence["paper_id"])
            supplementary_fields = (supplement or {}).get("extracted_fields", {})
            supplementary_available = {
                name: _has_value(supplementary_fields, aliases)
                for name, aliases in CONDITION_ALIASES.items()
            }
            combined_available = {
                name: available[name] or supplementary_available[name]
                for name in CONDITION_ALIASES
            }
            combined_missing = [name for name, present in combined_available.items() if not present]
            primary = primary_assessments.get(evidence["paper_id"])
            papers.append(
                {
                    "paper_id": evidence["paper_id"],
                    "title": title,
                    "conference_id": evidence["conference_id"],
                    "edition": evidence["edition"],
                    "evidence_tier": evidence["evidence_tier"],
                    "source_direction_id": evidence.get("source_direction_id"),
                    "role": "challenge" if is_challenge else "supporting_evidence",
                    "challenge_relation": (challenge or {}).get("relation") if is_challenge else None,
                    "record_path": path,
                    "record_status": record_status,
                    "available_conditions": available,
                    "missing_conditions": missing,
                    "condition_status": "complete" if not missing else "partial",
                    "supplementary_available_conditions": supplementary_available,
                    "combined_available_conditions": combined_available,
                    "combined_missing_conditions": combined_missing,
                    "combined_condition_status": "complete" if not combined_missing else "partial",
                    "supplementary_condition_fields": sorted(supplementary_fields),
                    "supplementary_source_locators": (supplement or {}).get("source_locators", []),
                    "supplementary_evidence_tier": (supplement or {}).get("evidence_tier"),
                    "supplementary_review_status": (supplement or {}).get("independent_review_status"),
                    "primary_assessment_path": (primary or {}).get("assessment_path"),
                    "primary_assessment_source_url": (primary or {}).get("source_url"),
                    "primary_assessment_source_tier": (primary or {}).get("source_tier"),
                    "primary_assessment_review_status": (primary or {}).get("independent_review_status"),
                    "primary_assessment_condition_fields": sorted((primary or {}).get("condition_payload", {}).keys()) if isinstance((primary or {}).get("condition_payload"), dict) else [],
                    "primary_assessment_unresolved_conditions": (primary or {}).get("unresolved_conditions", []),
                    "independent_review_status": row.get("independent_review_status", "pending"),
                    "next_action": (
                        "Extract missing conditions from the permitted primary source and prepare independent review."
                        if missing
                        else "Verify condition spans against the primary source and obtain independent review."
                    ),
                }
            )
        counts = Counter(paper["condition_status"] for paper in papers)
        direction_rows.append(
            {
                "direction_id": direction["direction_id"],
                "label": direction["label"],
                "page": direction["page"],
                "paper_count": len(papers),
                "complete_condition_records": counts["complete"],
                "partial_condition_records": counts["partial"],
                "supplementary_extraction_records": sum(bool(paper["supplementary_condition_fields"]) for paper in papers),
                "primary_assessment_records": sum(bool(paper["primary_assessment_path"]) for paper in papers),
                "independent_review_count": direction["independent_review_count"],
                "papers": papers,
                "next_evidence_action": direction["next_evidence_action"],
            }
        )

    result = {
        "schema": "direction-condition-register.v1",
        "status": "condition_extraction_queue",
        "as_of": atlas["as_of"],
        "source_atlas": "data/long-term-direction-atlas-v1.json",
        "condition_fields": list(CONDITION_ALIASES),
        "supplementary_source": "data/direction-condition-extractions-v1.jsonl" if supplementary_path.exists() else None,
        "primary_assessment_source": "data/primary-condition-assessments-v1.jsonl" if primary_path.exists() else None,
        "directions": direction_rows,
        "interpretation_limits": [
            "Presence of a field means a coded value exists; it does not establish that the value is correct or independently verified.",
            "A missing condition is an extraction gap, not negative evidence about the paper or direction.",
            "Description and preprint evidence remain subject to their recorded evidence tiers.",
        ],
    }
    output = root / "data/direction-condition-register-v1.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Direction condition register v1",
        "",
        "This register converts the canonical direction atlas into a condition-aware extraction queue. It preserves adjudicated-row condition status, separately surfaces supplementary source-condition extractions and primary-paper or artifact assessments, and reports a combined status only as a field-presence view across those explicitly tiered records.",
        "",
        "It is a gap register, not a scientific acceptance report. Missing fields are not negative evidence, and present fields are not independently verified.",
        "",
        "| Direction | Records | Complete | Partial | Supplementary extractions | Primary assessments | Independent reviews |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in direction_rows:
        lines.append(
            f"| [{row['label']}]({row['page'].split('reports/', 1)[-1]}) | {row['paper_count']} | {row['complete_condition_records']} | {row['partial_condition_records']} | {row['supplementary_extraction_records']} | {row['primary_assessment_records']} | {row['independent_review_count']} |"
        )
    lines += ["", "## Priority records", ""]
    priority = []
    for row in direction_rows:
        for paper in row["papers"]:
            if paper["missing_conditions"]:
                priority.append((len(paper["missing_conditions"]), row["label"], paper))
    for missing_count, label, paper in sorted(priority, key=lambda item: (-item[0], item[2]["paper_id"]))[:40]:
        missing = ", ".join(paper["missing_conditions"]) or "none"
        supplement = ", ".join(paper["supplementary_condition_fields"]) or "none"
        role = paper.get("role", "supporting_evidence")
        combined_missing = ", ".join(paper["combined_missing_conditions"]) or "none"
        lines.append(f"- `{paper['paper_id']}` — {label} ({role}); adjudicated missing: {missing}; combined missing: {combined_missing}; supplementary: {supplement}; source: `{paper['record_path'] or 'not yet in adjudicated ledger'}`")
    lines += ["", "## Next action", "", "Run primary-source condition extraction in stable priority order, then regenerate this register and route completed records to independent review. Do not promote a direction based on field presence alone.", ""]
    (root / "reports/direction-condition-register-v1.md").write_text("\n".join(lines), encoding="utf-8")
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = build(args.root)
    print(json.dumps({"status": "built", "directions": len(result["directions"]), "output": "data/direction-condition-register-v1.json"}, indent=2))
