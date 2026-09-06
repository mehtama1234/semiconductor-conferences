#!/usr/bin/env python3
"""Collect DAC 2025 research-program metadata for temporal comparison."""
from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen


DAYS = [f"2025-06-{day:02d}" for day in range(21, 27)]
BASE_URL = "https://62dac.conference-program.com/wp-content/linklings_snippets/wp_program_view_all_{day}.txt"
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")
PRESENTATION_RE = re.compile(
    r'<a data-link-type="full-program_all\.program\.presentations\.(RESEARCH[^.]+)\.presentation" '
    r'href="([^"]+)">(.*?)</a>(.*?)</td>', re.S
)


def text(fragment: str) -> str:
    return SPACE_RE.sub(" ", html.unescape(TAG_RE.sub(" ", fragment))).strip()


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "semiconductor-conferences-research/0.1"})
    with urlopen(request, timeout=45) as response:
        return response.read().decode("utf-8", errors="replace")


def extract(source: str, day: str) -> list[dict]:
    rows = []
    for match in PRESENTATION_RE.finditer(source):
        presentation_id, href, title_fragment, cell_tail = match.groups()
        prefix = source[max(0, match.start() - 5000):match.start()]
        times = re.findall(r'utc_time="([^"]+)"', prefix)
        authors = [text(name) for name in re.findall(r'<a data-link-type="[^"]+\.person"[^>]*>(.*?)</a>', cell_tail, re.S)]
        rows.append({
            "paper_id": f"dac-2025-{presentation_id.lower()}",
            "conference_id": "dac",
            "target_edition": 2025,
            "analysis_edition": 2025,
            "title": text(title_fragment),
            "authors": authors,
            "doi_or_identifier": presentation_id,
            "publisher_url": None,
            "program_url": "https://62dac.conference-program.com" + html.unescape(href),
            "program_day": day,
            "start_time_utc": times[-1] if times else None,
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
                "Official DAC 2025 research-program title, author, session, and time metadata only; "
                "no abstract/full-text technical evidence. Suitable for inventory and temporal "
                "coverage checks, not prevalence or technical conclusions."
            ),
            "source_id": "dac-2025-program",
        })
    return rows


def collect(root: Path) -> dict:
    raw_dir = root / "dac/data/raw/program-2025"
    raw_dir.mkdir(parents=True, exist_ok=True)
    deduped = {}
    for day in DAYS:
        source = fetch(BASE_URL.format(day=day))
        (raw_dir / f"{day}.html").write_text(source, encoding="utf-8")
        for row in extract(source, day):
            deduped[row["doi_or_identifier"]] = row
    output = root / "dac/data/papers-2025-program.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for row in sorted(deduped.values(), key=lambda item: item["doi_or_identifier"]):
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return {"paper_count": len(deduped), "output": str(output), "raw_capture_count": len(DAYS), "source_url": BASE_URL}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(collect(args.root), indent=2, sort_keys=True))
