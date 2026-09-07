import json
from pathlib import Path

from scripts.capture_review_sources import extract_ntu


def test_ntu_requires_unique_article_and_two_layer_title_doi_match():
    article = {"@type": "ScholarlyArticle", "name": "Test title", "identifier": ["10.1/test"], "abstract": "Original abstract " * 40}
    def html(items, title="Test title", doi="10.1/test"):
        return f'<meta name="citation_title" content="{title}"><meta name="citation_doi" content="{doi}"><script class="structured-data" type="application/ld+json">' + json.dumps({"@graph": items}) + '</script>'
    captured = extract_ntu(html([article]), "Test title", "10.1/test")
    assert captured["identity_status"] == "exact_normalized_title"
    assert captured["description"] == article["abstract"]
    for text in [html([article], title="Other"), html([article], doi="10.1/other"), html([{**article, "name": "Other"}]), html([{**article, "identifier": ["10.1/other"]}]), html([article, article]), html([])]:
        rejected = extract_ntu(text, "Test title", "10.1/test")
        assert rejected["identity_status"] != "exact_normalized_title"
        assert not rejected["description"]


def test_recovered_pair_has_original_review_text_and_withheld_metrics():
    from scripts.build_review_packets import build
    root = Path(__file__).resolve().parents[1]
    records = [json.loads(line) for line in (root / "iccad/data/adjudicated-2025-batch-8.jsonl").read_text().splitlines()]
    packets, _ = build(root)
    for row in records:
        packet = next(p for p in packets if p["paper_id"] == row["paper_id"])
        assert row["metrics"] == [] and row["independent_review_status"] == "pending"
        assert packet["source_text_status"] == "captured_original_abstract"
        assert packet["original_source_text"] and packet["supplementary_researcher_assessments"]
        assert not packet["independent_verdicts"]
    assert records[0]["evidence_depth_status"] == "institutional_abstract_only"
    assert records[1]["evidence_depth_status"] == "selected_full_text_conditions"
