from scripts.capture_review_sources import extract_nycu


def test_nycu_checks_title_doi_authors_and_unique_abstract():
    html = '<h1>Test title</h1><meta name="citation_title" content="Test title"><meta name="citation_doi" content="10.1/test"><meta name="citation_author" content="A Person"><div class="rendering_abstractportal"><div class="textblock">Original evidence</div></div>'
    assert extract_nycu(html, "Test title", "10.1/test", ["A Person"])["description"] == "Original evidence"
    for changed in [html.replace("A Person", "B Person"), html.replace("10.1/test", "10.1/other"), html.replace("<h1>Test title", "<h1>Other"), html + '<meta name="citation_title" content="Test title">', html + '<div class="rendering_abstractportal"><div class="textblock">Other</div></div>']:
        assert not extract_nycu(changed, "Test title", "10.1/test", ["A Person"])["description"]
    assert not extract_nycu(html, "Test title", "10.1/test", [])["description"]


def test_copa_packet_preserves_institutional_depth_and_review_gap():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    record = json.loads((root / "iccad/data/adjudicated-2025-batch-10.jsonl").read_text())
    packet = json.loads((root / "data/review-packets/iccad-2025-1155.json").read_text())
    assert record["evidence_depth_status"] == "institutional_abstract_only"
    assert record["metrics"] == [] and record["independent_review_status"] == "pending"
    assert packet["source_text_status"] == "captured_original_abstract"
    assert packet["original_source_text"] and not packet["independent_verdicts"]
