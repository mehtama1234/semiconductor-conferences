"""Expose reviewed version-specific metadata without rewriting the v8 inventory."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


DECISIONS = {
    "iccad-2025-1148": ("duplicate_affiliation_removed", "v8 marker 2 spells Inian Institute of Technology Kharagpur; v20 merges it into marker 1, Indian Institute of Technology Kharagpur. Aritra Hazra and Debdeep Mukhopadhyay markers renumber 3/4 to 2/3 with the same listed departments. No institutional move established."),
    "iccad-2025-44": ("duplicate_affiliation_removed", "Jin Lu changes marker 6 (University of Gerogia, United States) to marker 1 (University of Georgia, United States). Other affiliations remain; this removes a duplicate misspelled entry, not evidence of an institutional move."),
    "iccad-2025-493": ("listed_affiliation_changed", "Ing-Chao Lin changes marker 1 (National Cheng Kung University, Taiwan) to marker 3 (National Yang Ming Chiao Tung University). This is a version-specific program association, not proof of an employment event."),
    "iccad-2025-821": ("name_spelling_corrected", "v8 extracts Micha? Gorywoda; v20 prints Michal Gorywoda. KAIST affiliation and Wanyeong Jung remain. Do not infer a different person."),
    "iccad-2025-20002": ("author_list_expanded", "v8 lists Shao-Yun Fang; v20 lists Da-Wei Huang and Shao-Yun Fang with National Taiwan University of Science and Technology, Taiwan, plus Wen-Hao Liu with NVIDIA, Taiwan. Cause and manuscript history remain unknown."),
    "iccad-2025-803": ("page_locator_changed", "HERCULES moves from PDF page 113 in v8 to 114 in v20; extracted title and authors remain unchanged. Preserve both page locators."),
}
SOURCE_IDS = {"8": "iccad-2025-program-pdf-fallback", "20": "iccad-2025-program-pdf-v20"}
EXPECTED_HASHES = {"8": "982ed4265e233552d328139a853209789ed265151302a707c7568a8aa009ffdf", "20": "3950a2e9d1cccc841e49564a86054710161d6a385d811e3b85c7a209ccfd618a"}


def reconcile(comparison: dict) -> dict:
    if {r["paper_id"] for r in comparison["changes"]} != set(DECISIONS):
        raise ValueError("Version changes differ from reviewed six-entry scope")
    for version, digest in EXPECTED_HASHES.items():
        if comparison["sources"][version]["sha256"] != digest:
            raise ValueError("Program hash differs from reviewed version")
    records = []
    for change in comparison["changes"]:
        kind, explanation = DECISIONS[change["paper_id"]]
        observations = []
        for version, field in [("8", "before"), ("20", "after")]:
            observations.append({"version": version, "source_id": SOURCE_IDS[version],
                                 **comparison["sources"][version], **change[field]})
        records.append({"paper_id": change["paper_id"], "status": "resolved_version_specific_metadata",
                        "decision": kind, "explanation": explanation, "observations": observations,
                        "identity_matching_policy": "Consult both source-bound author lists; do not assume program authors prove manuscript identity.",
                        "independent_review_status": "pending"})
    return {"schema": "iccad-program-version-reconciliation.v1", "assessment_date": "2026-09-06",
            "inventory_policy": "Keep canonical v8 extraction unchanged; provide v20 observations as an explicit source-bound overlay for identity recovery. Never attach a v20 page or author list to the v8 source assertion.",
            "review_basis": "Compared both PDFs' extracted author/affiliation blocks and visually checked v20 PDF pages 40, 57, 59, 61, 112 and 114; v8 invited author line checked on page 59.",
            "limits": ["Researcher metadata reconciliation, not independent acceptance.", "No claims about manuscript changes, employment events or technical trends."],
            "records": records}


def build(root: Path) -> dict:
    comparison = json.loads((root / "iccad/data/program-v8-v20-comparison-v1.json").read_text())
    result = reconcile(comparison)
    (root / "iccad/data/program-version-reconciliation-v1.json").write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    print(json.dumps(build(parser.parse_args().root), indent=2, ensure_ascii=False))
