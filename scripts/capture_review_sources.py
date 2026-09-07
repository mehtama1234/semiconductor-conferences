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

HAL_DOCUMENT = re.compile(r"https://(?:inria\.)?hal\.science/(hal-\d+(?:v\d+)?)/document\Z")


def extract_hal_pages(pages: list[str], expected_title: str, hal_id: str) -> dict:
    """Only skip a verified HAL cover; never scan arbitrary pages for a match."""
    cover = pages[0] if pages else ""
    page = pages[1] if len(pages) > 1 else ""
    base_id = re.sub(r"v\d+$", "", hal_id)
    id_match = re.search(r"HAL Id:\s*(hal-\d+(?:v\d+)?)\b", cover)
    valid_cover = bool(id_match and re.sub(r"v\d+$", "", id_match[1]) == base_id
                       and "Submitted on" in cover
                       and title_key(expected_title) in title_key(cover))
    title_present = title_key(expected_title) in title_key(page[:2000])
    match = re.search(r"Abstract\s*[—–:-](.*?)(?:Index Terms|Keywords|I\.\s*I\s*NTRODUCTION|1\s+INTRODUCTION)", page, re.S | re.I)
    valid = valid_cover and title_present
    return {"observed_title": expected_title if title_present else None,
            "identity_status": "exact_normalized_title" if valid else "hal_cover_or_title_mismatch_requires_review",
            "description": " ".join(match[1].split()) if valid and match else "",
            "text_locator": "PDF page 2 abstract after HAL ID/title-checked cover; automatic extraction requires semantic review"}


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


