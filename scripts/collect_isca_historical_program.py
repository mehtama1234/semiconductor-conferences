#!/usr/bin/env python3
"""Collect a historical ISCA program as metadata-only temporal evidence."""
from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen


URL = "https://www.iscaconf.hosting.acm.org/isca2025/program/index.php"
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")
PAPER_RE = re.compile(
    r'<div class="paper-title">(.*?)</div>\s*'
    r'<div class="paper-authors">(.*?)</div>', re.S
)
SESSION_RE = re.compile(r'<h4 class="panel-title">\s*<a[^>]*>(.*?)</a>', re.S)
TIME_RE = re.compile(r'<div class="paper-time">(.*?)</div>', re.S)


def clean(fragment: str) -> str:
    return SPACE_RE.sub(" ", html.unescape(TAG_RE.sub(" ", fragment))).strip()


def collect(root: Path) -> dict:
    request = Request(URL, headers={"User-Agent": "semiconductor-conferences-research/0.1"})
    with urlopen(request, timeout=45) as response:
        source = response.read().decode("utf-8", errors="replace")

    raw_path = root / "isca/data/raw/program-2025.html"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(source, encoding="utf-8")

    records = []
    for index, match in enumerate(PAPER_RE.finditer(source), start=1):
        prefix = source[:match.start()]
        sessions = list(SESSION_RE.finditer(prefix))
        times = list(TIME_RE.finditer(prefix))
        title = clean(match.group(1))
        authors_display = clean(match.group(2))
        records.append({
            "paper_id": f"isca-2025-program-{index:03d}",
            "conference_id": "isca",
            "target_edition": 2025,
            "analysis_edition": 2025,
            "title": title,
            "doi_or_identifier": f"ISCA2025-PROGRAM-{index:03d}",
            "authors": [name.strip() for name in authors_display.split(",") if name.strip()],
            "authors_display": authors_display,
            "session_title": clean(sessions[-1].group(1)) if sessions else None,
            "program_time": clean(times[-1].group(1)) if times else None,
            "program_url": URL,
            "publisher_url": None,
            "collection_date": date.today().isoformat(),
            "access_status": "official_historical_program_metadata_only",
            "record_status": "historical_program_metadata_only",
            "problem": None,
            "method_or_artifact": None,
            "workload_or_benchmark": None,
            "baselines": [],
            "metrics": [],
            "theme_id": None,
            "subtheme_id": None,
            "subsubtheme_id": None,
            "classification_confidence": "not_classified",
            "limits": (
                "Official ISCA 2025 program title, author, session, and time metadata only; "
                "no abstract/full-text technical evidence. Suitable for inventory and temporal "
                "coverage checks, not prevalence or technical conclusions."
            ),
            "source_id": "isca-2025-program",
        })

    output = root / "isca/data/papers-2025-program.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return {"paper_count": len(records), "output": str(output), "raw_capture": str(raw_path), "source_url": URL}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(collect(args.root), indent=2, sort_keys=True))
