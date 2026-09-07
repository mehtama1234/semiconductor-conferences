#!/usr/bin/env python3
"""Map numbered entries to title/room/chair-identified program sessions."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from pypdf import PdfReader

from scripts.collect_iccad_invited import styled_blocks, clean
from scripts.collect_isca_crossref_metadata import title_key


def map_blocks(pages: list[tuple[int, list[tuple[str, str]]]]) -> list[dict]:
    sessions = []
    current = None
    seen = set()
    for page, blocks in pages:
        for title, body in blocks:
            title = clean(title)
            if title.endswith(" Room"):
                current = {"session_title": title[:-5], "session_pdf_page": page,
                           "chair_label_observed": "Session Chair" in body, "papers": []}
                sessions.append(current)
            elif title.startswith("Session Chair") and current:
                current["chair_label_observed"] = True
            elif match := re.match(r"^(\d+):\s+(.+)$", title):
                if not current or not current["chair_label_observed"]:
                    raise ValueError(f"Numbered entry lacks a room/chair-identified session: {match[1]}")
                paper_id = f"iccad-2025-{match[1]}"
                if paper_id in seen:
                    raise ValueError(f"Duplicate paper ID: {paper_id}")
                seen.add(paper_id)
                invited = match[2].startswith("Invited Paper:")
                student = current["session_title"] == "Student Research Competition (Oral Presentations)"
                special = current["session_title"].startswith("Special Session:")
                if special != invited or (student and invited):
                    raise ValueError(f"Session/entry type conflict: {paper_id}")
                kind = "invited_paper" if invited else "student_research_competition_oral" if student else "regular_paper"
                current["papers"].append({"paper_id": paper_id, "program_pdf_page": page,
                    "title": match[2].removeprefix("Invited Paper:").strip(), "program_entry_type": kind,
                    "regular_paper_comparison_eligible": kind == "regular_paper"})
    return [session for session in sessions if session["papers"]]


def apply_title_author_repairs(records: list[dict], repairs: dict) -> None:
    by_id = {row["paper_id"]: row for row in records}
    for change in repairs["changes"]:
        row = by_id[change["paper_id"]]
        for key in ["title", "authors"]:
            if row[key] not in (change["before"][key], change["after"][key]):
                raise ValueError(f"Metadata differs from reviewed boundary: {change['paper_id']}")
        row.update(change["after"])


def apply_scope(records: list[dict], ledger: dict) -> None:
    by_id = {row["paper_id"]: row for row in records}
    mapped = {paper["paper_id"] for session in ledger["sessions"] for paper in session["papers"]}
    if mapped != set(by_id):
        raise ValueError("Session mapping differs from inventory IDs")
    for session in ledger["sessions"]:
        for paper in session["papers"]:
            row = by_id[paper["paper_id"]]
            if title_key(row["title"]) != title_key(paper["title"]):
                raise ValueError(f"Session title identity mismatch: {paper['paper_id']}")
            if row.get("program_entry_type", paper["program_entry_type"]) != paper["program_entry_type"]:
                raise ValueError(f"Existing type conflicts with session: {paper['paper_id']}")
            row.update({key: paper[key] for key in ["program_pdf_page", "program_entry_type", "regular_paper_comparison_eligible"]})
            row["program_session_title"] = session["session_title"]
            row["program_session_pdf_page"] = session["session_pdf_page"]


def build(root: Path, integrate: bool = False) -> dict:
    source = root / "iccad/data/raw/ICCAD_2025_Program_v8.pdf"
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    audit = json.loads((root / "iccad/data/program-scope-audit-v1.json").read_text())
    if digest != audit["source_sha256"]:
        raise ValueError("Source differs from scope-audited PDF")
    reader = PdfReader(source)
    sessions = map_blocks([(index, styled_blocks(page)) for index, page in enumerate(reader.pages[37:], 38)])
    papers = [paper for session in sessions for paper in session["papers"]]
    counts = Counter(paper["program_entry_type"] for paper in papers)
    ledger = {"schema": "iccad-session-scope.v1", "assessment_date": "2026-09-06",
              "source_id": "iccad-2025-program-pdf-fallback", "source_sha256": digest,
              "record_count": len(papers), "entry_type_counts": dict(sorted(counts.items())),
              "session_count_with_numbered_entries": len(sessions),
              "regular_session_count": sum(all(p["program_entry_type"] == "regular_paper" for p in s["papers"]) for s in sessions),
              "sessions": sessions, "independent_review_status": "pending",
              "limits": ["Session placement establishes program stratum, not technical support or independent acceptance.",
                         "Only sessions containing numbered entries are counted; this is not the complete special-session or workshop count.",
                         "Regular-paper eligibility here addresses program type only, not completeness of evidence or temporal comparability."]}
    output = root / "iccad/data/papers-2025-program.jsonl"
    records = [json.loads(line) for line in output.read_text().splitlines()]
    repairs = json.loads((root / "iccad/data/title-author-repairs-v1.json").read_text())
    if repairs["source_sha256"] != digest:
        raise ValueError("Identity repairs differ from source")
    apply_title_author_repairs(records, repairs)
    apply_scope(records, ledger)
    (root / "iccad/data/session-scope-v1.json").write_text(json.dumps(ledger, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    if integrate:
        output.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in records))
    return {key: value for key, value in ledger.items() if key != "sessions"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--integrate", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build(args.root, args.integrate), indent=2))
