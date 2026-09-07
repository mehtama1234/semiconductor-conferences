import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


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
