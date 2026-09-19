import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_paretopilot_recheck_preserves_artifact_and_headline_boundaries() -> None:
    assessment = json.loads((ROOT / 'dac/data/paretopilot-primary-assessment-v1.json').read_text())
    recheck = assessment['current_source_recheck']
    assert recheck['capture_date'] == '2026-09-08'
    assert '49.5%' in ' '.join(recheck['official_program_observations'])
    assert '1.8x' in ' '.join(recheck['official_program_observations'])
    assert 'local Vitis HLS' in ' '.join(recheck['repository_observations'])
    assert 'No target manuscript' in recheck['full_text_status']
    assert assessment['headline_metric_status'] == 'withheld_pending_identity_and_experiment_reconciliation'
    assert assessment['independent_review_status'] == 'pending'
