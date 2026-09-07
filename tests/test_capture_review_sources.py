from scripts.capture_review_sources import extract_arxiv


def test_exact_title_and_original_abstract_are_separate_from_record_summary():
    html = '<meta name="citation_title" content="A Paper: Memory"><blockquote class="abstract"><span class="descriptor">Abstract:</span>Original source statement.</blockquote>'
    result = extract_arxiv(html, "A paper—Memory")
    assert result["identity_status"] == "exact_normalized_title"
    assert result["description"] == "Original source statement."


def test_wrong_paper_is_not_accepted_and_challenge_has_no_abstract():
    result = extract_arxiv('<meta name="citation_title" content="Unrelated work"><blockquote class="abstract">Some text</blockquote>', "Expected paper")
    assert result["identity_status"] == "title_mismatch_requires_review"
    challenge = extract_arxiv('<html>Checking your browser</html>', "Expected paper")
    assert not challenge["description"]
    assert challenge["identity_status"] != "exact_normalized_title"


def test_versioned_html_abstract_uses_document_heading_and_strips_label():
    html = '<h1 class="ltx_title ltx_title_document">A Paper</h1><div class="ltx_abstract"><h6 class="ltx_title ltx_title_abstract">Abstract</h6><p>Original paragraph.</p></div>'
    result = extract_arxiv(html, "A Paper")
    assert result["identity_status"] == "exact_normalized_title"
    assert result["description"] == "Original paragraph."
    assert extract_arxiv(html, "Another Paper")["identity_status"] == "title_mismatch_requires_review"
def test_html_title_excludes_structured_funding_note():
    from scripts.capture_review_sources import extract_arxiv
    result = extract_arxiv('<h1 class="ltx_title_document">Exact Title<span class="ltx_pubnotes">Thanks: funding</span></h1><div class="ltx_abstract">Technical abstract.</div>', 'Exact Title')
    assert result["identity_status"] == "exact_normalized_title"
    assert result["observed_title"] == "Exact Title"
