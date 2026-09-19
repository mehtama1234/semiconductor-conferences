"""Build paper-level evidence dossiers for the canonical direction pages."""
from __future__ import annotations

import json
from pathlib import Path

try:
    from scripts.build_theme_pages import read_current_sample
except ModuleNotFoundError:
    from build_theme_pages import read_current_sample


PAGE_NAMES = {
    "constraints-become-executable": "01-constraints-become-executable-evidence.md",
    "data-movement-as-contract": "02-data-movement-as-contract-evidence.md",
    "reliability-security-upstream": "04-reliability-security-upstream-evidence.md",
    "physical-reality-in-the-loop": "05-physical-reality-in-the-loop-evidence.md",
    "closed-loop-design": "03-closed-loop-design-evidence.md",
    "evaluation-as-research": "06-evaluation-as-research-evidence.md",
}

FIELD_NAMES = {
    "problem": ("problem",),
    "mechanism": ("method_or_artifact",),
    "workload": ("workload_or_benchmark", "workload_or_design_corpus"),
    "hardware": ("hardware_or_process_assumptions", "hardware_or_process"),
    "baselines": ("baselines",),
    "metrics": ("metrics",),
    "limits": ("limits", "limitations"),
    "locator": ("evidence_span", "evidence_locators"),
}


def value(row: dict, names: tuple[str, ...]) -> object:
    for name in names:
        if row.get(name) not in (None, "", [], {}):
            return row[name]
    return "UNKNOWN — not present in the current adjudicated record"


def display(value_: object) -> str:
    if isinstance(value_, list):
        return "; ".join(str(item) for item in value_)
    if isinstance(value_, dict):
        return "; ".join(f"{key}: {val}" for key, val in value_.items())
    return str(value_)


def build(root: Path) -> dict:
    atlas = json.loads((root / "data/long-term-direction-atlas-v1.json").read_text(encoding="utf-8"))
    current = {row['paper_id']: row for row in read_current_sample(root)}
    rows: dict[str, list[tuple[str, dict]]] = {}
    for path in sorted(root.glob("**/data/adjudicated-*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            rows.setdefault(row["paper_id"], []).append((str(path.relative_to(root)), row))

    output_dir = root / "reports/directions/evidence"
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = []
    for direction in atlas["directions"]:
        entries = []
        seen = set()
        for reference in direction["evidence"]:
            paper_id = reference["paper_id"]
            if paper_id in seen:
                continue
            seen.add(paper_id)
            candidates = rows.get(paper_id, [])
            if candidates:
                source_path, row = max(candidates, key=lambda item: sum(value(item[1], aliases) != "UNKNOWN — not present in the current adjudicated record" for aliases in FIELD_NAMES.values()))
            else:
                source_path, row = None, {"paper_id": paper_id, "title": paper_id}
            correction = current.get(paper_id, {}).get('_editorial_correction')
            if correction:
                # Keep the dossier's selected historical candidate intact; the dated
                # correction replaces only explicit fields in the current view.
                historical = row
                row = dict(row)
                row.update(correction['fields'])
                row['_editorial_correction'] = correction
                row['_historical_record'] = historical
            entries.append((reference, source_path, row))

        lines = [
            f"# Evidence dossier — {direction['label']}",
            "",
            "This dossier combines the canonical direction atlas, historical adjudicated records, and dated editorial corrections. It is a source-backed reading aid, not an independent review or a claim that the records are comparable.",
            "",
            f"- Direction page: [{direction['label']}](../{direction['page'].split('/')[-1]})",
            f"- Source direction IDs: `{', '.join(direction.get('source_direction_ids', []))}`",
            f"- Direction status: `{direction['status']}`",
            f"- Independent reviews recorded: `{direction['independent_review_count']}`",
            "",
            "## Reading rule",
            "",
            "`UNKNOWN` means a field is not recorded, not that the paper lacks the condition. Corrections supersede the current displayed fields while historical fields remain expandable. A historical condition-complete label does not establish that a correction has passed condition or independent review.",
            "",
        ]
        for reference, source_path, row in entries:
            paper_id = reference["paper_id"]
            title = row.get("title", paper_id)
            source_url = row.get("evidence_url") or row.get("source_url")
            correction = row.get('_editorial_correction')
            tier = row['_page_source_tier'] if correction else reference['evidence_tier']
            lines += [f"## {title}", "", f"- Paper ID: `{paper_id}`", f"- Conference/edition: `{reference['conference_id']}` / `{reference['edition']}`", f"- Evidence tier: `{tier}`", f"- Ledger record: `{source_path or 'not found in adjudicated ledgers'}`"]
            if correction:
                lines += ['', f'**Current evidence correction — {correction["review_date"]}**', '',
                          correction['reason'], '',
                          'Condition review of this correction and independent acceptance remain pending. The direction mapping is inherited, not revalidated by this update.', '',
                          '[Dated correction register](../../../data/editorial-paper-corrections-v1.json)', '']
            if source_url:
                lines.append(f"- Source: [{source_url}]({source_url})")
            lines += ["", "| Field | Current record |", "|---|---|"]
            for label, key in [("Problem", "problem"), ("Mechanism / artifact", "mechanism"), ("Workload / benchmark", "workload"), ("Hardware / process", "hardware"), ("Baselines", "baselines"), ("Metrics", "metrics"), ("Evidence locator / span", "locator"), ("Limits", "limits")]:
                aliases = ('evidence_locators',) if correction and key == 'locator' else FIELD_NAMES[key]
                text = display(value(row, aliases)).replace("\n", " ").replace('|', '\\|')
                lines.append(f"| {label} | {text} |")
            if correction:
                historical = row['_historical_record']
                lines += ['', '<details markdown="1">', '<summary>Historical captured record — superseded in the current table</summary>', '',
                          f'Historical atlas evidence tier: `{reference["evidence_tier"]}`.', '',
                          '| Field | Historical record |', '|---|---|']
                for label, aliases in FIELD_NAMES.items():
                    old = display(value(historical, aliases)).replace('\n', ' ').replace('|', '\\|')
                    lines.append(f'| {label} | {old} |')
                old_url = historical.get('evidence_url') or historical.get('source_url')
                if old_url:
                    lines += ['', f'[Historical source]({old_url})']
                lines += ['', '</details>', '']
            lines += ["", f"Mapping review status: `{reference.get('mapping_review_status', 'not recorded')}`; independent review status: `{row.get('independent_review_status', 'pending')}`.", ""]

        lines += [
            "## Direction boundary",
            "",
            direction["limits"],
            "",
            "Next evidence action: " + direction["next_evidence_action"],
            "",
        ]
        output = output_dir / PAGE_NAMES[direction["direction_id"]]
        output.write_text("\n".join(lines), encoding="utf-8")
        generated.append(str(output.relative_to(root)))

    index_lines = [
        "# Direction evidence dossiers",
        "",
        "Generated paper-level dossiers for the canonical long-term direction pages. Rebuild with `PYTHONPATH=.:src python3 scripts/build_direction_evidence_pages.py`.",
        "",
        "| Direction | Dossier |",
        "|---|---|",
    ]
    for direction in atlas["directions"]:
        filename = PAGE_NAMES[direction["direction_id"]]
        index_lines.append(f"| {direction['label']} | [{filename}]({filename}) |")
    index_lines.append("")
    (output_dir / "README.md").write_text("\n".join(index_lines), encoding="utf-8")
    generated.append(str((output_dir / "README.md").relative_to(root)))
    return {"schema": "direction-evidence-pages.v1", "status": "generated", "pages": generated}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(build(args.root), indent=2))
