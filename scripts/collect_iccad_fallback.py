#!/usr/bin/env python3
"""Collect ICCAD 2025 fallback paper metadata from the official program PDF."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from pypdf import PdfReader
from scripts.collect_iccad_invited import extract_invited


PDF_URL = "https://confcats-event-sessions.s3.us-east-1.amazonaws.com/iccad25/uploads/ICCAD_2025_Program_v8.pdf"
PAPER_LINE = re.compile(r"^\s*(\d{1,4}):\s+(.+)$")
TIME_LINE = re.compile(r"^\s*\d{1,2}:\d{2}\s*$")


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\u00ad", "")).strip()


def fetch_pdf() -> bytes:
    request = Request(PDF_URL, headers={"User-Agent": "semiconductor-conferences-research/0.1"})
    with urlopen(request, timeout=90) as response:
        return response.read()


def extract_papers(pdf: bytes) -> list[dict]:
    reader = PdfReader(BytesIO(pdf))
    # The official table of contents places the technical program on PDF pages 38–129.
    lines = "\n".join((page.extract_text() or "") for page in reader.pages[37:128]).splitlines()
    records = extract_program_lines(lines)
    corrections = json.loads((Path(__file__).resolve().parents[1] / "iccad/data/src-entry-reconciliation-v1.json").read_text())
    if hashlib.sha256(pdf).hexdigest() == corrections["source_sha256"]:
        apply_src_corrections(records, corrections)
    invited = extract_invited(reader)
    if {row["paper_id"] for row in records} & {row["paper_id"] for row in invited}:
        raise ValueError("Invited and legacy extraction IDs overlap")
    return sorted(records + invited, key=lambda row: row["paper_id"])


def apply_src_corrections(records: list[dict], corrections: dict) -> None:
    by_id = {row["paper_id"]: row for row in records}
    for correction in corrections["changes"]:
        row = by_id[correction["paper_id"]]
        before, after = correction["before"], correction["after"]
        if row["title"] not in (before["title"], after["title"]):
            raise ValueError("SRC title differs from reviewed source")
        if row["authors"] not in (before["authors"], after["authors"]):
            raise ValueError("SRC authors differ from reviewed source")
        row.update(after)


def extract_program_lines(lines: list[str]) -> list[dict]:
    """Keep wrapped authors, stopping before numbered affiliation blocks."""
    papers: list[dict] = []
    current: dict | None = None
    for line in lines + [""]:
        match = PAPER_LINE.match(line)
        if match and not TIME_LINE.match(line):
            if current:
                papers.append(current)
            current = {"identifier": match.group(1), "title_lines": [clean(match.group(2))], "author_line": None}
            continue
        if current is None:
            continue
        stripped = clean(line)
        if not stripped:
            if current.get("author_line"):
                papers.append(current)
                current = None
            continue
        if current.get("author_line") is None and ("," in stripped or re.search(r"\{\d+\}", stripped)):
            current["author_line"] = stripped
        elif current.get("author_line") is None:
            current["title_lines"].append(stripped)
        elif not current.get("authors_finished"):
            affiliation = re.match(r"^\{\d+\}\s+\S", stripped)
            continuation = re.search(r"\{\d+\}", stripped) or current["author_line"].endswith(",")
            if continuation and not affiliation:
                current["author_line"] += " " + stripped
            else:
                current["authors_finished"] = True
    deduped: dict[str, dict] = {}
    for item in papers:
        identifier = item["identifier"]
        title = clean(" ".join(item["title_lines"]))
        author_line = item.get("author_line") or ""
        authors = [clean(part) for part in author_line.split(",") if clean(part)]
        deduped[identifier] = {
            "paper_id": f"iccad-2025-{identifier}",
            "conference_id": "iccad",
            "target_edition": 2026,
            "analysis_edition": 2025,
            "title": title,
            "authors": authors,
            "doi_or_identifier": identifier,
            "publisher_url": None,
            "program_url": "https://2025.iccad.com/full-program/",
            "publication_date": None,
            "collection_date": date.today().isoformat(),
            "access_status": "official_fallback_program_pdf_metadata_only",
            "problem": None,
            "method_or_artifact": None,
            "workload_or_benchmark": None,
            "baselines": [],
            "metrics": [],
            "theme_id": None,
            "subtheme_id": None,
            "subsubtheme_id": None,
            "classification_confidence": "not_classified",
            "limits": "Title and author metadata extracted from the official ICCAD 2025 fallback program PDF. Abstract/full text and technical evidence are not yet collected; 2025 is not a substitute for the 2026 target corpus.",
            "source_id": "iccad-2025-program-pdf-fallback",
        }
    return [deduped[key] for key in sorted(deduped)]


def collect(root: Path) -> dict:
    raw_path = root / "iccad/data/raw/ICCAD_2025_Program_v8.pdf"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    pdf = fetch_pdf()
    raw_path.write_bytes(pdf)
    rows = extract_papers(pdf)
    output = root / "iccad/data/papers-2025-program.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return {"source_url": PDF_URL, "paper_count": len(rows), "output": str(output), "raw_capture": str(raw_path)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(collect(args.root), indent=2, sort_keys=True))
