#!/usr/bin/env python3
"""Compare numbered metadata using the same styled extractor for both PDFs."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader

from scripts.collect_iccad_invited import styled_blocks, invited_from_blocks, clean
from scripts.collect_isca_crossref_metadata import title_key


def extract(reader) -> dict:
    result = {}
    for number, page in enumerate(reader.pages[36:], 37):
        for heading, body in styled_blocks(page):
            match = re.match(r"^(\d+):\s+(.+)$", clean(heading))
            if not match:
                continue
            title = match[2].removeprefix("Invited Paper:").strip()
            # Reuse the title/body author-boundary parser only, not its invited classification.
            parsed = invited_from_blocks([(f"{match[1]}: Invited Paper: {title}", body)], number)[0]
            key = parsed["paper_id"]
            if key in result:
                raise ValueError(f"Duplicate numbered ID: {key}")
            result[key] = {"title": title, "authors_with_markers": parsed["authors"], "pdf_page": number}
    return result


def author_names(authors: list[str]) -> list[str]:
    return [title_key(re.sub(r"^and\s+", "", re.sub(r"\{\s*\d+\s*\}", "", name).strip())) for name in authors]


def compare(old: dict, new: dict) -> dict:
    changes = []
    for key in sorted(old.keys() & new.keys()):
        before, after = old[key], new[key]
        fields = [field for field in ["title", "authors_with_markers", "pdf_page"] if before[field] != after[field]]
        if fields:
            changes.append({"paper_id": key, "changed_fields": fields, "before": before, "after": after,
                            "normalized_title_changed": title_key(before["title"]) != title_key(after["title"]),
                            "normalized_author_names_changed": author_names(before["authors_with_markers"]) != author_names(after["authors_with_markers"])})
    return {"old_numbered_count": len(old), "new_numbered_count": len(new),
            "added_ids": sorted(new.keys() - old.keys()), "removed_ids": sorted(old.keys() - new.keys()),
            "normalized_title_change_count": sum(row["normalized_title_changed"] for row in changes),
            "author_field_change_count": sum("authors_with_markers" in row["changed_fields"] for row in changes),
            "normalized_author_name_change_count": sum(row["normalized_author_names_changed"] for row in changes),
            "changes": changes}


def build(root: Path) -> dict:
    sources, extracted = {}, {}
    for version in [8, 20]:
        path = root / f"iccad/data/raw/ICCAD_2025_Program_v{version}.pdf"
        reader = PdfReader(path)
        sources[str(version)] = {"path": str(path.relative_to(root)), "page_count": len(reader.pages),
                                 "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                                 "url": f"https://confcats-event-sessions.s3.us-east-1.amazonaws.com/iccad25/uploads/ICCAD_2025_Program_v{version}.pdf"}
        extracted[version] = extract(reader)
    result = {"schema": "iccad-program-version-comparison.v1", "assessment_date": "2026-09-06",
              "sources": sources, **compare(extracted[8], extracted[20]),
              "inventory_policy": "Retain v8-backed inventory and corrections; reconcile v20 author changes through a versioned overlay before updating canonical identities.",
              "limits": ["Numbered titles and extracted author fields only; not all program prose, affiliations, workshops or schedules.",
                         "Marker changes do not establish that an author's institution changed without comparing affiliation mappings.",
                         "Matching titles do not verify unchanged manuscripts or technical results.",
                         "Higher filename version is not independently verified publication chronology; preserve exact source URLs and hashes."]}
    (root / "iccad/data/program-v8-v20-comparison-v1.json").write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    print(json.dumps(build(parser.parse_args().root), indent=2, ensure_ascii=False))
