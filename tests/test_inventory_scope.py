from scripts.build_title_shift_candidates import compare


def test_blank_slots_do_not_dilute_title_shares():
    old = [{"paper_id": str(i), "title": "memory"} for i in range(3)]
    new = old + [{"paper_id": "blank", "title": "  "}]
    result = compare(old, new)
    assert result["new_inventory_count"] == 4
    assert result["new_record_count"] == 3
    assert result["new_excluded_ids"] == ["blank"]
    assert result["candidate_terms"][0]["share_delta"] == 0


def test_empty_edition_is_insufficient_not_zero_prevalence():
    result = compare([], [{"paper_id": "one", "title": "memory"}])
    assert result["comparison_status"] == "insufficient_titles"
    assert result["candidate_terms"] == []
