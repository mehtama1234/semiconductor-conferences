import json
from pathlib import Path


def test_mappingevolve_rejected_first_candidate_control_flow_model():
    """Model inspected branching, not execution/reproduction of the repository."""
    root = Path(__file__).resolve().parents[1]
    assessment = json.loads((root / "dac/data/mappingevolve-primary-assessment-v1.json").read_text())
    case = assessment["artifact_inspection"]["counterexample"]
    best_reward, best_state = case["initial_best_reward"], "initial"
    reward = -0.4 - case["candidate_failed_rate"] / 10
    candidate = "failed_candidate"
    if reward > best_reward:
        best_reward, best_state = reward, candidate
    delay_score, best_delay = 0.0, 0.0
    accepted = reward >= case["default_threshold"] or (
        reward > -0.4 and delay_score > 0.8 * best_delay
    )
    state = candidate if accepted else best_state
    assert not accepted and state == "failed_candidate"
    assert reward == case["candidate_reward"]
    assert assessment["independent_review_status"] == "pending"


def test_mappingevolve_pdf_crosscheck_does_not_imply_reproduction():
    root = Path(__file__).resolve().parents[1]
    assessment = json.loads((root / "dac/data/mappingevolve-primary-assessment-v1.json").read_text())
    verification = assessment["pdf_verification"]
    assert verification["page_one_based"] == 6
    assert len(verification["sha256"]) == 64
    assert "not independently verified" in verification["limits"]
    assert assessment["headline_metric_status"].startswith("withheld_")
    assert assessment["independent_review_status"] == "pending"
