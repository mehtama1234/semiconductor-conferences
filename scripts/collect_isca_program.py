#!/usr/bin/env python3
"""Collect ISCA 2026 paper/session/author metadata from the official program page."""
from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen


URL = "https://www.iscaconf.org/isca2026/program/"
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def clean(fragment: str) -> str:
    return SPACE_RE.sub(" ", html.unescape(TAG_RE.sub(" ", fragment))).strip()


def collect(root: Path) -> dict:
    request = Request(URL, headers={"User-Agent": "semiconductor-conferences-research/0.1"})
    with urlopen(request, timeout=45) as response:
        source = response.read().decode("utf-8", errors="replace")
    raw_path = root / "isca/data/raw/program-2026.html"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(source, encoding="utf-8")
    records = []
    pattern = re.compile(r'<div class="paper-title">(.*?)</div>\s*<div class="paper-authors">(.*?)</div>', re.S)
    for index, match in enumerate(pattern.finditer(source), start=1):
        prefix = source[:match.start()]
        session_matches = list(re.finditer(r'<h4 class="panel-title">\s*<a[^>]*>(.*?)</a>', prefix, re.S))
        time_matches = list(re.finditer(r'<div class="paper-time">(.*?)</div>', prefix, re.S))
        title = clean(match.group(1))
        authors_display = clean(match.group(2))
        authors = [clean(name) for name in re.findall(r"([^,]+?)\s*\([^)]*\)(?:,|$)", authors_display)]
        records.append({
            "paper_id": f"isca-2026-program-{index:03d}",
            "conference_id": "isca",
            "target_edition": 2026,
            "analysis_edition": 2026,
            "title": title,
            "doi_or_identifier": f"ISCA2026-PROGRAM-{index:03d}",
            "authors": authors,
            "authors_display": authors_display,
            "session_title": clean(session_matches[-1].group(1)) if session_matches else None,
            "program_time": clean(time_matches[-1].group(1)) if time_matches else None,
            "program_url": URL,
            "publisher_url": None,
            "collection_date": date.today().isoformat(),
            "access_status": "official_program_metadata_only",
            "record_status": "program_metadata_only",
            "problem": None,
            "method_or_artifact": None,
            "workload_or_benchmark": None,
            "baselines": [],
            "metrics": [],
            "theme_id": None,
            "subtheme_id": None,
            "subsubtheme_id": None,
            "classification_confidence": "not_classified",
            "limits": "Official program title, author, session, and time metadata only; abstract/full text and technical fields require separate collection.",
            "source_id": "isca-2026-program",
        })
    output = root / "isca/data/papers-2026-program.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return {"paper_count": len(records), "output": str(output), "raw_capture": str(raw_path), "source_url": URL}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(collect(args.root), indent=2, sort_keys=True))
