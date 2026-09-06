#!/usr/bin/env python3
"""Collect and normalize the public DAC 2026 program snippets.

The conference program publishes one HTML table fragment per day.  This collector
preserves those fragments as raw captures and emits metadata-only records.  It does
not infer paper methods, metrics, or research conclusions from program metadata.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen


DAYS = [f"2026-07-{day:02d}" for day in range(25, 32)]
BASE_URL = "https://63dac.conference-program.com/wp-content/linklings_snippets/wp_program_view_all_{day}.txt?v=1785425165"
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def text(fragment: str) -> str:
    return SPACE_RE.sub(" ", html.unescape(TAG_RE.sub(" ", fragment))).strip()


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "semiconductor-conferences-research/0.1"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def extract_rows(source: str, day: str) -> list[dict]:
    rows: list[dict] = []
    for chunk in source.split("<!-- slot_disp_row START -->")[1:]:
        row_match = re.search(r'<tr class="agenda-item presentation-row[^>]*>(.*?)<!-- slot_disp_row END -->', chunk, re.S)
        if not row_match:
            continue
        row = row_match.group(1)
        title_match = re.search(r'<span class="presentation-title"><a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', row, re.S)
        if not title_match:
            continue
        type_match = re.search(r'<div class="event-type-name [^"]+">(.*?)</div>', row, re.S)
        speaker_match = re.search(r'<span class="presentation-speaker">(.*?)</span>', row, re.S)
        time_match = re.search(r'<span class="dateTimeInfo start-time"[^>]*utc_time="([^"]+)"', row)
        rows.append({
            "presentation_id": re.search(r'psid="([^"]+)"', row).group(1) if re.search(r'psid="([^"]+)"', row) else None,
            "conference_id": "dac",
            "target_edition": 2026,
            "analysis_edition": 2026,
            "program_day": day,
            "title": text(title_match.group(2)),
            "program_url": "https://63dac.conference-program.com" + html.unescape(title_match.group(1)),
            "event_type": text(type_match.group(1)) if type_match else None,
            "contributors_display": text(speaker_match.group(1)) if speaker_match else "",
            "start_time_utc": time_match.group(1) if time_match else None,
            "source_url": BASE_URL.format(day=day),
            "collection_date": date.today().isoformat(),
            "record_status": "program_metadata_only",
            "evidence_limit": "Program metadata only; paper abstract/full text, problem, method, workload, baselines, metrics, and limitations require separate collection.",
        })
    return rows


def extract_research_rows(source: str, day: str) -> list[dict]:
    """Extract nested research presentations from session tables.

    Linklings nests individual manuscripts inside the session row, so these are
    intentionally parsed from their presentation links rather than outer rows.
    """
    rows: list[dict] = []
    pattern = re.compile(
        r'<a data-link-type="full-program_all\.program\.presentations\.(RESEARCH[^.]+)\.presentation" '
        r'href="([^"]+)">(.*?)</a>(.*?)</td>',
        re.S,
    )
    for match in pattern.finditer(source):
        presentation_id, href, title_fragment, cell_tail = match.groups()
        prefix = source[max(0, match.start() - 5000):match.start()]
        time_matches = re.findall(r'utc_time="([^"]+)"', prefix)
        authors = [text(name) for name in re.findall(r'<a data-link-type="[^"]+\.person"[^>]*>(.*?)</a>', cell_tail, re.S)]
        rows.append({
            "presentation_id": presentation_id,
            "conference_id": "dac",
            "target_edition": 2026,
            "analysis_edition": 2026,
            "program_day": day,
            "title": text(title_fragment),
            "program_url": "https://63dac.conference-program.com" + html.unescape(href),
            "event_type": "Research Manuscript",
            "authors": authors,
            "start_time_utc": time_matches[-1] if time_matches else None,
            "source_url": BASE_URL.format(day=day),
            "collection_date": date.today().isoformat(),
            "record_status": "program_metadata_only",
            "evidence_limit": "Program metadata only; paper abstract/full text, problem, method, workload, baselines, metrics, and limitations require separate collection.",
        })
    return rows


def collect(root: Path, days: list[str]) -> dict:
    raw_dir = root / "dac/data/raw/program"
    raw_dir.mkdir(parents=True, exist_ok=True)
    all_rows: list[dict] = []
    for day in days:
        url = BASE_URL.format(day=day)
        source = fetch(url)
        (raw_dir / f"{day}.html").write_text(source, encoding="utf-8")
        all_rows.extend(extract_rows(source, day))
        all_rows.extend(extract_research_rows(source, day))
    deduped: dict[str, dict] = {}
    for row in all_rows:
        key = row["presentation_id"] or row["program_url"]
        deduped[key] = row
    output = root / "dac/data/program-presentations.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for row in sorted(deduped.values(), key=lambda item: (item["program_day"], item["start_time_utc"] or "", item["title"])):
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    research_rows = [row for row in deduped.values() if row["event_type"] == "Research Manuscript"]
    normalized_output = root / "dac/data/papers-2026-program.jsonl"
    with normalized_output.open("w", encoding="utf-8") as handle:
        for row in sorted(research_rows, key=lambda item: item["presentation_id"]):
            normalized = {
                "paper_id": f"dac-2026-{row['presentation_id'].lower()}",
                "conference_id": "dac",
                "target_edition": 2026,
                "analysis_edition": 2026,
                "title": row["title"],
                "authors": row.get("authors", []),
                "doi_or_identifier": row["presentation_id"],
                "publisher_url": None,
                "program_url": row["program_url"],
                "publication_date": None,
                "collection_date": row["collection_date"],
                "access_status": "official_program_metadata_only",
                "problem": None,
                "method_or_artifact": None,
                "workload_or_benchmark": None,
                "baselines": [],
                "metrics": [],
                "theme_id": None,
                "subtheme_id": None,
                "subsubtheme_id": None,
                "classification_confidence": "not_classified",
                "limits": row["evidence_limit"],
                "source_id": "dac-2026-program",
            }
            handle.write(json.dumps(normalized, ensure_ascii=False, sort_keys=True) + "\n")
    return {"days": days, "raw_capture_count": len(days), "presentation_count": len(deduped), "research_paper_count": len(research_rows), "output": str(output), "normalized_output": str(normalized_output)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--day", action="append", dest="days", help="collect one YYYY-MM-DD day; repeatable")
    args = parser.parse_args()
    print(json.dumps(collect(args.root, args.days or DAYS), indent=2, sort_keys=True))
