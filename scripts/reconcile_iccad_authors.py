#!/usr/bin/env python3
"""Repair only author fields from the retained official program capture."""
import hashlib
import json
from pathlib import Path

from collect_iccad_fallback import PDF_URL, extract_papers


def reconcile(root: Path) -> dict:
    path = root / "iccad/data/papers-2025-program.jsonl"
    pdf = (root / "iccad/data/raw/ICCAD_2025_Program_v8.pdf").read_bytes()
    old = [json.loads(line) for line in path.read_text().splitlines()]
    new = {row["paper_id"]: row for row in extract_papers(pdf)}
    assert set(new) == {row["paper_id"] for row in old}
    assert all(row["title"] == new[row["paper_id"]]["title"] for row in old)
    changes = []
    for row in old:
        authors = new[row["paper_id"]]["authors"]
        if row["authors"] != authors:
            changes.append({"paper_id": row["paper_id"], "before": row["authors"], "after": authors})
            row["authors"] = authors
    report = {"schema": "metadata-reconciliation.v1", "assessment_date": "2026-09-06",
              "source_url": PDF_URL, "source_sha256": hashlib.sha256(pdf).hexdigest(),
              "scope": "Author wrapping repair only; IDs, titles, dates and evidence fields preserved. Not a new source capture or independent identity review.",
              "record_count": len(old), "changes": changes}
    if changes:
        path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in old))
        (root / "iccad/data/author-reconciliation-v1.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return {"record_count": len(old), "changed_authors": len(changes)}


if __name__ == "__main__":
    print(json.dumps(reconcile(Path(__file__).resolve().parents[1])))
