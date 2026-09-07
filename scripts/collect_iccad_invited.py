#!/usr/bin/env python3
"""Recover explicitly invited ICCAD entries using title-font boundaries."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path

from pypdf import PdfReader


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u00ad", "")).strip()


def styled_blocks(page) -> list[tuple[str, str]]:
    """Pair consecutive bold title text with subsequent nonbold body text."""
    blocks = []
    bold, body = [], []

    def visit(text, cm, tm, font, size):
        is_bold = font and "Bold" in str(font.get("/BaseFont", ""))
        if is_bold:
            if body and any(part.strip() for part in body):
                if bold:
                    blocks.append(("".join(bold), "".join(body)))
                bold.clear()
                body.clear()
            bold.append(text)
        elif bold:
            body.append(text)

    page.extract_text(visitor_text=visit)
    if bold:
        blocks.append(("".join(bold), "".join(body)))
    return blocks


def invited_from_blocks(blocks: list[tuple[str, str]], page_number: int) -> list[dict]:
    records = []
    for title_text, body in blocks:
        match = re.fullmatch(r"(\d+):\s+Invited Paper:\s+(.+)", clean(title_text))
        if not match:
            continue
        lines = [clean(line) for line in body.splitlines() if line.strip()]
        if not lines or re.match(r"^(?:\{\d+\}|\d+:\d+)", lines[0]):
            raise ValueError(f"Missing invited author line: {match[1]}")
        author_lines = [lines[0]]
        # Visually reviewed PDF page 105: a bare name wraps without a comma or marker.
        reviewed_wrap = match[1] == "20043"
        if reviewed_wrap:
            if len(lines) < 4 or not (lines[0].endswith("Archana") and lines[1].startswith("Pandey,") and lines[2].endswith("Tanay Karnik") and lines[3] == "Intel, United States"):
                raise ValueError("Invited 20043 differs from reviewed author boundary")
            author_lines = lines[:3]
        for line in ([] if reviewed_wrap else lines[1:]):
            if re.match(r"^\{\d+\}\s+\S", line):
                break
            if author_lines[-1].endswith(",") or re.search(r"\{\d+\}", line):
                author_lines.append(line)
            else:
                break
        authors = [clean(name) for name in " ".join(author_lines).split(",") if clean(name)]
        records.append({"paper_id": f"iccad-2025-{match[1]}", "conference_id": "iccad", "target_edition": 2026,
                        "analysis_edition": 2025, "title": match[2], "authors": authors,
                        "doi_or_identifier": match[1], "publisher_url": None,
                        "program_url": "https://2025.iccad.com/full-program/", "publication_date": None,
                        "collection_date": date.today().isoformat(),
                        "source_id": "iccad-2025-program-pdf-fallback", "program_entry_type": "invited_paper",
                        "regular_paper_comparison_eligible": False, "program_pdf_page": page_number,
                        "program_heading_label": "Invited Paper", "metadata_extraction": "bold_title_boundary_and_wrapped_author_lines",
                        "access_status": "official_fallback_program_pdf_metadata_only", "problem": None,
                        "method_or_artifact": None, "workload_or_benchmark": None, "baselines": [], "metrics": [],
                        "theme_id": None, "subtheme_id": None, "subsubtheme_id": None,
                        "classification_confidence": "not_classified",
                        "limits": "Official invited-paper metadata only; invited label separated from title. Not a regular-paper comparison entry, technical coding, or independent review. Author affiliation markers retained."})
    return records


def extract_invited(reader: PdfReader) -> list[dict]:
    records = [row for index, page in enumerate(reader.pages[37:], 38)
               for row in invited_from_blocks(styled_blocks(page), index)]
    identifiers = [row["paper_id"] for row in records]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Duplicate invited-paper ID")
    return sorted(records, key=lambda row: row["paper_id"])


def build(root: Path, integrate: bool = False) -> dict:
    source = root / "iccad/data/raw/ICCAD_2025_Program_v8.pdf"
    audit = json.loads((root / "iccad/data/program-scope-audit-v1.json").read_text())
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != audit["source_sha256"]:
        raise ValueError("PDF differs from scope-audited source")
    records = extract_invited(PdfReader(source))
    expected = {row["paper_id"] for row in audit["headings"] if row["observed_entry_type"] == "invited_paper"}
    if {row["paper_id"] for row in records} != expected:
        raise ValueError("Styled extraction does not match audited invited IDs")
    if integrate:
        output = root / "iccad/data/papers-2025-program.jsonl"
        existing = {row["paper_id"]: row for row in map(json.loads, output.read_text().splitlines())}
        for row in records:
            prior = existing.get(row["paper_id"])
            if prior and any(prior.get(key) != row.get(key) for key in ["title", "authors", "program_entry_type"]):
                raise ValueError("Invited entry conflicts with existing metadata")
            existing.setdefault(row["paper_id"], row)
        output.write_text("".join(json.dumps(existing[key], ensure_ascii=False, sort_keys=True) + "\n" for key in sorted(existing)))
    return {"source_sha256": digest, "record_count": len(records), "integrated": integrate, "records": records}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--integrate", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build(args.root, args.integrate), indent=2, ensure_ascii=False))
