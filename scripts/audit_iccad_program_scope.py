#!/usr/bin/env python3
"""Reconcile numbered official-program headings without inferring full titles/types."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from pypdf import PdfReader

HEADING = re.compile(r"^\s*(\d+):\s+(.+)$")


def reconcile(page_texts: list[str], inventory: list[dict], start_page: int = 38) -> dict:
    by_id = {row["paper_id"]: row for row in inventory}
    headings = []
    seen = set()
    for number, text in enumerate(page_texts, start_page):
        for line in text.splitlines():
            match = HEADING.match(line)
            if not match:
                continue
            paper_id = f"iccad-2025-{match[1]}"
            if paper_id in seen:
                raise ValueError(f"Duplicate numbered heading requires review: {paper_id}")
            seen.add(paper_id)
            row = by_id.get(paper_id)
            prefix = match[2].strip()
            entry_type = "invited_paper" if prefix.startswith("Invited Paper:") else (row or {}).get("program_entry_type", "numbered_entry_type_unresolved")
            headings.append({"paper_id": paper_id, "pdf_page": number,
                             "heading_first_line_not_complete_title": prefix,
                             "observed_entry_type": entry_type,
                             "in_current_inventory": row is not None,
                             "next_action": "Recover complete title/authors and register separately from regular-paper comparisons" if row is None else "Retain invited scope and pursue technical evidence" if entry_type == "invited_paper" else "Retain reviewed SRC scope" if entry_type == "student_research_competition_oral" else "Verify session-level regular-paper classification"})
    return {"numbered_heading_count": len(headings), "current_inventory_count": len(inventory),
            "type_counts": dict(sorted(Counter(row["observed_entry_type"] for row in headings).items())),
            "omitted_ids": [row["paper_id"] for row in headings if not row["in_current_inventory"]],
            "inventory_ids_without_heading": sorted(set(by_id) - seen), "headings": headings}


def build(root: Path) -> dict:
    path = root / "iccad/data/raw/ICCAD_2025_Program_v8.pdf"
    pdf = path.read_bytes()
    reader = PdfReader(path)
    inventory = [json.loads(line) for line in (root / "iccad/data/papers-2025-program.jsonl").read_text().splitlines() if line.strip()]
    result = reconcile([page.extract_text() or "" for page in reader.pages[37:]], inventory)
    result.update({"schema": "iccad-program-scope-audit.v1", "assessment_date": "2026-09-06",
                   "source_id": "iccad-2025-program-pdf-fallback", "source_path": str(path.relative_to(root)),
                   "source_sha256": hashlib.sha256(pdf).hexdigest(), "pdf_pages_scanned": [38, len(reader.pages)],
                   "independent_review_status": "pending",
                   "limits": ["Numbered headings are not a complete census of unnumbered talks, tutorials or workshops.",
                              "Heading first lines are not complete paper titles and must not be used for title-frequency analysis.",
                              "Invited papers are separate from the regular-paper denominator; omitted IDs, if any, require metadata recovery.",
                              "Matching the welcome message's aggregate accepted count does not verify individual entry types."]})
    (root / "iccad/data/program-scope-audit-v1.json").write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    return {key: value for key, value in result.items() if key != "headings"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    print(json.dumps(build(parser.parse_args().root), indent=2))
