import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_hal_cover_extractor_fails_closed():
    from scripts.capture_review_sources import extract_hal_pages, HAL_DOCUMENT
    title = "A precise floating-point title"
    cover = "HAL Id: hal-12345678\nSubmitted on 1 Jan 2025\n" + title
    page = title + "\nAbstract—" + "technical evidence " * 40 + "Index Terms—computing"
    result = extract_hal_pages([cover, page], title, "hal-12345678")
    assert result["identity_status"] == "exact_normalized_title"
    assert result["description"] and "page 2" in result["text_locator"]
    for pages, expected, identifier in [([cover], title, "hal-12345678"), ([cover, page], "Other title", "hal-12345678"), ([cover, page], title, "hal-00000000"), ([page, page], title, "hal-12345678"), ([cover, "other manuscript"], title, "hal-12345678")]:
        rejected = extract_hal_pages(pages, expected, identifier)
        assert rejected["identity_status"] != "exact_normalized_title"
        assert not rejected["description"]
    assert HAL_DOCUMENT.fullmatch("https://hal.science/hal-12345678/document")
    assert not HAL_DOCUMENT.fullmatch("https://hal.science.example.org/hal-12345678/document")


def test_sera_coding_reaches_review_without_metric_acceptance():
    from scripts.build_review_packets import build
    row = json.loads((ROOT / "iccad/data/adjudicated-2025-batch-7.jsonl").read_text())
    assert row["metrics"] == []
    assert row["subsubtheme_id"] == "precision-reallocation-for-selective-floating-point-protection"
    packets, _ = build(ROOT)
    packet = next(p for p in packets if p["paper_id"] == row["paper_id"])
    assert packet["source_text_status"] == "captured_original_abstract"
    assert "Approximate computing" in packet["original_source_text"]
    assert "HAL is a multi-disciplinary" not in packet["original_source_text"]
    assert packet["supplementary_researcher_assessments"]
    assert not packet["independent_verdicts"]


@pytest.mark.parametrize("url,limit", [("https://hal.science/hal-12345678/document", 6_000_000), ("https://example.org/paper.pdf", 5_000_000)])
def test_capture_size_limit_remains_bounded(monkeypatch, tmp_path, url, limit):
    from scripts import capture_review_sources as capture_module

    class OversizedResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self, size):
            assert size == limit + 1
            return b"x" * size

    monkeypatch.setattr(capture_module, "urlopen", lambda *args, **kwargs: OversizedResponse())
    result = capture_module.capture({"paper_id": "test", "title": "Test", "conference_id": "iccad", "evidence_url": url}, tmp_path)
    assert result["capture_status"] == "retrieval_failed"
    assert "exceeds capture limit" in result["error"]
    assert not list(tmp_path.rglob("review-*"))


def test_sera_extracted_conditions_and_arithmetic():
    row = json.loads((ROOT / "iccad/data/sera-float-primary-recovery-v1.json").read_text())
    conditions = row["conditions"]
    fmt = conditions["format"]
    assert sum(fmt[key] for key in ["exponent_encoded_bits", "control_bits", "mantissa_bits", "identifier_bits", "mantissa_parity_bits"]) == fmt["storage_bits"] == 32
    assert "One flip in each" in conditions["correction"]["two_bit_condition"]
    assert "not mantissa error correction" in conditions["correction"]["mantissa"]
    dnn = conditions["dnn"]
    a = dnn["accuracy_percent"]
    assert a["fp32_baseline"] - a["sera_no_fault"] == pytest.approx(dnn["calculated_no_fault_loss_percentage_points"])
    assert a["sera_no_fault"] - a["sera_F2E4"] == pytest.approx(dnn["calculated_F2E4_loss_from_sera_no_fault_percentage_points"])
    hw = conditions["hardware"]
    old, new = hw["table_IX"]["baseline"], hw["table_IX"]["sera"]
    assert round(100 * (1 - new["energy_pJ"] / old["energy_pJ"]), 2) == hw["calculated_saving_from_displayed_energy_percent"]
    assert round(100 * (1 - new["power_mW"] * new["delay_ns"] / (old["power_mW"] * old["delay_ns"])), 2) == hw["calculated_saving_from_displayed_power_times_delay_percent"]
    assert all(item["delay_ns"] > hw["clock_constraint_ns"] for item in [old, new])
    assert row["pdf_verification"]["visually_checked_tables"] == {"VIII": 8, "IX": 9}
    assert row["independent_review_status"] == "pending"
    assert row["headline_metric_status"].startswith("withheld")
