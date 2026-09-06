#!/usr/bin/env python3
"""Reconcile the ISCA 2026 program inventory with Crossref DOI metadata.

Crossref metadata supplies identifiers, publisher links, authors, pages, and
publication dates.  It does not by itself establish a paper's method, result,
workload, or trend classification, so the output remains metadata-only.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_URL = "https://api.crossref.org/works"
PROGRAM_PATH = "isca/data/papers-2026-program.jsonl"
SOURCE_ID = "isca-2026-crossref-metadata"
NON_WORD_RE = re.compile(r"[^a-z0-9]+")
TAG_RE = re.compile(r"<[^>]+>")


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def title_key(title: str) -> str:
    text = html.unescape(TAG_RE.sub(" ", title))
    text = re.sub(r"\\(?:mathrm|mathbf|text)\{([^{}]*)\}", r"\1", text)
    text = text.replace("\\mu", "mu").replace("μ", "mu")
    text = unicodedata.normalize("NFKC", text).lower()
    return NON_WORD_RE.sub("", text)


def title_prefix(title: str) -> str:
    return title_key(title.split(":", 1)[0])


def fetch_items() -> list[dict]:
    params = {
        "query": "ISCA",
        "filter": "from-pub-date:2026-01-01,until-pub-date:2026-12-31,prefix:10.1109,type:proceedings-article",
        "rows": 1000,
    }
    url = f"{API_URL}?{urlencode(params)}"
    request = Request(
        url,
        headers={
            "User-Agent": "semiconductor-conferences-research/0.1 (mailto:research@example.invalid)",
            "Accept": "application/json",
        },
    )
    with urlopen(request, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload["message"]["items"]


def date_value(item: dict) -> str | None:
    parts = (item.get("published-print") or item.get("published") or {}).get("date-parts", [[]])[0]
    if not parts:
        return None
    return "-".join(f"{part:02d}" if index else str(part) for index, part in enumerate(parts))


def collect(root: Path) -> dict:
    program_rows = read_jsonl(root / PROGRAM_PATH)
    crossref_rows = fetch_items()
    by_title: dict[str, list[dict]] = {}
    for item in crossref_rows:
        title = (item.get("title") or [""])[0]
        by_title.setdefault(title_key(title), []).append(item)
    by_prefix: dict[str, list[dict]] = {}
    for item in crossref_rows:
        title = (item.get("title") or [""])[0]
        prefix = title_prefix(title)
        if prefix:
            by_prefix.setdefault(prefix, []).append(item)

    records = []
    unmatched = []
    ambiguous = []
    for program in program_rows:
        matches = by_title.get(title_key(program["title"]), [])
        match_method = "exact_title"
        if len(matches) != 1 and title_prefix(program["title"]):
            prefix_matches = by_prefix.get(title_prefix(program["title"]), [])
            if len(prefix_matches) == 1:
                matches = prefix_matches
                match_method = "unique_title_prefix"
        if len(matches) != 1:
            (ambiguous if matches else unmatched).append(program["paper_id"])
            continue
        item = matches[0]
        doi = item.get("DOI")
        authors = [
            {
                "given": author.get("given"),
                "family": author.get("family"),
                "affiliations": [affiliation.get("name") for affiliation in author.get("affiliation", []) if affiliation.get("name")],
            }
            for author in item.get("author", [])
        ]
        abstract = item.get("abstract")
        if abstract:
            abstract = TAG_RE.sub(" ", html.unescape(abstract)).strip()
        records.append(
            {
                "paper_id": program["paper_id"],
                "conference_id": "isca",
                "target_edition": 2026,
                "analysis_edition": 2026,
                "title": program["title"],
                "crossref_title": (item.get("title") or [""])[0],
                "match_method": match_method,
                "authors": authors,
                "doi": doi,
                "doi_or_identifier": doi,
                "publisher_url": f"https://doi.org/{doi}" if doi else None,
                "publication_date": date_value(item),
                "pages": item.get("page"),
                "crossref_url": item.get("URL"),
                "abstract": abstract,
                "abstract_present": bool(abstract),
                "problem": None,
                "method_or_artifact": None,
                "workload_or_benchmark": None,
                "baselines": [],
                "metrics": [],
                "theme_id": None,
                "subtheme_id": None,
                "subsubtheme_id": None,
                "classification_confidence": "not_classified",
                "source_id": SOURCE_ID,
                "evidence_quality": "doi_metadata" if not abstract else "doi_metadata_with_abstract",
                "record_status": "doi_metadata_only",
                "access_status": "doi_metadata_only",
                "collection_date": date.today().isoformat(),
                "limits": "Crossref DOI metadata reconciled to the official program; metadata and any abstract do not establish technical claims, results, workloads, or taxonomy assignments.",
            }
        )

    records.sort(key=lambda row: row["paper_id"])
    output = root / "isca/data/crossref-metadata-2026.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return {
        "output": str(output),
        "program_count": len(program_rows),
        "crossref_result_count": len(crossref_rows),
        "matched_count": len(records),
        "unmatched_count": len(unmatched),
        "ambiguous_count": len(ambiguous),
        "unmatched_program_ids": unmatched,
        "ambiguous_program_ids": ambiguous,
        "source_url": API_URL,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(collect(args.root), indent=2, sort_keys=True))