def extract_hkust(html: str, expected_title: str, expected_doi: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    def meta(name):
        tag = soup.find("meta", attrs={"name": name})
        return tag.get("content", "").strip() if tag else ""
    title, doi = meta("citation_title"), meta("citation_doi")
    blocks = soup.select(".rendering_abstractportal .textblock")
    valid = bool(title and expected_doi and title_key(title) == title_key(expected_title) and doi.lower() == expected_doi.lower())
    return {"observed_title": title, "observed_doi": doi,
            "identity_status": "exact_normalized_title" if valid else "title_or_doi_mismatch_requires_review",
            "description": blocks[0].get_text(" ", strip=True) if len(blocks) == 1 else "",
            "text_locator": "HKUST institutional publication abstract (.rendering_abstractportal .textblock); title and DOI metadata checked"}


def extract_ntu(html: str, expected_title: str, expected_doi: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    def meta(name):
        tags = soup.find_all("meta", attrs={"name": name})
        return tags[0].get("content", "").strip() if len(tags) == 1 else ""
    title, doi = meta("citation_title"), meta("citation_doi")
    articles = []
    for script in soup.select('script.structured-data[type="application/ld+json"]'):
        try:
            data = json.loads(script.get_text())
        except (ValueError, TypeError):
            continue
        if isinstance(data, dict):
            articles.extend(node for node in data.get("@graph", []) if isinstance(node, dict) and node.get("@type") == "ScholarlyArticle")
    valid = bool(title and expected_doi and title_key(title) == title_key(expected_title) and doi.lower() == expected_doi.lower())
    article = articles[0] if len(articles) == 1 else {}
    identifiers = article.get("identifier", [])
    valid = valid and title_key(article.get("name", "")) == title_key(expected_title) and isinstance(identifiers, list) and expected_doi.lower() in [str(x).lower() for x in identifiers]
    abstract = article.get("abstract", "")
    return {"observed_title": title, "observed_doi": doi,
            "identity_status": "exact_normalized_title" if valid else "title_or_doi_or_article_mismatch_requires_review",
            "description": abstract if valid and isinstance(abstract, str) else "",
            "text_locator": "NTU unique ScholarlyArticle JSON-LD abstract; citation and article title/DOI checked"}


def extract_nycu(html: str, expected_title: str, expected_doi: str, expected_authors: list[str]) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    def values(name):
        return [tag.get("content", "").strip() for tag in soup.find_all("meta", attrs={"name": name})]
    titles, dois, authors = values("citation_title"), values("citation_doi"), values("citation_author")
    blocks = soup.select(".rendering_abstractportal .textblock")
    headings = soup.find_all("h1")
    valid = (len(titles) == len(dois) == len(headings) == len(blocks) == 1
             and bool(expected_doi) and bool(expected_authors)
             and title_key(titles[0]) == title_key(expected_title)
             and title_key(headings[0].get_text(" ", strip=True)) == title_key(expected_title)
             and dois[0].lower() == expected_doi.lower()
             and [title_key(a) for a in authors] == [title_key(a) for a in expected_authors])
    return {"observed_title": titles[0] if len(titles) == 1 else None,
            "observed_doi": dois[0] if len(dois) == 1 else None, "observed_authors": authors,
            "identity_status": "exact_normalized_title" if valid else "title_doi_authors_or_block_mismatch_requires_review",
            "description": blocks[0].get_text(" ", strip=True) if valid else "",
            "text_locator": "NYCU unique institutional abstract block; heading, title, DOI and ordered author metadata checked"}


def capture(record: dict, root: Path) -> dict:
    result = {"paper_id": record["paper_id"], "title": record["title"],
              "evidence_url": record["evidence_url"],
              "evidence_collection_date": datetime.now(timezone.utc).isoformat(),
              "capture_status": "not_attempted", "evidence_status": "not_captured"}
    hal_match = HAL_DOCUMENT.fullmatch(record["evidence_url"])
    is_pdf = record["evidence_url"].lower().endswith(".pdf") or bool(hal_match)
    is_hkust = record["evidence_url"].startswith("https://researchportal.hkust.edu.hk/en/publications/")
    is_ntu = record["evidence_url"].startswith("https://scholars.lib.ntu.edu.tw/entities/publication/")
    is_nycu = record["evidence_url"].startswith("https://scholar.nycu.edu.tw/en/publications/")
    if not record["evidence_url"].startswith(("https://arxiv.org/abs/", "https://arxiv.org/html/")) and not is_pdf and not is_hkust and not is_ntu and not is_nycu:
        result["capture_status"] = "requires_source_specific_extractor"
        return result
    try:
        req = Request(record["evidence_url"], headers={"User-Agent": "semiconductor-conference-research/0.1"})
        with urlopen(req, timeout=25) as response:
            limit = 6_000_000 if hal_match else 5_000_000
            body = response.read(limit + 1)
            if len(body) > limit:
                raise ValueError("Response exceeds capture limit")
            result["http_status"] = response.status
            result["resolved_url"] = response.url
        raw = root / record["conference_id"] / "data/raw" / f"review-{record['paper_id']}.{'pdf' if is_pdf else 'html'}"
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_bytes(body)
        if hal_match:
            reader = PdfReader(BytesIO(body))
            result.update(extract_hal_pages([p.extract_text() or "" for p in reader.pages[:2]], record["title"], hal_match[1]))
        elif is_pdf:
            first_page = PdfReader(BytesIO(body)).pages[0].extract_text()
            match = re.search(r"Abstract\s*[—–:-](.*?)(?:Index Terms|Keywords|I\.\s*I\s*NTRODUCTION|1\s+INTRODUCTION)", first_page, re.S | re.I)
            title_present = title_key(record["title"]) in title_key(first_page[:2000])
            result.update({"observed_title": record["title"] if title_present else None,
                           "identity_status": "exact_normalized_title" if title_present else "title_mismatch_requires_review",
                           "description": " ".join(match.group(1).split()) if match else "",
                           "text_locator": "PDF page 1 abstract; automatic extraction requires semantic review"})
        elif is_hkust:
            result.update(extract_hkust(body.decode("utf-8", errors="replace"), record["title"], record.get("doi", "")))
        elif is_ntu:
            result.update(extract_ntu(body.decode("utf-8", errors="replace"), record["title"], record.get("doi", "")))
        elif is_nycu:
            result.update(extract_nycu(body.decode("utf-8", errors="replace"), record["title"], record.get("doi", ""), record.get("authors", [])))
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
