#!/usr/bin/env python3
"""Capture original abstracts with exact identity checks; never infer support."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from pypdf import PdfReader

from scripts.build_evidence_summary import PATHS, read_jsonl
from scripts.collect_isca_crossref_metadata import title_key


def extract_arxiv(html: str, expected_title: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    title_meta = soup.find("meta", attrs={"name": "citation_title"})
    title = title_meta.get("content", "").strip() if title_meta else ""
    if not title:
        heading = soup.find("h1", class_="ltx_title_document")
        if heading:
            for note in heading.select(".ltx_pubnotes, .ltx_note"):
                note.decompose()
        title = heading.get_text(" ", strip=True) if heading else ""
    block = soup.find("blockquote", class_="abstract") or soup.find("div", class_="ltx_abstract")
    if block:
        label = block.find("span", class_="descriptor") or block.find(class_="ltx_title")
        if label:
            label.decompose()
    abstract = block.get_text(" ", strip=True) if block else ""
    return {"observed_title": title, "identity_status": "exact_normalized_title" if title and title_key(title) == title_key(expected_title) else "title_mismatch_requires_review",
            "description": abstract, "text_locator": "arXiv abstract block"}


def capture(record: dict, root: Path) -> dict:
    result = {"paper_id": record["paper_id"], "title": record["title"],
              "evidence_url": record["evidence_url"],
              "evidence_collection_date": datetime.now(timezone.utc).isoformat(),
              "capture_status": "not_attempted", "evidence_status": "not_captured"}
    is_pdf = record["evidence_url"].lower().endswith(".pdf")
    if not record["evidence_url"].startswith(("https://arxiv.org/abs/", "https://arxiv.org/html/")) and not is_pdf:
        result["capture_status"] = "requires_source_specific_extractor"
        return result
    try:
        req = Request(record["evidence_url"], headers={"User-Agent": "semiconductor-conference-research/0.1"})
        with urlopen(req, timeout=25) as response:
            body = response.read(5_000_001)
            if len(body) > 5_000_000:
                raise ValueError("Response exceeds capture limit")
            result["http_status"] = response.status
            result["resolved_url"] = response.url
        raw = root / record["conference_id"] / "data/raw" / f"review-{record['paper_id']}.{'pdf' if is_pdf else 'html'}"
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_bytes(body)
        if is_pdf:
            first_page = PdfReader(BytesIO(body)).pages[0].extract_text()
            match = re.search(r"Abstract\s*[—–:-](.*?)(?:Index Terms|Keywords|I\.\s*I\s*NTRODUCTION|1\s+INTRODUCTION)", first_page, re.S | re.I)
            title_present = title_key(record["title"]) in title_key(first_page[:2000])
            result.update({"observed_title": record["title"] if title_present else None,
                           "identity_status": "exact_normalized_title" if title_present else "title_mismatch_requires_review",
                           "description": " ".join(match.group(1).split()) if match else "",
                           "text_locator": "PDF page 1 abstract; automatic extraction requires semantic review"})
        else:
            result.update(extract_arxiv(body.decode("utf-8", errors="replace"), record["title"]))
        result["raw_sha256"] = hashlib.sha256(body).hexdigest()
        result["raw_path"] = str(raw.relative_to(root))
        matched = result["identity_status"] == "exact_normalized_title" and len(result["description"].split()) >= 30
        result["capture_status"] = "captured_exact_title_abstract" if matched else "captured_requires_identity_or_text_review"
        result["evidence_status"] = "substantive_abstract" if matched else "not_verified"
        result["source_text_sha256"] = hashlib.sha256(result["description"].encode()).hexdigest()
    except Exception as exc:
        result["capture_status"] = "retrieval_failed"
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--paper-id", action="append", help="Capture only selected records, preserving other prior captures")
    args = parser.parse_args()
    records = [r for p in PATHS for r in read_jsonl(args.root / p) if r["conference_id"] != "dac"]
    output = args.root / "data/review-source-captures.jsonl"
    previous = {r["paper_id"]: r for r in read_jsonl(output)} if output.exists() else {}
    if args.paper_id:
        requested = set(args.paper_id)
        missing = requested - {r["paper_id"] for r in records}
        if missing:
            parser.error(f"Unknown non-DAC paper IDs: {sorted(missing)}")
        records = [r for r in records if r["paper_id"] in requested]
    def cached_or_capture(record):
        prior = previous.get(record["paper_id"], {})
        if prior.get("evidence_status") == "substantive_abstract" and prior.get("evidence_url") == record["evidence_url"] and prior.get("title") == record["title"]:
            return prior
        return capture(record, args.root)
    with ThreadPoolExecutor(max_workers=2) as pool:
        captured = list(pool.map(cached_or_capture, records))
    merged = {**previous, **{r["paper_id"]: r for r in captured}} if args.paper_id else {r["paper_id"]: r for r in captured}
    output.write_text("".join(json.dumps(merged[key], ensure_ascii=False, sort_keys=True) + "\n" for key in sorted(merged)), encoding="utf-8")
    print(json.dumps([{k: r.get(k) for k in ["paper_id", "capture_status", "observed_title", "title", "error"]} for r in captured], indent=2))
