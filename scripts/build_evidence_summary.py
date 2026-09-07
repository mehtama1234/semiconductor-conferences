#!/usr/bin/env python3
"""Build a transparent coverage summary for the adjudicated evidence sample."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


PATHS = (
    "dac/data/adjudicated-2025-batch.jsonl",
    "dac/data/adjudicated-2026-batch.jsonl",
    "dac/data/adjudicated-2026-batch-2.jsonl",
    "dac/data/adjudicated-2026-batch-3.jsonl",
    "dac/data/adjudicated-2026-batch-4.jsonl",
    "iccad/data/adjudicated-2025-batch.jsonl",
    "iccad/data/adjudicated-2025-batch-2.jsonl",
    "iccad/data/adjudicated-2025-batch-3.jsonl",
    "iccad/data/adjudicated-2025-batch-4.jsonl",
    "iccad/data/adjudicated-2025-batch-5.jsonl",
    "iccad/data/adjudicated-2025-batch-6.jsonl",
    "iccad/data/adjudicated-2025-batch-7.jsonl",
    "iccad/data/adjudicated-2025-batch-8.jsonl",
    "iccad/data/adjudicated-2025-batch-9.jsonl",
    "iccad/data/adjudicated-2025-batch-10.jsonl",
    "iccad/data/adjudicated-2025-batch-11.jsonl",
    "isca/data/adjudicated-2026-batch.jsonl",
    "isca/data/adjudicated-2026-batch-2.jsonl",
    "isca/data/adjudicated-2026-batch-3.jsonl",
    "isca/data/adjudicated-2026-batch-4.jsonl",
    "isca/data/adjudicated-2026-batch-5.jsonl",
    "isca/data/adjudicated-2026-batch-6.jsonl",
    "isca/data/adjudicated-2026-batch-7.jsonl",
    "isca/data/adjudicated-2026-batch-8.jsonl",
    "isca/data/adjudicated-2026-batch-9.jsonl",
)
REQUIRED_TECHNICAL_FIELDS = (
    "problem",
    "method_or_artifact",
    "workload_or_benchmark",
    "baselines",
    "metrics",
    "limits",
)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def source_tier(record: dict) -> str:
    confidence = record.get("classification_confidence", "")
    if "primary" in confidence or "author_pdf" in confidence:
        return "primary_or_author_copy"
    if confidence == "medium_official_description" or record.get("evidence_source") == "dac-2026-presentation-page":
        return "official_description"
    if confidence == "medium_institutional_abstract":
        return "institutional_abstract"
    if confidence == "medium_company_author_source":
        return "company_author_source"
    return "other"


def build(root: Path) -> tuple[dict, str]:
    records = [record for relative in PATHS for record in read_jsonl(root / relative)]
    by_conference: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_conference[record["conference_id"]].append(record)
    theme_counts = Counter(record["theme_id"] for record in records)
    subtheme_counts = Counter((record["theme_id"], record["subtheme_id"]) for record in records)
    source_counts = Counter(source_tier(record) for record in records)
    missing_counts = Counter(
        field
        for record in records
        for field in REQUIRED_TECHNICAL_FIELDS
        if not record.get(field)
    )
    metric_counts = Counter(
        str(metric).split()[0].lower().rstrip(".,")
        for record in records
        for metric in record.get("metrics", [])
        if metric
    )
    summary = {
        "summary_version": "v1-adjudicated-evidence-coverage",
        "as_of": "2026-09-06",
        "record_count": len(records),
        "selection_warning": "This is a selected adjudication sample, not a conference prevalence estimate or market forecast.",
        "conference_counts": {conference: len(rows) for conference, rows in sorted(by_conference.items())},
        "source_tier_counts": dict(sorted(source_counts.items())),
        "theme_counts": dict(sorted(theme_counts.items())),
        "subtheme_counts": {f"{theme}/{subtheme}": count for (theme, subtheme), count in sorted(subtheme_counts.items())},
        "missing_field_counts": dict(sorted(missing_counts.items())),
        "records_with_all_required_technical_fields": sum(
            all(record.get(field) for field in REQUIRED_TECHNICAL_FIELDS) for record in records
        ),
        "distinct_subsubtheme_count": len({record["subsubtheme_id"] for record in records}),
        "metric_token_leaders": dict(metric_counts.most_common(15)),
        "unreviewed_adversarial_judge_count": len(records),
        "limits": [
            "Official descriptions and abstracts compress experimental conditions; numerical comparisons still require paper/table review.",
            "The adjudication sample is selected for recoverable evidence and diversity, so theme counts cannot be read as venue-wide frequencies.",
            "The deterministic preflight does not replace independent adversarial LLM or human judgment.",
        ],
    }
    lines = [
        "# Adjudicated evidence coverage — v1",
        "",
        "This report audits the current adjudication sample. It is not a",
        "conference prevalence estimate, market forecast, or ranking.",
        "",
        "## Coverage",
        "",
        "| Conference | Records |",
        "|---|---:|",
    ]
    for conference, count in summary["conference_counts"].items():
        lines.append(f"| {conference} | {count} |")
    lines += [
        "",
        "| Evidence tier | Records |",
        "|---|---:|",
    ]
    for tier, count in summary["source_tier_counts"].items():
        lines.append(f"| {tier} | {count} |")
    lines += ["", "## Theme distribution", "", "| Theme | Selected records |", "|---|---:|"]
    for theme, count in sorted(theme_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {theme} | {count} |")
    lines += [
        "",
        "## Field completeness",
        "",
        f"{summary['records_with_all_required_technical_fields']} of {len(records)} records have all required technical fields populated.",
        "Missing-field counts are recorded in the machine-readable JSON; an empty field means the evidence did not support a claim, not that the paper lacks the property.",
        "",
        "## Limits",
        "",
    ]
    lines.extend(f"- {limit}" for limit in summary["limits"])
    return summary, "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    summary, report = build(args.root)
    (args.root / "reports/evidence-summary-v1.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.root / "reports/evidence-summary-v1.md").write_text(report, encoding="utf-8")
    print(json.dumps({"record_count": summary["record_count"], "conference_counts": summary["conference_counts"], "source_tier_counts": summary["source_tier_counts"]}, indent=2, sort_keys=True))
