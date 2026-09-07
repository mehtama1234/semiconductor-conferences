"""Materialize a bounded theme/subtheme evidence matrix from the direction map."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def build(root: Path) -> dict:
    source = root / "data/technology-direction-evidence-v1.json"
    payload = json.loads(source.read_text(encoding="utf-8"))
    rows = []
    for direction in payload["directions"]:
        evidence = direction.get("evidence", [])
        tiers = Counter(item.get("evidence_tier", "unknown") for item in evidence)
        conferences = Counter(item.get("conference_id", "unknown") for item in evidence)
        rows.append(
            {
                "direction_id": direction["direction_id"],
                "label": direction["label"],
                "subskills": direction.get("subskills", []),
                "evidence_count": len(evidence),
                "evidence_tiers": dict(sorted(tiers.items())),
                "conference_counts": dict(sorted(conferences.items())),
                "primary_or_artifact_count": sum(
                    tier in {"primary_preprint", "primary_author_paper", "artifact", "company_author_source"}
                    for tier in (item.get("evidence_tier") for item in evidence)
                ),
                "independent_review_count": sum(
                    item.get("mapping_review_status") == "independent_reviewed" for item in evidence
                ),
                "limits": direction.get("limits", ""),
                "status": "provisional_mechanism_evidence",
            }
        )
    result = {
        "schema": "theme-evidence-matrix.v1",
        "status": "provisional_mechanism_evidence_only",
        "as_of": payload.get("as_of"),
        "source": "data/technology-direction-evidence-v1.json",
        "selection_warning": payload["selection_warning"],
        "rows": rows,
        "interpretation_limits": [
            "Counts are selected evidence references, not paper prevalence or temporal trend estimates.",
            "Primary or artifact evidence is not independent validation.",
            "Subskills are mechanism labels; they do not imply a shared benchmark or comparable magnitude.",
        ],
    }
    (root / "data/theme-evidence-matrix-v1.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# Theme evidence matrix v1",
        "",
        "This matrix is generated from the provisional technology-direction map. It organizes themes, subskills, evidence tiers, and limits; it is not a prevalence or trend estimate.",
        "",
        "| Theme | Evidence refs | Primary/artifact refs | Independent reviews | Main subskills |",
        "|---|---:|---:|---:|---|",
    ]
    for row in sorted(rows, key=lambda item: item["direction_id"]):
        skills = "; ".join(row["subskills"][:4])
        lines.append(
            f"| {row['label']} | {row['evidence_count']} | {row['primary_or_artifact_count']} | {row['independent_review_count']} | {skills} |"
        )
    lines += [
        "",
        "## Reading rule",
        "",
        "Use this as a routing and synthesis layer. A direction can be described as a recurring capability mechanism only when its cited records support that mechanism. Directional claims require comparable temporal coding and independent review; neither is implied by this matrix.",
        "",
    ]
    (root / "reports/theme-evidence-matrix-v1.md").write_text("\n".join(lines), encoding="utf-8")
    return {"row_count": len(rows), "output": "data/theme-evidence-matrix-v1.json"}


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    print(json.dumps(build(root), indent=2, sort_keys=True))
