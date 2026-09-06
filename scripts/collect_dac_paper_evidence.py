#!/usr/bin/env python3
"""Fetch DAC 2026 research presentation pages and preserve their descriptions."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

from scripts.normalize_dac_capture_labels import normalize


SPACE_RE = re.compile(r"\s+")


def clean(fragment: str) -> str:
    class TextParser(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.parts = []

        def handle_data(self, data):
            self.parts.append(data)

        def handle_starttag(self, tag, attrs):
            if tag in {"br", "p", "div"}:
                self.parts.append(" ")

        def handle_endtag(self, tag):
            if tag in {"p", "div"}:
                self.parts.append(" ")

    parser = TextParser()
    parser.feed(fragment)
    parser.close()
    return SPACE_RE.sub(" ", "".join(parser.parts)).strip()


def first(pattern: str, source: str) -> str | None:
    match = re.search(pattern, source, re.S)
    return clean(match.group(1)) if match else None


def fetch_one(row: dict, raw_dir: Path) -> dict:
    url = row["program_url"]
    request = Request(url, headers={"User-Agent": "semiconductor-conferences-research/0.1"})
    try:
        with urlopen(request, timeout=45) as response:
            source = response.read().decode("utf-8", errors="replace")
        (raw_dir / f"{row['doi_or_identifier']}.html").write_text(source, encoding="utf-8")
        description = first(r'<span class="abstract">(.*?)</span>', source)
        title = first(r'<div class="info-section presentation-title">(.*?)</div>', source) or row["title"]
        session = first(r'<span class="session-title"><a[^>]*>(.*?)</a>', source)
        event_type = first(r'<div class="event-types">.*?<div class="event-type-name [^"]+">(.*?)</div>', source)
        authors = [clean(name) for name in re.findall(r'<div class="presenter-name"><a[^>]*>(.*?)</a>', source)]
        evidence = []
        if description:
            evidence.append({"field": "description", "text": description})
        return normalize({
            **row,
            "title": title,
            "authors": authors or row.get("authors", []),
            "session_title": session,
            "event_type_detail": event_type,
            "description": description,
            "evidence_spans": evidence,
            "evidence_source_id": "dac-2026-presentation-pages",
            "evidence_status": "substantive_description" if description and len(description) >= 100 else "metadata_only",
            "evidence_url": url,
            "evidence_collection_date": date.today().isoformat(),
            "fetch_status": "ok",
        })
    except Exception as exc:  # Preserve failures as explicit rows for retry/audit.
        return {**row, "fetch_status": "error", "fetch_error": type(exc).__name__, "evidence_collection_date": date.today().isoformat(), "evidence_status": "unavailable"}


def collect(root: Path, limit: int | None, workers: int) -> dict:
    rows = [json.loads(line) for line in (root / "dac/data/papers-2026-program.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    rows = rows[:limit] if limit else rows
    raw_dir = root / "dac/data/raw/presentations"
    raw_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(fetch_one, row, raw_dir) for row in rows]
        for future in as_completed(futures):
            results.append(future.result())
            time.sleep(0.03)
    results.sort(key=lambda item: item["doi_or_identifier"])
    output = root / "dac/data/paper-evidence-2026.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for result in results:
            handle.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")
    return {
        "requested": len(rows),
        "fetched_ok": sum(item["fetch_status"] == "ok" for item in results),
        "substantive_description": sum(item.get("evidence_status") == "substantive_description" for item in results),
        "errors": sum(item["fetch_status"] == "error" for item in results),
        "output": str(output),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--limit", type=int, help="fetch only the first N records; default is all records")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    print(json.dumps(collect(args.root, args.limit, args.workers), indent=2, sort_keys=True))
