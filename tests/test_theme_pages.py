import json
import re
from pathlib import Path

from scripts.build_theme_pages import build
from scripts.research_articles import apply_editorial_corrections, evidence_card
import pytest


ROOT = Path(__file__).resolve().parents[1]


def test_formal_reading_map_covers_ten_records_without_claiming_completion() -> None:
    from fractions import Fraction as F
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-analysis-and-verification.md').read_text()
    ids = re.findall(r'<span id="paper-([^"]+)"', page)
    assert len(ids) == len(set(ids)) == 10
    for paper_id in ids:
        assert f'](#paper-{paper_id})' in page
    assert 'not a new source assessment' in page
    assert 'all ten papers have received an individual comprehension pass' in page
    assert 'All ten records have received the same paper-level pass' in page
    assert 'Original classifications remain unchanged' in page
    assert 100*F(1,1000) == F(1,10)


def test_beyond_exact_explanation_and_card_preserve_model_scope() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1552']
    assert 'eprints.whiterose.ac.uk' in row['evidence_url']
    assert '19.13%' in ' '.join(row['metrics'])
    assert 'not a guarantee for every physical GPU behavior' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-analysis-and-verification.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research1552"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1552)' in page
    assert 'The paper proves exactness under its scheduling assumption' in page
    assert 'This reduction is useful because it exposes the two quantities' in page
    assert 'Rodinia study' in page and '19.13%' in page and '39.39%' in page
    assert 'does not implement them or measure that overhead' in page


def test_atlas_explanation_separates_threat_model_property_and_proof() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2886']
    assert 'arxiv.org/pdf/2603.01170' in row['evidence_url']
    assert '39/48' in ' '.join(row['metrics'])
    assert 'formal proof establishes the generated property' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-analysis-and-verification.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research2886"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2886)' in page
    assert 'The basic security terms must remain separate' in page
    assert 'A formal proof establishes the generated property under its assumptions' in page
    assert '39/48 benchmark CWEs' in page
    assert 'CWE counts, bugs, generated properties and formal outcomes are different denominators' in page


def test_factored_form_explanation_preserves_equivalence_and_evidence_boundaries() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1388']
    assert 'RESEARCH1388' in row['evidence_url']
    assert '45.57' in ' '.join(row['metrics'])
    assert 'No public manuscript' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-analysis-and-verification.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research1388"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1388)' in page
    assert 'The obligation comes before the speedup' in page
    assert 'A faster solver does not establish a stronger equivalence property' in page
    assert '45.57× geometric-mean speedup' in page
    assert 'a faster weakened check would not be an equivalent-checking improvement' in page


def test_insights_explanation_separates_testbench_feedback_from_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2737']
    assert 'arxiv.org/pdf/2504.15804' in row['evidence_url']
    assert '55.2/67.5' in ' '.join(row['metrics'])
    assert 'Testbench pass is not formal equivalence' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-analysis-and-verification.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research2737"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2737)' in page
    assert 'The target is executable behavior, not token similarity' in page
    assert 'Analyze, Draft, Improve, and Rectify' in page
    assert 'The preference signal still inherits the testbench\'s blind spots' in page
    assert 'pass@k with 20 sampled programs' in page
    assert 'only 52.3% of code pairs' in page


def test_earl_explanation_separates_entropy_selection_from_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1612']
    assert 'arxiv.org/pdf/2511.12033' in row['evidence_url']
    assert '68.9' in ' '.join(row['metrics'])
    assert 'High entropy is a model- and context-dependent uncertainty measure' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-analysis-and-verification.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research1612"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1612)' in page
    assert 'The training problem is credit assignment in structured code' in page
    assert 'Entropy is measured at a position, not assigned to a word' in page
    assert 'response-level quantile threshold' in page
    assert '68.9 functional pass@5' in page
    assert '14.7 and 17.2 percentage points' in page
    assert '80% is a universal threshold' in page


def test_timing_comparison_and_warpstar_card_preserve_boundaries() -> None:
    from scripts.build_theme_pages import read_selected_sample
    from fractions import Fraction as F
    rows = read_selected_sample(ROOT)
    source = next(r for r in rows if r['paper_id'] == 'dac-2026-research004')
    row = next(r for r in apply_editorial_corrections(ROOT, rows) if r['paper_id'] == source['paper_id'])
    assert row['_original_evidence']['evidence_url'] == source['evidence_url']
    assert '2603.28381v1' in row['evidence_url']
    assert 'worse signed TNS' in ' '.join(row['metrics'])
    for key in set(source)-set(row['_editorial_correction']['fields']):
        assert row[key] == source[key]
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/timing-analysis-and-optimization.md').read_text()
    assert page.count('<span id="paper-') == 2
    assert 'Original captured fields' in page
    assert 'original description-only card still needs reconciliation' not in page
    assert 'not 6×' in page
    assert F(100)/(F(40,2)+F(60,3)) == F(5,2)


def test_powerpath_explains_bracket_validity_and_tail_errors() -> None:
    from fractions import Fraction as F
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/timing-analysis-and-optimization.md').read_text()
    assert page.count('<span id="paper-') == 2
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research025)' in page
    assert 'not a reconstruction of Powerpath' in page
    assert 'proposed safeguard, not a verified feature' in page
    assert 'No manuscript page citations' in page
    assert 128/2**7 == 1 and 16/2**4 == 1
    assert not 40 <= 30 <= 56
    assert F(11,10)*20+3 == 25
    assert (999*F(1,10)+20)/1000 == F(1199,10000)
    assert F(8)/(1+4+F(2,10)) == F(20,13)


def test_powerpath_correction_separates_search_reduction_from_signoff_accuracy() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research025']
    assert 'supply-current signature' in row['method_or_artifact']
    assert 'not demonstrated reliable tail-safe sequential characterization' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/timing-analysis-and-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research025"></span>') == 1
    section = page.split('## Powerpath: narrow a characterization search', 1)[1].split('<span id="explanation-dac-2026-research004"></span>', 1)[0]
    for phrase in (
        'Powerpath', 'supply-current', 'reference-delay', 'affine', 'ridge regression',
        'setup', 'hold', 'removal', 'bracket', 'interval', 'Monte Carlo',
        'PVT', '5 nm', '12 nm', '1.5×', '3.6×', 'fallback', 'tail',
        'signoff', 'not demonstrated reliable tail-safe sequential characterization',
    ):
        assert phrase in section


def test_exact_t_synthesis_explanation_separates_bounded_optimality_from_hardware_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research031']
    assert 'exact T synthesis' in row['method_or_artifact']
    assert 'not demonstrated globally optimal or hardware-efficient fault-tolerant compilation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/synthesis-and-compilation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research031"></span>') == 1
    section = page.split('## Exact-T synthesis:', 1)[1].split('## Gate count is not complete', 1)[0]
    for phrase in (
        'exact', 'T synthesis', 'Clifford', 'ancilla', 'N ≤ 7', 'EPFL',
        '5.3%', '0.5%', '11.7%', '16%', 'library', 'mapper',
        'global optimality', 'statevector', 'phase', 'routing', 'magic-state',
        'decoder', 'hardware', 'not demonstrated globally optimal or hardware-efficient fault-tolerant compilation',
    ):
        assert phrase in section
def test_warpstar_explains_dependency_and_measurement_boundaries() -> None:
    from fractions import Fraction as F
    import math
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/timing-analysis-and-optimization.md').read_text()
    assert page.count('<span id="paper-') == 2
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research004)' in page
    assert 'Both paper records now have expanded individual explanations' in page
    assert 'not reproductions of these circuits' in page
    assert 'more negative signed value indicates greater aggregate violation' in page
    assert max(2+3,4+2) == 6
    assert F(55,10)-6 == -F(1,2)
    assert F(16,4*13) == F(4,13)
    assert sum((1,2,3,4)) == 10
    assert 5+.1*math.log(2) > 5
    assert sum(min(0,s) for s in (-2,-1,4)) == -3
    assert 40+F(60)/F(24,10) == 65


def test_llm_manuscript_cards_reconcile_without_overwriting_history() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    original = {r['paper_id']: r for r in rows}
    snapshot = json.dumps(rows, sort_keys=True)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    expected = {
        'dac-2026-research012': ('ModuPlace_paper.pdf', 'P8 regresses'),
        'iccad-2025-1222': ('2507.14776v1', 'not timing-closure rate'),
        'iccad-2025-110': ('2508.18462v1', 'Twenty samples/task'),
    }
    for paper_id, (source, limit) in expected.items():
        row = revised[paper_id]
        assert source in row['evidence_url']
        assert limit in ' '.join(row['metrics'])
        assert row['_original_evidence']['evidence_url'] == original[paper_id]['evidence_url']
        assert row['_editorial_correction']['review_date'] == '2026-09-08'
        for key in set(original[paper_id])-set(row['_editorial_correction']['fields']):
            assert row[key] == original[paper_id][key]
        card = '\n'.join(evidence_card(row))
        assert 'Original captured fields' in card
    assert json.dumps(rows, sort_keys=True) == snapshot
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/llm-assisted-design-flows.md').read_text()
    assert page.count('<span id="paper-') == 8
    assert 'older captured card below remains description-only' not in page
    assert 'older abstract-backed card below still needs reconciliation' not in page
    assert 'older preprint-backed card below does not yet contain this extraction' not in page


def test_verirl_preserves_reward_and_acceptance_boundaries() -> None:
    from fractions import Fraction as F
    from math import comb
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/llm-assisted-design-flows.md').read_text()
    assert page.count('<span id="paper-') == 8
    assert '[Read the step-by-step explanation](#explanation-iccad-2025-110)' in page
    assert 'not A\'s own measured pass rate' in page
    assert 'not claims that the released implementation mislabels' in page
    assert 'not measured circuit power, area or timing' in page
    assert 'cannot establish a shift from one approach to another' in page
    assert (F(1)+F(8,10))/2 == F(9,10)
    assert F(4,20) == F(1,5)
    score = 1-F(comb(16,5),comb(20,5))
    assert F(717,1000) < score < F(719,1000)
    assert score > F(1,5)


def test_veriopt_separates_timing_margin_and_implementation_contract() -> None:
    from fractions import Fraction as F
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/llm-assisted-design-flows.md').read_text()
    assert page.count('<span id="paper-') == 8
    assert '[Read the step-by-step explanation](#explanation-iccad-2025-1222)' in page
    assert 'manual external synthesis feedback' in page
    assert 'Preserve that discrepancy rather than silently harmonizing it' in page
    assert 'not recreated VeriOpt circuits' in page
    assert (255+1)%256 == 0 and 255+1 == 256
    assert F(2)-F(24,10) == -F(4,10)
    assert F(2)-F(22,10) == -F(2,10)
    assert (F(3,100)-F(2,100))/F(2,100) == F(1,2)
    assert 2*F(11,10)+F(2,10) == F(24,10)
    assert F(11,10)+F(2,10) == F(13,10)
    assert 8*2 > 10*1
    assert 4<7 and 10>6 and 3>2


def test_hls_architecture_explanation_preserves_system_boundaries() -> None:
    from fractions import Fraction as F
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/llm-assisted-design-flows.md').read_text()
    assert page.count('<span id="paper-') == 8
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1110)' in page
    assert 'No manuscript page citations are available' in page
    assert 'does not show that the released Fire module deadlocks' in page
    assert 'stored HLS estimates, not a fresh synthesis run' in page
    assert 'not a decomposition of the reported 11.78× result' in page
    assert 10+3*5 == 25
    assert F(335494*10, 1000000) == F(335494,100000)
    assert F(229703*10, 1000000) == F(229703,100000)
    assert F(100,60+40//10) == F(25,16)
    assert [1,2]+[3,4] != [1+3,2+4]


def test_moduplace_explains_geometry_without_claiming_reproduction() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/llm-assisted-design-flows.md').read_text()
    assert page.count('<span id="paper-') == 8
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research012)' in page
    assert 'not improvement on every board' in page
    assert 'no model, placer or router was executed' in page
    assert 'preserves the original description-only fields in its disclosure' in page
    assert 'All eight paper records in this chapter now have expanded individual explanations' in page
    assert 3+10+3 == 16
    assert (10-0)+(4-0) == 14
    assert 4+4+4 != 0
    assert 5*abs(6-4) == 10
    assert (50+130)/2 == 90
    assert 816.2 > 688.6 and 23 > 12


def test_mappingevolve_separates_mapper_netlist_and_fallback() -> None:
    from fractions import Fraction as F
    from scripts.build_theme_pages import read_selected_sample, apply_editorial_corrections
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research535']
    assert row['evidence_url'].endswith('2604.26591v1')
    assert '1.0571' in ' '.join(row['metrics'])
    assert 'not evidence that a published circuit was invalid' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/llm-assisted-design-flows.md').read_text()
    assert page.count('<span id="paper-') == 8
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research535)' in page
    assert 'not evidence that a published circuit was invalid' in page
    assert 'found no outer reversion' in page
    assert 'mapper-runtime ratios 1.755 and 1.6557' in page
    assert F(1,2)*F(10,100)-F(1,2)*F(4,100) == F(3,100)
    assert -1 < -.45 < -.1
    for a in (False,True):
        for b in (False,True):
            assert (not (a and b)) == ((not a) or (not b))


def test_paretopilot_preserves_metric_and_artifact_boundaries() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/llm-assisted-design-flows.md').read_text()
    assert page.count('<span id="paper-') == 8
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research865)' in page
    assert 'Measured results are not passed into a second sampling call' in page
    assert 'not an assertion that the paper uses this exact formula' in page
    assert 'No manuscript page citations are available' in page
    assert 4**5*3**3 == 27648
    assert 3*2+3*6+2*8 == 40 and 5*6 == 30
    assert 5<6 and 4<6


def test_two_tier_verilog_explains_state_and_checking() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/llm-assisted-design-flows.md').read_text()
    assert page.count('<span id="paper-') == 8
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2545)' in page
    assert 'No manuscript page citations are available' in page
    assert 'not a verified component of this paper' in page
    assert 'No target model, generated RTL, simulator, synthesis flow, or benchmark was executed' in page
    def step(q, reset, enable):
        return 0 if reset else ((q+1)%16 if enable else q)
    assert step(14,False,True) == 15
    assert step(15,False,True) == 0
    assert step(7,True,True) == 0
    assert step(7,False,False) == 7


def test_two_tier_verilog_correction_separates_generation_from_hardware_acceptance() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2545']
    assert 'Two-tier methodology combining LLMs' in row['method_or_artifact']
    assert 'not demonstrated general Verilog capability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/llm-assisted-design-flows.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2545"></span>') == 1
    section = page.split('## Two-tier Verilog generation:', 1)[1].split('<span id="explanation-dac-2026-research2145"></span>', 1)[0]
    for phrase in (
        'language models', 'retrieval', 'classifier', 'heuristic', 'simulation',
        'functional', 'critical path', 'resource sharing', 'synthesis',
        'test preparation', 'human intervention', 'No target model',
        'not a verified component of this paper'
    ):
        assert phrase in section


def test_undocumented_instruction_correction_separates_discovery_from_security_verification() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2804']
    assert 'Automated instruction discovery' in row['method_or_artifact']
    assert 'not a general security-detection rate' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/hardware-security-validation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2804"></span>') == 1
    section = page.split('## Undocumented instructions:', 1)[1].split('## Benchmark shortcuts', 1)[0]
    for phrase in (
        'instruction', 'encoding', 'classifier', '99.8357%', '23', '29',
        'five', 'privilege', 'security property', 'exploit', 'held-out',
        'unit of prediction', 'measured security-detection rate'
    ):
        assert phrase in section


def test_drcagent_explanation_preserves_geometry_and_evidence_limits() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/llm-assisted-design-flows.md').read_text()
    assert page.count('<span id="paper-') == 8
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2145)' in page
    assert 'No manuscript page citations are available' in page
    assert 'not observed behavior of drcAgent' in page
    assert 'All eight paper records in this chapter now have expanded individual explanations' in page
    assert 5-2 == 3 and 11-7 == 4
    assert 6-2 == 4 and 11-8 == 3
    assert 4+2+4 > 11-2
    assert 100-90+20 == 30
    theme = (ROOT / 'reports/themes/ai-assisted-eda.md').read_text()
    assert 'Explanatory depth varies' in theme


def test_atlas_connects_themes_without_promoting_trends() -> None:
    page = (ROOT / 'reports/research-atlas-index-v1.md').read_text()
    assert '## Read the connected explanation first' in page
    assert 'not measured historical trends' in page
    assert 'individual subtheme and paper explanations remain uneven' in page
    assert '#explanation-isca-2026-program-008' in page
    assert '#explanation-dac-2026-research2566' in page
    for source in (ROOT / 'reports/theme-editorial').glob('*.md'):
        assert f'themes/{source.name}' in page
    synthesis = (ROOT / 'reports/technology-direction-synthesis-v1.md').read_text()
    assert 'selected DAC sample is 544 records' in synthesis
    assert 'selected DAC sample is 88 records' not in synthesis


def test_protection_theme_keeps_energy_fault_and_threat_models() -> None:
    from fractions import Fraction as F
    build(ROOT)
    page = (ROOT / 'reports/themes/power-reliability-and-security.md').read_text()
    assert '## Begin with the result that must remain valid' in page
    assert 'not demonstrated ISCA–DAC–ICCAD time trends' in page
    assert 'The reduction relies on independence' in page
    assert '#explanation-isca-2026-program-004' in page
    assert page.index('## Begin with the result') < page.index('## Subthemes and how')
    assert 70*F(16,10) == 112
    assert max(9,10) == 10 and max(12,10) == 12
    p=F(1,100)
    assert 3*p*p*(1-p)+p**3 == F(298,1_000_000)
    assert F(10,F(9,10)) > 11


def test_analog_theme_keeps_representation_and_calibration_limits() -> None:
    from fractions import Fraction as F
    build(ROOT)
    page = (ROOT / 'reports/themes/analog-mixed-signal-and-emerging-devices.md').read_text()
    assert '## Follow a number through its physical representation' in page
    assert 'not established ISCA–DAC–ICCAD time trends' in page
    assert 'one-week measured-device interval separately from ten-year simulated drift' in page
    assert 'not a quantum algorithm' in page
    assert page.index('## Follow a number') < page.index('## Subthemes and how')
    assert F(1000,256) == F(125,32)
    assert F(1,2)/10 == F(5,100)
    assert F(99,100)*F(80,100) == F(792,1000)


def test_chiplet_theme_keeps_handoff_thermal_and_cost_boundaries() -> None:
    from fractions import Fraction as F
    build(ROOT)
    page = (ROOT / 'reports/themes/chiplets-3d-and-packaging.md').read_text()
    assert '## Follow the information crossing a die boundary' in page
    assert 'not established ISCA–DAC–ICCAD time trends' in page
    assert 'not the bit-sparsity Duet' in page
    assert '#duet-give-different-inference-phases-different-hardware' in page
    assert page.index('## Follow the information') < page.index('## Subthemes and how')
    assert 2+3+2 > 3+3
    assert F(100_000_000,50_000_000_000) == F(2,1000)
    assert 20*2 == 40
    assert (100*2+50*8)/10 == 60
    assert F(100,F(80,100)) == 125


def test_physical_theme_preserves_electrical_and_manufacturing_boundaries() -> None:
    from fractions import Fraction as F
    build(ROOT)
    page = (ROOT / 'reports/themes/physical-design-and-manufacturing.md').read_text()
    assert '## Follow a logical connection into a physical implementation' in page
    assert 'not established ISCA–DAC–ICCAD time trends' in page
    assert 'A higher inspection-classifier score is not automatically higher yield' in page
    assert '#paper-dac-2026-research2297' in page
    assert page.index('## Follow a logical') < page.index('## Subthemes and how')
    assert 100-103 == -3
    assert -4+3+2 == 1
    assert F(1,10)*F(1,5) == F(1,50)
    assert F(90,100) == F(9,10)
    assert F(90,189) == F(10,21)


def test_ai_eda_theme_separates_proposal_checking_and_acceptance() -> None:
    build(ROOT)
    page = (ROOT / 'reports/themes/ai-assisted-eda.md').read_text()
    assert '## Separate proposing a design from establishing its properties' in page
    assert 'not measured ISCA–DAC–ICCAD growth trends' in page
    assert 'Final acceptance is 20% of attempts, not 80%' in page
    assert 'does not make their judgments independent' in page
    assert '#paper-dac-2026-research2145' in page
    assert '#paper-dac-2026-research523' in page
    assert page.index('## Separate proposing') < page.index('## Subthemes and how')
    assert 20/100 == .2 and 80/100 == .8
    assert not 12 <= 10 and 8 <= 10


def test_systems_theme_keeps_workload_and_service_boundaries() -> None:
    from fractions import Fraction as F
    build(ROOT)
    page = (ROOT / 'reports/themes/systems-applications-and-workloads.md').read_text()
    assert '## Follow a request from arrival to a usable result' in page
    assert 'not demonstrated cross-edition trends' in page
    assert 'DAC-only coded sample' in page
    assert 'The reciprocal rate is not its response time' in page
    assert '#hw-router-choose-using-current-queues-as-well-as-model-capability' in page
    assert page.index('## Follow a request') < page.index('## Subthemes and how')
    assert 20+10+30+5 == 65 and 20+10+30/3+5 == 45
    assert F(4,40)*1000 == 100
    assert F(980,1000) < F(99,100)
    assert 60*2 > 100*1
    assert F(1,1)*F(100,1000) == F(1,10)


def test_tooling_theme_keeps_validity_and_end_to_end_costs() -> None:
    from fractions import Fraction as F
    build(ROOT)
    page = (ROOT / 'reports/themes/design-methodology-and-tooling.md').read_text()
    assert '## Follow a design choice through its consequences' in page
    assert 'not established ISCA–DAC–ICCAD trends' in page
    assert 'DyTuner remains description-backed' in page
    assert '#explanation-dac-2026-research2566' in page
    assert '#explanation-dac-2026-research127' in page
    assert 'An average prediction error is not automatically the needed worst-case bound' in page
    assert page.index('## Follow a design choice') < page.index('## Subthemes and how')
    assert F(10, F(1,1000)) == 10_000
    assert 100*1 < 20*10
    assert 80 <= 100 and not 12 <= 10
    assert 95 <= 100 and 9 <= 10


def test_verification_theme_preserves_observation_and_proof_boundaries() -> None:
    build(ROOT)
    page = (ROOT / 'reports/themes/verification-and-validation.md').read_text()
    assert '## Follow a claim from requirement to evidence' in page
    assert '## Formal proof is conditional on a model and assumptions' in page
    assert 'not observed ISCA–DAC–ICCAD time trends' in page
    assert 'A solver timeout establishes neither correctness nor a counterexample' in page
    for paper in ('150', '2533', '616'):
        assert '#explanation-dac-2026-research'+paper in page
    assert page.index('## Follow a claim') < page.index('## Subthemes and how')
    assert [0,5,0][-1] == [0,6,0][-1]
    assert [0,5,0][1] != [0,6,0][1]
    assert 60*2 > 100*1
    assert all(not accepted or response for accepted,response in [(False,False)])


def test_memory_theme_separates_capacity_progress_and_recovery() -> None:
    from fractions import Fraction as F
    build(ROOT)
    page = (ROOT / 'reports/themes/memory-interconnect-and-storage.md').read_text()
    assert '## Follow a read before comparing memory systems' in page
    assert '## Recovery changes what completion means' in page
    assert 'not demonstrated ISCA–DAC–ICCAD trends' in page
    assert 'not a locally reproduced failure' in page
    assert '#explanation-isca-2026-program-045' in page
    assert '#explanation-dac-2026-research1061' in page
    assert page.index('## Follow a read') < page.index('## Subthemes and how')
    assert F(64,100)*10**9 == 640_000_000
    assert F(20_000_000_000*100,10**9*64) == F(125,4)
    assert 280-240 == 40
    assert F(10_000,100) == 100
    assert 80-30-10 == 40 and 80-20-10 == 50


def test_architecture_theme_connects_costs_and_bounded_hypotheses() -> None:
    from fractions import Fraction as F
    build(ROOT)
    page = (ROOT / 'reports/themes/architecture-and-accelerators.md').read_text()
    assert '## Follow one result through the machine' in page
    assert '## Three long-term hypotheses worth testing' in page
    assert 'not accepted longitudinal findings' in page
    assert 'does not complete their rewrites' in page
    assert '#explanation-dac-2026-research935' in page
    assert '#explanation-dac-2026-research680' in page
    assert page.index('## Follow one result') < page.index('## Subthemes and how')
    assert 2*5+3*7 == 31
    assert F(100_000_000,10_000_000_000) == F(10,1000)
    assert F(200_000_000,10_000_000_000) == F(20,1000)
    assert 20+50/5+30 == 60
    assert F(100,60+15) == F(4,3)


def test_theme_editorial_uses_supplied_root(tmp_path) -> None:
    from scripts.research_articles import theme_article
    folder = tmp_path / 'reports/theme-editorial'
    folder.mkdir(parents=True)
    (folder / 'architecture-and-accelerators.md').write_text('## Isolated editorial\n\nOnly this root.\n')
    page = '\n'.join(theme_article('architecture-and-accelerators', 'Architecture', [], [], root=tmp_path))
    assert 'Only this root.' in page
    assert '## Follow one result through the machine' not in page


def test_salut_explanation_preserves_dependencies_and_factorization_scope() -> None:
    from fractions import Fraction as F
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/sparse-and-irregular-compute.md').read_text()
    assert page.count('<span id="paper-') == 11
    assert page.count('[Read the step-by-step explanation](#explanation-') == 11
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research935)' in page
    assert 'No manuscript page citations are available' in page
    assert 'not a verified SALUT implementation' in page
    assert 'No SALUT hardware, solver, simulation, or benchmark was executed' in page
    lower, upper = [[1,0],[2,1]], [[2,1],[0,1]]
    product = [[sum(lower[i][k]*upper[k][j] for k in range(2))
                for j in range(2)] for i in range(2)]
    assert product == [[2,1],[4,3]]
    assert 0-F(1,2)*1 == F(-1,2)
    assert max(2,10)+3 == 13 and max(2+3,10) == 10
    assert 60+40/4 == 70
    assert 4*F(1,4) == 1


def test_precision_chapter_preserves_all_records_and_hap_scope() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/approximate-and-precision-aware-compute.md').read_text()
    assert page.count('<span id="paper-') == 14
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1999)' in page
    assert 'each now linked to an expanded individual explanation' in page
    assert page.count('[Read the step-by-step explanation](#explanation-') == 14
    assert 'not lossless inference relative to the floating-point model' in page
    assert 'normalized to Stripes' in page
    assert '1.56 percentage points' in page
    assert 'No HAP implementation was executed' in page


def test_spade_explanation_separates_turbo_and_similarity_proxy() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/sparse-and-irregular-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research680)' in page
    assert 'standard end-to-end ratios span 1.32–1.49×' in page
    assert 'SICS is not a proof of preserved output' in page
    assert 'No SPADE code, attention kernel, or video-generation benchmark was executed' in page
    def score(vectors):
        return sum(sum(v[j] for v in vectors)**2 for j in range(2))
    assert score([[1,0],[1,0]]) == 4
    assert score([[1,0],[-1,0]]) == 0
    assert score([[1,0],[0,1]]) == 2
    assert {1,2}|{2,3} == {1,2,3}
    assert 4096**2*2 == 32*1024**2


def test_florella_explanation_preserves_logarithmic_and_mapping_limits() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/sparse-and-irregular-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research588)' in page
    assert 'not Florella instructions, circuits, or measured traces' in page
    assert 'How the expanded papers connect' in page
    assert 'No Florella implementation, graph inference, arithmetic circuit, simulation, or synthesis was executed' in page
    import math
    a, b = math.log(2), math.log(3)
    result = max(a,b)+math.log1p(math.exp(-abs(a-b)))
    assert math.isclose(math.exp(result),5)
    assert 100-99 == 1 and 100.5-98.5 == 2
    assert math.log1p(math.exp(-10)) < 0.000046


def test_sparse_3d_explanation_separates_fusion_and_approximation() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/sparse-and-irregular-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2717)' in page
    assert 'not reconstructions of the paper\'s kernels' in page
    assert 'relative percentages versus percentage points' in page
    assert 'No sparse 3D detector, approximation, precision experiment, or GPU benchmark was executed' in page
    assert (80+200)/(5+5) == 28 and 80/5+200/5 == 56
    assert sum([0,10,0]) == 10 and sum([10,10,10]) == 30
    import struct
    assert struct.unpack('e',struct.pack('e',1000.1))[0] == 1000
    from fractions import Fraction as F
    assert 60-4 == 56 and 60*(1-F(4,100)) == F(576,10)
    assert 80+F(20,50) == F(804,10)


def test_pillarsparse_explanation_preserves_operation_and_encoding_limits() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/sparse-and-irregular-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2468)' in page
    assert 'not Pillar CSR layouts' in page
    assert 'not necessarily a single external-memory transaction' in page
    assert 'No PillarSparse conversion, GPU kernel, or benchmark was executed' in page
    assert [2*1+3*5,2*2+3*6,4*3,4*4] == [17,22,12,16]
    assert 1*7+2*8 == 23 and 3*5+4*6 == 39
    word = (700 << 12) | 9
    assert word == 2867209 and word >> 12 == 700 and word & 4095 == 9
    assert 6+4+9*6 == 64


def test_ltminer_explanation_preserves_event_and_source_boundaries() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/sparse-and-irregular-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research240)' in page
    assert 'separate PPoPP publication' in page
    assert 'not proof that LTMiner uses that cache or sizing rule' in page
    assert 'No LTMiner hardware, graph benchmark, or DTMiner implementation was executed' in page
    matches = [(1,t,u) for t in (2,4) for u in (5,9) if 1<t<u and u-1<=5]
    assert matches == [(1,2,5),(1,4,5)]
    def loads(seq):
        return sum(i == 0 or seq[i] != seq[i-1] for i in range(len(seq)))
    assert loads('ABCABCABC') == 9 and loads('AAABBBCCC') == 3
    assert 8-1-2 == 5 and 64*1000000 > 8*1024**2


def test_acc_spmv_explanation_preserves_permutation_and_timing_limits() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/sparse-and-irregular-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2105)' in page
    assert '93b7138bad9f3adbfbad4d86a362515fd3e4cd93' in page
    assert 'do not time identical reset work' in page
    assert 'No Acc-SpMV preprocessing, GPU kernel, or benchmark was executed' in page
    matrix, x, permutation = [[2,0,3],[0,4,0]], [5,7,11], [2,0,1]
    def mv(a, v):
        return [sum(w*z for w,z in zip(row,v)) for row in a]
    reordered = [[row[i] for i in permutation] for row in matrix]
    assert mv(matrix,x) == mv(reordered,[x[i] for i in permutation]) == [43,28]
    assert mv(reordered,x) == [29,44]
    assert [5+i for i in range(3)] == [5,6,7]
    assert [1000*v for v in mv(matrix,x)] == [43000,28000]


def test_trident_explanation_preserves_intermediate_and_order_limits() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/sparse-and-irregular-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research149)' in page
    assert 'two million versus two thousand multiplications' in page
    assert 'not TRIDENT\'s unrecovered implementation' in page
    assert 'No TRIDENT implementation, matrix benchmark, simulation, or synthesis was executed' in page
    assert (2*5+3*7)*13+3*11*17 == 10*13+21*13+33*17 == 964
    assert 2*1000**2 == 2000000 and 2*1000 == 2000
    assert [3*i for i in (1,2,3)] == [3,6,9]
    assert (1e16+(-1e16))+1 == 1 and 1e16+((-1e16)+1) == 0


def test_duet_explanation_preserves_sign_and_pipeline_boundaries() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/sparse-and-irregular-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1419)' in page
    assert 'not Duet encodings or measured traces' in page
    assert 'integer reconstruction' in page
    assert 'No Duet implementation, model benchmark, simulation, or synthesis was executed' in page
    assert int('11111101', 2)-256 == int('101', 2)-8 == -3
    assert 2*(-3)+5*(-2) == 2*1+5*2-4*(2+5) == -16
    assert 2+8+9*8 == 82 and 2+1+9*2 == 21
    assert sum([2,2,2,8])/(4*8) == 0.4375
    assert (16*4+16)/16 == 5


def test_pfgemm_explanation_preserves_prefix_and_reduction_boundaries() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/sparse-and-irregular-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research138)' in page
    assert 'not a prefix sum' in page
    assert 'not PFCSR encodings or PFGEMM schedules' in page
    assert 'No PFGEMM implementation, matrix benchmark, simulation, or synthesis was executed' in page
    assert [(0x12 << 8) | n for n in (1,2,7,15)] == [0x1201,0x1202,0x1207,0x120F]
    assert 2*11+5*13 == 87
    assert 1+4+1 == 6 and 4*2 == 8


def test_bsgcn_explanation_preserves_all_records_and_cache_limits() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/sparse-and-irregular-compute.md').read_text()
    assert page.count('<span id="paper-') == 11
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1242)' in page
    assert 'each now linked to an expanded individual explanation' in page
    assert 'No BSGCN implementation, graph benchmark, simulation, or synthesis was executed' in page
    def misses(sequence, capacity):
        cache, count = [], 0
        for item in sequence:
            if item in cache:
                cache.remove(item)
            else:
                count += 1
                if len(cache) == capacity:
                    cache.pop(0)
            cache.append(item)
        return count
    assert misses('ABCABC', 2) == 6
    assert misses('AABBCC', 2) == 3
    assert misses('ABAB', 1) == 4 and misses('ABAB', 2) == 2


def test_peace_explanation_preserves_indices_and_metric_units() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/approximate-and-precision-aware-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1885)' in page
    assert 'not throughput alone' in page
    assert 'not the unrecovered PEACE algorithm' in page
    assert 'No PEACE code, model benchmark, circuit, or synthesis was executed' in page
    inputs, values, indices = [2,3,5,7], [4,6], [0,3]
    assert sum(inputs[i]*v for i,v in zip(indices,values)) == 50
    assert sum(a*v for a,v in zip(inputs,values)) == 26
    assert 192*2 > 256 and 64*2 < 256
    assert 256*(-128)*(-128) > 2**22-1


def test_bayescvnn_explanation_preserves_dropout_and_sampling_boundaries() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/approximate-and-precision-aware-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1610)' in page
    assert '5.75-percentage-point accuracy loss' in page
    assert 'not a universal lower bound' in page
    assert 'different means unless compensated elsewhere' in page
    assert 'No BayesCVNN training, inference, HLS synthesis, or FPGA execution was performed' in page
    from fractions import Fraction as F
    x, keep = F(4), F(1,2)
    assert (keep**2*x, keep*x, keep*(x/keep)) == (1,2,4)
    assert (2+3j)*(4+5j) == -7+22j
    assert (2+3)*(4+5)-2*4-3*5 == 22
    assert F(381,100)*F(70,100)/3 == F(889,1000)
    assert F(8281,100)-F(7706,100) == F(575,100)


def test_resp_explanation_preserves_quality_loss_and_gradient_limits() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/approximate-and-precision-aware-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2650)' in page
    assert '66.87 and 47.00 percentage points' in page
    assert '15.47 and 28.00 percentage points' in page
    assert 'not uniformly better' in page
    assert 'not a recovered DAC camera-ready version' in page
    assert 'No RESP code, model benchmark, or pruning run was executed' in page
    from fractions import Fraction as F
    assert F(9674,100)-F(8127,100) == F(1547,100)
    assert F(8127,100)-F(1440,100) == F(6687,100)
    assert F(876,10)-F(596,10) == 28
    assert F(10,100)/F(80,100) == F(125,1000)
    # Zero local derivative does not imply zero deletion loss.
    assert 2*(1-1) == 0 and (0-1)**2 == 1
    assert 500*2048 == 1024000


def test_prism_and_mxp_explanations_preserve_scale_and_element_distinction() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/approximate-and-precision-aware-compute.md').read_text()
    for paper in ('2207', '2374'):
        assert f'[Read the step-by-step explanation](#explanation-dac-2026-research{paper})' in page
    assert 'not PRISM bit layouts' in page
    assert "not MXP's encoding" in page
    assert 'increases reported alongside an accuracy benefit, not reductions' in page
    assert 'No PRISM implementation, model benchmark, or synthesis was executed' in page
    assert 'No MXP implementation, model benchmark, or synthesis was executed' in page
    from fractions import Fraction as F
    errors_a, errors_b = [F(6,100), F(-16,10)], [F(-14,100),F(-2,10)]
    assert sum(e*e for e in errors_a) == F(25636,10000)
    assert sum(e*e for e in errors_b) == F(596,10000)
    assert 1000*errors_a[0]**2+errors_a[1]**2 == F(616,100)
    assert 1000*errors_b[0]**2+errors_b[1]**2 == F(1964,100)
    assert F(1125,1000)-F(11,10) == F(25,1000)
    assert 8*(F(1125,1000)-F(11,10)) == F(2,10)
    assert 4+F(8,16) == F(45,10)


def test_hierpas_explanation_separates_sparsity_precision_and_efficiency() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/approximate-and-precision-aware-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research259)' in page
    assert 'Neither ratio is a latency ratio' in page
    assert 'not HierPAS results' in page
    assert 'No HierPAS model, circuit, benchmark, or synthesis was executed' in page
    from fractions import Fraction as F
    weights, values = [F(8,10),F(15,100),F(5,100)], [2,4,10]
    full = sum(a*v for a,v in zip(weights,values))
    retained = sum(a*v for a,v in zip(weights[:2],values[:2]))
    delta = weights[-1]
    assert full == F(27,10) and retained == F(22,10)
    assert abs(full-retained) <= delta*max(values)
    assert abs(full-retained/(1-delta)) <= 2*delta*max(values)
    assert 0.72 < 0.99**32 < 0.73
    assert 20 + 80/4 + 15 == 55


def test_comac_explanation_preserves_pairing_and_evidence_limits() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/approximate-and-precision-aware-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research3029)' in page
    assert 'not recovered CO-MAC measurements' in page
    assert 'No CO-MAC circuit, code, benchmark, or synthesis was executed' in page
    assert 'description-backed' in page
    from fractions import Fraction as F
    first = [1, 1, 0, 0]
    assert [sum(a*b for a,b in zip(first, second)) for second in
            ([1,0,1,0], [1,1,0,0], [0,0,1,1])] == [1,2,0]
    inputs, weights = [2,3,5,7], [F(-6,10),F(1,10),F(-2,10),F(4,10)]
    ordered = sorted(zip(inputs, weights), key=lambda pair: abs(pair[1]))
    assert sum(a*w for a,w in ordered) == F(9,10)
    assert sum(a*w for a,w in zip(inputs, sorted(weights, key=abs))) == F(-26,10)
    assert 60 + 40*F(452,1000) == F(7808,100)


def test_hierarchical_boundary_recovery_separates_correspondence_from_cut_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1638']
    assert 'RESEARCH1638' in row['evidence_url']
    assert 'robust experimental recovery' in ' '.join(row['metrics'])
    assert 'Target manuscript' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-analysis-and-verification.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research1638"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1638)' in page
    assert 'Behavioral correspondence' in page
    assert 'Cut validity' in page
    assert 'SAT sweeping' in page
    assert 'logic sharing and satisfiability' in page
    assert 'target manuscript, benchmark tables and artifact execution' in page


def test_debug_like_a_human_explanation_separates_localization_from_bug_proof() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1355']
    assert row['evidence_url'].endswith('2605.17290v1')
    assert '24/28/28' in ' '.join(row['metrics'])
    assert 'ranked hypothesis' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-analysis-and-verification.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research1355"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1355)' in page
    assert 'The task is to rank code blocks, not to prove the bug' in page
    assert 'instruction execution path' in page
    assert 'top 1, top 5 or top 10' in page
    assert 'mutation-injected' in page
    assert 'does not establish a general fault-localization guarantee' in page


def test_svacoder_explanation_separates_formal_validity_from_semantic_alignment() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2361']
    assert row['evidence_url'].endswith('2603.14239v1')
    assert '75.8/89.4/90.4' in ' '.join(row['metrics'])
    assert 'not proof that the assertion expresses' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-analysis-and-verification.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research2361"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2361)' in page
    assert 'An assertion is a temporal requirement, not just legal syntax' in page
    assert 'pass formal verification against the design' in page
    assert 'Bidirectional translation tests whether meaning survives' in page
    assert 'Func.@k' in page
    assert 'does not establish that generated assertions cover the full design intent' in page


def test_hydracec_explanation_separates_parallel_scheduling_from_proof_soundness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research285']
    assert 'RESEARCH285' in row['evidence_url']
    assert '10.5×' in ' '.join(row['metrics'])
    assert 'Target manuscript' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-analysis-and-verification.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research285"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research285)' in page
    assert 'The proof obligation is unchanged; the work schedule changes' in page
    assert 'Task Benefit Graph' in page
    assert 'Asynchronous sharing removes a global barrier' in page
    assert 'not universal speedups' in page


def test_probabilistic_controller_explanation_separates_certificate_scope_from_deterministic_safety() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research720']
    assert 'RESEARCH720' in row['evidence_url']
    assert 'formally provable probabilistic safety guarantees' in ' '.join(row['metrics']) or 'probability' in ' '.join(row['metrics'])
    assert 'not deterministic safety' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-analysis-and-verification.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research720"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research720)' in page
    assert 'A probability statement needs a horizon and a distribution' in page
    assert 'The cGAN supplies a verifiable observation model' in page
    assert 'Martingale reasoning connects local inequalities' in page
    assert 'not deterministic safety for disturbances outside that model' in page


def test_pro_v_r1_explanation_separates_golden_agreement_from_fault_detection() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research142']
    assert row['evidence_url'].endswith('2506.12200v4')
    assert '57.7' in ' '.join(row['metrics']) and '34.0' in ' '.join(row['metrics'])
    assert 'not complete design correctness' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-and-functional-verification.md').read_text()
    assert page.count('<span id="paper-') == 7
    assert page.count('<span id="explanation-dac-2026-research142"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research142)' in page
    assert 'Verification needs an oracle and stimuli' in page
    assert 'The training data is filtered by executable agreement' in page
    assert 'The evaluation has three distinct levels' in page
    assert 'Eval2 is mutant-verdict robustness' in page
    assert 'does not establish complete functional correctness' in page


def test_riscv_invariant_explanation_separates_modular_proofs_from_soundness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1378']
    assert 'comsec.ethz.ch' in row['evidence_url']
    assert '43 seconds' in ' '.join(row['metrics'])
    assert 'modular proof is valid only' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-and-functional-verification.md').read_text()
    assert page.count('<span id="paper-') == 7
    assert page.count('<span id="explanation-dac-2026-research1378"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1378)' in page
    assert 'The property compares two implementations over time' in page
    assert 'Invariants constrain reachable state' in page
    assert 'A proof failure can expose a specification failure' in page
    assert 'They do not establish that every invariant preserves' in page


def test_safegen_explanation_separates_structural_propagation_from_safety_criticality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1945']
    assert row['evidence_url'].endswith('2606.25296v1')
    assert '2,287' in ' '.join(row['metrics'])
    assert 'not a failure probability' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-and-functional-verification.md').read_text()
    assert page.count('<span id="paper-') == 7
    assert page.count('<span id="explanation-dac-2026-research1945"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1945)' in page
    assert 'Fault propagation is not the same as safety criticality' in page
    assert 'The evidence chain has four separate links' in page
    assert 'HyperKG represents cross-document safety context' in page
    assert 'SafeGen detects 2,287 of 18,869' in page
    assert 'does not establish that the extracted requirements are complete' in page


def test_stellar_explanation_separates_retrieval_path_coverage_and_formal_coverage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3200']
    assert 'arxiv.org/pdf/2601.19903v3' in row['evidence_url']
    assert '99.80%' in ' '.join(row['metrics'])
    assert 'none alone proves that an assertion is nonvacuous' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-and-functional-verification.md').read_text()
    assert page.count('<span id="paper-') == 7
    assert page.count('<span id="explanation-dac-2026-research3200"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research3200)' in page
    assert 'The unit of retrieval is a block with local context' in page
    assert 'STELLAR traverses the target AST' in page
    assert 'UART, an I2C master controller and SHA-3/Keccak' in page
    assert 'does not establish universal assertion correctness' in page


def test_hidden_pmu_explanation_separates_event_observation_from_security_claims() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1037']
    assert 'RESEARCH1037' in row['evidence_url']
    assert 'hidden UMask-combination pattern' in ' '.join(row['metrics'])
    assert 'A counter correlation is not by itself a complete causal semantics' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-and-functional-verification.md').read_text()
    assert page.count('<span id="paper-') == 7
    assert page.count('<span id="explanation-dac-2026-research1037"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1037)' in page
    assert 'The observable is a counter, not the hardware meaning' in page
    assert 'Simulation supplies a second observation path' in page
    assert 'The security demonstrations use the recovered signal' in page
    assert 'The target manuscript, numerical tables, simulator details and artifact were not recovered' in page


def test_chatsva_explanation_separates_syntax_function_and_coverage_metrics() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1356']
    assert row['evidence_url'].endswith('2604.02811v1')
    assert '98.66%' in ' '.join(row['metrics'])
    assert 'different denominators and meanings' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-and-functional-verification.md').read_text()
    assert page.count('<span id="paper-') == 7
    assert page.count('<span id="explanation-dac-2026-research1356"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1356)' in page
    assert 'The target is a verified behavior, not merely legal SVA syntax' in page
    assert 'Spec → Verification Plan → Feature List → Checkpoint → SVA' in page
    assert 'The data loop uses forward and reverse checks' in page
    assert 'The results do not establish complete specification coverage' in page


def test_deepseq3_explanation_separates_representation_power_and_bmc_evidence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research080']
    assert row['evidence_url'].endswith('2608.28188v1')
    assert '191.11' in ' '.join(row['metrics'])
    assert 'different denominators' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/formal-and-functional-verification.md').read_text()
    assert page.count('<span id="paper-') == 7
    assert page.count('<span id="explanation-dac-2026-research080"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research080)' in page
    assert 'A sequential circuit is not only a combinational graph' in page
    assert 'The pretraining target is global state behavior' in page
    assert 'Guided BMC changes the search order but keeps a fallback' in page
    assert 'They do not establish that sampled reachability labels are complete' in page


def test_noisexplore_explanation_separates_noise_model_snr_and_application_result() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1152']
    assert 'RESEARCH1152' in row['evidence_url']
    assert '86.8%' in ' '.join(row['metrics'])
    assert 'three-class subset' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/analog-and-mixed-signal-synthesis.md').read_text()
    assert page.count('<span id="paper-') == 1
    assert page.count('<span id="explanation-dac-2026-research1152"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1152)' in page
    assert 'The design problem crosses several abstraction levels' in page
    assert 'Noise sources change the meaning of an error' in page
    assert 'Bayesian exploration chooses which configurations to evaluate' in page
    assert 'It does not establish a fabricated-chip result' in page


def test_hyperanalog_explanation_separates_representation_from_electrical_result() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research445']
    assert 'RESEARCH445' in row['evidence_url']
    assert 'reports no accuracy' in ' '.join(row['metrics'])
    assert 'does not automatically preserve terminal roles' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/analog-circuit-learning.md').read_text()
    assert page.count('<span id="paper-') == 1
    assert page.count('<span id="explanation-dac-2026-research445"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research445)' in page
    assert 'The representation is an input to a later engineering task' in page
    assert 'A pairwise graph can lose a shared relation' in page
    assert 'Domain awareness must be made concrete' not in page
    assert 'It does not establish a specific prediction accuracy' in page


def test_composer_explanation_separates_em_model_speedup_from_post_layout_evidence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1407']
    assert row['evidence_url'].endswith('2603.20486v3')
    assert '23.58' in ' '.join(row['metrics'])
    assert 'not fabricated-silicon measurements' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/analog-circuit-optimization.md').read_text()
    assert page.count('<span id="paper-') == 1
    assert page.count('<span id="explanation-dac-2026-research1407"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1407)' in page
    assert 'The target is a post-layout circuit, not only a schematic' in page
    assert 'Stage 1 combines equations with learned EM models' in page
    assert 'Stage 4 closes the schematic–layout loop' in page
    assert 'The ablation isolates the cost of ignoring layout' in page
    assert 'does not establish universal topology synthesis' in page


def test_fsgen_explanation_separates_design_space_pareto_results_and_power_model() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research868']
    assert row['evidence_url'].endswith('2608.09252v1')
    assert '768' in row['workload_or_benchmark']
    assert '12.8%' in ' '.join(row['metrics'])
    assert 'universal superiority' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/hardware-generation-and-compilation.md').read_text()
    assert page.count('<span id="paper-') == 1
    assert page.count('<span id="explanation-dac-2026-research868"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research868)' in page
    assert 'The search space is part of the hardware method' in page
    assert 'Fusion changes the lifetime of intermediate tensors' in page
    assert 'Sparsity has a condition, a location and a mapping' in page
    assert 'Early power estimation is built from primitives' in page
    assert 'It does not establish silicon results' in page


def test_notsotiny_explanation_separates_benchmark_scope_from_model_capability() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2760']
    assert row['evidence_url'].endswith('2512.20823v1')
    assert '3,062' in row['workload_or_benchmark']
    assert 'proof, timeout, unproven' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="paper-') == 20
    assert page.count('<span id="explanation-dac-2026-research2760"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2760)' in page
    assert 'The paper changes the object being evaluated' in page
    assert '3,062 tasks after deduplication' in page
    assert 'A timeout says that the evaluation did not finish' in page
    assert 'Contextual module completion is not unconstrained specification-to-chip generation' in page


def test_hlsdebugger_explanation_separates_location_correction_and_hardware_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['iccad-2025-1027']
    assert row['evidence_url'].endswith('2507.21485v1')
    assert '37.6%' in ' '.join(row['metrics'])
    assert 'not compilation' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="paper-') == 20
    assert page.count('<span id="explanation-iccad-2025-1027"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-iccad-2025-1027)' in page
    assert 'The debugging problem is not syntax repair' in page
    assert 'The dataset creates supervision by changing known code' in page
    assert 'The evaluation uses several denominators' in page
    assert 'not the same as compiling the corrected HLS' in page
    assert 'do not establish coverage of naturally occurring HLS failures' in page


def test_squat_explanation_separates_precision_quality_latency_and_table_errors() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['iccad-2025-105']
    assert row['evidence_url'].endswith('2402.10787v2')
    assert '2.03' in ' '.join(row['metrics'])
    assert 'not an iso-accuracy claim' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/architecture-software-co-design.md').read_text()
    assert page.count('<span id="paper-') == 13
    assert page.count('<span id="explanation-iccad-2025-105"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-iccad-2025-105)' in page
    assert 'The deployment problem is a joint numerical and instruction-format problem' in page
    assert 'The training losses preserve two different properties' in page
    assert 'The MKMP kernel closes the representation-to-instruction gap' in page
    assert 'The paper\'s displayed speedup labels contain an evidence issue' in page
    assert 'does not establish the same tradeoff for larger models' in page


def test_tasa_explanation_separates_thermal_model_bandwidth_and_speedup() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['iccad-2025-1103']
    assert row['evidence_url'].endswith('2508.07252v3')
    assert '2.85×' in ' '.join(row['metrics'])
    assert 'fabricated-silicon' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/3d-stacking-and-thermal-management.md').read_text()
    assert page.count('<span id="paper-') == 7
    assert page.count('<span id="explanation-iccad-2025-1103"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-iccad-2025-1103)' in page
    assert 'The workload creates two different bottlenecks' in page
    assert 'The thermal analysis establishes why placement matters' in page
    assert 'Bandwidth sharing is a cache-allocation problem' in page
    assert 'The simulator combines Timeloop' in page
    assert 'should not be presented as a physical operating temperature' in page


def test_energon_explanation_separates_sensor_leakage_architecture_and_attack() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['iccad-2025-1000']
    assert row['evidence_url'].endswith('2508.01768v1')
    assert '89%' in ' '.join(row['metrics'])
    assert 'not weight/training-data recovery' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="paper-') == 30
    assert page.count('<span id="explanation-iccad-2025-1000"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-iccad-2025-1000)' in page
    assert 'The leaked object is architecture, not a model output' in page
    assert 'The threat model depends on shared physical sensors' in page
    assert 'The downstream attack is a separate experiment' in page
    assert 'does not establish that every NVIDIA GPU' in page


def test_mirage_explanation_separates_hierarchy_pruning_and_timing_boundary() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2243']
    assert row['evidence_url'].endswith('2510.08976v3')
    assert '93.3 QPS' in ' '.join(row['metrics'])
    assert 'query decomposition' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/multimedia-and-edge-systems.md').read_text()
    assert page.count('<span id="paper-') == 9
    assert page.count('<span id="explanation-dac-2026-research2243"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2243)' in page
    assert 'The hierarchy creates three different opportunities to remove work' in page
    assert 'A stable ranking is evidence that this particular search has stopped changing' in page
    assert 'The timing boundary is essential' in page
    assert 'does not establish that ranking stability detects correctness' in page


def test_ellm_explanation_separates_memory_sharing_slo_and_throughput_boundaries() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1351']
    assert row['evidence_url'].endswith('2506.15155v2')
    assert '2.32× decode throughput' in ' '.join(row['metrics'])
    assert 'not online response-time improvement' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/datacenter-and-cloud-systems.md').read_text()
    assert page.count('<span id="paper-') == 5
    assert page.count('<span id="explanation-dac-2026-research1351"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1351)' in page
    assert 'The resource problem is separate logical lifetimes competing for the same bytes' in page
    assert 'CPU overflow changes queueing and token-generation cost in opposite directions' in page
    assert 'The scheduler treats buffer size as a control variable' in page
    assert 'does not establish the same gains on other GPU generations' in page


def test_hw_router_explanation_separates_runtime_prediction_quality_and_skew() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3129']
    assert row['evidence_url'].endswith('2608.14575v1')
    assert '200 µs' in ' '.join(row['metrics'])
    assert 'absolute queue-length difference' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/datacenter-and-cloud-systems.md').read_text()
    assert page.count('<span id="paper-') == 5
    assert page.count('<span id="explanation-dac-2026-research3129"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research3129)' in page
    assert 'Routing cost is a property of a query, model, device, and queue state' in page
    assert 'The polling interval creates a boundary' in page
    assert 'SLO and load-balance metrics have specific meanings' in page
    assert 'does not establish a hard deadline guarantee' in page


def test_greenllm_explanation_separates_prefill_decode_energy_and_slo() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research976']
    assert row['evidence_url'].endswith('2508.16449v1')
    assert '27.52%' in ' '.join(row['metrics'])
    assert '4.3 percentage points' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/datacenter-and-cloud-systems.md').read_text()
    assert page.count('<span id="paper-') == 5
    assert page.count('<span id="explanation-dac-2026-research976"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research976)' in page
    assert 'Power, energy, and service quality are different quantities' in page
    assert 'The control path has three linked decisions' in page
    assert 'The reported quality boundary needs to remain visible' in page
    assert 'does not establish transfer to other GPU generations' in page


def test_gemm_gs_explanation_separates_reformulation_kernel_quality_and_sorting() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research054']
    assert row['evidence_url'].endswith('2604.02120v1')
    assert '1.42× on A100' in ' '.join(row['metrics'])
    assert 'matrix dimensions' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-ai-accelerators.md').read_text()
    assert page.count('<span id="paper-') == 9
    assert page.count('<span id="explanation-dac-2026-research054"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research054)' in page
    assert 'The bottleneck is a mismatch between the calculation and the GPU datapath' in page
    assert 'The coordinate transformation exposes six reusable products' in page
    assert 'Matrix conversion does not eliminate the rest of volume rendering' in page
    assert 'does not establish equal image quality under all precisions' in page


def test_masq_explanation_separates_precision_dependency_quality_and_modeled_hardware() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1307']
    assert row['evidence_url'].endswith('2605.23226v1')
    assert '16.06×' in ' '.join(row['metrics'])
    assert 'FID regresses' in ' '.join(row['limits'])
    assert row['_original_evidence']['evidence_url'] != row['evidence_url']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-ai-accelerators.md').read_text()
    assert page.count('<span id="paper-') == 9
    assert page.count('<span id="explanation-dac-2026-research1307"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1307)' in page
    assert 'The mask does not define the full computation boundary' in page
    assert 'Spatial importance follows receptive fields' in page
    assert 'The hardware executes several precisions with one block-scaled format' in page
    assert 'does not establish zero quality loss' in page


def test_dspe_explanation_separates_reuse_approximation_security_and_hardware() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1206']
    assert row['evidence_url'].endswith('2605.08615v1')
    assert '109.4 TFLOPS/W' in ' '.join(row['metrics'])
    assert 'not a cryptographic' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-ai-accelerators.md').read_text()
    assert page.count('<span id="paper-') == 9
    assert page.count('<span id="explanation-dac-2026-research1206"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1206)' in page
    assert 'The paper combines three different reductions' in page
    assert 'MIPS uses approximate similarity decisions, not a cryptographic proof' in page
    assert 'MBLM changes the Booth path using observed bit patterns' in page
    assert 'does not establish cryptographic security' in page


def test_topgq_explanation_preserves_preparation_and_quality_limits() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/approximate-and-precision-aware-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research3214)' in page
    assert '32.22-percentage-point loss' in page
    assert '61.83%' in page and '63.18%' in page
    assert 'not fiftyfold inference improvements' in page
    assert 'No TopGQ model evaluation, inference benchmark, or source-code execution was performed' in page
    from fractions import Fraction as F
    adjacency = [F(1, 2), F(1, 2)]
    features, scales = [F(2), F(20)], [F(2), F(20)]
    assert sum(a*x for a,x in zip(adjacency, features)) == 11
    assert sum((a*s)*(x/s) for a,s,x in zip(adjacency, scales, features)) == 11


def test_ultrasketch_explanation_preserves_code_and_memory_limits() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/approximate-and-precision-aware-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2317)' in page
    assert 'maximum-magnitude rule on the inspected matrix-compression path' in page
    assert 'do not establish a packed four-bit exported representation' in page
    assert 'not a 14.9× speedup over an uncompressed language model' in page
    assert 'No UltraSketchLLM model evaluation, CUDA kernel, or training run was executed' in page
    assert 65 * 4 / 512 == 0.5078125
    assert 65 * 32 / 512 == 4.0625
    assert min([0.2, 0.8], key=abs) != max([0.2, 0.8], key=abs)


def test_capa_explanation_keeps_format_and_accuracy_boundaries() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/approximate-and-precision-aware-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2410)' in page
    assert 'not verified HDBFP layouts or CAPA schedules' in page
    assert 'No CAPA implementation, benchmark, or synthesis was executed' in page
    assert 'a universal arithmetic-correctness guarantee' in page
    assert 256 * (-8) * (-8) > 2**14 - 1
    # All signed INT8 values reconstruct from signed high and unsigned low parts.
    for weight in range(-128, 128):
        high, low = weight // 16, weight % 16
        assert -8 <= high <= 7 and 0 <= low <= 15
        assert 16 * high + low == weight


def test_core_explanation_keeps_description_only_boundary() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/approximate-and-precision-aware-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1692)' in page
    assert 'examples are not verified CORE encodings' in page
    assert 'No CORE implementation, benchmark, or synthesis was executed' in page
    assert 'operation-count convention' in page
    assert 'a 54.1% reduction' in page
    assert '200 on the extra path' in page


def test_adana_explanation_and_proxy_counterexample() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/approximate-and-precision-aware-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2184)' in page
    assert '17.91% energy reduction versus BitMod' in page
    assert '3.50% higher latency versus INT-Asym' in page
    assert 'No Adana model evaluation, quantizer implementation, or hardware synthesis was executed' in page
    assert 'five-bit fixed-point values for three-bit Adana' in page
    # Constructed in-range group: verify the article's proxy-ranking limitation.
    from fractions import Fraction as F
    values = [F(26, 100), F(26, 100), F(349, 100), F(5)] + [F(0)] * 12
    grids = [list(map(F, range(6))) + [F(m) + F(1, 2), F(m) + F(3, 2)] for m in range(4)]
    proxy_values = [F(round(x * 2), 2) for x in values]
    misses = [sum(x not in grid for x in proxy_values) for grid in grids]
    errors = [sum(min((x - y) ** 2 for y in grid) for x in values) for grid in grids]
    assert misses == [1, 3, 2, 2]
    assert errors[0] == F(3553, 10000)
    assert errors[2] == F(1353, 10000)
    assert errors[0] > errors[2]


def test_dapa_explanation_preserves_baselines_and_reproduction_limits() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/approximate-and-precision-aware-compute.md').read_text()
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2094)' in page
    assert '0.00409' in page
    assert '90.625 ms' in page
    assert '0.25 percentage points' in page
    assert 'does not implement that separate backward rule in this module' in page
    assert 'that comparison is eightfold' in page
    assert 'No DAPA model evaluation, training run, or hardware synthesis was executed' in page
    assert 'a2c58e0b83962cb3ea996998722b8ce35b234b5a' in page


def test_compiler_runtime_chapter_keeps_description_boundaries() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/compiler-and-runtime-optimization.md').read_text()
    assert page.count('<span id="paper-') == 2
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research127)' in page
    assert 'not verified DyTuner mechanisms' in page
    assert 'first integer count' in page and '112' in page
    assert '195× at five million' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2566)' in page
    assert '2τtotal' in page
    assert 'GPU comparison is indirect' in page
    assert '2.36 ps' in page
    assert 'matching full manuscript was not recovered' in page


def test_processor_chapter_preserves_method_and_source_conflict_boundaries() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/processor-and-rtl-verification.md').read_text()
    assert page.count('<span id="paper-') == 3
    assert page.count('<span id="explanation-dac-2026-research150"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research150)' in page
    assert 'the Spike reference model, not RTL state coverage' in page
    assert 'milliseconds while the surrounding prose says seconds' in page
    assert 'Implemented scope is therefore unresolved' in page
    assert 'Independent comprehension review remains open' in page
    assert '93.4 / 43.6 / 95.7' in page
    assert 'no result was reproduced' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2533)' in page
    assert 'six bugs, five marked new' in page
    assert 'a search policy, not proof' in page
    assert 'partly uses published comparison data' in page
    assert 'PDF page 1 is a repository cover sheet' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research616)' in page
    assert 'false negatives' in page
    assert '108.3%, not 60%' in page
    assert 'approximately 2× slower' in page
    assert 'All three paper discussions now have manuscript-backed explanations' in page
    # Navigation/source-boundary regression, not an assessment of readability.


def test_memory_chapter_preserves_records_and_links_hybrimoe_explanation() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/memory-hierarchy-and-persistence.md').read_text()
    assert page.count('<span id="paper-') == 14
    assert page.count('<span id="explanation-dac-2025-research1019"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2025-research1019)' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2945)' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research675)' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research461)' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2686)' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1986)' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research676)' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1061)' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1081)' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1028)' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research270)' in page
    assert '[Read the step-by-step explanation](#explanation-isca-2026-program-004)' in page
    assert '[Read the step-by-step explanation](#explanation-isca-2026-program-008)' in page
    assert 'Batch discrepancy unresolved' in page
    assert 'normal-path timing omits rare correction' in page
    assert 'not recovered ArrowMesh routes' in page
    assert "not Ctxmem's recovered state machine" in page
    assert '4.13 percentage points' in page
    assert 'accuracy and latency implementations' in page
    assert 'simultaneous high-throughput mutual host-memory access' in page
    assert 'Author preprint extending DAC; selected sections inspected' in page
    assert 'HybriMoE is a DAC 2025 comparison case, not a DAC 2026 paper.' in page
    assert '[Read the step-by-step explanation](#explanation-isca-2026-program-045)' in page
    assert 'All fourteen now have individual explanations' in page
    assert 'independent comprehension review remains open' in page


def test_nasic_explanation_separates_dense_expert_storage_from_moe_system_efficiency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1291']
    assert '3D NAND-based CAM-selected multibit computing-in-memory' in row['method_or_artifact']
    assert 'not demonstrated quality-preserving on-device MoE efficiency' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1291"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1291)' in page
    for phrase in (
        'Mixture-of-Experts', 'expert networks', 'CAM', '3D NAND', 'multibit',
        'computing-in-memory', 'top-k', 'routing', 'dropped tokens',
        'ADC', 'precision', 'perplexity', 'retention', 'read disturb',
        'endurance', 'throughput', 'energy per token', 'CMOS peripherals',
        'not demonstrated quality-preserving on-device MoE efficiency',
    ):
        assert phrase in page


def test_expertflow_explanation_separates_predictive_cache_from_moe_serving_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2199']
    assert 'Predictive expert caching' in row['method_or_artifact']
    assert 'not demonstrated quality-preserving end-to-end MoE serving' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2199"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2199)' in page
    for phrase in (
        'MoE', 'experts', 'GPU memory', 'CPU memory', 'routing-path predictor',
        'token scheduler', 'predictive expert cache', 'top-k', 'perplexity',
        'cache hit rate', 'evictions', 'dropped tokens', 'interconnect',
        'p50/p95/p99', 'prefill', 'decode', '93.72%', '10×',
        'not demonstrated quality-preserving end-to-end MoE serving',
    ):
        assert phrase in page


def test_scoutattention_explanation_separates_layer_ahead_cpu_work_from_kv_serving_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2345']
    assert 'layer-ahead CPU pre-computation' in row['method_or_artifact']
    assert 'not demonstrated quality-preserving long-context serving' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2345"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2345)' in page
    for phrase in (
        'Long-context', 'KV cache', 'CPU/DRAM', 'GPU waiting', 'block-wise sparse',
        'layer-ahead', 'asynchronous', 'recall', 'freshness', 'fallback',
        'logits', '2.4%', '2.1×', 'transferred bytes', 'GPU idle time',
        'p50/p95/p99', 'prefill', 'decode',
        'not demonstrated quality-preserving long-context serving',
    ):
        assert phrase in page


def test_paper_evidence_links_to_authored_explanation_without_duplicate_summary() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md').read_text()
    assert '## What the papers are trying to change' not in page
    assert 'These are evidence records, not substitutes for the explanations above.' in page
    for paper_id in ('iccad-2025-130', 'dac-2026-research1718', 'dac-2026-research1036', 'dac-2026-research2805', 'dac-2026-research2293', 'dac-2026-research1268', 'dac-2026-research1016', 'iccad-2025-1094'):
        assert page.count(f'<span id="explanation-{paper_id}"></span>') == 1
        assert page.count(f'<span id="paper-{paper_id}"></span>') == 1
        assert f'[Read the step-by-step explanation](#explanation-{paper_id})' in page
    # This checks navigation and record preservation, not conceptual quality.
    assert page.count('<span id="paper-') == 8


def test_editorial_corrections_preserve_originals_and_update_cards() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    before = json.dumps(rows, sort_keys=True)
    revised = apply_editorial_corrections(ROOT, rows)
    assert json.dumps(rows, sort_keys=True) == before
    corrected = [r for r in revised if '_editorial_correction' in r]
    expected = json.loads((ROOT / 'data/editorial-paper-corrections-v1.json').read_text())['rows']
    assert {r['paper_id'] for r in corrected} == {r['paper_id'] for r in expected}
    for row in corrected:
        card = '\n'.join(evidence_card(row))
        assert card.count(f'id="paper-{row["paper_id"]}"') == 1
        assert 'Updated source-backed reading card' in card
        assert '<details markdown="1">' in card and '</details>' in card
        import markdown
        rendered = markdown.markdown(card, extensions=['extra', 'toc', 'sane_lists'])
        original_section = rendered.split('<details>', 1)[1].split('</details>', 1)[0]
        assert '<strong>Problem:</strong>' in original_section
        assert '**Problem:**' not in original_section
        assert 'Original captured fields' in card
        assert row['evidence_url'] in card
        assert row['_original_evidence']['evidence_url'] in card
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/datacenter-and-cloud-systems.md').read_text()
    assert page.count('**Updated source-backed reading card**') >= 3
    assert 'not the tested GPU mix' in page


def test_editorial_corrections_reject_unknown_targets() -> None:
    with pytest.raises(ValueError, match='Unknown or duplicate'):
        apply_editorial_corrections(ROOT, [])


def test_current_view_is_idempotent_and_preserves_historical_review_state() -> None:
    from scripts.build_theme_pages import read_current_sample, read_selected_sample
    historical = {r['paper_id']: r for r in read_selected_sample(ROOT)}
    current = read_current_sample(ROOT)
    assert apply_editorial_corrections(ROOT, current) == current
    for row in current:
        old = historical[row['paper_id']]
        for field in ('theme_id', 'subtheme_id', 'independent_review_status'):
            assert row.get(field) == old.get(field)
        if row.get('_editorial_correction'):
            assert row['_current_evidence_review_status'] == 'correction_pending_condition_and_independent_review'
            assert row['_original_evidence']['metrics'] == old.get('metrics')
            assert row['evidence_url'] == row['_editorial_correction']['fields']['evidence_url']


def test_memory_article_preserves_description_only_evidence_boundaries() -> None:
    page = (ROOT / 'reports/observed-subthemes/memory-and-data-movement.md').read_text()
    assert page.count('**Updated source-backed reading card**') == 6
    assert page.count('<details markdown="1">') == 6
    assert 'not invented PDF pages' in page
    assert 'No thesis pages are cited as inspected' in page
    assert 'AMD Alveo U55C' in page
    assert 'RTX 4090 and A100' in page
    assert 'Register-file power is not whole-GPU energy' in page
    assert 'system baseline unresolved' in page


def test_edge_article_preserves_timing_and_negative_result_boundaries() -> None:
    page = (ROOT / 'reports/observed-subthemes/edge-embedded-and-mobile-systems.md').read_text()
    assert page.count('**Updated source-backed reading card**') == 6
    assert 'bounded response times' in page
    assert 'allows deadline misses' in page
    assert '11.37 ms' in page and '11.09 ms' in page
    assert 'DS-CNN and MobileNet unchanged' in page
    assert 'not every complete model' in page
    assert 'Its experimental pages were not inspected' in page
    assert 'PDF page 3' in page and 'page 7' in page


def test_ondemand_sparsity_explanation_separates_block_reuse_from_edge_task_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2030']
    assert 'block-granular units' in row['method_or_artifact']
    assert 'not demonstrated quality-preserving end-to-end edge efficiency' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2030"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2030)' in page
    for phrase in (
        'edge platform', 'memory', 'sparsity', 'multi-task', 'block-granular',
        'differential', 'task', 'accuracy', 'overlap', 'metadata', 'DMA',
        'cold', 'warm', 'p50/p95/p99', 'energy', '6.6×',
        'not demonstrated quality-preserving end-to-end edge efficiency',
    ):
        assert phrase in page


def test_specmoe_explanation_separates_speculative_acceptance_from_moe_serving_equivalence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research257']
    assert 'self-assisted speculative decoding' in row['method_or_artifact']
    assert 'not demonstrated exact or quality-preserving end-to-end serving' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research257"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research257)' in page
    for phrase in (
        'speculative decoding', 'draft', 'target model', 'accepted', 'rejected',
        'rollback', 'MoE', 'expert routing', 'token distributions', 'logits',
        'perplexity', 'acceptance rate', 'p50/p95/p99', 'memory/interconnect',
        '4.30×', 'no additional model training',
        'not demonstrated exact or quality-preserving end-to-end serving',
    ):
        assert phrase in page


def test_robotics_article_preserves_feedback_and_measurement_boundaries() -> None:
    page = (ROOT / 'reports/observed-subthemes/robotics-and-edge-ai.md').read_text()
    assert page.count('**Updated source-backed reading card**') == 7
    assert 'Observation-to-action delay' in page
    assert 'trainable-parameter ratio' in page
    assert 'not an uncertainty-estimation ensemble' in page.lower()
    assert 'seconds per output' in page
    assert 'not physical robot or neuromorphic-chip energy evidence' in page
    assert '2.92 versus 2.82' in page


@pytest.mark.parametrize('invalid', ['duplicate', 'missing_field', 'missing_provenance'])
def test_editorial_corrections_reject_incomplete_changes(tmp_path, invalid) -> None:
    register = json.loads((ROOT / 'data/editorial-paper-corrections-v1.json').read_text())
    entry = register['rows'][0]
    register['rows'] = [entry]
    if invalid == 'duplicate':
        register['rows'].append(entry)
    elif invalid == 'missing_field':
        del entry['fields']['limits']
    else:
        del entry['review_date']
    (tmp_path / 'data').mkdir()
    (tmp_path / 'data/editorial-paper-corrections-v1.json').write_text(json.dumps(register))
    with pytest.raises(ValueError):
        apply_editorial_corrections(tmp_path, [{'paper_id': entry['paper_id']}])


def test_quantum_article_preserves_distinct_optimization_and_evidence_boundaries() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/quantum-architectures-and-control.md').read_text()
    assert 'Five manuscripts were recovered' in page
    assert 'equal-depth schedules differ in logical error' in page
    assert 'not a demonstrated fabricated compressor' in page
    assert '92,600 to 236,000 μs' in page
    assert 'retrieved manuscript has nine pages' in page
    assert 'not a runtime complexity result' in page
    assert page.count('<summary>Original captured fields') == 9
    assert len(re.findall(r'<span id="paper-[^"]+"></span>', page)) == 9


def test_quantum_template_matching_separates_local_search_speed_from_circuit_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1052']
    assert 'commutativity-aware hypergraph' in row['method_or_artifact']
    assert 'not demonstrated hardware-aware compilation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/optimization-and-search-methods.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1052"></span>') == 1
    section = page.split('## Quantum template matching:', 1)[1].split('## Learned placement policies', 1)[0]
    for phrase in (
        'hypergraph', 'commuting gates', 'locality', 'circuit equivalence',
        'global phase', 'statevector', 'two-qubit', 'routing', '11–606x',
        'not demonstrated hardware-aware compilation',
    ):
        assert phrase in section


def test_specialized_accelerators_keep_quality_and_implementation_boundaries() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-ai-accelerators.md').read_text()
    assert 'Four full manuscripts were recovered' in page
    assert 'FID rises from 13.60 to 14.07' in page
    assert 'its H100 reference [1] is a DeepSeek paper' in page
    assert 'dimension inconsistency' in page
    assert '4.3×/2.8× correspond to HiHGNN/GDR-HGNN' in page
    assert page.count('<summary>Original captured fields') == 9


def test_interconnect_explanations_separate_exploration_controller_and_source_limits() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    c2c = revised['dac-2026-research130']
    cxl = revised['isca-2026-program-044']
    assert '7.8× simulation speedup' in ' '.join(c2c['metrics'])
    assert '64 nodes' in ' '.join(cxl['metrics'])
    assert cxl['evidence_url'].startswith('https://panmnesia.com/')
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/chiplet-and-on-chip-interconnect.md').read_text()
    assert page.count('<span id="paper-') == 2
    assert page.count('<span id="explanation-dac-2026-research130"></span>') == 1
    assert page.count('<span id="explanation-isca-2026-program-044"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research130)' in page
    assert '[Read the step-by-step explanation](#explanation-isca-2026-program-044)' in page
    assert 'The design problem is a large conditional search' in page
    assert 'A CXL transfer crosses several responsibilities' in page
    assert 'Simulation speed is not LLM inference speed' in page
    assert 'Silicon-proven wording does not establish' in page


def test_architecture_modeling_explanations_separate_bounds_and_fhe_specialization() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    ideal = revised['dac-2026-research690']
    hades = revised['dac-2026-research912']
    assert 'not a realizable processor forecast' in ' '.join(ideal['limits'])
    assert 'cryptographic-correctness' in ' '.join(hades['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/architecture-modeling-and-exploration.md').read_text()
    assert page.count('<span id="paper-') == 2
    assert page.count('<span id="explanation-dac-2026-research690"></span>') == 1
    assert page.count('<span id="explanation-dac-2026-research912"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research690)' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research912)' in page
    assert 'IdealSim: an upper-bound model is useful only when its idealization is named' in page
    assert 'Hades: application-specific FHE hardware must preserve the cryptographic task' in page
    assert 'Security is a fixed constraint, not a quality score' in page


def test_advanced_packaging_explanations_separate_rdl_and_ground_plane_evidence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    rdl = revised['dac-2026-research799']
    grace = revised['dac-2026-research1473']
    assert 'complete-net rate' in ' '.join(rdl['metrics'])
    assert 'receiver-level signal integrity' in ' '.join(grace['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/advanced-packaging-and-interconnect.md').read_text()
    assert page.count('<span id="paper-') == 2
    assert page.count('<span id="explanation-dac-2026-research799"></span>') == 1
    assert page.count('<span id="explanation-dac-2026-research1473"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research799)' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1473)' in page
    assert 'The object being routed is not a flat board' in page
    assert 'A signal needs a return path' in page
    assert 'Co-design is not the same as adding two optimizers' in page


def test_analog_design_explanations_separate_floquet_and_adc_uncertainty() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    floquet = revised['dac-2026-research2838']
    adc = revised['dac-2026-research3082']
    assert 'slow-decaying' in ' '.join(floquet['method_or_artifact'].split())
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/analog-and-mixed-signal-design.md').read_text()
    assert page.count('<span id="paper-') == 2
    assert page.count('<span id="explanation-dac-2026-research2838"></span>') == 1
    assert page.count('<span id="explanation-dac-2026-research3082"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2838)' in page
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research3082)' in page
    assert 'The analysis starts from a periodic operating state' in page
    assert "An ADC's transfer curve is a set of transition decisions" in page
    assert 'Sample count is not the same as test time' in page
    assert 'Fewer samples do not necessarily mean a shorter test' in page


def test_pangaea_explanation_separates_graph_validity_memory_and_abstract_evidence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2762']
    assert '1.47× throughput' in ' '.join(row['metrics'])
    assert 'Locus' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/bioinformatics-and-scientific-computing.md').read_text()
    assert page.count('<span id="paper-') == 1
    assert page.count('<span id="explanation-dac-2026-research2762"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2762)' in page
    assert 'The input is a read and the output is a scored graph correspondence' in page
    assert 'Memory efficiency and exact mapping are separate claims' in page
    assert 'The same abstract describes Locus separately' in page


def test_mahl_explanation_separates_hierarchy_validation_pass_at_five_and_ppa() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['iccad-2025-1207']
    assert 'Pass@5' in ' '.join(row['metrics'])
    assert 'not first-attempt success' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/chiplet-partitioning-and-integration.md').read_text()
    assert page.count('<span id="paper-') == 1
    assert page.count('<span id="explanation-iccad-2025-1207"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-iccad-2025-1207)' in page
    assert 'Partitioning creates a contract between dies' in page
    assert 'The six roles divide work, not responsibility' in page
    assert 'Pass@5 is a budgeted success probability' in page
    assert 'not an independent 2026 publication' in page


def test_confidential_migration_explanation_separates_functional_security_and_downtime() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2079']
    assert 'AMD SEV-to-Hygon CSV' in ' '.join(row['metrics'])
    assert 'attestation is not authorization' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/confidential-and-trusted-computing.md').read_text()
    assert page.count('<span id="paper-') == 1
    assert page.count('<span id="explanation-dac-2026-research2079"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2079)' in page
    assert 'Migration has a functional state problem and a security state problem' in page
    assert 'Heterogeneous TEEs expose representation and policy differences' in page
    assert 'Live migration has a moving-state and failure problem' in page


def test_l2l_explanation_separates_logic_layout_characterization_and_library_utility() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1765']
    assert 'Logical equivalence' in ' '.join(row['limits'])
    assert 'signoff' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/cross-layer-design-automation.md').read_text()
    assert page.count('<span id="paper-') == 1
    assert page.count('<span id="explanation-dac-2026-research1765"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1765)' in page
    assert 'A standard cell has several representations' in page
    assert 'A candidate must survive a chain of checks' in page
    assert 'Cell quality and library utility are different measurements' in page


def test_physics_prior_compact_model_explanation_separates_fidelity_range_and_decision_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2336']
    assert 'Agreement between symbolic and neural models' in ' '.join(row['limits'])
    assert 'process-calibrated validation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/device-and-process-modeling.md').read_text()
    assert page.count('<span id="paper-') == 1
    assert page.count('<span id="explanation-dac-2026-research2336"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2336)' in page
    assert 'Distillation has two different fidelity targets' in page
    assert 'Validity is a region, not a property of the expression alone' in page
    assert 'The downstream design decision is the strongest test' in page


def test_wfpinn_explanation_separates_weak_form_self_supervision_from_device_solver_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2346']
    assert 'Weak-form PINN' in row['method_or_artifact']
    assert 'not demonstrated calibrated device-model accuracy' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/device-modeling-and-simulation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2346"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2346)' in page
    for phrase in (
        'TCAD', 'semiconductor equations', 'FinFET', 'weak-form',
        'integral', 'Dirichlet', 'interior labels', 'material parameters',
        'boundary', 'junction', 'conservation', 'terminal current',
        '5.36×10⁻²', '2.16×10⁴', 'strong-form PINNs',
        'held-out', 'training time', 'not demonstrated calibrated device-model accuracy',
    ):
        assert phrase in page


def test_ram_cgra_explanation_separates_reachability_mapping_and_execution() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1712']
    assert 'Static connectivity' in ' '.join(row['limits'])
    assert 'initiation interval' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/compilation-and-mapping.md').read_text()
    assert page.count('<span id="paper-') == 1
    assert page.count('<span id="explanation-dac-2026-research1712"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1712)' in page
    assert 'A CGRA mapping must construct a timed data path' in page
    assert 'Reachability needs a defined state and time model' in page
    assert 'A valid mapping is not automatically a fast mapping' in page


def test_busybarn_explanation_separates_collectives_latency_faults_and_reproduction() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['isca-2026-program-060']
    assert 'No quantitative result' in ' '.join(row['metrics'])
    assert 'not independent execution' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/distributed-and-wafer-scale-inference.md').read_text()
    assert page.count('<span id="paper-') == 1
    assert page.count('<span id="explanation-isca-2026-program-060"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-isca-2026-program-060)' in page
    assert 'Distributed inference has two coupled schedules' in page
    assert 'Collective communication does not equal application latency' in page
    assert 'Artifact availability is not artifact reproduction' in page


def test_boolean_emulation_explanation_separates_target_semantics_speed_capacity_and_visibility() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3153']
    assert 'target progress' in ' '.join(row['limits'])
    assert 'target-cycle rate' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/emulation-and-prototyping.md').read_text()
    assert page.count('<span id="paper-') == 1
    assert page.count('<span id="explanation-dac-2026-research3153"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research3153)' in page
    assert 'An emulator executes a model, not the final chip' in page
    assert 'Capacity, speed and visibility form a three-way constraint' in page
    assert 'Correctness needs a reference at the target level' in page


def test_tob_sched_explanation_separates_topological_balance_from_emulation_throughput() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1348']
    assert 'topological-order balancing-driven static scheduling' in row['method_or_artifact']
    assert 'not demonstrated cycle-accurate PBE throughput' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1348"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1348)' in page
    for phrase in (
        'processor-based emulation', 'computation graph', 'dependencies',
        'inter-processor communication', 'topological-order balancing',
        'mobility', 'forward and backward', 'O(1)', 'cycle-accurate',
        'functional equivalence', 'deadlock', 'makespan', 'utilization',
        'communication bytes', '72%', '22.5%', '55%',
        'not demonstrated cycle-accurate PBE throughput',
    ):
        assert phrase in page


def test_atlas_explanation_separates_fit_prediction_from_safety_case_evidence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1390']
    assert 'bidirectional asynchronous topological message passing' in row['method_or_artifact']
    assert 'not demonstrated calibrated FIT prediction' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/thermal-and-reliability-modeling.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1390"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1390)' in page
    section = page.split('<span id="explanation-dac-2026-research1390"></span>', 1)[1].split('## Power integrity', 1)[0]
    for phrase in (
        'Failure in time', 'FIT', 'ASIL-D', 'graph neural network',
        'asynchronous topological', 'RankNet', 'CalibNet', 'top-k%',
        'O(|V|+|E|)', 'calibration', 'rare-event', 'selective hardening',
        'BFIT', 'DeepGate2', '220x', '53%',
        'not demonstrated calibrated FIT prediction',
    ):
        assert phrase in section


def test_ignite_explanation_separates_surrogate_speed_from_circuit_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1420']
    assert 'self-supervised circuit-topology encoder' in row['method_or_artifact']
    assert 'not demonstrated calibrated circuit-simulation replacement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/device-modeling-and-simulation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1420"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1420)' in page
    section = page.split('<span id="explanation-dac-2026-research1420"></span>', 1)[1].split('## Check the decision made with the model', 1)[0]
    for phrase in (
        'Circuit simulation', 'SPICE', 'self-supervised circuit-topology encoder',
        'Prior-data Fitted Network', 'in-context learning', 'active-learning',
        'waveform', 'worst-case', 'topology families', 'technology nodes',
        'Transistor sizing', 'yield optimization', 'R2 > 0.9', '95 samples',
        '15.8x', '2–30x', 'more than 5x',
        'not demonstrated calibrated circuit-simulation replacement',
    ):
        assert phrase in section


def test_pfats_explanation_separates_queue_isolation_from_tsn_guarantees() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research163']
    assert 'per-flow frame eligibility-time calculator' in row['method_or_artifact']
    assert 'not demonstrated deterministic end-to-end guarantees' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/real-time-and-networked-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research163"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research163)' in page
    section = page.split('<span id="explanation-dac-2026-research163"></span>', 1)[1].split('## Pareto-guided scheduling', 1)[0]
    for phrase in (
        'Time-Sensitive Networking', 'TSN', 'eligibility-time', 'Per-flow queues',
        'Synchronous Shift Register Matrix', 'SSRM', 'shared links',
        'arrival and service', 'clock domains', 'deadline misses',
        'queue occupancy', 'overload', 'FPGA', '192 flows', '7.14%',
        '5 μs', 'not demonstrated deterministic end-to-end guarantees',
    ):
        assert phrase in section


def test_zparaswap_explanation_separates_zns_placement_from_gnn_and_ssd_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2074']
    assert 'identifies access correlations in graph data' in row['method_or_artifact']
    assert 'not demonstrated general GNN speedup' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2074"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2074)' in page
    section = page.split('<span id="explanation-dac-2026-research2074"></span>', 1)[1].split('## Laelaps changes', 1)[0]
    for phrase in (
        'Zoned Namespace', 'ZNS', 'heterogeneous GNN', 'irregular access',
        'access correlations', 'correlated pages', 'SSD chips', 'zone',
        'page faults', 'queue depth', 'garbage collection', 'write amplification',
        'endurance', '34%', '44%', 'not demonstrated general GNN speedup',
    ):
        assert phrase in section


def test_compart_explanation_separates_community_guidance_from_partition_optimality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1300']
    assert 'community-guided framework' in row['method_or_artifact']
    assert 'not demonstrated globally optimal partitioning' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/graph-and-hypergraph-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1300"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1300)' in page
    section = page.split('<span id="explanation-dac-2026-research1300"></span>', 1)[1].split('## HySpecPro', 1)[0]
    for phrase in (
        'Hypergraph partitioning', 'hyperedges', 'coarsening', 'uncoarsening',
        'community', 'locally-dense decomposition', 'balance', 'epsilon',
        'hMETIS', 'KaHyPar', 'equal total time', 'Titan23', '0.943',
        'per-instance', 'MPSoC', 'multi-FPGA',
        'not establish globally optimal partitions',
    ):
        assert phrase in section


def test_vrram_lut_cim_explanation_separates_quantization_quality_from_array_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1412']
    assert 'Greedy G-Shuffle quantization' in row['method_or_artifact']
    assert 'not demonstrated universal 4-bit ViT edge deployment efficiency' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/analog-compute-in-memory.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1412"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1412)' in page
    section = page.split('<span id="explanation-dac-2026-research1412"></span>', 1)[1].split('## SDM:', 1)[0]
    for phrase in (
        'Dense prediction', 'INT4/2/1', 'Greedy G-Shuffle', 'PCA-based',
        'reconfigurable LUT-based CiM', '1TnR VRRAM', 'mIoU', 'RMSE',
        'ADE20K', 'NYUDv2', 'full precision', 'variation', 'ADC/DAC',
        'reconfiguration', '28-nm', '0.9-V', '400-MHz', '8.9×', '9.7×',
        'not demonstrated universal 4-bit ViT edge deployment efficiency',
    ):
        assert phrase in section


def test_inferweave_explanation_separates_bandwidth_scheduling_from_llm_equivalence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1466']
    assert 'bandwidth-aware inference framework' in row['method_or_artifact']
    assert 'not demonstrated universal end-to-end inference improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1466"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1466)' in page
    section = page.split('<span id="explanation-dac-2026-research1466"></span>', 1)[1].split('<span id="explanation-dac-2026-research3067"></span>', 1)[0]
    for phrase in (
        'heterogeneous unified-memory', 'HUMA', 'shared DRAM', 'InferWeave',
        'offline planner', 'data staging', 'asynchronous pipeline',
        'bandwidth-aware', 'operator placement', 'logits', 'perplexity',
        'DRAM bytes', 'time to first token', 'FlexGen', 'llama2.c',
        'LLaMA/GPT', 'MT-3000', '2.3×',
        'not demonstrated universal end-to-end inference improvement',
    ):
        assert phrase in section


def test_cacheparallel_explanation_separates_reuse_from_diffusion_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1976']
    assert 'fusion node' in row['method_or_artifact']
    assert 'not demonstrated quality-preserving universal diffusion acceleration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1976"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1976)' in page
    section = page.split('<span id="explanation-dac-2026-research1976"></span>', 1)[1].split('<span id="explanation-dac-2026-research2199"></span>', 1)[0]
    for phrase in (
        'Diffusion generation', 'timesteps', 'fusion node', 'pre-fusion',
        'post-fusion', 'CPS', 'intra-step', 'at different steps',
        'error-correction', 'sampler', 'random-seed', 'cache hit',
        'sample quality', 'p50/p95/p99', 'memory bandwidth',
        'training-free', '100%',
        'not demonstrated quality-preserving universal diffusion acceleration',
    ):
        assert phrase in section


def test_cox_moe_explanation_separates_expert_coalescing_from_serving_equivalence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2235']
    assert 'coalescing-aware orchestration' in row['method_or_artifact']
    assert 'not demonstrated quality-preserving universal throughput improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2235"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2235)' in page
    section = page.split('<span id="explanation-dac-2026-research2235"></span>', 1)[1].split('<span id="explanation-dac-2026-research2199"></span>', 1)[0]
    for phrase in (
        'Mixture-of-Experts', 'Micro-batches', 'AMX', 'CPU-GPU',
        'ordinary batches', 'attention', 'expert-aware stratification',
        'top-k routing', 'token dropping', 'logits', 'perplexity',
        'PCIe/interconnect', 'p50/p95/p99', 'FlexGen', 'MoE-Lightning',
        '7.1×', '2.4×',
        'not demonstrated quality-preserving universal throughput improvement',
    ):
        assert phrase in section


def test_pefool_explanation_separates_optimizer_memory_from_finetuning_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2271']
    assert 'PeFoo-L' in row['method_or_artifact']
    assert 'not demonstrated gradient-equivalent training' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2271"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2271)' in page
    section = page.split('<span id="explanation-dac-2026-research2271"></span>', 1)[1].split('<span id="explanation-dac-2026-research3067"></span>', 1)[0]
    for phrase in (
        'Backpropagation', 'forward-only optimizer', 'PeFoo', 'PeFoo-L',
        'preconditioning', 'one layer per iteration', 'forward evaluations',
        'query estimator', 'layer-selection schedule', 'loss/task quality',
        'peak memory', 'checkpoint', 'model sizes', 'edge feasibility',
        'MeZO', 'convergence curves',
        'not demonstrated gradient-equivalent training',
    ):
        assert phrase in section


def test_fault_tolerance_explanation_separates_correction_faults_quality_and_synthesis() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['iccad-2025-1109']
    assert 'Mantissa parity detects an error but does not reconstruct' in row['method_or_artifact']
    assert 'injected experiment settings' in ' '.join(row['limits'])
    assert '1.18 ns' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/fault-tolerance-and-reliability.md').read_text()
    assert page.count('<span id="paper-') == 1
    assert page.count('<span id="explanation-iccad-2025-1109"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-iccad-2025-1109)' in page
    assert 'The correction guarantee has a precise boundary' in page
    assert 'Hardware savings are not complete-system savings' in page


def test_accshield_explanation_separates_sensitivity_dependencies_and_missing_fault_model() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2057']
    assert 'operator-level error sensitivity' in row['method_or_artifact']
    assert 'does not establish a probability' in ' '.join(row['limits'])
    assert 'no numeric reliability' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/accelerator-reliability.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research2057"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2057)' in page
    assert 'What operator sensitivity means' in page
    assert 'The comparison that would establish benefit' in page


def test_xrel_graph_explanation_separates_layers_criticality_and_learning_evidence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2424']
    assert 'machine-learning approach' in row['method_or_artifact']
    assert 'not automatically lower total system cost' in ' '.join(row['limits'])
    assert 'no numeric power' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/accelerator-reliability.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research2424"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2424)' in page
    assert 'Why layer placement changes the cost' in page
    assert 'Why mixed criticality changes the objective' in page


def test_repair_explanation_separates_wear_writes_lifetime_and_flexibility_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2976']
    assert 'differential partial-bitstream generation' in row['method_or_artifact']
    assert 'lower maximum per-cell stress' in ' '.join(row['limits'])
    assert 'at least 7×' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/accelerator-reliability.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research2976"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2976)' in page
    assert 'The three mechanisms operate at different times' in page
    assert 'The comparison that would establish the 7× result' in page


def test_dfa_drive_explanation_separates_delay_faults_task_quality_cycles_and_safety() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1585']
    assert 'DFA-DRIVE propagates circuit-level timing failures' in row['method_or_artifact']
    assert 'not automatically a perception failure' in ' '.join(row['limits'])
    assert '92% fewer computation cycles' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/accelerator-reliability.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research1585"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1585)' in page
    assert 'Why delay faults become task-level faults' in page
    assert 'The comparison that would establish the claim' in page


def test_epar_explanation_separates_layout_scores_calibration_and_execution_reliability() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3059']
    assert 'effective Hamiltonian' in row['method_or_artifact']
    assert 'not a 10× execution speedup' in ' '.join(row['limits'])
    assert '100% agreement' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/accelerator-reliability.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research3059"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research3059)' in page
    assert 'Why a calibrated error rate is not the whole physical explanation' in page
    assert 'What the structural score can and cannot prove' in page


def test_probabilistic_memory_explanation_separates_sampling_system_scope_and_trustworthiness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1664']
    assert 'stores distribution parameters' in row['method_or_artifact']
    assert 'must not be pooled' in ' '.join(row['metrics'])
    assert 'not complete BNN inference' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/accelerator-reliability.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research1664"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1664)' in page
    assert 'What changes when samples are generated in memory' in page
    assert 'What “trustworthy” must mean here' in page


def test_tram_explanation_separates_joint_training_error_power_and_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2245']
    assert 'jointly optimizes approximate multiplier structures' in row['method_or_artifact']
    assert 'must not be pooled' in ' '.join(row['limits'])
    assert '25.05%' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/accelerator-reliability.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research2245"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2245)' in page
    assert 'Why multiplier error is not one number' in page
    assert 'What joint training changes' in page


def test_metric_explanation_separates_ecc_redundancy_sensitivity_and_analog_coverage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2347']
    assert 'two redundancy columns' in row['method_or_artifact']
    assert 'do not by themselves define' in ' '.join(row['limits'])
    assert 'claimed qualitatively' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/accelerator-reliability.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research2347"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2347)' in page
    assert 'Why two redundancy columns are not a universal guarantee' in page
    assert 'What analog syndrome decoding must establish' in page


def test_strix_explanation_separates_fault_model_detection_correction_and_silicon() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research043']
    assert 'pipeline' in row['method_or_artifact']
    assert 'not a measured correction-latency bound' in ' '.join(row['metrics'])
    assert 'Synthesis estimates are not fabricated-silicon measurements' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/accelerator-reliability.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research043"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research043)' in page
    assert 'Why full replication is expensive and targeted protection is difficult' in page
    assert 'The recovered fault model and evaluation boundary' in page


def test_bfp_npu_explanation_separates_shared_scale_faults_checks_and_dmr_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1139']
    assert 'Row/column-wise blocking' in row['method_or_artifact']
    assert 'Near-DMR reliability is not a defined universal metric' in ' '.join(row['limits'])
    assert '3.55%' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/accelerator-reliability.md').read_text()
    assert page.count('<span id="paper-') == 10
    assert page.count('<span id="explanation-dac-2026-research1139"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1139)' in page
    assert 'Why an end-to-end check can miss the important fault' in page
    assert 'What the row and column blocking is intended to do' in page


def test_marlin_explanation_separates_kv_capacity_selection_overlap_ttft_and_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1331']
    assert 'query-agnostic subset' in row['method_or_artifact']
    assert 'not a correctness guarantee' in ' '.join(row['limits'])
    assert 'no numeric TTFT' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="paper-') >= 1
    assert page.count('<span id="explanation-dac-2026-research1331"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1331)' in page
    assert 'Why token selection changes the retrieval problem' in page
    assert 'Why overlap is a scheduling claim, not free latency' in page


def test_ecprefix_explanation_separates_coded_distribution_from_serving_latency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1632']
    assert 'Erasure-coded distribution of hot prefix KV-cache blocks' in row['method_or_artifact']
    assert 'not demonstrated robust end-to-end LLM serving improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1632"></span>') == 1
    section = page.split('## ECPrefix: erasure coding', 1)[1].split('## Adaptive token-fluctuation prediction', 1)[0]
    for phrase in (
        'prefix', 'KV', 'Erasure coding', 'replication', 'reconstruction', 'striping',
        'pipelining', 'consistency', 'failure', 'TTFT', 'p95', 'p99', '52.3%',
        'not demonstrated robust end-to-end LLM serving improvement',
    ):
        assert phrase in section


def test_pimgrag_explanation_separates_graph_movement_pim_scheduling_and_rag_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1596']
    assert 'PIM architecture' in row['method_or_artifact']
    assert 'not automatically equal retrieval quality' in ' '.join(row['limits'])
    assert 'no numeric value' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1596"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1596)' in page
    assert 'Why graph retrieval is different from dense neural computation' in page
    assert 'Retrieval quality is separate from generation quality' in page


def test_pegasus_explanation_separates_placement_routing_communication_and_batching() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1922']
    assert 'selective local fine-tuning' in row['method_or_artifact']
    assert 'may change model quality' in ' '.join(row['limits'])
    assert '11.8x' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-embedded-and-mobile-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1922"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1922)' in page
    assert 'Start with the computation' in page
    assert 'The evaluation that would establish the claim' in page


def test_rtfl_explanation_separates_rounds_energy_participation_precision_and_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1936']
    assert 'adaptive quantization-based scheduling' in row['method_or_artifact']
    assert 'do not by themselves establish more useful learning' in ' '.join(row['limits'])
    assert 'qualitatively claims faster convergence' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-embedded-and-mobile-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1936"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1936)' in page
    assert 'Start with one federated-learning round' in page
    assert 'The tradeoffs that must be measured separately' in page


def test_satsfl_explanation_separates_feedback_approximation_compression_and_deployment() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1011']
    assert 'interpolated gradient approximation' in row['method_or_artifact']
    assert 'not the feedback that would have been computed' in ' '.join(row['limits'])
    assert 'qualitatively claims superior accuracy' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-embedded-and-mobile-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1011"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1011)' in page
    assert 'Start with the split-federated path' in page
    assert 'The evaluation that would establish disconnection tolerance' in page


def test_trace_explanation_separates_graph_position_objective_and_eda_evidence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research194']
    assert 'function-shift learning' in row['method_or_artifact']
    assert 'does not automatically prove' in ' '.join(row['limits'])
    assert 'qualitatively claims substantial improvement' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/graph-learning-for-eda.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research194"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research194)' in page
    assert 'What it means to compute on a circuit graph' in page
    assert 'What function-shift learning changes' in page


def test_gsr_gnn_explanation_separates_depth_memory_recomputation_sparsity_and_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research795']
    assert 'reversible residual modules' in row['method_or_artifact']
    assert 'trades stored memory for recomputation' in ' '.join(row['limits'])
    assert '87.2%' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/graph-learning-for-eda.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research795"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research795)' in page
    assert 'The resource problem is created by depth' in page
    assert 'What GSR-GNN changes' in page


def test_pba_rgat_edge_explanation_separates_arcs_paths_r_squared_and_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2333']
    assert 'dual-task' in row['method_or_artifact']
    assert 'not a percentage accuracy' in ' '.join(row['limits'])
    assert '0.997' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/graph-learning-for-eda.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2333"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2333)' in page
    assert 'Start with the timing objects' in page
    assert 'The evaluation that would establish timing-flow usefulness' in page


def test_crosstalk_prompt_explanation_separates_rc_coupling_prompts_and_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2537']
    assert 'Dual-level graph prompt learning' in row['method_or_artifact']
    assert 'Logical connectivity does not contain' in ' '.join(row['limits'])
    assert 'qualitatively claims precise prediction' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/graph-learning-for-eda.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2537"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2537)' in page
    assert 'What the electrical problem is' in page
    assert 'What the graph-prompt method changes' in page


def test_pg_gnn_explanation_separates_pvt_residuals_active_learning_and_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1562']
    assert 'uncertainty-driven active learning' in row['method_or_artifact']
    assert 'does not bound the worst' in ' '.join(row['limits'])
    assert '98.7%' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/graph-learning-for-eda.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1562"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1562)' in page
    assert 'What cell-library characterization produces' in page
    assert 'What PG-GNN changes' in page


def test_3d_eflash_explanation_separates_stack_temperature_programming_calibration_and_task_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1862']
    assert 'temperature-insensitive differential programming' in row['method_or_artifact']
    assert 'programming range differs' in ' '.join(row['limits'])
    assert '60.7%' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/3d-integration-and-thermal-management.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1862"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1862)' in page
    assert 'Start with the physical stack' in page
    assert 'What the thermal-stability strategy changes' in page


def test_polt_explanation_separates_hard_soft_tessellation_hpwl_and_physical_feasibility() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3027']
    assert 'pressure-driven orthogonal Laguerre' in row['method_or_artifact']
    assert 'does not establish routability' in ' '.join(row['limits'])
    assert '5.6%' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/3d-integration-and-thermal-management.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3027"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research3027)' in page
    assert 'What a 3D floorplan must represent' in page
    assert 'What POLT changes' in page


def test_integrated_3d_placement_explanation_separates_timing_parasitics_slack_and_routing() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research900']
    assert 'True-3D STA' in row['method_or_artifact']
    assert 'do not substitute for absolute slack' in ' '.join(row['limits'])
    assert '30–1002x' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/3d-integration-and-thermal-management.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research900"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research900)' in page
    assert 'Why ordinary placement models are insufficient' in page
    assert 'What the integrated framework changes' in page


def test_escaping_flatland_explanation_separates_tiers_vertical_resources_placement_and_routing() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3100']
    assert 'partitioning-based initialization' in row['method_or_artifact']
    assert 'not a routing or silicon improvement' in ' '.join(row['limits'])
    assert '3/7%' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/3d-integration-and-thermal-management.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3100"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research3100)' in page
    assert 'What an FPGA placement actually chooses' in page
    assert 'The evaluation that would establish a usable 3D FPGA flow' in page


def test_flexicts_explanation_separates_cppr_skew_physical_delay_and_hbt_resources() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research518']
    assert 'adaptive cross-die buffer assignment' in row['method_or_artifact']
    assert 'does not physically remove clock delay' in ' '.join(row['limits'])
    assert '4.1x' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/3d-integration-and-thermal-management.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research518"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research518)' in page
    assert 'What a clock tree and CPPR measure' in page
    assert 'What FlexiCTS changes' in page


def test_rtl3d_explanation_separates_prediction_relaxation_discrete_tiers_and_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research793']
    assert 'Transformer-based pre-synthesis timing-analysis model' in row['method_or_artifact']
    assert 'relaxed optimization representation' in ' '.join(row['limits'])
    assert '59.3%' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/3d-integration-and-thermal-management.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research793"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research793)' in page
    assert 'What tier partitioning decides' in page
    assert 'What the reported method changes' in page


def test_cool_explanation_separates_point_representation_boundaries_hotspots_and_speedup() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1846']
    assert 'cooling-aware point transformer' in row['method_or_artifact'].lower()
    assert 'does not bound maximum or hotspot error' in ' '.join(row['limits'])
    assert '2.4%' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/3d-stacking-and-thermal-management.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1846"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1846)' in page
    assert 'What the thermal prediction problem contains' in page
    assert 'What COOL changes in the representation and loss' in page


def test_pno_therm_explanation_separates_pde_transfer_data_cost_metrics_and_fem() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research553']
    assert 'foundation neural operator' in row['method_or_artifact']
    assert 'does not establish less than 20% of total preparation cost' in ' '.join(row['limits'])
    assert '940x' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/3d-stacking-and-thermal-management.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research553"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research553)' in page
    assert 'Why thermal data are expensive' in page
    assert 'What PNO-Therm changes' in page


def test_flash3d_explanation_separates_steady_state_modal_solver_error_and_speedups() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1065']
    assert 'spectral modal decomposition' in row['method_or_artifact']
    assert 'do not establish transient accuracy' in ' '.join(row['limits'])
    assert '0.5 K' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/3d-stacking-and-thermal-management.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1065"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1065)' in page
    assert 'What steady-state thermal analysis computes' in page
    assert 'What the analytical components do' in page


def test_legotherm_explanation_separates_mesh_reduction_ports_reassembly_and_hotspots() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research132']
    assert 'aggregate thermally coupled interface ports' in row['method_or_artifact']
    assert 'does not bound maximum or hotspot error' in ' '.join(row['limits'])
    assert '10.39x' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/3d-stacking-and-thermal-management.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research132"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research132)' in page
    assert 'Why repeated full simulations are expensive' in page
    assert 'What the modular reduction represents' in page


def test_seeing_through_silicon_explanation_separates_observations_inference_error_and_control() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1907']
    assert 'conditional diffusion reconstruction' in row['method_or_artifact']
    assert 'do not bound maximum hotspot error' in ' '.join(row['limits'])
    assert '0.48°C' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/3d-stacking-and-thermal-management.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1907"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1907)' in page
    assert 'Why neither input modality is enough' in page
    assert 'What the physics-informed conditional diffusion model does' in page


def test_ailfm_explanation_separates_migration_vf_locality_oracle_and_thermal_safety() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1302']
    assert 'active imitation-learning scheduler' in row['method_or_artifact'].lower()
    assert 'no quantitative thermal-safety' in ' '.join(row['limits'])
    assert 'generalization across diverse LFM workloads' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/3d-stacking-and-thermal-management.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1302"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1302)' in page
    assert 'What the scheduler controls' in page
    assert 'What active imitation learning contributes' in page


def test_duet_explanation_separates_prefill_decode_packages_handoff_and_serving_metrics() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3120']
    assert 'systolic-array chiplets' in row['method_or_artifact']
    assert 'adds a handoff' in ' '.join(row['limits'])
    assert '4x lower time to first token' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/chiplet-system-architecture.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3120"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research3120)' in page
    assert 'Why one accelerator sees two different workloads' in page
    assert 'What the two packages do' in page


def test_chipplanner_explanation_separates_early_estimates_bayesian_search_slack_and_closure() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research380']
    assert 'approximate placement before partitioning' in row['method_or_artifact']
    assert 'can reduce violations without achieving timing closure' in ' '.join(row['limits'])
    assert '42.4%' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/chiplet-system-architecture.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research380"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research380)' in page
    assert 'What the planning problem is' in page
    assert 'What ChiPlanner adds' in page


def test_chiser_explanation_separates_surrogate_ranking_search_coverage_and_weighted_objective() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research399']
    assert 'compact architecture-aware surrogate' in row['method_or_artifact']
    assert 'cannot recover a good design discarded' in ' '.join(row['limits'])
    assert '62%' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/chiplet-system-architecture.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research399"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research399)' in page
    assert 'Why accelerator exploration has two fidelity levels' in page
    assert 'What the surrogate must preserve' in page


def test_amber_explanation_separates_lossless_bits_quantization_bitserial_cost_and_inference() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research640']
    assert 'bit-transposed lossless compression' in row['method_or_artifact'].lower()
    assert 'does not reverse quantization error' in ' '.join(row['limits'])
    assert '3.16x' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/ai-accelerator-microarchitecture.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research640"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research640)' in page
    assert 'What lossless bit compression preserves' in page
    assert 'What the bit-serial processing element changes' in page


def test_mba_explanation_separates_capacity_bandwidth_kv_mapping_overlap_eviction_and_hardware() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research509']
    assert 'KV-cache-prioritized mapping' in row['method_or_artifact']
    assert 'does not guarantee full utilization' in ' '.join(row['limits'])
    assert '5.99x' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/ai-accelerator-microarchitecture.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research509"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research509)' in page
    assert 'Why capacity and bandwidth are different limits' in page
    assert 'What MBA changes in the memory and execution path' in page


def test_ahasd_explanation_separates_draft_acceptance_overlap_policy_and_system_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research384']
    assert 'task-level asynchronous heterogeneous architecture' in row['method_or_artifact'].lower()
    assert 'not end-to-end latency' in ' '.join(row['limits'])
    assert '4.2x throughput' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/ai-accelerator-microarchitecture.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research384"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research384)' in page
    assert 'What speculative decoding computes' in page
    assert 'What AHASD changes' in page


def test_oasis_explanation_separates_codes_values_luts_outliers_metrics_and_silicon() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['isca-2026-program-020']
    assert 'Cartesian-product lookup-table GEMM' in row['method_or_artifact']
    assert 'not automatically end-to-end speed' in ' '.join(row['limits'])
    assert '3.00x speedup' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/ai-accelerator-microarchitecture.md').read_text()
    assert page.count('<span id="explanation-isca-2026-program-020"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-isca-2026-program-020)' in page
    assert 'Why non-uniform quantization does not fit ordinary integer MACs' in page
    assert 'How outlier handling changes the numerical path' in page


def test_smoe_explanation_separates_expert_skew_dag_scaling_replicas_concurrency_and_slo() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research734']
    assert 'DAGNN cross-layer features' in row['method_or_artifact']
    assert 'does not establish hard per-request deadlines' in ' '.join(row['limits'])
    assert '21.4–39.2%' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/datacenter-and-cloud-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research734"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research734)' in page
    assert 'What an MoE serving pipeline contains' in page
    assert 'What the DAG representation makes visible' in page


def test_green_explanation_separates_graph_placement_rl_energy_slo_and_simulation_boundaries() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2970']
    assert 'GNN-RL cloud resource manager' in row['method_or_artifact']
    assert 'repository availability is not reproduction' in ' '.join(row['limits'])
    assert '2.17x energy savings' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/datacenter-and-cloud-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2970"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2970)' in page
    assert 'What scheduling and placement decide' in page
    assert 'What the graph formulation represents' in page


def test_train_once_calibrate_explanation_separates_adc_error_db_metrics_testchips_and_live_use() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3087']
    assert 'ConvRec' in row['method_or_artifact']
    assert 'ResConv' in row['method_or_artifact']
    assert 'not percentage-point accuracy' in ' '.join(row['limits'])
    assert '20 dB' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/analog-calibration-and-modeling.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3087"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research3087)' in page
    assert 'What ADC calibration is correcting' in page
    assert 'What “blind” means in this method' in page


def test_scale_gest_explanation_separates_model_space_selection_and_deployment_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3067']
    assert 'model-space synthesis' in row['method_or_artifact']
    assert 'runtime model-selection' in row['method_or_artifact']
    assert 'no accuracy, latency, energy, memory' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3067"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research3067)' in page
    assert 'What a gesture detector has to decide' in page
    assert 'What runtime selection changes' in page


def test_skist_explanation_separates_temporal_state_training_memory_and_inference() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research293']
    assert 'spatio-temporal adaptation' in row['method_or_artifact']
    assert 'no accuracy, peak memory, energy' in ' '.join(row['metrics'])
    assert 'Training-memory reduction does not establish lower inference memory' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research293"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research293)' in page
    assert 'Why spiking-network fine-tuning has a different memory problem' in page
    assert 'What must remain equal in the comparison' in page


def test_edgesc_explanation_separates_stochastic_representation_stream_cost_and_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research239']
    assert 'universal stochastic-computing architecture' in row['method_or_artifact']
    assert 'no detection quality, bitstream length, area, power' in ' '.join(row['metrics'])
    assert 'correlation can bias operations' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research239"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research239)' in page
    assert 'What edge detection computes' in page
    assert 'What a universal stochastic architecture must cover' in page


def test_flashfps_explanation_separates_fps_state_pruning_cache_and_downstream_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research124']
    assert 'pruning-and-caching method' in row['method_or_artifact']
    assert 'no runtime, memory, distance error' in ' '.join(row['metrics'])
    assert 'unsafe pruning or stale caching' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research124"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research124)' in page
    assert 'What farthest-point sampling does' in page
    assert 'What an efficiency claim must preserve' in page


def test_visual_wakeup_explanation_separates_frontend_power_false_wakeups_and_system_energy() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1691']
    assert 'Visual wakeup accelerator subsystem' in row['method_or_artifact']
    assert 'sub-mW target' in ' '.join(row['metrics'])
    assert 'not complete-system energy' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1691"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1691)' in page
    assert 'What a visual wakeup subsystem does' in page
    assert 'Why the sub-milliwatt boundary is not a complete system result' in page


def test_kerv_explanation_separates_speculation_acceptance_kinematics_and_control_latency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1900']
    assert 'Kinematic-rectified speculative decoding' in row['method_or_artifact']
    assert 'no token acceptance, observation-to-action latency' in ' '.join(row['metrics'])
    assert 'token acceptance is not the same as useful action rate' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1900"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1900)' in page
    assert 'What a VLA control loop produces' in page
    assert 'Why language-model acceptance is not enough' in page


def test_hyperlidar_explanation_separates_drift_hdc_updates_and_adaptation_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1960']
    assert 'Adaptive hyperdimensional-computing' in row['method_or_artifact']
    assert 'no segmentation accuracy, adaptation time, energy' in ' '.join(row['metrics'])
    assert 'adaptive wording does not establish' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1960"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1960)' in page
    assert 'What LiDAR segmentation produces' in page
    assert 'What hyperdimensional computing represents' in page


def test_sharedkd_explanation_separates_distillation_gradients_discovery_and_deployment_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2058']
    assert 'gradient-guided dynamic student discovery' in row['method_or_artifact']
    assert 'no detection accuracy, localization quality, latency' in ' '.join(row['metrics'])
    assert 'does not by itself establish' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2058"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2058)' in page
    assert 'What knowledge distillation changes' in page
    assert 'What dynamic student discovery is deciding' in page


def test_tsetlinwisard_explanation_separates_discrete_state_automata_and_onchip_scope() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2372']
    assert 'on-chip Tsetlin-automata training' in row['method_or_artifact']
    assert 'no accuracy, convergence, FPGA resource' in ' '.join(row['metrics'])
    assert 'does not mean no learned memory' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2372"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2372)' in page
    assert 'What a weightless neural network stores' in page
    assert 'What “on-chip training” includes' in page


def test_adaptive_snn_explanation_separates_event_execution_adaptation_and_deadlines() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research920']
    assert 'Adaptive spiking-neural-network detector' in row['method_or_artifact']
    assert 'no detection accuracy, latency, energy, event-rate' in ' '.join(row['metrics'])
    assert 'does not by itself establish a fixed real-time deadline' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research920"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research920)' in page
    assert 'What a spiking detector processes' in page
    assert 'What adaptive means in this detector' in page


def test_deltasight_explanation_separates_crossstage_validity_refresh_and_endtoend_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research952']
    assert 'cross-stage consistent redundancy-elimination architecture' in row['method_or_artifact']
    assert 'no accuracy, bandwidth, bytes transferred, latency' in ' '.join(row['metrics'])
    assert 'validity condition, refresh trigger and fallback path' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/edge-ai-and-deployment.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research952"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research952)' in page
    assert 'What a video AIoT pipeline does' in page
    assert 'What “cross-stage consistent” has to mean' in page


def test_multimedia_article_preserves_task_quality_and_timing_boundaries() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/multimedia-and-edge-systems.md').read_text()
    assert 'Five matching full manuscripts were inspected' in page
    assert 'not an untouched-test-set guarantee' in page
    assert 'query decomposition by Qwen3-8B is excluded' in page
    assert 'time to first token' in page
    assert '1.85×, whereas the conclusion says 1.87×' in page
    assert '0.97 percentage points, not 0.97% relative' in page
    assert 'slows to 0.3–0.6×' in page
    assert page.count('<summary>Original captured fields') == 9
    assert len(re.findall(r'<span id="paper-[^"]+"></span>', page)) == 9


def test_physical_compute_article_preserves_distinct_correctness_conditions() -> None:
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md').read_text()
    assert 'Three full manuscripts were inspected' in page
    assert 'squared error from the analytical result' in page
    assert 'not a complete PDE solution' in page
    assert '51.901 versus 51.549' in page
    assert '74,551 LUTs versus' in page
    assert 'not an engineering-time measurement' in page
    assert 'does not itself hide its input values or establish a general privacy guarantee' in page
    assert page.count('<summary>Original captured fields') == 4
    assert len(re.findall(r'<span id="paper-[^"]+"></span>', page)) == 8


def test_uninl_explanation_separates_nonlinear_approximation_fusion_and_endtoend_claims() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research617']
    assert 'primitive decomposition' in row['method_or_artifact']
    assert '6.89x speedup' in ' '.join(row['metrics'])
    assert 'task quality and approximation error' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/architecture-software-co-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research617"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research617)' in page
    assert 'Why nonlinear operators can leave a matrix accelerator underused' in page
    assert 'What utilization and energy claims must include' in page


def test_sparse_gpu_explanation_separates_metadata_decode_kernel_and_endtoend_speed() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1839']
    assert 'Three-layer sparse storage format' in row['method_or_artifact']
    assert '1.64x kernel-level speedup' in ' '.join(row['metrics'])
    assert 'different denominators' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/architecture-software-co-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1839"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1839)' in page
    assert 'What sparsity changes' in page
    assert 'Kernel speedup and inference speedup answer different questions' in page


def test_pimm_noc_explanation_separates_pimm_peripherals_noc_mapping_and_simulation() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2098']
    assert 'Heterogeneous PiMM/processing-unit tile NoC' in row['method_or_artifact']
    assert '3.45x DNN speedup' in ' '.join(row['metrics'])
    assert 'ADC/DAC' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/architecture-software-co-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2098"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2098)' in page
    assert 'What process-in-memristor memory changes' in page
    assert 'What RL and MCTS are searching' in page


def test_atb_explanation_separates_tile_lifetime_reuse_switching_and_ratio_discrepancy() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1000']
    assert 'independently chooses input and output tile dimensions' in row['method_or_artifact']
    assert '24.3/4.8=5.0625' in ' '.join(row['metrics'])
    assert 'differing matrix dimensions prevent' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/architecture-software-co-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1000"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1000)' in page
    assert 'What tiled matrix multiplication needs to store' in page
    assert 'What asymmetric buffering changes' in page


def test_kl_moe_explanation_separates_routing_kl_pruning_restore_and_metric_boundaries() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research094']
    assert 'Hierarchical expert clustering' in row['method_or_artifact']
    assert '1.31x inference speedup' in ' '.join(row['metrics'])
    assert 'KL divergence is directional' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/architecture-software-co-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research094"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research094)' in page
    assert 'What a mixture-of-experts layer does' in page
    assert 'What KL divergence is comparing' in page


def test_gendse_explanation_separates_sequential_search_gflownet_sketching_and_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1047']
    assert 'Markov-decision-process formulation' in row['method_or_artifact']
    assert '90% average simulation-cost reduction' in ' '.join(row['metrics'])
    assert 'cannot be interpreted as better design quality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/architecture-software-co-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1047"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1047)' in page
    assert 'What design-space exploration is evaluating' in page
    assert 'What a GFlowNet-style generator and sketching are for' in page


def test_hypercim_explanation_separates_hierarchy_surrogate_pareto_and_silicon_scope() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1101']
    assert 'digital 28-nm CIM template' in row['method_or_artifact']
    assert '90.8 TOPS/W' in ' '.join(row['metrics'])
    assert '297 million predicted configurations' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/architecture-software-co-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1101"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1101)' in page
    assert 'What the hierarchical predictive flow is doing' in page
    assert 'What silicon verification can and cannot establish' in page


def test_cassandra_explanation_separates_draft_acceptance_representation_and_edge_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['isca-2026-program-006']
    assert 'Training-free self-speculative decoding pipeline' in row['method_or_artifact']
    assert '2.41x speedup over BF16' in ' '.join(row['metrics'])
    assert 'generated-token count is not accepted-output latency' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/architecture-software-co-design.md').read_text()
    assert page.count('<span id="explanation-isca-2026-program-006"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-isca-2026-program-006)' in page
    assert 'What speculative decoding changes' in page
    assert 'Why reasoning LLMs need a stronger quality boundary' in page


def test_plena_explanation_separates_capacity_bandwidth_quantization_simulation_and_throughput() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['isca-2026-program-007']
    assert 'asymmetric-quantization compute/memory units' in row['method_or_artifact']
    assert '2.24x throughput over A100' in ' '.join(row['metrics'])
    assert 'Capacity and bandwidth are different limits' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/architecture-software-co-design.md').read_text()
    assert page.count('<span id="explanation-isca-2026-program-007"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-isca-2026-program-007)' in page
    assert 'What the two memory walls mean' in page
    assert 'What PLENA changes in the hardware/software path' in page


def test_mtia300_explanation_separates_collectives_message_engines_communication_and_perf_tco() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['isca-2026-program-069']
    assert '12×800-Gbps RDMA NICs' in row['method_or_artifact']
    assert '3.9x communication performance' in ' '.join(row['metrics'])
    assert 'have different denominators' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/architecture-software-co-design.md').read_text()
    assert page.count('<span id="explanation-isca-2026-program-069"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-isca-2026-program-069)' in page
    assert 'Why recommendation training becomes communication-bound' in page
    assert 'What the hardware numbers do and do not say' in page


def test_dynamic_inswitch_moe_explanation_separates_routing_switch_compute_simulation_and_training() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['isca-2026-program-058']
    assert 'DySHARP dynamic multimem addressing' in row['method_or_artifact']
    assert 'Numerical headline measurements are withheld' in ' '.join(row['metrics'])
    assert 'directional queue pressure' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/architecture-software-co-design.md').read_text()
    assert page.count('<span id="explanation-isca-2026-program-058"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-isca-2026-program-058)' in page
    assert 'Why MoE routing creates directional traffic' in page
    assert 'What in-switch computing is changing' in page


def test_patterns_behind_chaos_explanation_separates_routing_structure_forecast_placement_and_topology() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['isca-2026-program-005']
    assert 'Data-movement-centric temporal/spatial profiling' in row['method_or_artifact']
    assert '6.6x average speedup on wafer-scale GPUs' in ' '.join(row['metrics'])
    assert 'prediction error metric' in ' '.join(row['limits']) or 'forecast' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/architecture-software-co-design.md').read_text()
    assert page.count('<span id="explanation-isca-2026-program-005"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-isca-2026-program-005)' in page
    assert 'Why expert routing moves so much data' in page
    assert 'What forecasting can and cannot establish' in page


def test_lpn_acceleration_explanation_separates_crypto_parameters_pipeline_bandwidth_and_speed() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1822']
    assert 'heterogeneous FPGA architecture' in row['method_or_artifact']
    assert '52.80x performance gain' in ' '.join(row['metrics'])
    assert 'does not establish cryptographic superiority' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1822"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1822)' in page
    assert 'What LPN computation is' in page
    assert 'What the heterogeneous FPGA architecture is trying to coordinate' in page


def test_gkp_decoder_explanation_separates_syndrome_correlation_synthesis_and_loop_timing() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research727']
    assert 'Low-latency hardware accelerator' in row['method_or_artifact']
    assert '12.96 ns decoding latency' in ' '.join(row['metrics'])
    assert 'does not establish post-layout timing' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research727"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research727)' in page
    assert 'What a GKP decoder is deciding' in page
    assert 'Why correlation changes the computation' in page


def test_kcd_cam_explanation_separates_knn_distance_selection_pruning_recall_and_system_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1499']
    assert '4T2R ReRAM charge-domain CAM' in row['method_or_artifact']
    assert '279.79x speed' in ' '.join(row['metrics'])
    assert 'cannot change the required neighbors' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1499"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1499)' in page
    assert 'What K-nearest-neighbor search does' in page
    assert 'What KCD-CAM changes' in page


def test_cim_mp_explanation_separates_physical_updates_forward_error_backward_error_and_validation_boundary() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2128']
    assert 'pulse-based weight mapping' in row['method_or_artifact']
    assert '35.1%' in ' '.join(row['metrics'])
    assert 'does not establish robust physical CIM personalization' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2128"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2128)' in page
    assert 'What on-device personalization means' in page
    assert 'FVE addresses variation in the forward path' in page
    assert 'GAP addresses the backward path' in page


def test_modular_riscv_pqc_explanation_separates_kernel_reuse_instruction_latency_area_and_security() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2713']
    assert 'CV-X-IF' in row['method_or_artifact']
    assert '48 kGE' in ' '.join(row['metrics'])
    assert 'not a demonstrated secure' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2713"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2713)' in page
    assert 'What post-quantum cryptography requires from hardware' in page
    assert 'What the modular extension contributes' in page
    assert 'Why sharing and specialization are in tension' in page


def test_attina_explanation_separates_ntt_field_arithmetic_spatial_dataflow_and_proof_boundary() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research983']
    assert 'additive number-theoretic transform' in row['method_or_artifact']
    assert 'qualitative claim' in ' '.join(row['metrics'])
    assert 'not a measured edge zkSNARK advantage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research983"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research983)' in page
    assert 'What a zkSNARK prover is doing' in page
    assert 'What a number-theoretic transform does' in page
    assert 'What “spatial acceleration” means at the hardware boundary' in page


def test_isa_pm_explanation_separates_curve_math_isa_boundary_area_time_and_security() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2824']
    assert 'Montgomery and short-Weierstrass curves' in row['method_or_artifact']
    assert '8.37x area-time-product' in ' '.join(row['metrics'])
    assert 'side-channel validation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2824"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2824)' in page
    assert 'What elliptic-curve point multiplication does' in page
    assert 'Why supporting more than one curve form is a hardware problem' in page
    assert 'Why the area-time product needs a complete comparison boundary' in page


def test_coda_explanation_separates_computation_data_schedules_mapping_legality_and_performance() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1409']
    assert 'non-uniform loop-space modeling' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not evidence of an NPU speedup' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1409"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1409)' in page
    assert 'What a DNN dataflow has to decide' in page
    assert 'What computation-data decoupling changes' in page
    assert 'Why mapping expressiveness is not a performance result' in page


def test_factored_fpmac_explanation_separates_normalization_carry_save_numerics_and_ppa() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1837']
    assert '4:2 carry-save adders' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not evidence of numerical equivalence' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1837"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1837)' in page
    assert 'What a floating-point MAC normally does' in page
    assert 'What carry-save accumulation changes' in page
    assert 'Why numerical equivalence must be demonstrated' in page


def test_sparc_explanation_separates_sparse_values_metadata_scheduling_mapping_and_runtime() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1374']
    assert 'sparse-tensor scheduling' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not a demonstrated end-to-end sparse accelerator gain' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1374"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1374)' in page
    assert 'What sparsity changes in a tensor computation' in page
    assert 'Why sparse formats determine the hardware work' in page
    assert 'Why a qualitative compilation claim is not an accelerator result' in page


def test_pd_swap_explanation_separates_prefill_decode_reconfiguration_state_and_end_to_end_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1942']
    assert 'Dynamic partial reconfiguration' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'does not establish a measured FPGA advantage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1942"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1942)' in page
    assert 'What changes between prefill and decode' in page
    assert 'What dynamic partial reconfiguration does' in page
    assert 'What an end-to-end comparison must include' in page


def test_exquant_explanation_separates_expert_usage_sensitivity_precision_routing_and_serving_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research121']
    assert 'Global expert-ranking-guided' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'do not establish a serving benefit' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research121"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research121)' in page
    assert 'What an MoE layer is doing' in page
    assert 'What global expert ranking means' in page
    assert 'What a valid efficiency comparison requires' in page


def test_zk_tracer_explanation_separates_vm_trace_generation_memory_movement_and_proof_boundary() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1338']
    assert 'Heterogeneous accelerator' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not an end-to-end prover improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1338"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1338)' in page
    assert 'What a zero-knowledge VM trace represents' in page
    assert 'Why trace generation can become a bottleneck' in page
    assert 'Why trace throughput is not proof throughput' in page


def test_stcg_explanation_separates_sparse_tiles_tensor_core_occupancy_metadata_and_runtime() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1447']
    assert 'adaptive tile scheduling' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'does not establish a complete sparse-GPU gain' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1447"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1447)' in page
    assert 'Why tensor cores expose a sparse-tensor problem' in page
    assert 'What adaptive tile scheduling decides' in page
    assert 'Why occupancy is not just lane utilization' in page


def test_easy_zkp_explanation_separates_proof_stages_field_arithmetic_memory_and_system_boundary() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2504']
    assert 'End-to-end FPGA' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not a measured universal ZK-proving advantage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2504"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2504)' in page
    assert 'What a zero-knowledge prover has to compute' in page
    assert 'Why arithmetic and memory are coupled' in page
    assert 'What “end-to-end FPGA acceleration” should mean' in page


def test_pihg_explanation_separates_typed_aggregation_pivot_reuse_graph_memory_and_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1438']
    assert 'Pivot-centric' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not a demonstrated heterogeneous-GNN improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1438"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1438)' in page
    assert 'What a heterogeneous GNN computes' in page
    assert 'What a pivot-centric approach changes' in page
    assert 'Why irregular memory can dominate' in page


def test_ternainfer_explanation_separates_ternary_encoding_gpu_decode_quality_and_serving_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research200']
    assert 'approximately 1.58-bit' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not a measured universal GPU speedup' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research200"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research200)' in page
    assert 'What ternary weights are' in page
    assert 'What ternary arithmetic requires' in page
    assert 'Why model quality is a separate problem' in page


def test_overmind_nsa_explanation_separates_neural_symbolic_semantics_approximation_bypass_and_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2125']
    assert 'Unified neuro-symbolic' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not a demonstrated neuro-symbolic benefit' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2125"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2125)' in page
    assert 'What neuro-symbolic computation combines' in page
    assert 'What approximate nonlinear activations change' in page
    assert 'What preemptive memory bypass means' in page


def test_bibnn_explanation_separates_bayesian_uncertainty_bernoulli_conversion_computation_and_calibration() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2698']
    assert 'Post-training Bernoullization' in row['method_or_artifact']
    assert '88.6%' in ' '.join(row['metrics'])
    assert 'not preserved Bayesian uncertainty' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2698"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2698)' in page
    assert 'What Bayesian neural inference is estimating' in page
    assert 'What Bernoullization changes' in page
    assert 'What uncertainty evaluation must show' in page


def test_exra_explanation_separates_register_pressure_isa_compiler_spills_and_processor_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2897']
    assert 'expandable register files' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not a demonstrated system gain' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2897"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2897)' in page
    assert 'What register pressure means' in page
    assert 'What an expandable register file changes' in page
    assert 'Why ISA and compiler design are one problem here' in page


def test_adaptive_graph_transformer_explanation_separates_attention_partition_communication_and_convergence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3050']
    assert 'adaptive parallel-training framework' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not a demonstrated graph-transformer benefit' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3050"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research3050)' in page
    assert 'What a graph transformer adds to graph training' in page
    assert 'What partitioning decides' in page
    assert 'Why throughput is not convergence' in page


def test_tag_explanation_separates_graph_topology_memory_reuse_configuration_and_overhead() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research341']
    assert 'topology-aware GNN accelerator' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not a demonstrated benefit across graphs' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research341"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research341)' in page
    assert 'Why graph topology changes accelerator behavior' in page
    assert 'What topology-aware configuration can change' in page
    assert 'What configurability costs' in page


def test_aloha_explanation_separates_stochastic_streams_correlation_sequence_length_and_hardware_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2256']
    assert 'Hammersley-sequence' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not establish numerical quality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2256"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2256)' in page
    assert 'What stochastic computing represents' in page
    assert 'Why correlation changes the arithmetic' in page
    assert 'What Hammersley sequences are intended to provide' in page


def test_zk_flex_explanation_separates_proof_system_variation_reuse_reconfiguration_and_scaling() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research272']
    assert 'Flexible scalable' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not a measured advantage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research272"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research272)' in page
    assert 'Why zero-knowledge proof systems differ in hardware work' in page
    assert 'What a flexible framework must abstract' in page
    assert 'What scalability can mean' in page


def test_ai_asic_zk_explanation_separates_tensor_assumptions_exact_field_arithmetic_memory_and_flexibility() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2888']
    assert 'AI-ASIC-inspired' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not an ASIC result' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2888"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2888)' in page
    assert 'What an AI ASIC usually optimizes' in page
    assert 'What exact finite-field arithmetic requires' in page
    assert 'Why programmability changes the hardware tradeoff' in page


def test_adapt_explanation_separates_spiking_events_temporal_state_pruning_hierarchy_and_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1480']
    assert 'Training-free adaptive token pruning' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'does not establish preserved spiking-transformer quality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1480"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1480)' in page
    assert 'What a spiking transformer processes' in page
    assert 'What training-free means here' in page
    assert 'What hierarchical pruning changes' in page


def test_filco_explanation_separates_composition_reconfiguration_dataflow_utilization_and_full_inference() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1569']
    assert 'Composable' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'does not establish a complete DNN-inference benefit' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1569"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1569)' in page
    assert 'Why DNN layers need different hardware shapes' in page
    assert 'What composition means at the dataflow boundary' in page
    assert 'What real-time reconfiguration changes' in page


def test_rfipsa_explanation_separates_systolic_dataflow_reconfiguration_workload_shape_and_fip_uncertainty() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2157']
    assert 'Reconfigurable FIP-based' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'FIP is undefined' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2157"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2157)' in page
    assert 'What a systolic array is optimizing' in page
    assert 'What reconfiguration can change' in page
    assert 'What the unresolved FIP term means for interpretation' in page


def test_moe_token_stationary_explanation_separates_padding_routing_reconfiguration_and_energy() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2753']
    assert 'Token-stationary' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'does not by itself establish an end-to-end energy advantage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2753"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2753)' in page
    assert 'Why expert inputs have different sizes' in page
    assert 'What token-stationary execution changes' in page
    assert 'Why padding reduction is not yet an energy result' in page


def test_ucme_explanation_separates_pipeline_decoupling_async_ordering_overlap_and_ppa() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research552']
    assert 'decouples the matrix unit from the CPU pipeline' in row['method_or_artifact']
    assert '2.31× speedup' in ' '.join(row['metrics'])
    assert 'not a fully reproducible cross-CPU advantage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research552"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research552)' in page
    assert 'Why tight pipeline coupling limits reuse' in page
    assert 'What decoupling changes' in page
    assert 'How matrix-vector overlap produces a gain' in page


def test_torr_explanation_separates_representation_cache_validity_temporal_reuse_precision_and_energy() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research641']
    assert 'hyperdimensional computing similarity' in row['method_or_artifact']
    assert 'millijoule energy' in ' '.join(row['metrics'])
    assert 'not independently reproducible' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research641"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research641)' in page
    assert 'What the baseline computation is doing' in page
    assert 'Why temporal coherence permits caching' in page
    assert 'What precision-gated item memory controls' in page


def test_trine_explanation_separates_operator_modes_pruning_overlap_and_platform_comparison() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research660']
    assert 'single-bitstream FPGA accelerator' in row['method_or_artifact']
    assert '22.57×' in ' '.join(row['metrics'])
    assert 'not a fully reproducible end-to-end comparison' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research660"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research660)' in page
    assert 'Why multimodal inference stresses one accelerator' in page
    assert 'What the processing-element modes change' in page
    assert 'What top-k token pruning removes and what it adds' in page


def test_maliwan_explanation_separates_gemm_mapping_pareto_search_surrogate_and_measurement_limits() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research693']
    assert 'automated GEMM design-space exploration' in row['method_or_artifact']
    assert '6,000' in ' '.join(row['metrics'])
    assert 'source capture is truncated' in row['_page_source_tier']
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research693"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research693)' in page
    assert 'Why throughput and energy conflict' in page
    assert 'What MALIWAN’s search loop contributes' in page
    assert 'What the approximately 6,000 experiments mean' in page


def test_chimera_explanation_separates_fhe_schemes_transforms_keyswitch_and_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research885']
    assert 'dual-mode computational flow' in row['method_or_artifact']
    assert '14.84×' in ' '.join(row['metrics'])
    assert 'not a scheme-independent FHE advantage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research885"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research885)' in page
    assert 'What the two schemes require' in page
    assert 'What a shared FFT/NTT flow can and cannot share' in page
    assert 'Why constrained auto-tuning is part of correctness' in page


def test_unicon_explanation_separates_activation_math_log_domain_reconfiguration_and_accuracy() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research946']
    assert 'logarithmic-domain computing paradigm' in row['method_or_artifact']
    assert '1.55× speedup' in ' '.join(row['metrics'])
    assert 'not proof of equal-quality advantage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/specialized-accelerators-and-dataflow.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research946"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research946)' in page
    assert 'What a nonlinear activation computes' in page
    assert 'What logarithmic-domain computation changes' in page
    assert 'What unified reconfigurable hardware has to control' in page


def test_drcgen_explanation_separates_violation_meaning_control_diversity_transfer_and_validation() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research907']
    assert 'conditional diffusion-based generator' in row['method_or_artifact']
    assert '2.27×' in ' '.join(row['metrics'])
    assert 'diversity claims only' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/physical-verification.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research907"></span>') == 1
    assert 'What a DRC test case has to establish' in page
    assert 'What controllable generation changes' in page
    assert 'Why diversity is not coverage' in page


def test_ams_standard_cell_explanation_separates_abstraction_bias_extraction_and_silicon_evidence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research407']
    assert 'Circuit-level analog standard-cell library' in row['method_or_artifact']
    assert '4.1 ps measured' in ' '.join(row['metrics'])
    assert 'not universal analog-layout automation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/analog-layout-and-circuit-automation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research407"></span>') == 1
    assert 'What analog layout must preserve' in page
    assert 'What a circuit-level analog standard cell provides' in page
    assert 'What self-biasing changes' in page


def test_alphaplacer_explanation_separates_sequence_pairs_search_prior_geometric_and_electrical_evidence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research713']
    assert 'Monte Carlo tree-search analog placement' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'does not establish better analog behavior or practical deployment' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/analog-layout-and-circuit-automation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research713"></span>') == 1
    assert 'What a sequence pair represents' in page
    assert 'How Monte Carlo tree search allocates effort' in page
    assert 'What expert-layout pretraining changes' in page


def test_diffsp_explanation_separates_relaxation_objectives_legalization_and_postlayout_evidence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research776']
    assert 'Gumbel–Sinkhorn' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not a demonstrated general analog-circuit advantage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/analog-layout-and-circuit-automation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research776"></span>') == 1
    assert 'Why sequence-pair placement is difficult to differentiate' in page
    assert 'What the Gumbel–Sinkhorn relaxation changes' in page
    assert 'What MILP legalization contributes' in page


def test_drca_explanation_separates_bitline_sensing_dual_rail_logic_concurrency_and_reliability() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research544']
    assert 'dual-rail compute-and-access scheme' in row['method_or_artifact']
    assert '2.29×' in ' '.join(row['metrics'])
    assert 'not silicon-level reliability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-compute-and-reliability.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research544"></span>') == 1
    assert 'What a DRAM bitline pair normally does' in page
    assert 'What dual-rail compute changes' in page
    assert 'Why concurrent operations matter' in page


def test_mantis_explanation_separates_microscaling_charge_mac_adc_reuse_and_model_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1605']
    assert 'MANTIS' in row['method_or_artifact']
    assert '22.5 TOPS/W' in ' '.join(row['metrics'])
    assert 'not a complete system-level advantage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-compute-and-reliability.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1605"></span>') == 1
    assert 'Why reduced precision needs a scale' in page
    assert 'What charge-domain accumulation means' in page
    assert 'Why reusing the SAR ADC DAC matters' in page


def test_accelcim_explanation_separates_macro_dataflow_hierarchy_simulation_and_search_limits() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research155']
    assert 'systematic SRAM-CIM dataflow exploration' in row['method_or_artifact']
    assert 'no TOPS/W' in ' '.join(row['metrics'])
    assert 'not a universal CIM dataflow conclusion' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-compute-and-reliability.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research155"></span>') == 1
    assert 'What a CIM dataflow decides' in page
    assert 'Why macro and macro-array choices are different' in page
    assert 'What systematic exploration and simulation provide' in page


def test_bskmq_explanation_separates_activation_edges_quantizer_adc_cost_and_accuracy() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2282']
    assert 'BS-KMQ' in row['method_or_artifact']
    assert '4× speedup' in ' '.join(row['metrics'])
    assert 'not a universal IMC advantage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-compute-and-reliability.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2282"></span>') == 1
    assert 'Why ReLU and clamping create boundary mass' in page
    assert 'What BS-KMQ changes' in page
    assert 'How quantization error becomes model accuracy' in page


def test_dypamear_explanation_separates_dynamic_graph_irregularity_pim_balance_async_and_scaling() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2123']
    assert 'full-stack hardware-software co-design' in row['method_or_artifact']
    assert '267.38×' in ' '.join(row['metrics'])
    assert 'not a general speedup independent of graph distribution' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-compute-and-reliability.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2123"></span>') == 1
    assert 'What dynamic graph pattern mining computes' in page
    assert 'What load-aware task distribution controls' in page
    assert 'What data-driven asynchronous execution changes' in page


def test_com_bnn_explanation_separates_binary_work_mram_sensing_serial_tradeoffs_and_alias() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2425']
    assert 'RES-BNN' in row['method_or_artifact']
    assert '85% energy reduction' in ' '.join(row['metrics'])
    assert 'source also names RES-BNN' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-compute-and-reliability.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2425"></span>') == 1
    assert 'What binary convolution still has to compute' in page
    assert 'What serial operation changes' in page
    assert 'Why the name discrepancy remains visible' in page


def test_ubfp_imc_explanation_separates_wide_fp_bitserial_mac_alignment_and_numerical_evidence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2378']
    assert 'ultralarge-bit-width bit-serial mantissa MAC' in row['method_or_artifact']
    assert '27× lower accumulation latency' in ' '.join(row['metrics'])
    assert 'not proof of scientific-kernel accuracy' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-compute-and-reliability.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2378"></span>') == 1
    assert 'What wide floating point has to preserve' in page
    assert 'What bit-serial mantissa MACs change' in page
    assert 'Why exponent alignment is a separate bottleneck' in page


def test_arc_sram_explanation_separates_local_addressing_read_write_activity_and_workload_boundary() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2631']
    assert 'local-addressing SRAM subarray' in row['method_or_artifact']
    assert '63–76%' in ' '.join(row['metrics'])
    assert 'not a general random-access or production-process advantage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-compute-and-reliability.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2631"></span>') == 1
    assert 'Why random-access SRAM can waste energy on regular work' in page
    assert 'What local address generation changes' in page
    assert 'How the write scheme reuses bitline charge' in page


def test_onyx_explanation_separates_transaction_guarantees_pim_locality_balance_async_and_benchmarks() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research529']
    assert 'high-throughput transaction-processing system' in row['method_or_artifact']
    assert 'qualitatively claims' in ' '.join(row['metrics'])
    assert 'not a quantified transactional correctness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-compute-and-reliability.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research529"></span>') == 1
    assert 'What a transaction has to guarantee' in page
    assert 'What local-access orchestration changes' in page
    assert 'What rank-level asynchronous transfer changes' in page


def test_prism_explanation_separates_ann_recall_pruning_distance_bounds_and_host_pim_overlap() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research796']
    assert 'PIM-based ANNS system' in row['method_or_artifact']
    assert '2.7–19.8×' in ' '.join(row['metrics'])
    assert 'not a recall-preserving general speedup' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-compute-and-reliability.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research796"></span>') == 1
    assert 'What approximate nearest-neighbor search computes' in page
    assert 'What proximity-aware pruning and dual affiliations do' in page
    assert 'How host-PIM overlap affects throughput' in page


def test_pcbgen3d_explanation_separates_datasheet_graph_tasks_self_correction_and_cad_validation() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1991']
    assert 'self-correcting graph-based multimodal LLM' in row['method_or_artifact']
    assert 'outperforms a state-of-the-art general-purpose MLLM' in ' '.join(row['metrics'])
    assert 'not proof of usable production CAD output' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/generative-design-automation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1991"></span>') == 1
    assert 'What the input actually contains' in page
    assert 'What the dynamic task graph changes' in page
    assert 'What self-correction must observe' in page


def test_pcbgen_explanation_separates_specification_search_ir_simulation_and_electrical_acceptance() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research241']
    assert 'SPICE-in-the-loop' in row['method_or_artifact']
    assert 'Pass@5' in ' '.join(row['metrics'])
    assert 'not general electrical correctness or manufacturing readiness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/generative-design-automation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research241"></span>') == 1
    assert 'What a power-supply specification becomes' in page
    assert 'How the framework reduces the search' in page
    assert 'What SPICE-in-the-loop and TF-GRPO change' in page


def test_stitch_explanation_separates_assertion_passes_from_protocol_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2443']
    assert 'assertion-guided LLM patching' in row['method_or_artifact']
    assert 'accepted-patch rate' in ' '.join(row['metrics'])
    assert 'not general protocol correctness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/generative-design-automation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2443"></span>') == 1
    assert 'What an assertion contributes' in page
    assert 'What acceptance requires after a patch' in page


def test_llm4sdc_explanation_separates_sdc_syntax_from_timing_intent() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2642']
    assert 'multi-agent LLM workflow' in row['method_or_artifact']
    assert 'constraint correctness' in ' '.join(row['metrics'])
    assert 'not signoff-ready SDC' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/generative-design-automation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2642"></span>') == 1
    assert 'What an SDC file actually specifies' in page
    assert 'How benchmarking must distinguish a good constraint from a convenient one' in page


def test_stl_explanation_separates_structured_representation_from_semantic_equivalence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2829']
    assert 'structured intermediate representation' in row['method_or_artifact']
    assert 'semantic-equivalence rate' in ' '.join(row['metrics'])
    assert 'not semantic equivalence' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/generative-design-automation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2829"></span>') == 1
    assert 'What is being transformed' in page
    assert 'What the structured intermediate representation contributes' in page


def test_cupilot_explanation_separates_kernel_search_from_correctness_and_transfer() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research561']
    assert 'strategy-coordinated framework' in row['method_or_artifact']
    assert 'compile time' in ' '.join(row['metrics'])
    assert 'not general kernel correctness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/generative-design-automation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research561"></span>') == 1
    assert 'What a CUDA optimization changes' in page
    assert 'What a valid evaluation must include' in page


def test_directional_transport_explanation_separates_modeled_fidelity_from_device_speedup() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1608']
    assert 'static and dynamic ancillary paths' in row['method_or_artifact']
    assert 'modeled fidelity' in ' '.join(row['metrics'])
    assert 'Not device measurements' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/quantum-architectures-and-control.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1608"></span>') == 1
    assert 'What static and dynamic paths mean' in page
    assert 'How to read the reported QFT result' in page


def test_hamiltonian_pretraining_explanation_separates_initial_error_from_total_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1966']
    assert 'Fourier reconstruction' in row['method_or_artifact']
    assert 'initial energy error' in ' '.join(row['metrics'])
    assert 'Not final runtime' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/quantum-architectures-and-control.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1966"></span>') == 1
    assert 'What the initialization problem is' in page
    assert 'What “nearly 30-fold lower initial energy error” means' in page


def test_syndrome_extraction_explanation_separates_depth_bounds_from_logical_error() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research144']
    assert 'Three-stage QALP scheduling' in row['method_or_artifact']
    assert 'logical error' in ' '.join(row['metrics'])
    assert 'Not all codes or physical timing' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/quantum-architectures-and-control.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research144"></span>') == 1
    assert 'What a syndrome-extraction circuit does' in page
    assert 'Why equal depth does not mean equal protection' in page


def test_ohqs_explanation_separates_numerical_error_from_end_to_end_runtime() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1963']
    assert 'fixed-point optimization' in row['method_or_artifact']
    assert '99.91% accuracy' in ' '.join(row['metrics'])
    assert 'not runtime scaling' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/quantum-architectures-and-control.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1963"></span>') == 1
    assert 'What transient computation requires' in page
    assert 'How to interpret the reported numbers' in page


def test_cryzip_explanation_separates_compression_predecoding_and_fabrication() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research210']
    assert 'Gap coding' in row['method_or_artifact']
    assert '5.35× compression' in ' '.join(row['metrics'])
    assert 'predecoder bandwidth is a separate result' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/quantum-architectures-and-control.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research210"></span>') == 1
    assert 'How the compressor reduces representation size' in page
    assert 'Why the reported numbers are separate results' in page


def test_atom_detection_explanation_separates_image_latency_from_control_cycle() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2540']
    assert 'Parallel FPGA reconstruction' in row['method_or_artifact']
    assert '115 μs' in ' '.join(row['metrics'])
    assert 'not complete cycle' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/quantum-architectures-and-control.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2540"></span>') == 1
    assert 'What the accelerator must infer' in page
    assert 'What must be included in the complete control cycle' in page


def test_code_switching_explanation_separates_minimum_cut_from_physical_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2621']
    assert 'minimum-cut assignment' in row['method_or_artifact']
    assert '4.79–5.56%' in ' '.join(row['metrics'])
    assert 'not minimum physical cost' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/quantum-architectures-and-control.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2621"></span>') == 1
    assert 'Why a minimum cut appears' in page
    assert 'How to read the reported depth savings' in page


def test_sita_explanation_separates_readout_mitigation_from_state_correction() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research279']
    assert 'probability/state parallelism' in row['method_or_artifact']
    assert '4.9–1605×' in ' '.join(row['metrics'])
    assert 'Not proven whole-application speedup' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/quantum-architectures-and-control.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research279"></span>') == 1
    assert 'What readout mitigation is correcting' in page
    assert 'What the tensor-product cost is' in page


def test_linsearch_explanation_separates_exact_gate_count_from_depth_and_global_optimality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2756']
    assert 'Iterative deepening' in row['method_or_artifact']
    assert '15 qubits/15 CNOTs' in ' '.join(row['metrics'])
    assert 'Gate count is not depth' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/quantum-architectures-and-control.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2756"></span>') == 1
    assert 'How iterative deepening proves a count' in page
    assert 'What the reported limits mean' in page


def test_diacim_explanation_separates_sparse_dataflow_from_algorithmic_and_power_claims() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1194']
    assert 'CSR-driven streamed edge processing' in row['method_or_artifact']
    assert '60.01 TFLOPS/W' in ' '.join(row['metrics'])
    assert 'not a general GNN efficiency or accuracy result' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/specialized-ai-accelerators.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1194"></span>') == 1
    assert 'What dynamic iterative aggregation computes' in page
    assert 'How to interpret the efficiency claims' in page


def test_fusedot_explanation_separates_multiplier_sharing_from_quantization_and_end_to_end_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1182']
    assert 'MFDP multiplication-fused' in row['method_or_artifact']
    assert '1.51–1.98× speedup' in ' '.join(row['metrics'])
    assert 'not a general LLM speedup' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/specialized-ai-accelerators.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1182"></span>') == 1
    assert 'What the dot product computes' in page
    assert 'Why numerical correctness needs its own test' in page


def test_stemcam_explanation_separates_metric_encoding_from_physical_cam_results() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1095']
    assert 'segmented thermometer-encoded' in row['method_or_artifact']
    assert 'no numeric throughput' in ' '.join(row['metrics'])
    assert 'not exact or efficient physical computation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/specialized-ai-accelerators.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1095"></span>') == 1
    assert 'What the distance computation means' in page
    assert 'What the FeFET cell changes' in page


def test_tdhgnn_explanation_separates_incremental_reuse_from_invalidation_and_comparator_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research032']
    assert 'Hyperedge-indexed incremental updates' in row['method_or_artifact']
    assert '4.3×/2.8×' in ' '.join(row['metrics'])
    assert 'prediction-equivalence checks insufficiently specified' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/specialized-ai-accelerators.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research032"></span>') == 1
    assert 'What the hyperedge structure and cache do' in page
    assert 'What correctness and energy validation require' in page


def test_hdgas_explanation_separates_feature_selection_from_sparse_acceleration_and_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research052']
    assert 'Jointly learned feature filter' in row['method_or_artifact']
    assert '6.76×' in ' '.join(row['metrics'])
    assert 'Full text and quality conditions unrecovered' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/specialized-ai-accelerators.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research052"></span>') == 1
    assert 'What a learned feature filter does' in page
    assert 'What sparse matrix multiplication adds' in page
    assert 'retained-feature fractions' in page
    assert 'distribution-shifted graphs' in page


def test_geometry_guided_coda_explanation_separates_sort_removal_from_visibility_and_guidance_cost() -> None:
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/specialized-ai-accelerators.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1096"></span>') == 1
    section = page.split('### Geometry-guided CODA: sort-free rendering', 1)[1].split('### Geometry-guided CODA: remove sorting', 1)[0]
    for phrase in (
        'accumulated transmittance',
        'order matters',
        '2D Gaussian model',
        'guidance generation',
        'total rendering cost',
        'thin objects',
        'ordered reference',
        '8.4–11.6×',
    ):
        assert phrase in section


def test_pel_explanation_separates_palette_overhead_bdrate_and_fpga_latency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1334']
    assert 'Palette enhancement' in row['method_or_artifact']
    assert '18.13% BD-rate reduction' in ' '.join(row['metrics'])
    assert 'Sequences, quality metric' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/multimedia-and-edge-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1334"></span>') == 1
    section = page.split('### PEL: palette assistance', 1)[1].split('### PEL: add a screen-content', 1)[0]
    for phrase in (
        'rate–distortion',
        'palette itself',
        '5H2V',
        'BD-rate',
        'tri-core implementation',
        'eight additional lines',
        'camera-to-display latency',
    ):
        assert phrase in section


def test_relay_gs_explanation_separates_temporal_reuse_from_visibility_changes_and_energy_scope() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2027']
    assert 'Selective sort reuse' in row['method_or_artifact']
    assert '1.55–1.64× speed' in ' '.join(row['metrics'])
    assert 'No numerical quality loss' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/multimedia-and-edge-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2027"></span>') == 1
    section = page.split('### Relay-GS: reusing a previous depth order', 1)[1].split('### Relay-GS: reuse ordering', 1)[0]
    for phrase in (
        'accumulated transmittance',
        'cached result',
        'selectively sorts',
        'periodic correction',
        'depth crossings',
        'worst frame',
        '16.5% energy savings',
        'full sorting',
    ):
        assert phrase in section


def test_pipegs_explanation_separates_pipeline_overlap_from_frame_speed_and_efficiency_ratios() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2036']
    assert 'Hierarchical reuse' in row['method_or_artifact']
    assert '1.96–3.34× area efficiency' in ' '.join(row['metrics'])
    assert 'not elapsed-time speedups' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/multimedia-and-edge-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2036"></span>') == 1
    section = page.split('### PipeGS: overlapping rendering stages', 1)[1].split('### PipeGS: reduce waiting', 1)[0]
    for phrase in (
        'pipeline bubble',
        'steady-state throughput',
        'hierarchical reuse',
        'dynamic partitioning',
        'area efficiency',
        'tail latency',
        'deadline misses',
        'frame-time speedup',
    ):
        assert phrase in section


def test_orbis_explanation_separates_token_reduction_matching_cost_modeled_hardware_and_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2495']
    assert 'Output-guided pairing' in row['method_or_artifact']
    assert '3.5–4.5× modeled speed' in ' '.join(row['metrics'])
    assert '0.3–0.6×' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/multimedia-and-edge-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2495"></span>') == 1
    section = page.split('### ORBIS: token reduction', 1)[1].split('### ORBIS: prepare matching', 1)[0]
    for phrase in (
        'three subsequent reduced steps',
        'validity interval',
        'dedicated matching engine',
        '0.3–0.6×',
        '28 nm synthesis',
        'not measurements from a fabricated ORBIS chip',
        '63.95 to 63.66',
        'whole-system energy advantage',
    ):
        assert phrase in section


def test_excave_explanation_separates_shared_inversion_cache_validity_edit_success_and_source_scope() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2778']
    assert 'Shared inversion' in row['method_or_artifact']
    assert '108.58→26.62 s' in ' '.join(row['metrics'])
    assert 'Metric scope and platform missing' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/multimedia-and-edge-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2778"></span>') == 1
    section = page.split('### ExCave: shared inversion', 1)[1].split('### ExCave: share initial', 1)[0]
    for phrase in (
        'shared inversion',
        'CacheDiff',
        'dependency rule',
        'edit success',
        'protected regions',
        '108.58/26.62 seconds',
        'anonymous same-title manuscript',
        'source identity',
    ):
        assert phrase in section


def test_adagscale_explanation_separates_contribution_culling_from_geometric_culling_and_test_tuning() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2845']
    assert 'Contribution-guided intersection extent reduction' in row['method_or_artifact']
    assert '13.8× city-scale speed' in ' '.join(row['metrics'])
    assert 'tunes on test views' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/multimedia-and-edge-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2845"></span>') == 1
    section = page.split('### AdaGScale: contribution-guided culling', 1)[1].split('### AdaGScale: omit small contributions', 1)[0]
    for phrase in (
        'transmittance',
        'geometrically impossible intersection',
        'omitted contributions',
        'retained-pair fraction',
        '13.8× speedup',
        '0.5 dB PSNR drop',
        'test dataset',
        'untouched-test generalization',
    ):
        assert phrase in section


def test_livevlm_explanation_separates_retention_retrieval_first_token_latency_and_accuracy() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research670']
    assert 'Coverage-aware retention' in row['method_or_artifact']
    assert '1.73× first-token speedup' in ' '.join(row['metrics'])
    assert 'offloaded ReKV is more accurate' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/multimedia-and-edge-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research670"></span>') == 1
    section = page.split('### LiveVLM: bounded video memory', 1)[1].split('### LiveVLM: preserve coverage', 1)[0]
    for phrase in (
        'retention decision',
        'position-based coverage',
        'temporarily removes positional encoding',
        'restores positions',
        'time to first token',
        '55.6',
        '59.0',
        'rare event',
        'full answer latency',
    ):
        assert phrase in section


def test_galaxydt_explanation_separates_guidance_branches_proxy_calibration_and_quality_units() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research999']
    assert 'synchronized guidance reuse' in row['method_or_artifact']
    assert '1.3B slow: Table 2 1.85×' in ' '.join(row['metrics'])
    assert 'Pixel agreement is not prompt correctness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/multimedia-and-edge-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research999"></span>') == 1
    section = page.split('### GalaxyDiT: guidance reuse', 1)[1].split('### GalaxyDiT: synchronize reuse', 1)[0]
    for phrase in (
        'classifier-free guidance',
        'conditioned and unconditioned',
        'first block',
        'first 20%',
        '16 prompts',
        '1.85×',
        '1.87×',
        '0.97 percentage points',
        'proxy error',
    ):
        assert phrase in section


def test_dynamic_cost_fpga_explanation_separates_contextual_packing_from_reconfiguration_and_measured_area() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1183']
    assert 'Dynamic-cost area-recovery method' in row['method_or_artifact']
    assert 'Area recovery is claimed qualitatively' in ' '.join(row['metrics'])
    assert 'not runtime FPGA reconfiguration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/fpga-and-reconfigurable-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1183"></span>') == 1
    section = page.split('### Dynamic-Cost Area Recovery:', 1)[1].split('## Why fracturable resources', 1)[0]
    for phrase in (
        'fracturable LUT',
        'physical costs',
        'static model',
        'dynamic-cost method',
        'functionally equivalent',
        'placement and routing',
        'runtime FPGA partial reconfiguration',
        'no LUT count',
    ):
        assert phrase in section


def test_adahuff_gnn_explanation_separates_adaptive_coding_from_codebook_cost_and_training_outcome() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1468']
    assert 'Adaptive Huffman compression' in row['method_or_artifact']
    assert 'Communication reduction is claimed qualitatively' in ' '.join(row['metrics'])
    assert 'Compression may add latency' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/distributed-and-disaggregated-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1468"></span>') == 1
    section = page.split('### Adahuff-GNN: adaptive compression', 1)[1].split('## Scientific learning', 1)[0]
    for phrase in (
        'distributed graph-neural-network',
        'variable-length',
        'codebook',
        'convergence behavior',
        'critical path',
        'total time to the same training target',
        'lossless',
        'worker count',
    ):
        assert phrase in section


def test_two_teacher_sciml_explanation_separates_physics_guidance_hardware_guidance_and_system_outcomes() -> None:
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/distributed-and-disaggregated-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1741"></span>') == 1
    section = page.split('### Two Teachers Better Than One:', 1)[1].split('## Shared execution resources', 1)[0]
    for phrase in (
        'governing equation',
        'hardware teacher',
        'physics teacher',
        'optimization objective',
        'physical residuals',
        'worker count',
        'communication volume',
        'not demonstrated scientific validity',
    ):
        assert phrase in section


def test_hestia_explanation_separates_hyperthread_interference_policy_cost_tail_latency_and_fairness() -> None:
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/distributed-and-disaggregated-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2395"></span>') == 1
    section = page.split('### Hestia: hyperthread-level placement', 1)[1].split('## Compare useful system outcomes', 1)[0]
    for phrase in (
        'hardware thread',
        'shared resources',
        'Interference is a change',
        'tail latency',
        'attention-based policy',
        'migration',
        'oscillation',
        'fairness',
        'scheduler overhead',
    ):
        assert phrase in section


def test_prism_explanation_separates_primitive_forecasting_from_scheduler_gain_and_drift() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2531']
    assert 'Dynamic primitive-based workload forecasting' in row['method_or_artifact']
    assert 'no error by horizon' in ' '.join(row['metrics'])
    assert 'concept drift' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/distributed-and-disaggregated-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2531"></span>') == 1
    section = page.split('### PRISM: primitive-aware forecasts', 1)[1].split('## Compare useful system outcomes', 1)[0]
    for phrase in (
        'workload primitive',
        'concept drift',
        'forecast error',
        'rolling time splits',
        'queue time',
        'preemption',
        'telemetry',
        'end-to-end cluster improvement',
    ):
        assert phrase in section


def test_distributed_preemption_explanation_separates_utilization_from_training_progress_and_restart_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3208']
    assert 'Preemption analysis or scheduling method' in row['method_or_artifact']
    assert 'no time-to-quality' in ' '.join(row['metrics'])
    assert 'Higher utilization does not establish faster completion' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/distributed-and-disaggregated-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3208"></span>') == 1
    section = page.split('### Making Sense of Job Preemption:', 1)[1].split('## Compare useful system outcomes', 1)[0]
    for phrase in (
        'synchronization point',
        'valid distributed state',
        'optimizer state',
        'checkpoint interval',
        'recomputation',
        'fairness',
        'time-to-quality',
        'useful progress',
        'cluster-trace experiment',
    ):
        assert phrase in section


def test_asymcheck_explanation_separates_checkpoint_volume_from_consistent_restart_and_failure_recovery() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research513']
    assert 'Asymmetric partitioned checkpointing' in row['method_or_artifact']
    assert 'no checkpoint volume' in ' '.join(row['metrics'])
    assert 'consistency problem' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/distributed-and-disaggregated-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research513"></span>') == 1
    section = page.split('### Asymcheck: asymmetric checkpointing', 1)[1].split('## Compare useful system outcomes', 1)[0]
    for phrase in (
        'optimizer state',
        'asymmetric strategy',
        'write frequencies',
        'shared version',
        'partial write',
        'recomputed steps',
        'time to the same quality target',
        'Failure injection',
        'restart state remains consistent',
    ):
        assert phrase in section


def test_procyon_explanation_separates_occupancy_from_tenant_interference_fairness_and_tail_latency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research986']
    assert 'Fine-grained multi-tenant scheduling' in row['method_or_artifact']
    assert 'no throughput' in ' '.join(row['metrics'])
    assert 'Higher aggregate throughput' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/distributed-and-disaggregated-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research986"></span>') == 1
    section = page.split('### Procyon: fine-grained accelerator sharing', 1)[1].split('## Compare useful system outcomes', 1)[0]
    for phrase in (
        'sparse workload',
        'Fine-grained scheduling',
        'arbitration',
        'memory bandwidth',
        'Tenant isolation',
        'tail latency',
        'fairness',
        'per-tenant',
        'isolation bound',
    ):
        assert phrase in section


def test_hbspec_explanation_separates_accepted_tokens_memory_state_and_package_feasibility() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2417']
    assert 'Hybrid-bonding heterogeneous accelerator' in row['method_or_artifact']
    assert 'no acceptance rate' in ' '.join(row['metrics'])
    assert 'accepted-token throughput' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/chiplets-and-heterogeneous-integration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2417"></span>') == 1
    section = page.split('### HBSpec: heterogeneous speculative decoding', 1)[1].split('## What HBSpec changes', 1)[0]
    for phrase in (
        'accepted output tokens',
        'draft model',
        'target model',
        'Branch-KV',
        'branch-private state',
        'cross-bank traffic',
        'hybrid bonding',
        'bond yield',
        'output-quality requirement',
    ):
        assert phrase in section


def test_miter_aware_lut_explanation_separates_equivalence_soundness_from_solver_specific_par2() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research214']
    assert 'Miter-aware LUT mapping' in row['method_or_artifact']
    assert '856.6 to 67.4' in ' '.join(row['metrics'])
    assert 'solver-dependent' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/formal-and-equivalence-verification.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research214"></span>') == 1
    section = page.split('### Miter-Aware LUT Mapping:', 1)[1].split('## Multi-literal dropping', 1)[0]
    for phrase in (
        'same outputs',
        'miter',
        'satisfying assignment',
        'timeout is not a proof',
        'Gaussian elimination',
        'Xeon Platinum 8375C',
        '3,600-second timeout',
        'PAR2',
        'CEC',
        '92.1%',
    ):
        assert phrase in section


def test_multi_literal_ic3_explanation_separates_generalization_from_soundness_and_conditioned_results() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2512']
    assert 'Multiple-literal dropping strategy' in row['method_or_artifact']
    assert '28 uniquely solved' in ' '.join(row['metrics'])
    assert 'not additive' in ' '.join(row['metrics'])
    assert 'soundness argument' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/formal-and-equivalence-verification.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2512"></span>') == 1
    section = page.split('### Dropping Multiple Literals per SAT Call:', 1)[1].split('## PRS:', 1)[0]
    for phrase in (
        'transition system',
        'larger generalization',
        'failed generalizations',
        'inductive',
        'soundness',
        '28 uniquely solved',
        '16 additional solved',
        '6% faster',
        'not interchangeable',
        'proof-checking results',
    ):
        assert phrase in section


def test_prs_explanation_separates_parallel_search_clause_validity_proof_checking_and_speedup_reference() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research284']
    assert 'PRS parallel SAT framework' in row['method_or_artifact']
    assert '12 more solved' in ' '.join(row['metrics'])
    assert 'reference configuration' in ' '.join(row['metrics'])
    assert 'proof format' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/formal-and-equivalence-verification.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research284"></span>') == 1
    section = page.split('### PRS: parallel SAT search', 1)[1].split('## Parallel reachability', 1)[0]
    for phrase in (
        'Boolean formula',
        'branching orders',
        'learn a clause',
        'formula and assumptions',
        'proof format',
        'checker',
        '12 more solved',
        '11.4%',
        '4.7×',
        'one-to-64-core',
    ):
        assert phrase in section


def test_parallel_reachability_explanation_separates_approximation_direction_task_validity_and_conclusion() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research896']
    assert 'Parallelizing complementary approximate-reachability' in row['method_or_artifact']
    assert 'no soundness' in ' '.join(row['metrics'])
    assert 'over-approximation' in ' '.join(row['limits'])
    assert 'under-approximation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/formal-and-equivalence-verification.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research896"></span>') == 1
    section = page.split('### Parallelizing Complementary Approximate Reachability:', 1)[1].split('## What connects the papers', 1)[0]
    for phrase in (
        'initial-state set',
        'over-approximation',
        'under-approximation',
        'distributed concurrent task repository',
        'task ownership',
        'duplicate detection',
        'termination',
        'false alarm',
        'soundness checks',
    ):
        assert phrase in section


def test_lexi_explanation_separates_lossless_exponent_coding_from_precision_and_link_level_benefit() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3121']
    assert 'Lossless exponent coding scheme' in row['method_or_artifact']
    assert 'no compression ratio distribution' in ' '.join(row['metrics'])
    assert 'does not lower numerical precision' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/chiplet-interconnects.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3121"></span>') == 1
    section = page.split('### LEXI: lossless exponent coding', 1)[1].split('## Bonded wafers', 1)[0]
    for phrase in (
        'floating-point value',
        'same supported representation',
        'precision',
        'Exponent distributions',
        'fallback representation',
        'metadata',
        'codec throughput',
        'link utilization',
        'model-accuracy result',
    ):
        assert phrase in section


def test_wafer_network_explanation_separates_logical_topology_from_physical_links_faults_thermal_and_yield() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research363']
    assert 'Network design for wafer-scale systems' in row['method_or_artifact']
    assert 'no bandwidth' in ' '.join(row['metrics'])
    assert 'logical topology' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/chiplet-interconnects.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research363"></span>') == 1
    section = page.split('### Wafer-on-wafer network design:', 1)[1].split('## Hold the computation', 1)[0]
    for phrase in (
        'traffic matrix',
        'logical graph',
        'Hybrid bonding',
        'Bond pitch',
        'power delivery',
        'fault model',
        'bandwidth',
        'thermal',
        'yield',
    ):
        assert phrase in section


def test_niaq_explanation_separates_drift_tracking_accuracy_calibration_and_cmos_boundaries() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1200']
    assert 'Kalman filtering for drift tracking' in row['method_or_artifact']
    assert '88% accuracy' in ' '.join(row['metrics'])
    assert 'future labels' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/quantum-hardware-and-control.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1200"></span>') == 1
    section = page.split('### NIAQ: adaptive readout', 1)[1].split('## NIAQ: follow changes', 1)[0]
    for phrase in (
        'analog measurement signal',
        'classical label',
        'Kalman filter',
        'neural discriminator',
        'available during operation',
        '88% accuracy',
        '19× lower degradation rate',
        '148 mW',
        '5 ns',
        'fabricated continuously operating',
    ):
        assert phrase in section


def test_break_even_explanation_separates_encoded_quality_from_classical_advantage_and_device_claims() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1709']
    assert 'Compiler pipeline predicting algorithmic break-even' in row['method_or_artifact']
    assert '2,517 physical qubits' in ' '.join(row['metrics'])
    assert 'not universal thresholds' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/quantum-hardware-and-control.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1709"></span>') == 1
    section = page.split('### Algorithmic break-even:', 1)[1].split('## Movable logical qubits', 1)[0]
    for phrase in (
        'unencoded circuit',
        'fault-tolerant circuit',
        'classical algorithm',
        'lattice surgery',
        '500,000 shots',
        'Stim',
        'PyMatching',
        '2,517 physical qubits',
        '1,737 physical qubits',
        'magic-state preparation',
        'device demonstration',
    ):
        assert phrase in section


def test_movable_logical_qubit_explanation_separates_teleportation_routing_depth_and_physical_runtime() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2596']
    assert 'Compiler exploiting movable logical qubits' in row['method_or_artifact']
    assert '47.9 to 40.2' in ' '.join(row['metrics'])
    assert '3.8%' in ' '.join(row['metrics'])
    assert '15.8%' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/quantum-hardware-and-control.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2596"></span>') == 1
    section = page.split('### Exploiting Movable Logical Qubits:', 1)[1].split('## The connection across the four papers', 1)[0]
    for phrase in (
        'logical qubit',
        'teleportation',
        'does not copy an unknown state',
        '120 logical qubits',
        '47.9 to 40.2',
        '3.8%',
        '15.8%',
        'space-time volume',
        'decoder',
        'physical runtime',
    ):
        assert phrase in section


def test_luna_explanation_separates_fpga_design_points_readout_fidelity_and_full_loop_latency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2914']
    assert 'quantized LogicNet classifier' in row['method_or_artifact']
    assert '6,095 LUTs' in ' '.join(row['metrics'])
    assert '22.10 ns' in ' '.join(row['metrics'])
    assert 'same stated 90,000/10,000 split' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/quantum-hardware-and-control.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2914"></span>') == 1
    section = page.split('### LUNA: reducing FPGA readout logic', 1)[1].split('## Algorithmic break-even', 1)[0]
    for phrase in (
        'analog signal',
        'non-overlapping signal windows',
        'LogicNet classifier',
        '6,095 LUTs',
        '66,600',
        '22.10 ns',
        '95.969%',
        'not the fidelity of an entire quantum state',
        'XCZU49DR',
        'untouched final session',
        'shift 9',
    ):
        assert phrase in section


def test_strap_vit_explanation_separates_token_scoring_randomization_clean_cost_and_source_correction() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1613']
    assert 'Jensen–Shannon divergence' in row['method_or_artifact']
    assert '100.3%' in ' '.join(row['metrics'])
    assert 'impossible' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/secure-and-robust-ml.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1613"></span>') == 1
    section = page.split('### STRAP-ViT: token randomization', 1)[1].split('## CipherShield', 1)[0]
    for phrase in (
        'vision transformer',
        'adversarial patch',
        'Jensen–Shannon divergence',
        'reference population',
        'adaptive attacker',
        'clean-performance decreases',
        '100.3%',
        '15% from the clean baseline',
        'end-to-end runtime',
        'false-positive rate',
    ):
        assert phrase in section


def test_ciphershield_explanation_separates_ciphertext_hit_rate_attack_success_legitimate_accuracy_and_security_scope() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1764']
    assert 'block-based processing' in row['method_or_artifact']
    assert '50–80%' in ' '.join(row['metrics'])
    assert 'not a general confidentiality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/secure-and-robust-ml.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1764"></span>') == 1
    section = page.split('### CipherShield: breaking a ciphertext pattern', 1)[1].split('## Flip-Agent', 1)[0]
    for phrase in (
        'trusted execution environment',
        'side channel',
        'block processing',
        '50–80%',
        'nearly zero',
        'MNIST',
        'legitimate DNN inference',
        'over 20× shorter',
        'timing',
        'not a security proof',
    ):
        assert phrase in section


def test_flip_agent_explanation_separates_bit_fault_access_trigger_invocation_output_agreement_and_authorization() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research797']
    assert 'Targeted bit-flip attack methodology' in row['method_or_artifact']
    assert '22.2%' in ' '.join(row['metrics'])
    assert 'agreement with the original agent output' in ' '.join(row['metrics'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/secure-and-robust-ml.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research797"></span>') == 1
    section = page.split('### Flip-Agent: targeted model faults', 1)[1].split('## Runtime-ADAR', 1)[0]
    for phrase in (
        'bit flip',
        'precise bit placement',
        'internal-trigger attack',
        'invocation attack',
        'output',
        '22.2%',
        '94.4%',
        '67.3%',
        '100%',
        'requested tool action',
        'remote attack',
    ):
        assert phrase in section


def test_runtime_adar_explanation_separates_encryption_noise_detection_compensation_and_relative_accuracy() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research821']
    assert 'Noise-based statistical detection' in row['method_or_artifact']
    assert 'over 90%' in ' '.join(row['metrics'])
    assert '97% of baseline accuracy' in ' '.join(row['metrics'])
    assert 'not necessarily 97% absolute accuracy' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/secure-and-robust-ml.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research821"></span>') == 1
    section = page.split('### Runtime-ADAR: encrypted-runtime detection', 1)[1].split('## A comparison must preserve', 1)[0]
    for phrase in (
        'Homomorphic encryption',
        'scheme noise',
        'false alarms',
        'sparse projections',
        'gradient-field weight-compensation',
        'exact repair',
        'over 90%',
        '97% of baseline accuracy',
        'decryption success',
        'false-positive rates',
    ):
        assert phrase in section


def test_process_aware_noc_explanation_separates_rc_pdn_traffic_metrics_and_manufacturing_claims() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2290']
    assert 'Design-technology co-optimization' in row['method_or_artifact']
    assert '53%' in ' '.join(row['metrics'])
    assert '68%' in ' '.join(row['metrics'])
    assert 'traffic workloads' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/process-aware-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2290"></span>') == 1
    section = page.split('### DTCO for 3 nm NoCs:', 1)[1].split('## Lithography connects', 1)[0]
    for phrase in (
        'network-on-chip',
        'resistance and capacitance',
        'IR drop',
        'post-layout extraction',
        '53%',
        '68%',
        'EDP',
        'traffic',
        'core size',
        'yield',
    ):
        assert phrase in section


def test_inverse_lithography_explanation_separates_generated_masks_printed_fidelity_simulator_cost_and_manufacturing() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research209']
    assert 'Style-aware GAN pretraining' in row['method_or_artifact']
    assert 'no printed-pattern metric' in ' '.join(row['metrics'])
    assert 'printed pattern' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/process-aware-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research209"></span>') == 1
    section = page.split('### Generative inverse lithography:', 1)[1].split('## Fill changes', 1)[0]
    for phrase in (
        'desired layout',
        'printed pattern',
        'edge-placement error',
        'style-aware GAN',
        'policy optimization',
        'reward',
        'simulator errors',
        'process-window',
        'training and refinement time',
        'mask-writing',
    ):
        assert phrase in section


def test_differentiable_fill_explanation_separates_density_capacitance_elmore_delay_and_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research648']
    assert 'learned capacitance extraction' in row['method_or_artifact']
    assert 'no delay' in ' '.join(row['metrics'])
    assert 'Elmore delay is an approximation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/process-aware-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research648"></span>') == 1
    section = page.split('### Differentiable fill insertion:', 1)[1].split('## Distinguish prediction', 1)[0]
    for phrase in (
        'density rules',
        'self-capacitance',
        'coupling capacitance',
        'learned capacitance model',
        'Elmore delay',
        'signoff extractor',
        'delay and slack',
        'process variation',
        'design-rule checks',
    ):
        assert phrase in section


def test_cpw_smo_explanation_separates_common_process_window_source_mask_coupling_and_runtime_speedup() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1282']
    assert 'Single-shot set-based generative source/mask optimization' in row['method_or_artifact']
    assert 'nearly 2×' in ' '.join(row['metrics'])
    assert 'approximately 200×' in ' '.join(row['metrics'])
    assert 'process-window definition' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/process-aware-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1282"></span>') == 1
    section = page.split('### CPW-SMO: a larger common process window', 1)[1].split('## Distinguish prediction', 1)[0]
    for phrase in (
        'source-mask optimization',
        'one source',
        'common process window',
        'focus and exposure',
        'attention',
        'parallel simulation',
        'scalarization',
        'nearly 2×',
        'approximately 200×',
        'mask-writability',
    ):
        assert phrase in section


def test_mdp_ilt_explanation_separates_wafer_fidelity_mask_writability_gradients_shots_and_fabrication() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1287']
    assert 'Physics-aware differentiable electron-beam-lithography' in row['method_or_artifact']
    assert 'no wafer error' in ' '.join(row['metrics'])
    assert 'Mask writability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/process-aware-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1287"></span>') == 1
    section = page.split('### Differentiable MDP-ILT:', 1)[1].split('## Distinguish prediction', 1)[0]
    for phrase in (
        'wafer pattern',
        'mask data preparation',
        'writability',
        'curvilinear',
        'differentiable EBL simulator',
        'exact gradients',
        'shot fracturing',
        'calibrated EBL model',
        'mask-write',
        'fabrication result',
    ):
        assert phrase in section


def test_freqsem_explanation_separates_contour_model_epe_calibration_annotation_and_transfer() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1298']
    assert 'Frequency-aware FFT decomposition' in row['method_or_artifact']
    assert '0.334 nm' in ' '.join(row['metrics'])
    assert 'calibration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/process-aware-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1298"></span>') == 1
    section = page.split('### FreqSEM: a small edge-placement error', 1)[1].split('## Distinguish prediction', 1)[0]
    for phrase in (
        'SEM image',
        'edge placement error',
        'FFT',
        'SAM2',
        'Sobel-gradient loss',
        '0.334 nm',
        '0.661 nm',
        'pixel-to-distance calibration',
        'annotation uncertainty',
        'new SEM session',
    ):
        assert phrase in section


def test_rsizing_explanation_separates_yield_pareto_surrogate_uncertainty_monte_carlo_and_runtime_conditions() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['iccad-2025-1080']
    assert 'Three-phase robust Bayesian optimization' in row['method_or_artifact']
    assert '1,000 samples' in row['hardware_or_process_assumptions']
    assert 'approximation error' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/process-aware-design.md').read_text()
    assert page.count('<span id="explanation-iccad-2025-1080"></span>') == 1
    section = page.split('### RSizing: robust analog sizing', 1)[1].split('## Lithography connects', 1)[0]
    for phrase in (
        'device parameters',
        'Pareto set',
        'yield target',
        'heteroscedastic Gaussian-process',
        'Thompson sampling',
        'MVaR approximation',
        'ITC 2017',
        'TSMC 40 nm',
        '1,000 samples',
        'Table III',
        'NSGA-II is omitted for PLL',
    ):
        assert phrase in section


def test_lrta_explanation_separates_track_capacity_layer_reassignment_via_cost_and_signoff_legality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2037']
    assert 'Routability-driven 3D-aware track assignment' in row['method_or_artifact']
    assert 'no completed-connection count' in ' '.join(row['metrics'])
    assert 'A track assignment' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/physical-design-and-routing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2037"></span>') == 1
    section = page.split('### LRTA: layer reassignment', 1)[1].split('## Rail-signal co-design', 1)[0]
    for phrase in (
        'track assignment',
        'Routability',
        'layer reassignment',
        'via',
        'resistance',
        'capacitance',
        '3D-aware',
        'monolithic 3D',
        'detailed routing',
        'DRC',
    ):
        assert phrase in section


def test_rail_signal_explanation_separates_shared_layers_ir_drop_signal_integrity_and_fabrication() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research732']
    assert 'Unified resource-allocation co-design' in row['method_or_artifact']
    assert 'no IR-drop' in ' '.join(row['metrics'])
    assert 'layers' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/physical-design-and-routing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research732"></span>') == 1
    section = page.split('### Unified rail-signal co-design:', 1)[1].split('## What these cases support', 1)[0]
    for phrase in (
        'multilayer PCB',
        'voltage drop',
        'resistance',
        'signal integrity',
        'crosstalk',
        'current demand',
        'sequential',
        'electrical signoff',
        'fabricated-board',
    ):
        assert phrase in section


def test_activity_rtl_explanation_separates_event_load_balance_causality_synchronization_and_scaling() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research440']
    assert 'Activity-aware partitioning' in row['method_or_artifact']
    assert 'no complete simulation time' in ' '.join(row['metrics'])
    assert 'event ordering' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/simulation-and-emulation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research440"></span>') == 1
    section = page.split('### Activity-aware RTL partitioning:', 1)[1].split('## Generating a trace', 1)[0]
    for phrase in (
        'event-driven simulator',
        'quiet region',
        'event work',
        'partition boundary',
        'timestamps',
        'causality',
        'synchronization',
        'determinism',
        'thread count',
        'complete wall time',
    ):
        assert phrase in section


def test_phantom_pcie_explanation_separates_trace_plausibility_protocol_state_coverage_and_replay() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research514']
    assert 'Constraint mechanism for generative AI' in row['method_or_artifact']
    assert 'no protocol-validity rate' in ' '.join(row['metrics'])
    assert 'validity and useful coverage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/simulation-and-emulation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research514"></span>') == 1
    section = page.split('### The Phantom of PCIe:', 1)[1].split('## Updating a benchmark', 1)[0]
    for phrase in (
        'ordered record',
        'configuration reads',
        'device-state model',
        'protocol version',
        'state transitions',
        'Validity and coverage',
        'replay success',
        'DMA',
        'backpressure',
        'hardware result',
    ):
        assert phrase in section


def test_rtl_benchmt_explanation_separates_benchmark_revision_task_validity_checker_strength_and_comparability() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research874']
    assert 'Agent-assisted benchmark analysis' in row['method_or_artifact']
    assert 'no benchmark-validity' in ' '.join(row['metrics'])
    assert 'benchmark is both' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/simulation-and-emulation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research874"></span>') == 1
    section = page.split('### RTL-Benchmt: changing a benchmark', 1)[1].split('## The end-to-end implication', 1)[0]
    for phrase in (
        'procedure that turns',
        'checker',
        'synthesis',
        'agent-assisted maintenance',
        'versioned task',
        'contamination',
        'baseline score',
        'hidden tests',
        'historical and current instruments',
    ):
        assert phrase in section


def test_bflex_explanation_separates_fsm_exhaustiveness_from_physical_cell_correctness_ppa_and_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2394']
    assert 'Exhaustive finite-state-machine search' in row['method_or_artifact']
    assert 'no candidate count' in ' '.join(row['metrics'])
    assert 'not every possible transistor circuit' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/cell-and-circuit-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2394"></span>') == 1
    section = page.split('### B-Flex: exhaustive FSM search', 1)[1].split('## Celle:', 1)[0]
    for phrase in (
        'flip-flop',
        'finite-state machine',
        'setup and hold',
        'clock-to-Q',
        'Exhaustiveness',
        'state encoding',
        'transistor topology',
        'characterization',
        'process corners',
        'larger designs',
    ):
        assert phrase in section


def test_celle_explanation_separates_equality_saturation_from_physical_library_acceptance() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research278']
    assert 'Equality-saturation-based standard-cell library extension' in row['method_or_artifact']
    assert 'not global optimality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/cell-and-circuit-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research278"></span>') == 1
    section = page.split('### Celle: equality saturation', 1)[1].split('## A better individual cell', 1)[0]
    for phrase in (
        'standard-cell library',
        'Boolean formulas',
        'e-graph',
        'equivalence class',
        'rewrite rule',
        'extraction',
        'cost model',
        'design-rule checks',
        'characterization',
        'placement, routing',
        'global optimality',
    ):
        assert phrase in section


def test_stone_skimming_explanation_separates_translation_signal_from_practical_attack_claim() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1793']
    assert 'Page-table-walk side-channel attack' in row['method_or_artifact']
    assert 'not a generally practical attack' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/hardware-and-system-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1793"></span>') == 1
    section = page.split('### Stone-Skimming: a page-table side channel', 1)[1].split('## Physical measurements', 1)[0]
    for phrase in (
        'virtual addresses',
        'physical location',
        'page-table walk',
        'translation cache',
        'observation',
        'protected workload',
        'noise',
        'co-location',
        'false positives',
        'unseen inputs',
        'mitigations',
        'generally practical attack',
    ):
        assert phrase in section


def test_odbp_explanation_separates_protocol_obfuscation_from_biochemical_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2107']
    assert 'Protocol-obfuscation design' in row['method_or_artifact']
    assert 'not demonstrated confidentiality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/hardware-and-system-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2107"></span>') == 1
    section = page.split('### ODBP: protocol obfuscation', 1)[1].split('## Comparing attacks', 1)[0]
    for phrase in (
        'continuous-flow microfluidic',
        'ordered set of operations',
        'observer',
        'protocols that must be confused',
        'biochemical result',
        'assay yield',
        'reagent volume',
        'unseen protocols',
        'manufacturing variation',
        'faults',
        'confidentiality guarantee',
    ):
        assert phrase in section


def test_per_core_em_explanation_separates_signal_detection_from_secret_recovery() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research213']
    assert 'Per-core electromagnetic side-channel monitoring' in row['method_or_artifact']
    assert 'not established remote observability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/hardware-and-system-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research213"></span>') == 1
    section = page.split('### Per-core electromagnetic leakage', 1)[1].split('## Obscuring a protocol', 1)[0]
    for phrase in (
        'voltage and current',
        'electromagnetic fields',
        'physical mixture',
        'per-core',
        'attribution method',
        'probe position',
        'threat model',
        'secret value',
        'trace count',
        'false positives',
        'mitigation',
        'remote observability',
    ):
        assert phrase in section


def test_reconnaissance_explanation_separates_multi_secret_tracking_from_policy_proof() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2369']
    assert 'Reveal/conceal paradigm' in row['method_or_artifact']
    assert 'not established complete flow detection' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/hardware-and-system-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2369"></span>') == 1
    section = page.split('### Reconnaissance: reveal and conceal labels', 1)[1].split('## Comparing attacks', 1)[0]
    for phrase in (
        'information-flow analysis',
        'multiple secrets',
        'secret A',
        'reveal operation',
        'conceal operation',
        'Soundness',
        'Precision',
        'declassification',
        'concurrency',
        'runtime',
        'scalability',
        'forbidden multi-secret flows',
    ):
        assert phrase in section


def test_sram_aging_explanation_separates_historical_imprint_from_direct_remanence_and_recovery() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3019']
    assert 'Attack or forensic method' in row['method_or_artifact']
    assert 'not established recovery' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/hardware-and-system-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3019"></span>') == 1
    section = page.split('### Decoding the Past: an aging imprint', 1)[1].split('## Comparing attacks', 1)[0]
    for phrase in (
        'SRAM bit',
        'feedback circuit',
        'electrical stress',
        'Device aging',
        'not ordinary memory remanence',
        'weak, noisy statistical relationship',
        'process variation',
        'calibration',
        'bit error rate',
        'retention horizon',
        'sanitization',
        'cross-device',
    ):
        assert phrase in section


def test_touchscreen_em_explanation_separates_touch_detection_from_trajectory_recovery() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research315']
    assert 'Electromagnetic side-channel recovery' in row['method_or_artifact']
    assert 'not established remote trajectory recovery' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/hardware-and-system-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research315"></span>') == 1
    section = page.split('### Touchscreen electromagnetic emanations', 1)[1].split('## Comparing attacks', 1)[0]
    for phrase in (
        'capacitive touchscreen',
        'grid of conductive electrodes',
        'scans',
        'electromagnetic fields',
        'trajectory',
        'time-ordered sequence',
        'physical threat model',
        'probe orientation',
        'coordinate error',
        'cross-device',
        'remote trajectory recovery',
    ):
        assert phrase in section


def test_scimi_explanation_separates_semantic_context_from_safe_collaborative_vehicle_detection() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research462']
    assert 'Semantic-aware collaborative intrusion-detection system' in row['method_or_artifact']
    assert 'not safe deployment' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/hardware-and-system-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research462"></span>') == 1
    section = page.split('### SCIMI: collaborative intrusion detection', 1)[1].split('## Comparing attacks', 1)[0]
    for phrase in (
        'in-vehicle network',
        'sender',
        'operating mode',
        'Semantic-aware',
        'local detector',
        'communication delay',
        'attack surface',
        'compromised node',
        'replay',
        'false-positive rate',
        'vehicle platform',
        'safe deployment',
    ):
        assert phrase in section


def test_attestllm_explanation_separates_model_measurement_from_runtime_integrity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research625']
    assert 'Efficient attestation framework' in row['method_or_artifact']
    assert 'not end-to-end runtime trust' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/hardware-and-system-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research625"></span>') == 1
    section = page.split('### AttestLLM: efficient model attestation', 1)[1].split('## Comparing attacks', 1)[0]
    for phrase in (
        'cryptographic measurement',
        'hardware-protected key',
        'verifier',
        'billion-scale',
        'chunks',
        'rollback',
        'freshness',
        'tokenizer',
        'runtime',
        'does not prove',
        'tamper-detection',
        'end-to-end model trust',
    ):
        assert phrase in section


def test_emudrop_explanation_separates_reserved_opcode_fingerprint_from_universal_emulation_detection() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research663']
    assert 'reserved opcodes' in row['method_or_artifact']
    assert 'not portable detection' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/hardware-and-system-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research663"></span>') == 1
    section = page.split('### Emudrop: reserved-opcode detection', 1)[1].split('## Comparing attacks', 1)[0]
    for phrase in (
        'instruction encoding',
        'reserved or invalid',
        'illegal-instruction exception',
        'hardware-behavior fingerprint',
        'virtualized',
        'false positive',
        'hypervisor',
        'binary translation',
        'attacker budget',
        'false negatives',
        'evasion',
        'portable detection',
    ):
        assert phrase in section


def test_mistletunnel_explanation_separates_tlb_activity_from_general_kaslr_defeat() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research681']
    assert 'Novel TLB side-channel attack' in row['method_or_artifact']
    assert 'not general KASLR defeat' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/hardware-and-system-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research681"></span>') == 1
    section = page.split('### Mistletunnel: a TLB side channel', 1)[1].split('## Comparing attacks', 1)[0]
    for phrase in (
        'KASLR',
        'randomized',
        'translation lookaside buffer',
        'TLB hit',
        'kernel base',
        'follow-on action',
        'co-location',
        'Apple M-series',
        'OS versions',
        'noise tolerance',
        'mitigations',
        'general KASLR defeat',
    ):
        assert phrase in section


def test_tdsnap_explanation_separates_snapshot_encryption_from_fresh_isolated_state_restore() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research876']
    assert 'Trusted-domain snapshot mechanism' in row['method_or_artifact']
    assert 'not established confidential' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/hardware-and-system-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research876"></span>') == 1
    section = page.split('### Tdsnap: fast restoration', 1)[1].split('## Comparing attacks', 1)[0]
    for phrase in (
        'Function-as-a-service',
        'trusted domain',
        'registers',
        'heap memory',
        'Confidentiality',
        'Integrity',
        'Freshness',
        'replay',
        'external state',
        'metadata',
        'tail latency',
        'rollback-safe',
    ):
        assert phrase in section


def test_celestialeye_explanation_separates_item_frequency_from_signal_frequency_and_exact_counting() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1587']
    assert 'item-frequency summaries' in row['method_or_artifact']
    assert 'not electrical signal-frequency measurement' in row['method_or_artifact']
    assert 'not a proven exact frequency instrument' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/embedded-and-edge-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1587"></span>') == 1
    section = page.split('### CelestialEye: a stream-frequency engine', 1)[1].split('## WINNER:', 1)[0]
    for phrase in (
        'item\'s frequency',
        'electrical signal',
        'observation window',
        'summary',
        'FPGA',
        'CPU',
        'hot and cold',
        'bounds',
        'heuristic',
        'backpressure',
        'count error',
        'exact-recovery rate',
        'universal throughput improvement',
    ):
        assert phrase in section


def test_winner_explanation_separates_intermitttent_trace_visibility_from_biomedical_and_complete_observability_claims() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2997']
    assert 'Runtime analyzer' in row['method_or_artifact']
    assert 'does not establish a biomedical implant' in row['method_or_artifact']
    assert 'not validated biomedical deployment' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/embedded-and-edge-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2997"></span>') == 1
    section = page.split('### WINNER: intermittent debugging', 1)[1].split('## SemCom:', 1)[0]
    for phrase in (
        'intermittent device',
        'nonvolatile',
        'trace write',
        'reset boundary',
        'in-vivo',
        'biomedical implant',
        'power loss',
        'software-controlled electromagnetic',
        'property trigger',
        'trace completeness',
        'Bluetooth Low Energy',
        'total energy',
    ):
        assert phrase in section


def test_semcom_explanation_separates_bit_exact_decoding_from_image_and_task_fidelity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research791']
    assert 'Semantic-enhanced on-board image compression' in row['method_or_artifact']
    assert 'not demonstrated ultra-low-bitrate superiority' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/embedded-and-edge-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research791"></span>') == 1
    section = page.split('### SemCom: semantic compression', 1)[1].split('## EnergyHDC:', 1)[0]
    for phrase in (
        'bitrate',
        'codebook',
        'entropy coder',
        'side information',
        'bit-exact decoding',
        'original uncompressed pixels',
        'quantization',
        'downstream task',
        'rare-event',
        'packet',
        'flight evidence',
        'ultra-low-bitrate superiority',
    ):
        assert phrase in section


def test_energyhdc_explanation_separates_resume_correctness_accuracy_and_outage_completion() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research962']
    assert 'Hyperdimensional inference designed for intermittent operation' in row['method_or_artifact']
    assert 'not verified end-to-end completion' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/embedded-and-edge-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research962"></span>') == 1
    section = page.split('### EnergyHDC: intermittent inference', 1)[1].split('## Compare retained', 1)[0]
    for phrase in (
        'Hyperdimensional computing',
        'many components',
        'checkpoint',
        'resume',
        'internally consistent',
        'dimension-first',
        'priority pruning',
        'accuracy',
        'wall-clock time',
        'harvested-energy trace',
        'outage',
        'MSP432P401R',
        'end-to-end completion',
    ):
        assert phrase in section


def test_fbs_explanation_separates_sparsity_from_proportional_encrypted_work_reduction() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1187']
    assert 'Sparsity-aware RNS-CKKS inference strategy' in row['method_or_artifact']
    assert 'not demonstrated proportional speedup' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/privacy-preserving-computing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1187"></span>') == 1
    section = page.split('### FBS: sparsity can reduce encrypted work', 1)[1].split('## Encoding data', 1)[0]
    for phrase in (
        'RNS-CKKS',
        'ciphertext',
        'modulus chain',
        'scale',
        'Bootstrapping',
        'Sparsity',
        'zero pattern',
        'ciphertext packing',
        'input-dependent',
        'numerical error',
        'security level',
        'proportional speedup',
    ):
        assert phrase in section


def test_holocode_explanation_separates_encoded_representation_from_cryptographic_privacy() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2996']
    assert 'Hybrid optical-electronic encoding scheme' in row['method_or_artifact']
    assert 'not cryptographic confidentiality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/privacy-preserving-computing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2996"></span>') == 1
    section = page.split('### Holocode: an encoded training input', 1)[1].split('## Multiple GPUs', 1)[0]
    for phrase in (
        'transformed data',
        'not automatically encrypted',
        'protected attributes',
        'honest-but-curious',
        'paired examples',
        'gradients',
        'reconstruction',
        'sensitive-attribute inference',
        'optical noise',
        'calibration',
        'known-encoder attacks',
        'cryptographic confidentiality',
    ):
        assert phrase in section


def test_multigpu_fusion_explanation_separates_execution_optimization_from_privacy_protection() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research574']
    assert 'Tensor fusion and adaptive memory-management system' in row['method_or_artifact']
    assert 'not established privacy preservation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/privacy-preserving-computing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research574"></span>') == 1
    section = page.split('### Multi-GPU tensor fusion', 1)[1].split('## A shared research', 1)[0]
    for phrase in (
        'multidimensional arrays',
        'intermediate',
        'materialized',
        'synchronization',
        'client',
        'model owner',
        'GPU memory',
        'host memory',
        'interconnect',
        'allocator metadata',
        'trusted parties',
        'privacy leakage',
    ):
        assert phrase in section


def test_transsyn_explanation_separates_sat_boolean_equivalence_from_transistor_and_post_layout_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2007']
    assert 'Cut-based transistor-network mapper' in row['method_or_artifact']
    assert 'not proven area improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/logic-synthesis-and-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2007"></span>') == 1
    section = page.split('### Transsyn: cut-based mapping', 1)[1].split('## How to compare', 1)[0]
    for phrase in (
        'Boolean network',
        'cut',
        'transistor network',
        'pull-up',
        'SAT',
        'equivalence',
        'unknown values',
        'analog transistor effects',
        'setup/hold',
        'parasitic',
        'post-layout',
        'global optimality',
    ):
        assert phrase in section


def test_shared_logic_explanation_separates_multi_node_search_from_mapped_hardware_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3091']
    assert 'Multiple-node Boolean optimization' in row['method_or_artifact']
    assert 'not proven mapped-circuit improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/logic-synthesis-and-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3091"></span>') == 1
    section = page.split('### Shared Logic Unleashed: coordinated multi-node', 1)[1].split('## Satisfiability', 1)[0]
    for phrase in (
        'single-node rewrite',
        'several nodes',
        'shared intermediate',
        'fanout',
        'wire length',
        'mapped cell area',
        'equivalence check',
        'timeout',
        'reconvergent',
        'buffering',
        'mapped implementation',
        'universal advantage',
    ):
        assert phrase in section


def test_delay_sat_explanation_separates_boolean_equivalence_from_timing_model_and_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research754']
    assert 'SAT-based local-improvement area optimizer' in row['method_or_artifact']
    assert 'not proven PPA improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/logic-synthesis-and-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research754"></span>') == 1
    section = page.split('### Delay-constrained SAT local improvement', 1)[1].split('## Transistor-network', 1)[0]
    for phrase in (
        'local region',
        'counterexample',
        'functionally equivalent',
        'Delay is not a Boolean property',
        'timing tables',
        'fanout',
        'parasitic extraction',
        'hard limit',
        'timeout',
        'unresolved',
        'placement, routing',
        'timing closure',
    ):
        assert phrase in section


def test_lipcon_explanation_preserves_page_backed_height_results_and_separates_them_from_assay_validation() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research397']
    assert '1.25–5.50%' in ' '.join(row['metrics'])
    assert '2,476' in ' '.join(row['workload_or_benchmark'].split())
    assert 'does not establish the same gain in assay accuracy' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/biochips-and-specialized-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research397"></span>') == 1
    section = page.split('### LiPCon: a geometry correction model', 1)[1].split('## Scheduling a valve array', 1)[0]
    for phrase in (
        '3D printer',
        'light penetrates',
        'fabricated feature',
        'convolutional neural network',
        '1,037 raw points',
        '622 retained measurements',
        '2,488 cases',
        '2,476',
        'Anycubic Photon D2',
        'Table 4',
        'intended height',
        'assay yield',
        'failed prints',
    ):
        assert phrase in section


def test_valve_schedule_explanation_separates_logical_protocol_order_from_physical_pressure_execution() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research959']
    assert 'Timing-driven scheduling and placement' in row['method_or_artifact']
    assert 'not demonstrated fluidic reliability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/biochips-and-specialized-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research959"></span>') == 1
    section = page.split('### Pressure-path-aware valve scheduling', 1)[1].split('## What connects', 1)[0]
    for phrase in (
        'programmable valve-array',
        'pressure',
        'fluid identity',
        'dependencies',
        'Placement',
        'Scheduling',
        'interference',
        'flow rate',
        'cross-contamination',
        'assay correctness',
        'fabricated chips',
        'fluidic reliability',
    ):
        assert phrase in section


def test_schemacoder_explanation_separates_log_variation_from_schema_meaning_and_diagnostic_evidence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1841']
    assert 'Automatic schema-extraction coder' in row['method_or_artifact']
    assert 'not demonstrated cross-system diagnostic reliability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/verification-and-debugging-tools.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1841"></span>') == 1
    section = page.split('### Schemacoder: schema extraction', 1)[1].split('## Akirarust:', 1)[0]
    for phrase in (
        'log record',
        'field',
        'event type',
        'variation in value',
        'incorrect merge',
        'incorrect split',
        'residual Q-tree boosting',
        'tree representation',
        'nested',
        'multiline',
        'version changes',
        'raw record',
        'drift robustness',
    ):
        assert phrase in section


def test_akirarust_explanation_separates_feedback_guidance_from_specification_level_repair_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2871']
    assert 'Feedback-guided LLM Rust-repair workflow' in row['method_or_artifact']
    assert 'not demonstrated better correctness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/verification-and-debugging-tools.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2871"></span>') == 1
    section = page.split('### Akirarust: feedback can steer', 1)[1].split('## A useful connection', 1)[0]
    for phrase in (
        'repair loop',
        'compiler',
        'borrow',
        'tests',
        'thinking switch',
        'control policy',
        'candidate limit',
        'visible-test success',
        'held-out-test success',
        'regression',
        'benchmark leakage',
        'repeat trials',
        'end-to-end repair cost',
    ):
        assert phrase in section


def test_transistor_placement_explanation_separates_wirelength_score_from_mol_routing_and_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2006']
    assert 'Transistor-level placement independent' in row['method_or_artifact']
    assert 'not proven signoff-ready improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-floorplanning.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2006"></span>') == 1
    section = page.split('### Cell-structure-independent placement', 1)[1].split('## Three-dimensional', 1)[0]
    for phrase in (
        'standard-cell flow',
        'transistor-level',
        'MOL-aware',
        'M0',
        'pin access',
        'design rules',
        'wirelength',
        'extraction',
        'unrouted nets',
        'design-rule violations',
        'signoff',
        'signoff-ready improvement',
    ):
        assert phrase in section


def test_true_3d_placement_explanation_separates_analytical_proxy_from_bonded_routed_timing_closure() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2133']
    assert 'Timing-driven net weighting' in row['method_or_artifact']
    assert 'not demonstrated timing closure' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-floorplanning.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2133"></span>') == 1
    section = page.split('### True-3D timing-driven placement', 1)[1].split('## Weighting', 1)[0]
    for phrase in (
        'mixed-size',
        'analytical',
        'face-to-face',
        'hybrid bonds',
        'micro-bumps',
        'vertical',
        'critical path',
        'RC',
        'differentiable',
        'legalization',
        'thermal',
        'signoff',
        'timing closure',
    ):
        assert phrase in section


def test_hybrid_net_pin_explanation_separates_placement_weights_from_final_timing_closure() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1290']
    assert 'Analytical hybrid weighting' in row['method_or_artifact']
    assert 'not established timing closure' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-floorplanning.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1290"></span>') == 1
    section = page.split('### Hybrid net–pin weighting', 1)[1].split('## Compare completed', 1)[0]
    for phrase in (
        'net-level weight',
        'receiving pins',
        'critical path',
        'slack',
        'fanout',
        'congestion',
        'legalization',
        'detailed routing',
        'parasitic extraction',
        'worst negative slack',
        'total negative slack',
        'final STA',
    ):
        assert phrase in section


def test_fpga_slack_placement_explanation_separates_learned_priority_from_routed_closure() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1404']
    assert 'Learning-based slack-aware' in row['method_or_artifact']
    assert 'not proven timing closure' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-floorplanning.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1404"></span>') == 1
    section = page.split('### Learning-based slack-aware FPGA placement', 1)[1].split('## Compare completed', 1)[0]
    for phrase in (
        'heterogeneous FPGA', 'discrete site types', 'slack', 'legalization',
        'routing', 'fanout', 'congestion', 'training', 'held-out',
        'worst negative slack', 'unrouted nets', 'final timing',
        'not proven FPGA timing closure',
    ):
        assert phrase in section


def test_drama_explanation_separates_maze_pathfinding_from_legal_signoff_routing() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1534']
    assert 'Versatile maze-routing' in row['method_or_artifact']
    assert 'not demonstrated signoff-scale superiority' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-floorplanning.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1534"></span>') == 1
    section = page.split('### DRΛMA maze routing', 1)[1].split('## Compare completed', 1)[0]
    for phrase in (
        'routing graph', 'maze router', 'congestion', 'rip-up', 'reroute',
        'design-rule', 'parasitic extraction', 'wirelength', 'via count',
        'overflow', 'timing slack', 'signoff', 'not demonstrated signoff-scale superiority',
    ):
        assert phrase in section


def test_soft_rectilinear_explanation_separates_relaxed_shapes_from_legal_floorplans() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2024']
    assert 'Differentiable polygon-shaping' in row['method_or_artifact']
    assert 'relaxation-to-legalization gap' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-floorplanning.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2024"></span>') == 1
    section = page.split('### Differentiable rectilinear floorplanning', 1)[1].split('## Compare completed', 1)[0]
    for phrase in (
        'soft rectilinear module', 'horizontal or vertical', 'non-overlap',
        'differentiable', 'proxy', 'flow-based legalization', 'displacement',
        'shape distortion', 'routing-channel', 'wirelength', 'congestion',
        'detailed routing', 'extraction', 'timing', 'relaxation-to-legalization gap',
    ):
        assert phrase in section


def test_flip_fet_explanation_separates_dual_side_resources_from_fabrication_ready_routing() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2139']
    assert 'Congestion-aware dual-side' in row['method_or_artifact']
    assert 'not demonstrated fabrication-ready quality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-floorplanning.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2139"></span>') == 1
    section = page.split('### Flip-FET dual-side routing', 1)[1].split('## Compare completed', 1)[0]
    for phrase in (
        'dual-side', 'routing domains', 'transition', 'side-specific', 'congestion',
        'high-fanout', 'contacts', 'alignment', 'power', 'thermal', 'yield',
        'extraction', 'design-rule', 'fabrication-ready quality',
    ):
        assert phrase in section


def test_multirow_complementary_fet_explanation_separates_area_from_library_routability() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2416']
    assert 'Area-optimal, routability-driven' in row['method_or_artifact']
    assert 'not demonstrated signoff-ready library quality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-floorplanning.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2416"></span>') == 1
    section = page.split('### Multi-row complementary-FET layout synthesis', 1)[1].split('## Compare completed', 1)[0]
    for phrase in (
        'standard cell', 'multi-row', 'complementary-FET', 'pin access', 'diffusion',
        'contacts', 'design-rule', 'area-optimal', 'routability', 'parasitics',
        'characterization', 'abutted neighbors', 'chip-level', 'signoff-ready library quality',
    ):
        assert phrase in section


def test_latte_explanation_separates_differentiable_timing_from_legal_routed_placement() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research373']
    assert 'Legality-assured differentiable' in row['method_or_artifact']
    assert 'not demonstrated final timing closure' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-floorplanning.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research373"></span>') == 1
    section = page.split('### LATTE detailed placement', 1)[1].split('## Compare completed', 1)[0]
    for phrase in (
        'standard-cell row', 'detailed placement', 'timing', 'differentiable',
        'proxy', 'overlap', 'density', 'legality', 'legalizer', 'legalization',
        'worst and total negative slack', 'pin-access', 'routing', 'extracted',
        'static timing analysis', 'not demonstrated final timing closure',
    ):
        assert phrase in section


def test_quad_gradient_explanation_separates_relaxed_sizing_from_discrete_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research843']
    assert 'Differentiable timing-power' in row['method_or_artifact']
    assert 'not demonstrated signoff improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-floorplanning.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research843"></span>') == 1
    section = page.split('### Differentiable timing–power gate sizing', 1)[1].split('## Compare completed', 1)[0]
    for phrase in (
        'gate sizing', 'drive strength', 'input capacitance', 'fanout', 'discrete',
        'relaxed', 'rounded', 'timing gradient', 'power gradient', 'dynamic',
        'leakage', 'setup', 'hold', 'parasitic extraction', 'multi-corner STA',
        'not demonstrated signoff improvement',
    ):
        assert phrase in section


def test_saap_explanation_separates_partition_quality_from_parallel_routing_completion() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research320']
    assert 'Spatial-aware analytic' in row['method_or_artifact']
    assert 'not demonstrated end-to-end parallel speedup' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-floorplanning.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research320"></span>') == 1
    section = page.split('### SAAP spatial-aware partitioning', 1)[1].split('## Compare completed', 1)[0]
    for phrase in (
        'netlist', 'graph', 'hypergraph', 'spatial', 'cut nets', 'high-fanout',
        'balance', 'boundary', 'congestion', 'synchronization', 'worker',
        'speedup', 'worker idle time', 'communication volume', 'unrouted nets',
        'signoff-routing superiority',
    ):
        assert phrase in section


def test_bspdn_explanation_separates_backside_power_proxy_from_integrity_and_process_validation() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research335']
    assert 'Comprehensive multi-objective BSPDN' in row['method_or_artifact']
    assert 'not demonstrated signoff integrity' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-floorplanning.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research335"></span>') == 1
    section = page.split('### BSPDN-Elite', 1)[1].split('## Compare completed', 1)[0]
    for phrase in (
        'backside power', 'IR drop', 'current density', 'electromigration',
        'timing', 'signal-routing', 'thermal', 'alignment', 'yield',
        'voltage-aware timing', 'extraction', 'frontside power delivery',
        'not demonstrated signoff integrity',
    ):
        assert phrase in section


def test_capbench_explanation_separates_dataset_scope_from_transfer_and_reproduction_claims() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1224']
    assert 'Multi-PDK, multi-representation dataset' in row['method_or_artifact']
    assert 'not independently established transfer generalization' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/reproducibility-artifacts-and-benchmarks.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1224"></span>') == 1
    section = page.split('### CapBench: a capacitance dataset', 1)[1]
    for phrase in (
        'post-layout capacitance', 'three-dimensional windows', 'RWCap', 'Raphael',
        '1.75%', '41.4-fold', '10.2%', 'reference-label error', 'learned prediction error',
        'overlap', 'unseen-technology', 'split manifest', 'absolute runtimes',
        'reproduced the reported experiments', 'not independently established transfer generalization',
    ):
        assert phrase in section


def test_attentioncap_explanation_separates_matrix_prediction_from_full_chip_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1222']
    assert 'Transformer-based learned capacitance-matrix' in row['method_or_artifact']
    assert 'not demonstrated full-chip signoff substitution' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-eda-and-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1222"></span>') == 1
    section = page.split('### Attentioncap: a learned capacitance matrix', 1)[1]
    for phrase in (
        'capacitance matrix', 'q = C V', 'off-diagonal', 'coupling', 'transformer',
        'tokens', 'full-chip', 'tiling', 'memory', 'matrix error', 'downstream',
        'technology transfer', 'physical-validity', 'signoff substitution',
    ):
        assert phrase in section


def test_learned_prior_explanation_separates_zero_tuning_from_corner_coverage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1646']
    assert 'Learned-prior method' in row['method_or_artifact']
    assert 'not demonstrated zero-assumption behavior' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-eda-and-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1646"></span>') == 1
    section = page.split('### Learned-prior multi-corner analysis', 1)[1].split('## Compare the results', 1)[0]
    for phrase in (
        'corner', 'process', 'voltage', 'temperature', 'learned prior', 'hyperparameter',
        'training', 'fallback', 'unseen designs', 'PDKs', 'corner coverage',
        'false passes', 'false failures', 'solver calls', 'reference analysis tool',
        'not demonstrated zero-assumption behavior',
    ):
        assert phrase in section


def test_perifi_explanation_separates_feasible_region_sampling_from_search_completeness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1804']
    assert 'Physics-infused inverse design' in row['method_or_artifact']
    assert 'not demonstrated search completeness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-eda-and-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1804"></span>') == 1
    section = page.split('### Perifi inverse design', 1)[1].split('## Compare the results', 1)[0]
    for phrase in (
        'inverse design', 'RF', 'feasible region', 'sampling', 'simulator', 'surrogate',
        'exclusion', 'frequency', 'fabrication', 'robustness', 'simulation budget',
        'rejected', 'failed candidates', 'high-fidelity electromagnetic simulation',
        'not demonstrated search completeness',
    ):
        assert phrase in section


def test_ace_nas_explanation_separates_zero_cost_proxy_from_trained_hardware_outcomes() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1899']
    assert 'Zero-cost NAS' in row['method_or_artifact']
    assert 'not demonstrated zero-cost behavior' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-eda-and-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1899"></span>') == 1
    section = page.split('### ACE-NAS: a zero-cost search score', 1)[1].split('## Compare the results', 1)[0]
    for phrase in (
        'spiking neural network', 'architecture', 'encoding', 'spike', 'temporal',
        'zero-cost', 'proxy', 'trained', 'rank correlation', 'search regret',
        'event count', 'memory traffic', 'energy', 'hardware utilization',
        'not demonstrated zero-cost behavior',
    ):
        assert phrase in section


def test_causal_cpu_explanation_separates_association_from_intervention_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research271']
    assert 'Causal-aware learning' in row['method_or_artifact']
    assert 'not demonstrated intervention validity' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-eda-and-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research271"></span>') == 1
    section = page.split('### Learning the why: a causal claim', 1)[1].split('## Compare the results', 1)[0]
    for phrase in (
        'predictive model', 'causal', 'intervention', 'counterfactual', 'confounder',
        'workload', 'cache', 'power', 'area', 'authoritative CPU simulator',
        'held-out', 'sample efficiency', 'simulator calls', 'not demonstrated intervention validity',
    ):
        assert phrase in section


def test_legend_explanation_separates_generated_lemmas_from_sound_completed_proofs() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research523']
    assert 'Data-driven lemma generation' in row['method_or_artifact']
    assert 'not demonstrated sound acceleration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-eda-and-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research523"></span>') == 1
    section = page.split('### Legend lemma generation', 1)[1].split('## Compare the results', 1)[0]
    for phrase in (
        'transition system', 'property', 'counterexample', 'lemma', 'invariant',
        'soundness', 'unverified', 'rejected', 'redundant', 'proof time',
        'proof certificates', 'unseen designs', 'not demonstrated sound acceleration',
    ):
        assert phrase in section


def test_epicell_explanation_separates_electro_physical_prediction_from_library_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research550']
    assert 'Electro-physical co-model' in row['method_or_artifact']
    assert 'not demonstrated library replacement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-eda-and-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research550"></span>') == 1
    section = page.split('### Epicell: electro-physical PPA prediction', 1)[1].split('## Compare the results', 1)[0]
    for phrase in (
        'standard cell', 'power', 'performance', 'area', 'delay', 'leakage',
        'parasitics', 'electrical-only', 'layout-only', 'timing-critical',
        'high-fanout', 'PDK', 'process corner', 'characterization',
        'technology transfer', 'not demonstrated library replacement',
    ):
        assert phrase in section


def test_diffdeg_explanation_separates_design_history_representation_from_final_optimization() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research692']
    assert 'Diffusion-enhanced design-evolution graph' in row['method_or_artifact']
    assert 'not demonstrated final PPA improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-eda-and-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research692"></span>') == 1
    section = page.split('### DiffDEG: a graph of design changes', 1)[1].split('## Compare the results', 1)[0]
    for phrase in (
        'post-layout', 'static graph', 'design-evolution graph', 'history', 'action',
        'diffusion', 'representation', 'optimizer', 'leakage', 'rollback',
        'rejected', 'timing slack', 'congestion', 'extraction', 'signoff',
        'not demonstrated final PPA improvement',
    ):
        assert phrase in section


def test_soberdse_explanation_separates_algorithm_selection_from_total_budget_advantage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research859']
    assert 'Learning-based selection of DSE algorithms' in row['method_or_artifact']
    assert 'not demonstrated total-budget advantage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-eda-and-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research859"></span>') == 1
    section = page.split('### SoberDSE: selecting a search algorithm', 1)[1].split('## Compare the results', 1)[0]
    for phrase in (
        'design-space exploration', 'Bayesian optimization', 'random search', 'selector',
        'pilot', 'total budget', 'overfit', 'held-out', 'fallback', 'regret',
        'simulator calls', 'unseen design-space family', 'not demonstrated total-budget advantage',
    ):
        assert phrase in section


def test_function_family_analog_explanation_separates_family_reuse_from_new_topology_validation() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research951']
    assert 'Function-family-aware analog optimization' in row['method_or_artifact']
    assert 'not demonstrated transfer' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-eda-and-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research951"></span>') == 1
    section = page.split('### Function-family analog optimization', 1)[1].split('## Compare the results', 1)[0]
    for phrase in (
        'analog', 'function family', 'topology', 'Bayesian optimization',
        'simulator-call budget', 'PDK', 'process', 'feasible', 'gain',
        'bandwidth', 'phase margin', 'noise', 'Monte Carlo',
        'unseen topology', 'not demonstrated transfer'
    ):
        assert phrase in section


def test_semi_virtual_addressing_explanation_separates_address_space_from_memory_safety_enforcement() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1715']
    assert 'Lightweight Address Translation Module' in row['method_or_artifact']
    assert 'not demonstrated equivalence' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1715"></span>') == 1
    section = page.split('### Semi-virtual addressing:', 1)[1].split('## Protecting computation', 1)[0]
    for phrase in (
        'memory-safety', 'address space', 'access enforcement', 'page-table-free',
        'RISC-V', 'randomization', 'type-safe allocation', 'out-of-bounds',
        'use-after-free', 'attacker', 'DMA', 'software-only', 'full-MMU',
        'worst-case', 'software compatibility', 'not demonstrated equivalence'
    ):
        assert phrase in section


def test_s2cim_explanation_separates_secure_cim_assets_from_accuracy_and_macro_efficiency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research208']
    assert 'FeFET-based secure CIM' in row['method_or_artifact']
    assert 'not complete end-to-end confidentiality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research208"></span>') == 1
    section = page.split('### S2CIM: protecting compute-in-memory', 1)[1].split('## Protecting computation', 1)[0]
    for phrase in (
        'compute-in-memory', 'weights', 'inputs', 'FeFET', 'Affine-Transform',
        'attacker', 'key handling', 'random-guess', 'accuracy', 'ADC/DAC',
        'area boundary', 'energy per MAC', 'side-channel', 'fault',
        'end-to-end confidentiality'
    ):
        assert phrase in section


def test_safe_iot_explanation_separates_ml_dsa_correctness_from_efficiency_and_leakage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2216']
    assert 'Memory-efficient ML-DSA accelerator' in row['method_or_artifact']
    assert 'not a comparable end-to-end result' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2216"></span>') == 1
    section = page.split('### Safe-IoT: an ML-DSA accelerator', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'ML-DSA', 'digital-signature', 'NTT', 'lookup-table', 'parameter set',
        'memory boundary', 'correctness', 'test vectors', 'side-channel',
        'constant-time', 'fault', 'CPU', 'end-to-end',
        'not a comparable end-to-end result'
    ):
        assert phrase in section


def test_remote_mlkem_explanation_separates_scheme_security_from_remote_implementation_leakage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research296']
    assert 'Generic remote power side-channel analysis' in row['method_or_artifact']
    assert 'not a universal ML-KEM break' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research296"></span>') == 1
    section = page.split('### Remote ML-KEM side channels:', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'ML-KEM', 'key-encapsulation', 'mathematical security', 'implementation',
        'plaintext-checking oracle', 'remote', 'network noise', 'processor SKU',
        'secret-key recovery', 'traces', 'queries', 'mitigations',
        'speculative execution', 'not a universal ML-KEM break'
    ):
        assert phrase in section


def test_janus_explanation_separates_control_flow_hardening_from_complete_transient_leakage_protection() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1444']
    assert 'Compiler-based defense using ARM pointer authentication' in row['method_or_artifact']
    assert 'not protection against all transient-execution variants' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1444"></span>') == 1
    section = page.split('### Janus: control-flow protection', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'transient execution', 'branch predictor', 'microarchitectural',
        'pointer authentication', 'BTI', 'indirect branch', 'compiler',
        'modifier fusion', 'carrier-register reuse', 'ABI', 'shared libraries',
        'attack coverage', 'SPEC CPU2017', 'code size',
        'not protection against all transient-execution variants'
    ):
        assert phrase in section


def test_interrupt_security_explanation_separates_interrupt_delivery_from_attack_feasibility() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1497']
    assert 'Automated interrupt-feature and trigger-condition testing framework' in row['method_or_artifact']
    assert 'not general platform prevalence' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1497"></span>') == 1
    section = page.split('### Hardware-interrupt security:', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'interrupt', 'privilege', 'trigger', 'handler', 'microarchitectural',
        'secret', 'oracle', 'false positives', 'false negatives',
        'six', 'four', 'processor', 'operating system', 'mitigation',
        'not general platform prevalence'
    ):
        assert phrase in section


def test_cloud_tee_explanation_separates_cpu_availability_from_confidentiality_and_integrity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1494']
    assert 'Availability-verifiable remote attestation' in row['method_or_artifact']
    assert 'Confidentiality and integrity do not imply availability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1494"></span>') == 1
    section = page.split('### Cloud-TEE availability:', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'trusted execution environment', 'confidentiality', 'integrity', 'availability',
        'remote attestation', 'resource commitment', 'scheduler', 'contention',
        'preemptive', 'fairness', 'TCB', '94.8%', '19.7x', 'FPGA',
        'deployed CPU TEEs'
    ):
        assert phrase in section


def test_pmu_faker_explanation_separates_performance_counters_from_timer_replacement_side_channels() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1495']
    assert 'Automated PMU-event fuzzing' in row['method_or_artifact']
    assert 'not prevalence across processors' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1495"></span>') == 1
    section = page.split('### PMU-Faker: a performance counter', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'performance-monitoring unit', 'PMU', 'timer', 'event count',
        'secret-dependent', 'fuzzing', 'calibration', 'counter width',
        'privilege', 'virtualization', '118', 'four', 'false positives',
        'mitigation', 'not prevalence across processors'
    ):
        assert phrase in section


def test_vehicle_traceback_explanation_separates_alert_quality_from_graph_path_reconstruction() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1920']
    assert 'Certification-compatible gateway traceback' in row['method_or_artifact']
    assert 'not proven causal attribution' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1920"></span>') == 1
    section = page.split('### In-vehicle attack-chain traceback:', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'IDS', 'host', 'Ethernet', 'CAN', 'temporal graph', 'edge', 'causal',
        'plausibility checks', 'alert precision', 'alert recall', 'false alert',
        'UN R155', 'ISO/SAE 21434', 'edge-level F1', 'false-discovery rate',
        'Leapmotor C10', 'cross-vehicle', 'not proven causal attribution'
    ):
        assert phrase in section


def test_masked_ml_dsa_explanation_separates_first_order_tvla_from_universal_security_and_unit_speedup_from_signing_gain() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1732']
    assert 'Drop-in masked modular-reduction architecture' in row['method_or_artifact']
    assert 'not a universal security proof' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1732"></span>') == 1
    section = page.split('### Masked ML-DSA modular reduction:', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'ML-DSA', 'modular reduction', 'masked', 'shares', 'first-order',
        'Caliptra', 'drop-in', 'LUT', 'FF', 'area-delay', 'signing-throughput',
        'TVLA', '1,000,000', 'higher-order', 'randomness',
        'not a universal security proof'
    ):
        assert phrase in section


def test_brew_rc_explanation_separates_ecc_matrix_recovery_from_general_reram_vulnerability() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3042']
    assert 'SAT-based recovery of the bit-exact ECC parity matrix' in row['method_or_artifact']
    assert 'does not establish a general ReRAM vulnerability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3042"></span>') == 1
    section = page.split('### BREW-RC: write latency', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'ReRAM', 'error-correcting code', 'parity', 'write timing',
        'side channel', 'SAT', 'bit-exact', 'unique', 'physical access',
        'sample complexity', 'measurement noise', 'two commercial',
        'countermeasures', 'not establish a general ReRAM vulnerability'
    ):
        assert phrase in section


def test_thrend_explanation_separates_counting_thread_detection_from_universal_timing_attack_prevention() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1464']
    assert 'Fuzz-generated training corpus' in row['method_or_artifact']
    assert 'does not establish universal timing-attack prevention' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1464"></span>') == 1
    section = page.split('### Thrend: detecting a counting-thread timing attack', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'counting thread', 'performance counter', 'co-scheduling', 'same-core',
        'co-location', 'fuzzing', 'counter permissions', 'core topology',
        '99.71%', 'false-negative', 'false-positive', 'adaptive attacker',
        '100 Hz', '1.42%', 'does not establish universal timing-attack prevention'
    ):
        assert phrase in section


def test_voltage_waveform_explanation_separates_instruction_recovery_from_remote_universal_disassembly() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2254']
    assert 'End-to-end voltage-waveform sequence-to-sequence model' in row['method_or_artifact']
    assert 'not represent remote or production attack settings' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2254"></span>') == 1
    section = page.split('### Voltage-waveform instruction recovery:', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'voltage waveform', 'aggregate', 'out-of-order', 'speculation',
        'CNN-Conformer', 'Transformer decoder', 'sequence', 'token-level',
        '34.70%', '645', '50,000', 'physical access', 'cross-CPU',
        'per-instruction', 'remote or production attack claim'
    ):
        assert phrase in section


def test_plonk_hammer_explanation_separates_zero_knowledge_privacy_from_fault_recovery_and_soundness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2771']
    assert 'Rowhammer fault injection' in row['method_or_artifact']
    assert 'does not establish a protocol-wide break' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2771"></span>') == 1
    section = page.split('### PLONK-Hammer: zero-knowledge privacy', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'PLONK', 'zero-knowledge', 'privacy', 'soundness', 'availability',
        'Rowhammer', 'DRAM', 'fault', 'polynomial commitment', 'gnark',
        'verifier', 'memory placement', 'proof parameters', 'recovery',
        'does not establish a protocol-wide break'
    ):
        assert phrase in section


def test_netdetox_explanation_separates_gnn_detector_evasion_from_underlying_hardware_security_impact() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2536']
    assert 'RL-LLM orchestration' in row['method_or_artifact']
    assert 'does not establish that a real hardware vulnerability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2536"></span>') == 1
    section = page.split('### Netdetox: evading a hardware-security graph detector', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'GNN', 'graph', 'node', 'edge', 'evasion', 'hardware security',
        'RL-LLM', 'reinforcement learning', 'large-language-model',
        'semantic', 'query budget', 'transfer', 'false negative',
        'synthesis', 'detector impact', 'does not establish that a real hardware vulnerability'
    ):
        assert phrase in section


def test_securerouter_explanation_separates_payload_encryption_from_metadata_and_endpoint_security() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3092']
    assert 'Encrypted routing mechanism' in row['method_or_artifact']
    assert 'not demonstrated end-to-end confidentiality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3092"></span>') == 1
    section = page.split('### Securerouter: encrypting inference traffic', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'secure inference', 'payload', 'metadata', 'routing', 'confidentiality',
        'integrity', 'availability', 'key management', 'hop-by-hop',
        'end-to-end', 'latency', 'bandwidth', 'energy', 'accuracy',
        'freshness', 'replay', 'not demonstrated end-to-end confidentiality'
    ):
        assert phrase in section


def test_tt_seal_explanation_separates_selective_encryption_coverage_from_robustness_and_privacy() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research848']
    assert 'Selective encryption strategy' in row['method_or_artifact']
    assert 'may leave exploitable unprotected paths' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research848"></span>') == 1
    section = page.split('### TT-SEAL: selective encryption', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'edge-AI', 'adversarial robustness', 'selective encryption',
        'full encryption', 'unencrypted robust inference', 'threat distribution',
        'protected', 'unprotected', 'attacker', 'key management',
        'adaptive', 'attack success', 'privacy leakage', 'latency',
        'energy', 'may leave exploitable unprotected paths'
    ):
        assert phrase in section


def test_signed_cim_columns_explanation_separates_integrity_metadata_from_complete_model_provenance() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1853']
    assert 'Column-level signing scheme' in row['method_or_artifact']
    assert 'does not establish end-to-end model provenance' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1853"></span>') == 1
    section = page.split('### Signed CIM columns:', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'CIM', 'crossbar', 'weights', 'integrity', 'provenance', 'column-level',
        'digest', 'replay', 'rollback', 'within-column', 'cross-column',
        'attacker', 'verification', 'ADC/DAC', 'analog', 'key management',
        'latency', 'energy', 'does not establish end-to-end model provenance'
    ):
        assert phrase in section


def test_isomorphic_ip_explanation_separates_function_preservation_from_structural_confidentiality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2832']
    assert 'Isomorphic graph transformations' in row['method_or_artifact']
    assert 'does not establish confidentiality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2832"></span>') == 1
    section = page.split('### Isomorphic hardware-IP transformations:', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'hardware IP', 'RTL', 'netlist', 'graph', 'isomorphism', 'function',
        'invariants', 'semantic', 'synthesis', 'side channels', 'equivalence',
        'attacker', 'adaptive', 'area', 'timing', 'power',
        'does not establish confidentiality'
    ):
        assert phrase in section


def test_caramel_explanation_separates_device_utilization_from_control_flow_audit_completeness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1665']
    assert 'Device-utilization optimization' in row['method_or_artifact']
    assert 'does not establish security-preserving audit acceleration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1665"></span>') == 1
    section = page.split('### CARAMEL: using more of the audit device', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'control flow', 'audit', 'soundness', 'completeness', 'utilization',
        'ordering', 'dependency', 'dropped', 'adversarial', 'queue',
        'false positives', 'false negatives', 'throughput', 'latency',
        'energy', 'does not establish security-preserving audit acceleration'
    ):
        assert phrase in section


def test_athena_explanation_separates_pre_silicon_estimation_from_measured_leakage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1949']
    assert 'Analytical timing-aware pre-silicon side-channel leakage estimator' in row['method_or_artifact']
    assert 'not demonstrated physical leakage prediction' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1949"></span>') == 1
    section = page.split('### Athena: pre-silicon leakage', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'side channel', 'timing', 'pre-silicon', 'analytical',
        'microarchitecture', 'power', 'attacker', 'calibration',
        'post-silicon', 'false positives', 'false negatives',
        'process', 'PVT', 'correlation', 'mutual information',
        'TVLA', 'attack success', 'not demonstrated physical leakage prediction'
    ):
        assert phrase in section


def test_spike_ptsd_explanation_separates_digital_snn_evasion_from_hardware_attack() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1430']
    assert 'Bio-plausible spike-scaling adversarial attack' in row['method_or_artifact']
    assert 'not demonstrated adaptive security impact' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1430"></span>') == 1
    section = page.split('### Spike-PTSD: a temporal attack', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'spiking neural network', 'spike', 'temporal', 'adversarial',
        'scaling', 'biological', 'hardware', 'threat model', 'budget',
        'encoder', 'transferability', 'adaptive', 'defense',
        'attack success', 'perturbation cost', 'not demonstrated adaptive security impact'
    ):
        assert phrase in section


def test_pd_net_explanation_separates_device_invariance_from_preserved_leakage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2648']
    assert 'Device-invariant representation learning' in row['method_or_artifact']
    assert 'not demonstrated device-invariant key recovery' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2648"></span>') == 1
    section = page.split('### PD-Net: device-invariant representations', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'side-channel', 'device', 'representation', 'nuisance', 'leakage',
        'profiling', 'target', 'attacker', 'alignment', 'noise',
        'zero-shot', 'few-shot', 'key recovery', 'held out',
        'domain adaptation', 'not demonstrated device-invariant key recovery'
    ):
        assert phrase in section


def test_cpa_bnn_explanation_separates_integrated_security_claims_and_efficiency_boundary() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1185']
    assert 'Secure RRAM CIM' in row['method_or_artifact']
    assert 'not a demonstrated end-to-end security' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1185"></span>') == 1
    section = page.split('### CPA-BNN: a secure CIM accelerator', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'model confidentiality', 'integrity', 'inference correctness',
        'PUF', 'reliability', 'uniqueness', 'entropy', 'masking',
        'side-channel', 'attack model', 'security game', 'accuracy',
        'compute density', 'storage density', 'peripheral', 'end-to-end'
    ):
        assert phrase in section


def test_trac_explanation_separates_activation_counting_from_rowhammer_prevention() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1275']
    assert 'Transparent row activation counting' in row['method_or_artifact']
    assert 'not demonstrated RowHammer prevention' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1275"></span>') == 1
    section = page.split('### TRAC: row-activation monitoring', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'RowHammer', 'DRAM', 'activation', 'threshold', 'LFSR', 'subarray',
        'timing', 'controller', 'false-positive', 'disturbance',
        'threat model', 'adversarial', 'PRAC', 'missed',
        'not demonstrated RowHammer prevention'
    ):
        assert phrase in section


def test_shooting_falcon_explanation_separates_fault_induction_from_key_recovery() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1320']
    assert 'RowHammer-induced single-bit fault' in row['method_or_artifact']
    assert 'not demonstrated practical key recovery' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1320"></span>') == 1
    section = page.split('### Shooting Falcon with One Fault:', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'RowHammer', 'Falcon', 'single-bit', 'fault', 'memory placement',
        'DRAM', 'privilege', 'faulty signature', 'cryptanalytic',
        'key recovery', 'success probability', 'hammering time',
        'repeatability', '800x', 'not demonstrated practical key recovery'
    ):
        assert phrase in section


def test_slcross_explanation_separates_covert_channel_from_embedding_inference() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1373']
    assert 'Reverse-engineered SLC mechanisms' in row['method_or_artifact']
    assert 'not demonstrated general or remote leakage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1373"></span>') == 1
    section = page.split('### Slcross: a cross-component cache channel', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'cache', 'SLC', 'GPU', 'CPU', 'covert channel', 'embedding',
        'bandwidth', 'error rate', 'inference', 'sample complexity',
        'privilege', 'noise', 'Apple M2', 'mitigation',
        'not demonstrated general or remote leakage'
    ):
        assert phrase in section


def test_dm_mark_explanation_separates_watermark_authorization_from_accelerator_speed() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1085']
    assert 'Software-hardware co-designed diffusion watermarking framework' in row['method_or_artifact']
    assert 'not demonstrated robust authorization' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1085"></span>') == 1
    section = page.split('### DM-MARK: watermarking authorization', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'watermark', 'diffusion', 'authorization', 'provenance', 'key',
        'false-positive', 'false-negative', 'robustness', 'adaptive',
        'forgery', 'quality', 'latency', 'EMA', '12 nm', 'area',
        'yield', 'not demonstrated robust authorization'
    ):
        assert phrase in section


def test_icarus_explanation_separates_moe_mechanism_from_general_dos_impact() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1054']
    assert 'Gradient-based universal hidden-prefix attack' in row['method_or_artifact']
    assert 'not demonstrated universal or deployment-general attack impact' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/side-channel-and-hardware-security.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1054"></span>') == 1
    section = page.split('### Icarus’s Wings: an MoE slowdown claim', 1)[1].split('## What a useful comparison', 1)[0]
    for phrase in (
        'MoE', 'expert', 'offloading', 'prefetch', 'cache replacements',
        'temporal locality', 'denial-of-service', 'attacker', 'prefix',
        'victim', 'latency', 'throughput', 'universal', 'held-out',
        'defenses', 'not demonstrated universal or deployment-general attack impact'
    ):
        assert phrase in section


def test_ihyperg_explanation_separates_incremental_state_from_partition_quality_and_speed() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research223']
    assert 'GPU-parallel incremental k-way hypergraph partitioner' in row['method_or_artifact']
    assert 'not universal incremental partitioning performance' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/partitioning-and-placement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research223"></span>') == 1
    section = page.split('### iHyperG: incremental partitioning', 1)[1].split('## ATOM-3D', 1)[0]
    for phrase in (
        'hypergraph', 'delta', 'incremental', 'rebalancing', 'temporary group',
        'cut-critical', 'balance', 'quality', 'GPU', 'synchronization',
        'A6000', '3%', '190.17', '82.82', 'not universal incremental partitioning performance'
    ):
        assert phrase in section


def test_atom3d_explanation_separates_orientation_modeling_from_3d_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research934']
    assert 'Analytical 3D orientation-aware mixed-size placer' in row['method_or_artifact']
    assert 'not demonstrated routable or manufacturable 3D placement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/partitioning-and-placement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research934"></span>') == 1
    section = page.split('### ATOM-3D: orientation-aware placement', 1)[1].split('## ATOM-3D: orientation changes', 1)[0]
    for phrase in (
        '3D', 'orientation', 'partition', 'layer', 'macro', 'pins',
        'wire length', 'differentiable', 'legal', 'routing', 'timing',
        'via', 'thermal', 'DRC', 'face-to-face', 'manufacturing',
        'not demonstrated routable or manufacturable 3D placement'
    ):
        assert phrase in section


def test_module_placement_explanation_separates_abstraction_from_signoff_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research954']
    assert 'Force-based deformation module-level placer' in row['method_or_artifact']
    assert 'not demonstrated detailed routability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/partitioning-and-placement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research954"></span>') == 1
    section = page.split('### Module-level placement: deformation', 1)[1].split('## Module-level placement: estimate', 1)[0]
    for phrase in (
        'module', 'force-based', 'deformation', 'aspect ratio', 'area',
        'pins', 'routability', 'HPWL', 'wire length', 'timing',
        'congestion', 'longest 10%', 'recall', 'speedup', 'legalization',
        'signoff', 'not demonstrated detailed routability'
    ):
        assert phrase in section


def test_stamp_explanation_separates_toolchain_attestation_from_yield_and_drift() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3145']
    assert 'Machine-learning process-monitoring model' in row['method_or_artifact']
    assert 'not a general manufacturing-security guarantee' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/manufacturing-monitoring-and-yield.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3145"></span>') == 1
    section = page.split('### STAMP: wafer measurements', 1)[1]
    for phrase in (
        'attestation', 'yield', 'tool chain', 'metrology', 'electrical',
        'false acceptance', 'false rejection', 'temporal', 'drift',
        'held-out', 'chain of custody', 'calibration', '7,000',
        'cross-fab', 'not a general manufacturing-security guarantee'
    ):
        assert phrase in section


def test_wfh_bfs_explanation_separates_selective_pruning_from_weight_repair() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1284']
    assert 'Dynamic weight-function hierarchy' in row['method_or_artifact']
    assert 'not a general guarantee of bit-flip security' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/reliable-and-secure-ai-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1284"></span>') == 1
    section = page.split('## WFH-BFs: selective protection', 1)[1].split('## Compare the results', 1)[0]
    for phrase in (
        'Anchor Core', 'class-sensitive', 'Reservoir', 'pruning', 'repair',
        'bit-flip', 'fault', 'checker', 'attack cost', 'accuracy',
        'detection latency', 'GFLOPs', 'energy', 'adaptive',
        'not a general guarantee of bit-flip security'
    ):
        assert phrase in section


def test_stac_explanation_separates_activation_context_from_fault_detection() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2307']
    assert 'Spatial-temporal activation contextualization' in row['method_or_artifact']
    assert 'not a general reliable-LLM guarantee' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/reliable-and-secure-ml.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2307"></span>') == 1
    section = page.split('## STAC: an unusual activation', 1)[1].split('## Selective temporal redundancy', 1)[0]
    for phrase in (
        'prefill', 'decoding', 'outlier', 'spatial', 'temporal',
        'false alarm', 'missed', 'fault', 'prompt', 'sequence',
        'accuracy', 'latency', 'energy', 'negligible overhead',
        'not a general reliable-LLM guarantee'
    ):
        assert phrase in section


def test_temporal_redundancy_explanation_separates_repetition_from_fault_coverage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research374']
    assert 'Sparsity- and tolerance-aware temporally redundant neural network design' in row['method_or_artifact']
    assert 'not general fault tolerance' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/reliable-and-secure-ml.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research374"></span>') == 1
    section = page.split('## Selective temporal redundancy', 1)[1].split('## E³-CODE', 1)[0]
    for phrase in (
        'temporal redundancy', 'disagreement', 'persistent', 'correlated',
        'outer product', 'zero-skipping', 'residual quantization',
        'single-bit', 'fault coverage', 'accuracy', 'latency', 'energy',
        '16.0%', '0.20–1.26%', 'not general fault tolerance'
    ):
        assert phrase in section


def test_e3_code_explanation_separates_parity_embedding_from_lifetime_and_quality_claims() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research800']
    assert 'Embedded error-correcting code' in row['method_or_artifact']
    assert 'not observed years of operation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/reliable-and-secure-ml.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research800"></span>') == 1
    section = page.split('## E³-CODE: use weight representation', 1)[1].split('## DRIFT:', 1)[0]
    for phrase in (
        'error-correcting code', 'parity', 'weight representation',
        'mixed-integer linear programming', 'burst error', 'codeword',
        'decoder', 'accuracy', 'lifetime', '4.8×', '10×',
        'fault coverage', 'not observed years of operation'
    ):
        assert phrase in section


def test_drift_explanation_separates_approximate_checkpoint_recovery_from_fault_free_execution() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research816']
    assert 'Fault-tolerance-aware diffusion inference method' in row['method_or_artifact']
    assert 'not fault-free execution' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/reliable-and-secure-ml.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research816"></span>') == 1
    section = page.split('## DRIFT: tolerate some timing errors', 1)[1].split('## The shared direction', 1)[0]
    for phrase in (
        'timing errors', 'voltage', 'frequency', 'approximate substitution',
        'checkpoint', 'checksum', 'uniform random bit flips', '32-bit',
        'eight-bit', '14 nm', 'SCALE-Sim', '0.68 V/2 GHz',
        '0.88 V/3.5 GHz', '36%', '1.7×', 'fabricated',
        'not fault-free execution'
    ):
        assert phrase in section


def test_single_gpu_finetuning_explanation_separates_capacity_from_time_to_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1286']
    assert 'Heterogeneous algorithm-hardware co-design' in row['method_or_artifact']
    assert 'not demonstrated single-GPU training efficiency' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/llm-systems-and-runtime.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1286"></span>') == 1
    section = page.split('## Single-GPU fine-tuning', 1)[1].split('## Checkpointing trades', 1)[0]
    for phrase in (
        'single GPU', 'weights', 'gradients', 'optimizer', 'activations',
        'host memory', 'storage', 'transfer', 'interconnect',
        'parameter-efficient', 'time-to-quality', 'throughput',
        'energy', 'multi-GPU', 'not demonstrated single-GPU training efficiency'
    ):
        assert phrase in section


def test_expcheck_explanation_separates_activity_aware_checkpointing_from_exact_recovery() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1414']
    assert 'Checkpointing policy that adapts to expert activity' in row['method_or_artifact']
    assert 'not demonstrated exact recovery' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/llm-systems-and-runtime.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1414"></span>') == 1
    section = page.split('## Checkpointing trades', 1)[1].split('## Arithmetic intensity', 1)[0]
    for phrase in (
        'checkpoint', 'mixture-of-experts', 'expert', 'router', 'optimizer',
        'inactive', 'reconstructible', 'distributed', 'consistency',
        'failure', 'restart', 'storage', 'exact recovery',
        'not demonstrated exact recovery'
    ):
        assert phrase in section


def test_arithmetic_intensity_explanation_separates_ratio_model_from_runtime_result() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2169']
    assert 'Acceleration framework orchestrating arithmetic-intensity-driven stage boundaries' in row['method_or_artifact']
    assert 'not demonstrated model-diverse acceleration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/llm-systems-and-runtime.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2169"></span>') == 1
    section = page.split('## Arithmetic intensity can help', 1)[1].split('## What the comparison', 1)[0]
    for phrase in (
        'arithmetic intensity', 'operations', 'bytes', 'memory boundary',
        'diffusion', 'stage', 'transition', 'synchronization',
        'latency', 'throughput', 'bandwidth', 'energy', 'autoregressive',
        'model-diverse acceleration'
    ):
        assert phrase in section


def test_hero_explanation_separates_rag_quality_from_mobile_orchestration_efficiency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2300']
    assert 'Adaptive RAG orchestration' in row['method_or_artifact']
    assert 'not demonstrated quality-preserving orchestration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/llm-systems-and-runtime.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2300"></span>') == 1
    section = page.split('## Hero: mobile RAG orchestration', 1)[1].split('## Checkpointing trades', 1)[0]
    for phrase in (
        'retrieval-augmented generation', 'retriever', 'generator', 'answer quality',
        'grounding', 'CPU', 'GPU', 'NPU', 'cloud', 'privacy', 'thermal',
        'battery', 'latency', 'energy', 'query distribution', 'tail',
        'not demonstrated quality-preserving orchestration'
    ):
        assert phrase in section


def test_sandwich_explanation_separates_hot_switching_from_slo_safe_serving() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research235']
    assert 'Joint configuration search and runtime hot-switching' in row['method_or_artifact']
    assert 'not demonstrated SLO-safe hot-switching' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/llm-systems-and-runtime.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research235"></span>') == 1
    section = page.split('## Sandwich: hot-switching', 1)[1].split('## Checkpointing trades', 1)[0]
    for phrase in (
        'CPU', 'LLM', 'configuration', 'search', 'hot-switching',
        'switch', 'cache', 'KV-cache', 'SLO', 'tail latency',
        'p95', 'p99', 'throughput', 'energy', 'exploration',
        'held-out', 'not demonstrated SLO-safe hot-switching'
    ):
        assert phrase in section


def test_preba_explanation_separates_gpu_co_design_from_multitenant_qos() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research256']
    assert 'Hardware/software co-design for multi-instance GPU inference serving' in row['method_or_artifact']
    assert 'not demonstrated QoS-safe' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/llm-systems-and-runtime.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research256"></span>') == 1
    section = page.split('## PREBA: multi-instance GPU serving', 1)[1].split('## Checkpointing trades', 1)[0]
    for phrase in (
        'multi-instance', 'GPU', 'tenant', 'partition', 'interference',
        'memory', 'scheduling', 'tail latency', 'p95', 'p99',
        'throughput', 'fairness', 'isolation', 'energy', 'QoS',
        'not demonstrated QoS-safe'
    ):
        assert phrase in section


def test_deinfer_explanation_separates_parallelism_from_communication_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2620']
    assert 'Parallel inference system for decomposed LLMs' in row['method_or_artifact']
    assert 'not demonstrated efficient and quality-preserving parallel inference' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/llm-systems-and-runtime.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2620"></span>') == 1
    section = page.split('## Deinfer: decomposed-model parallelism', 1)[1].split('## Checkpointing trades', 1)[0]
    for phrase in (
        'decomposed', 'LLM', 'parallel', 'dependency', 'communication',
        'synchronization', 'prefill', 'decode', 'KV-cache', 'quality',
        'latency', 'throughput', 'scaling', 'energy', 'small requests',
        'not demonstrated efficient and quality-preserving parallel inference'
    ):
        assert phrase in section


def test_smoothspec_explanation_separates_acceptance_from_resource_allocation() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research292']
    assert 'Intra-device speculative-decoding schedule' in row['method_or_artifact']
    assert 'not demonstrated quality-preserving throughput' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/llm-systems-and-runtime.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research292"></span>') == 1
    section = page.split('## SmoothSpec: speculative decoding', 1)[1].split('## Checkpointing trades', 1)[0]
    for phrase in (
        'speculative decoding', 'draft', 'target', 'accepted', 'acceptance',
        'verification', 'intra-device', 'resource allocation', 'controller',
        'quality', 'latency', 'p95', 'p99', 'throughput', 'memory',
        'energy', 'tail-latency', 'not demonstrated quality-preserving throughput'
    ):
        assert phrase in section


def test_amoeba_explanation_separates_tp_reconfiguration_from_steady_state_throughput() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research538']
    assert 'Runtime transformation of tensor parallelism' in row['method_or_artifact']
    assert 'not demonstrated SLO-safe reconfiguration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/llm-systems-and-runtime.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research538"></span>') == 1
    section = page.split('## Amoeba: changing tensor parallelism', 1)[1].split('## Checkpointing trades', 1)[0]
    for phrase in (
        'tensor parallelism', 'runtime', 'KV-cache', 'migration', 'reconfiguration',
        'long-context', 'short-context', 'SLO', 'latency', 'p95', 'p99',
        'throughput', 'energy', '1.75×–6.57×', 'not demonstrated SLO-safe reconfiguration'
    ):
        assert phrase in section


def test_faster_moa_explanation_separates_latency_reduction_from_answer_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research628']
    assert 'Early-exit and overlap-aware MoA serving runtime' in row['method_or_artifact']
    assert 'not demonstrated quality-preserving serving' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/llm-systems-and-runtime.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research628"></span>') == 1
    section = page.split('## Faster-MoA: reducing agent connections', 1)[1].split('## Checkpointing trades', 1)[0]
    for phrase in (
        'Mixture-of-Agents', 'tree', 'early exit', 'semantic similarity',
        'confidence', 'prefill', 'decode', 'dependency', 'KV-cache',
        'accuracy', 'latency', 'throughput', 'energy', 'p95', 'p99',
        '90%', '±1%', 'not demonstrated quality-preserving serving'
    ):
        assert phrase in section


def test_unispike_explanation_separates_address_saving_from_timing_and_hardware_evidence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1640']
    assert 'aggregates spikes for a common destination' in row['method_or_artifact']
    assert 'not fabricated silicon' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/neuromorphic-and-emerging-architectures.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1640"></span>') == 1
    section = page.split('## UniSpike: address aggregation', 1)[1].split('## Logical time', 1)[0]
    for phrase in (
        'spiking neural network', 'address', 'event', 'packet', 'barrier',
        'bitmap', 'partition', 'timing', 'traffic', 'speed', 'energy',
        'area', '512 cores', '2-D mesh', '1.93×', '1.77×', '1.50×',
        'not fabricated silicon'
    ):
        assert phrase in section


def test_synchoros_explanation_separates_estimator_accuracy_from_energy_and_thermal_claims() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2851']
    assert 'Interconnect-aware Synchoros energy-estimation methodology' in row['method_or_artifact']
    assert 'not general full-system energy or thermal improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/power-and-thermal-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2851"></span>') == 1
    section = page.split('## Synchoros: an energy estimator', 1)[1]
    for phrase in (
        'CGRA', 'energy', 'interconnect', 'mapping', 'post-route',
        'accuracy', '98%', 'calibration', 'ranking', 'runtime',
        'power', 'temperature', 'thermal', 'silicon',
        'not general full-system energy or thermal improvement'
    ):
        assert phrase in section


def test_gmatcher_explanation_separates_gpu_speed_from_pattern_matching_recall() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1434']
    assert 'GPU-accelerated hierarchical/multi-level and multi-stage layout pattern matcher' in row['method_or_artifact']
    assert 'not demonstrated complete hotspot safety' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/manufacturing-and-yield.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1434"></span>') == 1
    section = page.split('## G-Matcher: a faster layout search', 1)[1].split('## Scheduling the computation', 1)[0]
    for phrase in (
        'layout', 'pattern matching', 'GPU', 'multi-stage', 'filter',
        'recall', 'precision', 'false negatives', 'memory', 'transfer',
        '407×', '7.1×', '100%', 'zero false matches', 'yield',
        'not demonstrated complete hotspot safety'
    ):
        assert phrase in section


def test_clipwise_ilt_explanation_separates_local_gradients_from_full_chip_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2525']
    assert 'Policy-learned coordinated gradient scheduling' in row['method_or_artifact']
    assert 'not demonstrated faster complete ILT' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/manufacturing-and-yield.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2525"></span>') == 1
    section = page.split('## Coordinated clip-wise ILT', 1)[1].split('## Rare defects', 1)[0]
    for phrase in (
        'inverse lithography', 'mask', 'clip', 'gradient', 'global',
        'graph neural network', 'policy', 'reward', 'boundary',
        'process window', 'convergence', 'runtime', 'wafer',
        'not demonstrated faster complete ILT'
    ):
        assert phrase in section


def test_difftail_explanation_separates_synthetic_defects_from_real_tail_recall() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research649']
    assert 'Mask-guided diffusion augmentation' in row['method_or_artifact']
    assert 'not demonstrated reliable cross-fab detection' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/manufacturing-and-yield.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research649"></span>') == 1
    section = page.split('## DiffTail: synthetic rare-defect images', 1)[1].split('## What would establish a manufacturing benefit?', 1)[0]
    for phrase in (
        'wafer', 'defect', 'SEM', 'long-tailed', 'mask', 'diffusion',
        'process-aware', 'metric', 'synthetic', 'real-only', 'recall',
        'precision', 'false-negative', 'cross-fab', 'yield', 'runtime',
        'not demonstrated reliable cross-fab detection'
    ):
        assert phrase in section


def test_separate_explanation_separates_weak_labels_from_pixel_localization() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research838']
    assert 'Weakly supervised defect-segmentation framework' in row['method_or_artifact']
    assert 'not demonstrated reliable localization' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/manufacturing-and-yield.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research838"></span>') == 1
    section = page.split('## SePArate: image-level labels', 1)[1].split('## What would establish a manufacturing benefit?', 1)[0]
    for phrase in (
        'segmentation', 'pixel', 'wafer', 'defect', 'weak supervision',
        'image-level', 'pretraining', 'knowledge transfer', 'synthetic',
        'recall', 'precision', 'localization', 'cross-process', 'label cost',
        'yield', 'not demonstrated reliable localization'
    ):
        assert phrase in section


def test_shortcircuit_explanation_separates_aig_correctness_from_mapped_ppa() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2329']
    assert 'Transformer-based AIG generator' in row['method_or_artifact']
    assert 'not demonstrated scalable physical circuit improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/generative-design-and-synthesis.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2329"></span>') == 1
    section = page.split('## Shortcircuit: a search-generated Boolean graph', 1)[1].split('## Evolving a design tool', 1)[0]
    for phrase in (
        'AND-inverter graph', 'truth table', 'functional equivalence',
        'AlphaZero', 'search', 'rollout', 'correctness', 'circuit size',
        'technology mapping', 'area', 'delay', 'power', '31×',
        '500 eight-input', 'not demonstrated scalable physical circuit improvement'
    ):
        assert phrase in section


def test_self_evolved_abc_explanation_separates_code_evolution_from_qor_validation() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1784']
    assert 'Multi-agent LLM code-evolution loop' in row['method_or_artifact']
    assert 'not demonstrated generally improved or maintainable synthesis tooling' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/generative-design-and-synthesis.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1784"></span>') == 1
    section = page.split('## Self-evolved ABC: changing synthesis software', 1)[1].split('## StepPRM-RTL', 1)[0]
    for phrase in (
        'ABC', 'software', 'code-evolution', 'LLM', 'correctness', 'regression',
        'QoR', 'area', 'delay', 'power', 'benchmark', 'overfit', 'held-out',
        'search cost', 'maintainability',
        'not demonstrated generally improved or maintainable synthesis tooling'
    ):
        assert phrase in section


def test_stepprm_rtl_explanation_separates_process_reward_from_executable_synthesis() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1742']
    assert 'Stepwise reasoning trajectories' in row['method_or_artifact']
    assert 'not demonstrated executable, synthesizable and PPA-improving hardware generation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/generative-design-and-synthesis.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1742"></span>') == 1
    section = page.split('## StepPRM-RTL: rewarding intermediate RTL steps', 1)[1].split('## Compare accepted implementations', 1)[0]
    for phrase in (
        'RTL', 'Verilog', 'VHDL', 'process-reward', 'PRM', 'RAFT', 'MCTS',
        'trajectory', 'correctness', 'simulation', 'synthesis', 'area',
        'timing', 'power', 'reward calibration', '10%', 'PPA',
        'not demonstrated executable, synthesizable and PPA-improving hardware generation'
    ):
        assert phrase in section


def test_flowplace_explanation_separates_generated_placement_from_legal_pPA() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2476']
    assert 'Flow-matching generative model' in row['method_or_artifact']
    assert 'not demonstrated robust end-to-end PPA improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/generative-design-and-synthesis.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2476"></span>') == 1
    section = page.split('## FlowPlace: a generated placement', 1)[1].split('## Evolving a design tool', 1)[0]
    for phrase in (
        'placement', 'flow matching', 'mask', 'constraint', 'overlap',
        'legal', 'wirelength', 'congestion', 'timing', 'power', 'area',
        'OpenROAD', 'ICCAD 2015', '10–50×', 'PPA',
        'not demonstrated robust end-to-end PPA improvement'
    ):
        assert phrase in section


def test_llmva_explanation_separates_verilog_a_generation_from_physical_calibration() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research179']
    assert 'LLM-assisted iterative Verilog-A generation/modeling' in row['method_or_artifact']
    assert 'not demonstrated calibrated model accuracy' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/generative-design-and-synthesis.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research179"></span>') == 1
    section = page.split('## LLMVA: a generated Verilog-A model', 1)[1].split('## Evolving a design tool', 1)[0]
    for phrase in (
        'Verilog-A', 'STT-MTJ', 'MRAM', 'physical', 'calibrated', 'device',
        'circuit', 'DTCO', '9.2%', '4-Mb', '28-nm', 'tape-out',
        '50%', 'PPA', 'convergence', 'human',
        'not demonstrated calibrated model accuracy'
    ):
        assert phrase in section


def test_topcell_explanation_separates_generated_topology_from_signoff_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2646']
    assert 'LLM-guided standard-cell topology optimization' in row['method_or_artifact']
    assert 'not demonstrated signoff-quality standard-cell improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/generative-design-and-synthesis.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2646"></span>') == 1
    section = page.split('## TOPCELL: a transistor topology', 1)[1].split('## Evolving a design tool', 1)[0]
    for phrase in (
        'standard cell', 'transistor', 'topology', 'LLM', 'GRPO', 'logical',
        'spatial', 'design-rule', 'routing', 'extraction', 'signoff',
        'area', 'timing', 'power', '2-nm', '7-nm', '85.91×',
        'not demonstrated signoff-quality standard-cell improvement'
    ):
        assert phrase in section


def test_circuitdiff_explanation_separates_metric_prediction_from_synthesis() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2793']
    assert 'RTL graphs as conditions' in row['method_or_artifact']
    assert 'not demonstrated RTL-to-netlist synthesis' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/generative-design-and-synthesis.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2793"></span>') == 1
    section = page.split('## CircuitDiff: an RTL-conditioned netlist representation', 1)[1].split('## Evolving a design tool', 1)[0]
    for phrase in (
        'RTL', 'netlist', 'graph', 'diffusion', 'cross-attention', 'equivalence',
        'early circuit-metric prediction', 'timing', 'area', 'power', 'congestion',
        'not demonstrated RTL-to-netlist synthesis'
    ):
        assert phrase in section


def test_hybrimoe_correction_preserves_phase_specific_metrics_and_boundaries() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2025-research1019']
    assert 'dynamic intra-layer CPU/GPU scheduling' in row['method_or_artifact']
    assert '1.33x average TTFT/prefill speedup' in row['metrics'][0]
    assert 'accuracy parity' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-hierarchy-and-persistence.md').read_text()
    assert page.count('<span id="explanation-dac-2025-research1019"></span>') == 1
    section = page.split('## HybriMoE connects model behavior to cache decisions', 1)[1].split('## RememTier:', 1)[0]
    for phrase in (
        'CPU', 'GPU', 'expert', 'prefetch', 'cache', 'prefill', 'token generation',
        '1.33×', '1.70×', 'accuracy parity', 'concurrency', 'RTX A6000',
    ):
        assert phrase in section


def test_agenticdse_explanation_separates_search_metrics_from_chiplet_ppa() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1519']
    assert 'Three cooperating LLM agents' in row['method_or_artifact']
    assert 'not independently reproducible chiplet PPA improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1519"></span>') == 1
    section = page.split('## AgenticDSE: multi-agent search', 1)[1]
    for phrase in (
        'chiplet', 'LLM', 'Bayesian', 'surrogate', 'Pareto', 'reference-front',
        'diversity', 'token', 'PPA', 'feasible', '36.9%', '66%', '46×', '18×',
        'not independently reproducible PPA or manufacturing conclusions'
    ):
        assert phrase in section


def test_adaptive_prefetch_explanation_separates_kv_accuracy_from_transfer_overlap() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1441']
    assert 'Adaptive token-fluctuation prediction' in row['method_or_artifact']
    assert 'universal long-context speedup' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1441"></span>') == 1
    section = page.split('## Adaptive token-fluctuation prediction', 1)[1].split('<span id="explanation-dac-2026-research1596"></span>', 1)[0]
    for phrase in (
        'KV', 'cache', 'prediction', 'recovery', 'Prefetching', 'attention',
        '256-token', 'full-KV', '2.50×', 'TTFT', 'concurrency',
        'demonstrated accuracy preservation'
    ):
        assert phrase in section


def test_photomt_correction_separates_hash_correctness_from_optical_speed() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2293']
    assert 'Photonic-electronic Merkle-tree engine' in row['method_or_artifact']
    assert 'not demonstrated complete-proof acceleration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/neuromorphic-quantum-and-non-von-neumann.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2293"></span>') == 1
    section = page.split('### PhotoMT: accelerate hash-tree construction', 1)[1].split('<span id="explanation-dac-2026-research1268"></span>', 1)[0]
    for phrase in (
        'cryptographic', 'Merkle', 'Zero knowledge', 'Poseidon', 'microring',
        'matrix-vector', 'digital', 'S-box', '18.8–20.5×', 'energy',
        'exact', 'complete proof', 'not every part of a proof'
    ):
        assert phrase in section


def test_rememtier_correction_separates_cxl_tiering_from_swapin_latency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2945']
    assert 'Workload-aware reversed memory tiering' in row['method_or_artifact']
    assert 'not demonstrated general CXL-system performance' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-hierarchy-and-persistence.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2945"></span>') == 1
    section = page.split('## RememTier: protect useful residency', 1)[1].split('<span id="explanation-dac-2026-research675"></span>', 1)[0]
    for phrase in (
        'CXL', 'DRAM', 'host memory', 'burst', 'replacement', 'CXL.io',
        'reordering', 'execution time', 'swap-in latency', '35%', '60%',
        'not a persistence contract'
    ):
        assert phrase in section


def test_ctxmem_explanation_separates_cxl_tiering_from_end_to_end_memory_gain() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1028']
    assert 'OS-hardware co-designed tiered memory' in row['method_or_artifact']
    assert 'not establish general end-to-end memory-system improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-hierarchy-and-persistence.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1028"></span>') == 1
    section = page.split('## Ctxmem: who handles a memory access', 1)[1].split('<span id="explanation-dac-2026-research270"></span>', 1)[0]
    for phrase in (
        'CXL', 'DRAM', 'flash', 'asynchronous', 'page fault', 'direct-mapped',
        'hot', 'migration', 'dirty', 'persistence', 'tail', 'gem5',
        '1.4×', '2×', 'not demonstrated general end-to-end memory-system improvement'
    ):
        assert phrase in section


def test_raf_explanation_separates_communication_bounds_from_llm_efficiency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1113']
    assert 'Remote-Access-Free (RAF) tensor-rotation dataflow' in row['method_or_artifact']
    assert 'not establish universal LLM/NMP efficiency or communication optimality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1113"></span>') == 1
    section = page.split('## RAF: a communication lower bound', 1)[1].split('<span id="explanation-dac-2026-research2294"></span>', 1)[0]
    for phrase in (
        'near-memory', 'vault', 'channel', 'Remote-Access-Free', 'tensor-rotation',
        'intra-operator', 'inter-operator', 'partitioning', 'fusion', 'lower bound',
        'local-bank conflicts', 'accuracy', '50.4%', '39.0%', '37.8%',
        '3.98×', '1.72×', '1.57×',
        'not demonstrated universal LLM/NMP efficiency or communication optimality'
    ):
        assert phrase in section


def test_diffpart_explanation_separates_learned_partitioning_from_simulation_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research068']
    assert 'DiffPart, a differentiable task-graph partitioning framework' in row['method_or_artifact']
    assert 'not establish reproducible general RTL-simulation acceleration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/optimization-and-search-methods.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research068"></span>') == 1
    section = page.split('## DiffPart: a learned partition', 1)[1].split('<span id="explanation-dac-2026-research1052"></span>', 1)[0]
    for phrase in (
        'RTL', 'simulation', 'task', 'dependency', 'partition', 'differentiable',
        'thread', 'schedule', 'correctness', 'sequential', 'critical path',
        'synchronization', 'Verilator', '1.22×', '55.25×',
        'not demonstrated reproducible general RTL-simulation acceleration'
    ):
        assert phrase in section


def test_blade_explanation_separates_package_plane_search_from_physical_validation() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research073']
    assert 'Metal-density-aware power/ground-plane synthesis' in row['method_or_artifact']
    assert 'not demonstrated production-ready power integrity' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/package-system-co-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research073"></span>') == 1
    section = page.split('## BLADE: package-plane search', 1)[1]
    for phrase in (
        'power/ground', 'metal-density', 'warpage', 'degassing', 'skeleton',
        'IR-drop', 'Bayesian', 'evaluator', 'trusted', 'mechanical',
        'fabrication', 'six SiP', 'not demonstrated production-ready power integrity'
    ):
        assert phrase in section


def test_dataflowgen_explanation_separates_mlir_ir_from_hardware_performance() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research083']
    assert 'Open-source Dataflowgen MLIR compiler' in row['method_or_artifact']
    assert 'not demonstrated reusable hardware-performance improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/high-level-synthesis-and-compilers.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research083"></span>') == 1
    section = page.split('## Dataflowgen: a richer IR', 1)[1].split('## CODO connects legality', 1)[0]
    for phrase in (
        'MLIR', 'IR', 'H-CDFG', 'dataflow', 'dependency', 'memory ordering',
        'precision', 'buffer', 'scheduling', 'resource', 'frequency',
        'timing', 'LUT', 'DSP', 'BRAM', 'synthesis', 'place-and-route',
        'not demonstrated reusable hardware-performance improvement'
    ):
        assert phrase in section


def test_gearls_explanation_separates_zero_shot_policy_transfer_from_timing_claims() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1042']
    assert 'Logic-cone-aware RL framework' in row['method_or_artifact']
    assert 'not establish technology-independent zero-shot PPA improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/optimization-and-search-methods.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1042"></span>') == 1
    section = page.split('## Gearls: zero-shot logic optimization', 1)[1].split('<span id="explanation-dac-2026-research1052"></span>', 1)[0]
    for phrase in (
        'logic', 'reinforcement-learning', 'logic cone', 'cut weighting', 'Policy Similarity Metric',
        'zero-shot', 'timing', 'WNS', 'TNS', 'PPA', 'technology library',
        'equivalence', 'mapping', '31.7%', '32.5%', '13%',
        'not demonstrated technology-independent zero-shot PPA improvement'
    ):
        assert phrase in section


def test_cannon_explanation_separates_real_cxl_hardware_from_ann_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research108']
    assert 'CXL-based near-memory processing architecture' in row['method_or_artifact']
    assert 'not demonstrated recall-preserving end-to-end ANN/RAG acceleration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research108"></span>') == 1
    section = page.split('## CANNON: real CXL hardware', 1)[1].split('<span id="explanation-dac-2026-research2294"></span>', 1)[0]
    for phrase in (
        'ANN', 'CXL', 'near-memory', 'real CXL hardware', 'pipelined', 'hashing',
        'speculative', 'recall@k', 'distance', 'top-k', 'p50/p95/p99',
        'QPS', 'power', 'two orders of magnitude',
        'not demonstrated recall-preserving end-to-end ANN/RAG acceleration'
    ):
        assert phrase in section


def test_accdrc_explanation_separates_fpga_speedup_from_drc_equivalence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1080']
    assert 'FPGA DRC accelerator' in row['method_or_artifact']
    assert 'not demonstrated signoff-equivalent DRC replacement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-timing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1080"></span>') == 1
    section = page.split('## AccDRC: DRC acceleration', 1)[1].split('## Placement and sizing influence each other', 1)[0]
    for phrase in (
        'DRC', 'layout', 'FPGA', 'cell-aware', 'partition', 'halo', 'rule',
        'equivalence', 'KLayout', 'OpenDRC', 'sparse', 'LUT', 'BRAM',
        '522.11×', '1071.03×', '9.62×', '26.07×',
        'not demonstrated signoff-equivalent DRC replacement'
    ):
        assert phrase in section


def test_hlsarchopt_explanation_separates_llm_architecture_generation_from_fpga_closure() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1110']
    assert 'LLM-based generation and optimization of modular dataflow HLS architectures' in row['method_or_artifact']
    assert 'does not establish production-ready FPGA acceleration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/llm-assisted-design-flows.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1110"></span>') == 1
    section = page.split('## FPGA HLS architecture optimization', 1)[1].split('<span id="explanation-dac-2026-research012"></span>', 1)[0]
    for phrase in (
        'LLM', 'HLS', 'dataflow', 'Fire-module', 'Vivado HLS', 'ZCU102',
        'functional', 'Backpressure', 'deadlock', '335,494', '229,703',
        '8.419', 'post-route', 'board', '11.78×',
        'not demonstrated production-ready FPGA acceleration'
    ):
        assert phrase in section


def test_copa_explanation_separates_pin_congestion_from_routing_and_timing_closure() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['iccad-2025-1155']
    assert 'COPA, a gradient-based nonlinear optimization framework' in row['method_or_artifact']
    assert 'not establish signoff-quality routing or timing improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-timing.md').read_text()
    assert page.count('<span id="explanation-iccad-2025-1155"></span>') == 1
    section = page.split('## COPA: pin assignment', 1)[1].split('## How to evaluate a timing improvement', 1)[0]
    for phrase in (
        'feedthrough', 'pin', 'boundary', 'congestion', 'routing-demand', 'gradient',
        'legal', 'overflow', 'detailed-routing', 'wirelength', 'timing',
        '7.6%', '9%', 'commercial EDA tool',
        'not demonstrated signoff-quality routing or timing improvement'
    ):
        assert phrase in section


def test_gaia_explanation_separates_glass_scheduling_from_deployed_storage_gain() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['iccad-2025-1144']
    assert 'GAIA glass-aware I/O middleware' in row['method_or_artifact']
    assert 'does not establish durable, deployable 82% end-to-end improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-iccad-2025-1144"></span>') == 1
    section = page.split('## GAIA: glass-aware scheduling', 1)[1]
    for phrase in (
        'Quartz-glass', 'mechanical', 'optical', 'X/Y', 'Z', 'Zigzag Data Placement',
        'Z-Axis First Placement', 'SMTF', 'movement time', 'address', 'mapping',
        'p50/p95/p99/p99.9', '82%', 'trace-driven', 'baseline schedulers',
        'not demonstrated durable, deployable 82% end-to-end archival-storage improvement'
    ):
        assert phrase in section


def test_tieranns_explanation_separates_cxl_placement_from_ann_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2268']
    assert 'CXL-aware priority queue' in row['method_or_artifact']
    assert 'not demonstrated scalable or high-speed ANNS performance' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2268"></span>') == 1
    section = page.split('## TierANNS: CXL tiering', 1)[1].split('<span id="explanation-dac-2026-research1596"></span>', 1)[0]
    for phrase in (
        'ANNS', 'graph', 'CXL', 'priority queue', 'Queue hints',
        'speculative', 'recall@k', 'tail latency', 'CXL bytes',
        'capacity', 'not demonstrated scalable or high-speed ANNS performance'
    ):
        assert phrase in section


def test_gpu_fuzz_explanation_separates_input_generation_from_bug_confirmation() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2056']
    assert 'Constraint-guided GPU-kernel fuzzer' in row['method_or_artifact']
    assert 'not a general detection rate' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2056"></span>') == 1
    section = page.split('## GPU-Fuzz: boundary generation', 1)[1].split('## Vten changes', 1)[0]
    for phrase in (
        'GPU', 'operator', 'constraint', 'solver', 'boundary', 'oracle',
        'sanitizer', 'Deduplicate', 'confirmed', 'severity', 'PyTorch',
        'TensorFlow', 'PaddlePaddle', '13', 'not a general detection rate'
    ):
        assert phrase in section


def test_m2cam_explanation_separates_analog_cam_density_from_genome_accuracy() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2708']
    assert 'Multi-level memristor analog CAM encoding' in row['method_or_artifact']
    assert 'not demonstrated end-to-end biological accuracy' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/emerging-memory-and-devices.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2708"></span>') == 1
    section = page.split('## M²CAM: represent sequence symbols', 1)[1].split('## Adder-DCIM:', 1)[0]
    for phrase in (
        'CAM', 'conductance', 'nucleotide', 'sensing', 'variation',
        'error correction', 'Single-cell RNA', 'reference tool',
        'device reduction', 'energy', 'latency', 'ADC/DAC', 'STAR',
        'not demonstrated end-to-end genome-processing efficiency'
    ):
        assert phrase in section


def test_3d_resac_correction_separates_refresh_safety_from_llm_latency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research270']
    assert 'sequential refresh-skip method' in row['method_or_artifact']
    assert 'not demonstrated refresh safety' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-hierarchy-and-persistence.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research270"></span>') == 1
    section = page.split('## 3D-ReSAC: nearby memory', 1)[1].split('<span id="explanation-isca-2026-program-004"></span>', 1)[0]
    for phrase in (
        'low-batch', 'model', 'DRAM', 'refresh', 'row', 'retention',
        'temperature', 'ArrowMesh', 'link utilization', 'collective',
        'partition', '7–100%', '53–75%', '1.12–2.02×',
        'not proof that every low-batch model benefits'
    ):
        assert phrase in section


def test_moe_balance_correction_separates_task_balance_from_inference_latency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research461']
    assert 'Real-time heterogeneous CPU-GPU scheduler' in row['method_or_artifact']
    assert 'not universal inference improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-hierarchy-and-persistence.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research461"></span>') == 1
    section = page.split('## MoE-Balance: schedule for completion time', 1)[1].split('<span id="explanation-dac-2026-research2686"></span>', 1)[0]
    for phrase in (
        'CPU', 'GPU', 'expert', 'task', 'scheduler', 'prefetch', 'chunk',
                'PCIe', 'routing', 'completion time', '1.6×', '37.5%',
        'throughput', 'latency', 'cannot establish it'
    ):
        assert phrase in section


def test_ir_drop_placement_correction_separates_mna_estimation_from_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2297']
    assert 'GPU-accelerated modified nodal analysis' in row['method_or_artifact']
    assert 'not demonstrated signoff-quality power-integrity closure' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-timing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2297"></span>') == 1
    section = page.split('## IR-drop-aware placement:', 1)[1].split('## Placement and sizing', 1)[0]
    for phrase in (
        'IR drop', 'PDN', 'GPU', 'MNA', 'density', 'current', 'voltage',
        'resistance', 'extracted', 'signoff', 'routing', 'thermal',
        'wirelength', 'runtime', 'not demonstrated signoff-quality power-integrity closure'
    ):
        assert phrase in section


def test_specanns_correction_separates_speculation_from_ann_recall() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research343']
    assert 'Computational-storage device with in-storage FPGA' in row['method_or_artifact']
    assert 'not demonstrated end-to-end search improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research343"></span>') == 1
    section = page.split('## SpecANNS: speculative in-storage search', 1)[1].split('<span id="explanation-dac-2026-research2550"></span>', 1)[0]
    for phrase in (
        'ANNS', 'graph', 'flash', 'FPGA', 'CSD', 'speculative', 'NAND',
        'recall@k', 'top-k', 'prediction', 'timely', 'energy', 'endurance',
            'exceeds 90%', 'not demonstrated end-to-end search improvement'
    ):
        assert phrase in section


def test_active_calibration_correction_separates_policy_efficiency_from_fidelity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2805']
    assert 'Bayesian information-gain-per-time' in row['method_or_artifact']
    assert 'not demonstrated autonomous fidelity maintenance' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/neuromorphic-quantum-and-non-von-neumann.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2805"></span>') == 1
    section = page.split('### Active calibration:', 1)[1].split('## Quantum compilation', 1)[0]
    for phrase in (
            'calibration', 'drift', 'dependency graph', 'Bayesian', 'information gain',
            'Reinforcement learning', 'randomized-benchmarking', 'uncertainty', 'physical operation',
            'mean time between', 'operating requirement', 'useful work',
            'not a numerical conclusion'
    ):
        assert phrase in section


def test_attackonctf_correction_separates_obfuscation_from_benchmark_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1628']
    assert 'LLM-oriented benchmark obfuscation' in row['method_or_artifact']
    assert 'not a universal claim' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/hardware-security-validation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1628"></span>') == 1
    section = page.split('## Benchmark shortcuts', 1)[1].split('## Preserving behavior', 1)[0]
    for phrase in (
            'detector', 'rewrites', 'reference-comparison shortcuts',
            'Verilator', 'Yosys', 'equivalence', '50 injected vulnerabilities',
            'precision', 'recall', 'directly observed model process'
    ):
        assert phrase in section


def test_memflow_explanation_separates_simulator_fidelity_from_hardware_gain() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2550']
    assert 'Flow-centric simulator' in row['method_or_artifact']
    assert 'not demonstrated simulator fidelity' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2550"></span>') == 1
    section = page.split('## MemFlow: a detailed contention model', 1)[1].split('<span id="explanation-dac-2026-research1596"></span>', 1)[0]
    for phrase in (
        'disaggregated', 'load-store', 'cache', 'network', 'memory controller',
        'flow-centric', 'contention', 'validation', 'microbenchmarks',
        'p95', 'p99', 'design-space', 'hardware', 'not demonstrated simulator fidelity'
    ):
        assert phrase in section


def test_hypas_explanation_separates_surrogate_guidance_from_signoff_ppa() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1317']
    assert 'Hybrid differentiable/discrete placement and sizing' in row['method_or_artifact']
    assert 'not demonstrated signoff-quality PPA improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-timing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1317"></span>') == 1
    section = page.split('## HyPAS: a differentiable placement proposal', 1)[1].split('## Placement and sizing influence', 1)[0]
    for phrase in (
        'placement', 'sizing', 'DREAMPlace', 'GNN', 'surrogate', 'OpenROAD',
        'straight-through', 'legal', 'timing', 'power', 'routing', 'extraction',
        'signoff', 'PPA', 'ICCAD 2025', 'not demonstrated signoff-quality PPA'
    ):
        assert phrase in section


def test_vten_explanation_separates_batching_speed_from_verification_completeness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2348']
    assert 'Declarative tensor-centric verification DSL' in row['method_or_artifact']
    assert 'not demonstrated verification completeness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2348"></span>') == 1
    section = page.split('## vTen: batching simulation', 1)[1].split('## Fault injection changes', 1)[0]
    for phrase in (
        'tensor', 'RTL', 'DSL', 'batch', 'synchronization', 'oracle', 'correctness',
        'coverage', 'debug', '2×', '60.3%', 'Cocotb', 'UVM', 'simulation latency',
        'not demonstrated verification completeness'
    ):
        assert phrase in section


def test_adaptive_read_retry_correction_separates_recovery_from_lifetime_claims() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2686']
    assert 'Adaptive read-retry table extension' in row['method_or_artifact']
    assert 'not demonstrated vendor-general reliability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-hierarchy-and-persistence.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2686"></span>') == 1
    section = page.split('## Adaptive flash read retry:', 1)[1].split('<span id="explanation-dac-2026-research1986"></span>', 1)[0]
    for phrase in (
        'stored charge', 'read reference', 'retry table', 'wordline', 'interpolation',
        'multidimensional', 'Error-correcting', 'recovery', 'usable capacity', '12- and 30-month',
                'delay', 'wear', 'end-of-life', 'lifetime'
    ):
        assert phrase in section


def test_dcts_explanation_separates_continuous_search_from_clock_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1211']
    assert 'End-to-end differentiable CTS' in row['method_or_artifact']
    assert 'not demonstrated signoff-quality clock improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/placement-routing-and-timing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1211"></span>') == 1
    section = page.split('## DCTS: a continuous clock-tree search', 1)[1].split('## How to evaluate a timing improvement', 1)[0]
    for phrase in (
        'Clock-tree', 'CTS', 'PGM', 'topology', 'buffer', 'legal', 'routing',
        'extracted', 'timing', 'skew', 'convergence', 'PPA', '2.78×', '1.98×',
        'ASAP7', 'not demonstrated signoff-quality clock'
    ):
        assert phrase in section


def test_reflex_correction_separates_row_alignment_from_accuracy_and_llm_gain() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1986']
    assert 'Rewrite-free row-aligned KV placement' in row['method_or_artifact']
    assert 'not demonstrated general LLM throughput' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-hierarchy-and-persistence.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1986"></span>') == 1
    section = page.split('## REFLEX: fewer selected tokens', 1)[1].split('<span id="explanation-dac-2026-research676"></span>', 1)[0]
    assert 'row' in section
    for phrase in (
        'attention', 'KV cache', 'DRAM', 'PIM', 'activated rows', 'rewrite',
        'accuracy', 'dense', 'sparse', 'mapping', 'throughput', 'energy',
        '1.64×', '1.36×', '1.37×'
    ):
        assert phrase in section


def test_scout_explanation_separates_thermal_scheduling_from_deadline_feasibility() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2481']
    assert 'SCOUT couples task-level dynamic frequency scaling' in row['method_or_artifact']
    assert 'not demonstrated real-time guarantees' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/thermal-and-reliability-modeling.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2481"></span>') == 1
    section = page.split('## SCOUT: thermal-aware SRAM allocation', 1)[1].split('## A predicted failure rate needs exposure', 1)[0]
    for phrase in (
        'SRAM', 'Edge TPU', 'real-time', 'frequency', 'DFS', 'reallocation', 'thermal model',
        'deadline', 'response time', 'deadline miss', 'sensor delay', 'cooling', 'package',
        '46%', 'not demonstrated real-time guarantees',
    ):
        assert phrase in section


def test_fp_ddm_explanation_separates_domain_decomposition_from_stress_fidelity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research158']
    assert 'Foundation-model-based physics-guided adaptation' in row['method_or_artifact']
    assert 'not demonstrated reliability-grade thermal-stress prediction' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/thermal-and-reliability-modeling.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research158"></span>') == 1
    section = page.split('## FP-DDM: neural domain decomposition', 1)[1].split('## Thermal control has timing consequences', 1)[0]
    for phrase in (
        'thermal', 'stress', 'overlapping', 'subdomains', 'interface', 'automatic differentiation',
        'physics-guided', 'finite-element', 'flux', 'traction', 'conservation', 'convergence',
        '10-billion-cell', 'unseen domains', 'not demonstrated reliability-grade thermal-stress prediction',
    ):
        assert phrase in section


def test_early_thermal_correction_separates_prediction_from_physical_reliability() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research706']
    assert 'ML power-density prediction during global placement' in row['method_or_artifact']
    assert 'not demonstrated package- or silicon-level thermal reliability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/energy-and-thermal-efficiency.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research706"></span>') == 1
    section = page.split('## Early-stage ML thermal placement:', 1)[1].split('## Lit Silicon:', 1)[0]
    for phrase in (
        'thermal', 'power density', 'placement', 'steady-state', 'physics', 'ML',
        'prediction', 'hotspot', 'routed', 'parasitics', 'timing', 'package',
        'electromigration', '49.0%', '34.9%', '9.97°C',
        'not demonstrated package- or silicon-level thermal reliability'
    ):
        assert phrase in section


def test_neutral_atom_compiler_correction_separates_search_from_physical_execution() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1316']
    assert 'Goal-directed Iterative Diving Search compiler' in row['method_or_artifact']
    assert 'not demonstrated physical-device execution' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/synthesis-and-compilation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1316"></span>') == 1
    section = page.split('## IDS and relaxed routing:', 1)[1].split('## Why minimizing T gates', 1)[0]
    for phrase in (
        'neutral-atom', 'compiler', 'IDS', 'Iterative Diving Search', 'routing',
        'atom', 'movement', 'occupancy', 'fidelity', 'loss', 'memory', 'runtime',
        'thousands of qubits', '28.1%', 'not demonstrated physical-device execution'
    ):
        assert phrase in section


def test_clue_ecc_correction_separates_parity_pooling_from_composed_reliability() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research676']
    assert 'CLUE-ECC pools 16-bit on-die and system ECC parity' in row['method_or_artifact']
    assert 'not demonstrated standards-compatible reliability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/memory-hierarchy-and-persistence.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research676"></span>') == 1
    section = page.split('## CLUE-ECC: make the correction unit', 1)[1].split('<span id="explanation-dac-2026-research1061"></span>', 1)[0]
    for phrase in (
        'LPDDR', '12-bit', 'Reed–Solomon', 'on-die', 'system ECC', 'parity',
        'decoder', 'fault', 'correction', 'bandwidth', 'latency', 'area', 'power',
        '33.3%', '14.83%', '24.18%'
    ):
        assert phrase in section


def test_loha_correction_separates_storage_pipeline_from_ann_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1560']
    assert 'CPU-storage hybrid architecture' in row['method_or_artifact']
    assert 'not demonstrated recall-preserving end-to-end latency' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1560"></span>') == 1
    section = page.split('## LOHA: splitting graph traversal', 1)[1].split('## COSM:', 1)[0]
    for phrase in (
        'ANNS', 'graph', 'CPU', 'storage', 'PQ', 're-ranking', 'SSD', 'speculative',
        'recall@k', 'top-k', 'read amplification', 'latency', 'throughput',
        '9.6×', '6.2×', '4.0×'
    ):
        assert phrase in section


def test_nvllm_explanation_separates_nand_execution_from_quality_and_endurance() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1570']
    assert '3D NAND-centric inference architecture' in row['method_or_artifact']
    assert 'not demonstrated durable, quality-preserving end-to-end edge inference' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1570"></span>') == 1
    section = page.split('## NVLLM: NAND-resident inference', 1)[1].split('## Reliability can create additional movement', 1)[0]
    for phrase in (
        '3D NAND', 'FFN', 'attention', 'DRAM', 'ECC', 'KV-cache', 'GEMM', 'GEMV',
        'numerical', 'perplexity', 'NAND generation', 'latency', 'endurance',
        '16.7×', '1.1×–4.7×', '2.7%',
        'not demonstrated durable, quality-preserving end-to-end edge inference',
    ):
        assert phrase in section


def test_hiband_explanation_separates_nominal_bandwidth_from_noc_execution() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research282']
    assert 'Bandwidth-aware HB-DRAM accelerator' in row['method_or_artifact']
    assert 'not demonstrated portable end-to-end LLM acceleration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research282"></span>') == 1
    section = page.split('## HiBand: more in-situ DRAM bandwidth', 1)[1].split('## Reliability can create additional movement', 1)[0]
    for phrase in (
        'HB-DRAM', 'bandwidth', 'NoC', 'array', 'tensor', 'attention', 'FFN', 'routing',
        'queueing', 'buffer', 'synchronization', 'reconfiguration', 'KV-cache',
        '4.28×', '1.67×', 'not demonstrated portable end-to-end LLM acceleration',
    ):
        assert phrase in section


def test_impart_correction_separates_memetic_search_from_partition_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1292']
    assert 'Single multilevel hypergraph-partitioning framework' in row['method_or_artifact']
    assert 'not demonstrated scalable partition quality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/optimization-and-search-methods.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1292"></span>') == 1
    section = page.split('## Impart: integrated memetic search', 1)[1].split('## Template matching', 1)[0]
    for phrase in (
        'hypergraph', 'partitioning', 'vertices', 'k', 'cut', 'balance', 'coarsening',
        'uncoarsening', 'recombination', 'mutation', 'memory', 'runtime', 'seeds',
        'large-`k`', 'not demonstrated scalable partition quality'
    ):
        assert phrase in section


def test_aimx_compiler_correction_separates_transfer_reduction_from_model_behavior() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1365']
    assert 'ONNX Runtime graph compiler for SK hynix AiMX' in row['method_or_artifact']
    assert 'not a general LLM speedup' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1365"></span>') == 1
    section = page.split('## AiMX graph compilation:', 1)[1].split('## COSM:', 1)[0]
    for phrase in (
        'PIM', 'graph', 'tensor', 'AiMX', 'ONNX Runtime', 'DMA', 'layout', 'fusion',
        'kernel coverage', 'fallback', 'prefill', 'decode', 'transfer', 'synchronization',
        '50.07%', '78.36%', '2.00–2.73×', '18.50–38.29×'
    ):
        assert phrase in section


def test_hddb_correction_separates_hdc_noise_tolerance_from_sql_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1619']
    assert 'HDC encoding for standard SQL tables' in row['method_or_artifact']
    assert 'not demonstrated exact database correctness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1619"></span>') == 1
    section = page.split('## HDDB: noise-robust in-storage SQL', 1)[1].split('NVLLM uses NAND', 1)[0]
    for phrase in (
        'SQL', 'HDC', 'predicate', 'aggregation', 'FeNAND', 'MLC', 'TLC', 'noise',
        'ECC', 'false-positive', 'false-negative', 'sensing', 'corruption',
        'latency', 'energy', '80.6×', '12,636×'
    ):
        assert phrase in section


def test_flashhd_correction_separates_in_storage_filtering_from_exact_recall() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2773']
    assert '3D-NAND in-storage sequence-matching framework' in row['method_or_artifact']
    assert 'not demonstrated exact-recall' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2773"></span>') == 1
    section = page.split('## FlashHD: in-storage HDC filtering', 1)[1].split('## EtherSSD:', 1)[0]
    for phrase in (
        'DNA', 'sequence', '3D NAND', 'in-storage', 'hyperdimensional', 'HDC',
        'hierarchical', 'recall', 'false negatives', 'false positives', 'exact',
        'sensing', 'ECC', 'latency', 'energy', 'endurance', 'read disturb',
        'not demonstrated exact-recall'
    ):
        assert phrase in section


def test_lhgstore_correction_separates_learned_layout_from_graph_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2806']
    assert 'degree-aware Learned Hierarchical Graph store' in row['method_or_artifact']
    assert 'not demonstrated portable 5.9–28.2x end-to-end benefit' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2806"></span>') == 1
    section = page.split('## LHGstore: learned adjacency layout', 1)[1].split('## EtherSSD:', 1)[0]
    for phrase in (
        'in-memory', 'graph', 'updates', 'analytics', 'degree', 'two-level',
        'arrays', 'learned indexes', 'vertex', 'edge', 'traversal', 'consistency',
        'rebuild', 'NUMA', 'memory', 'p50', 'p95', 'p99', '5.9–28.2×',
        'distribution shift', 'not demonstrated portable 5.9–28.2× end-to-end benefit',
    ):
        assert phrase in section


def test_valve_explanation_separates_in_storage_vvs_from_mvcc_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research442']
    assert 'visible-version searching from the host to a computational-storage device' in row['method_or_artifact']
    assert 'not demonstrated serializable/consistent HTAP correctness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research442"></span>') == 1
    section = page.split('## VALVE: in-storage visible-version search', 1)[1].split('## FlashHD:', 1)[0]
    for phrase in (
        'MVCC', 'version', 'HTAP', 'transaction', 'analytical', 'CSD', 'visible',
        'skip list', 'snapshot', 'commit', 'abort', 'consistency', 'uncommitted',
        'p50/p95/p99', 'power loss', 'recovery', 'latency', 'throughput',
        'not demonstrated consistency, failure-safe persistence',
    ):
        assert phrase in section


def test_llm_hybrid_ssd_explanation_separates_adaptive_tuning_from_controller_safety() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research609']
    assert 'LLM-based tuner for adaptive configuration' in row['method_or_artifact']
    assert 'not demonstrated safe, durable, low-tail' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research609"></span>') == 1
    section = page.split('## LLM-hybridSSD: adaptive tuning', 1)[1].split('## VALVE:', 1)[0]
    for phrase in (
        'hybrid SSD', 'SLC', 'QLC', 'conversion', 'migration', 'garbage collection',
        'LLM', 'reinforcement-learning', 'parameter', 'controller', 'FTL', 'ECC',
        'wear-leveling', 'power loss', 'write amplification', 'logical-to-physical',
        'p50/p95/p99', 'endurance', '58.92%', '28.56%', 'held-out',
        'not demonstrated safe, durable, low-tail',
    ):
        assert phrase in section


def test_freezone_explanation_separates_slc_buffering_from_zone_durability() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research698']
    assert 'SLC flash' in row['method_or_artifact']
    assert 'not demonstrated crash-safe consistency' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research698"></span>') == 1
    section = page.split('## FreeZone: SLC-backed out-of-order buffering', 1)[1].split('## LLM-hybridSSD:', 1)[0]
    for phrase in (
        'zoned', 'zone', 'logical order', 'kernel', 'SLC', 'reorder buffer', 'out of order',
        'write pointer', 'flush/FUA', 'zone reset', 'durability', 'power loss',
        'metadata', 'garbage-collection', 'write amplification', 'TBW',
        'p50/p95/p99', '2.3×', 'not demonstrated crash-safe consistency',
    ):
        assert phrase in section


def test_ragnmp_explanation_separates_near_memory_search_from_rag_fidelity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research701']
    assert 'general-purpose near-memory RAG accelerator' in row['method_or_artifact']
    assert 'not demonstrated ANN recall' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research701"></span>') == 1
    section = page.split('## RAGNMP: near-memory elimination trees', 1)[1].split('## PIMGRAG moves', 1)[0]
    for phrase in (
        'RAG', 'retrieval', 'knowledge corpus', 'vector', 'near-memory', 'elimination tree',
        'data placement', 'parallelism', 'pipelining', 'top-k', 'recall', 'precision',
        'factuality', 'reranking', 'bandwidth', 'p50/p95/p99', 'dynamic', 'index',
        'not demonstrated ANN recall',
    ):
        assert phrase in section


def test_piano_explanation_separates_admittance_surrogate_from_pi_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research733']
    assert 'equivalent port admittance matrix' in row['method_or_artifact']
    assert 'not demonstrated signoff-grade voltage integrity' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/thermal-and-reliability-modeling.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research733"></span>') == 1
    section = page.split('## PIANO: a learned admittance', 1)[1].split('## What a useful combined study', 1)[0]
    for phrase in (
        'DC', 'power-integrity', 'PDN', 'Kirchhoff', 'SPD', 'resistive', 'graph',
        'admittance', 'GNN', 'port', 'voltage', 'symmetry', 'positive definiteness',
        'passivity', 'residual', 'geometry', 'current-sink', 'conditioning',
        '12.6×', '1.95%', '17.2×', 'signoff-grade voltage integrity',
    ):
        assert phrase in section


def test_smartswap_explanation_separates_swap_capacity_from_training_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research484']
    assert 'Eager-Mode operator sequences' in row['method_or_artifact']
    assert 'not demonstrated accuracy-preserving' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research484"></span>') == 1
    section = page.split('## SmartSwap: adaptive tensor swapping', 1)[1].split('## FlashHD:', 1)[0]
    for phrase in (
        'LLM', 'training', 'HBM', 'activation', 'optimizer', 'Eager Mode',
        'operator sequence', 'profiler', 'swap', 'prefetch', 'eviction',
        'autograd', 'gradient', 'checkpoint', 'recomputation', 'DMA',
        'synchronization', 'p50/p95/p99', '84.25%', '4×', '38.94%',
        'convergence', 'not demonstrated accuracy-preserving',
    ):
        assert phrase in section


def test_uncharted_correction_separates_surrogate_speed_from_spice_fidelity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2385']
    assert 'Hierarchical autoregressive spatio-temporal graph-neural surrogate' in row['method_or_artifact']
    assert 'not demonstrated universal SPICE fidelity' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2385"></span>') == 1
    section = page.split('## UNCHARTED: a transient surrogate', 1)[1].split('<span id="explanation-dac-2026-research1519"></span>', 1)[0]
    for phrase in (
        'analog', 'transient', 'SPICE', 'surrogate', 'graph', 'auto-regressive',
        'spatio-temporal', 'sizing', 'inverse design', 'gradient',
        'process', 'corner', 'waveform', 'stability', '241.9×', '95%', '70%'
    ):
        assert phrase in section


def test_laelaps_correction_separates_numa_locality_from_system_fairness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research651']
    assert 'Workload-aware I/O coordination' in row['method_or_artifact']
    assert 'not demonstrated universal throughput improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research651"></span>') == 1
    section = page.split('## Laelaps: NUMA-aware cache placement', 1)[1].split('## Moving computation toward stored data', 1)[0]
    for phrase in (
        'NUMA', 'NVMe', 'page-cache', 'I/O-thread', 'eviction', 'topology', 'affinity',
        'coherence', 'fairness', 'tail latency', 'queue', 'migration', 'writeback',
        '1.41×', '3.5%'
    ):
        assert phrase in section


def test_simultaneous_fault_correction_separates_campaign_speed_from_fault_coverage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1417']
    assert 'Interaction-aware simultaneous DNN fault-injection assessment' in row['method_or_artifact']
    assert 'not demonstrated broad reliability coverage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1417"></span>') == 1
    section = page.split('## Simultaneous DNN fault injection:', 1)[1].split('## A comparison that explains', 1)[0]
    for phrase in (
        'fault', 'DNN', 'simultaneous', 'interaction', 'masking', 'pruning', 'software',
        'RTL', 'oracle', 'single-fault', 'critical', 'false negatives', '42 million',
        '3.82×', '5.29×'
    ):
        assert phrase in section


def test_ares_explanation_separates_oracle_generation_from_security_assurance() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research177']
    assert 'Automated specification-to-executable-oracle extraction' in row['method_or_artifact']
    assert 'not demonstrated oracle completeness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research177"></span>') == 1
    section = page.split('## ARES: an executable protocol oracle', 1)[1].split('## A comparison that explains', 1)[0]
    for phrase in (
        'IoT', 'protocol', 'specification', 'executable', 'oracle', 'LLM', 'filtering',
        'state', 'transition', 'precision', 'recall', 'false negatives', 'CVE',
        'not demonstrated oracle completeness'
    ):
        assert phrase in section


def test_defvul_risk_explanation_separates_cve_counts_from_tool_security_assurance() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2306']
    assert 'DefVul-Risk' in row['method_or_artifact']
    assert 'not demonstrated exploitability coverage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/hardware-security-validation.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2306"></span>') == 1
    section = page.split('## DefVul-Risk:', 1)[1].split('## What connects these papers', 1)[0]
    for phrase in (
        'DefVul-Risk', 'FPGA', 'HDL', 'synthesis', 'LLM', 'trigger',
        'crash', 'miscompile', 'denial of service', 'attacker', 'permissions',
        'CVE', 'deduplication', 'precision', 'recall', 'held-out',
        '26', 'nine', 'tool/version', 'exploitability',
        'not demonstrated exploitability coverage',
    ):
        assert phrase in section


def test_ssd_reforge_explanation_separates_tbw_from_protection_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1872']
    assert 'Dynamic intra-device parity strengthening' in row['method_or_artifact']
    assert 'not demonstrated device-level endurance improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1872"></span>') == 1
    section = page.split('## SSD Reforge: extra parity', 1)[1].split('## How to compare complete requests', 1)[0]
    for phrase in (
        'SSD', 'flash', 'aging', 'RBER', 'parity', 'RAS', 'SUPERL', 'stripe',
        'calibration', 'write amplification', 'latency', 'capacity', 'energy',
        '40%', 'user-TBW', 'not demonstrated device-level endurance improvement'
    ):
        assert phrase in section


def test_gpower_explanation_separates_transfer_from_power_calibration() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1431']
    assert 'Knowledge-aggregated architecture-level GPU power modeling' in row['method_or_artifact']
    assert 'not demonstrated cross-GPU generalization' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1431"></span>') == 1
    section = page.split('## G-Power: cross-GPU knowledge', 1)[1].split('## Hardware-aware BEV NAS:', 1)[0]
    for phrase in (
        'GPU', 'power', 'pre-training', 'aggregation', 'fine-tuning', 'AccelWattch',
        'calibrated', 'voltage', 'frequency', 'temperature', 'zero-shot', 'MAPE',
        'correlation', '14%', '0.88', 'not demonstrated cross-GPU generalization',
    ):
        assert phrase in section


def test_compilation_tells_energy_separates_compiler_proxy_from_power_calibration() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1474']
    assert 'Compiler-IR feature extraction with multi-task learning' in row['method_or_artifact']
    assert 'not demonstrated calibrated silicon power prediction' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1474"></span>') == 1
    section = page.split('## Compilation Tells Energy:', 1)[1].split('## Hardware-aware BEV NAS:', 1)[0]
    for phrase in (
        'compiler', 'IR', 'power', 'energy', 'multi-task', 'Gemmini', 'hls4ml',
        'synthesis', 'calibration', 'voltage', 'held-out', 'label',
        'not demonstrated calibrated silicon power prediction',
    ):
        assert phrase in section


def test_multidie_fpga_floorplanning_separates_gnn_prediction_from_routed_timing() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2048']
    assert 'Slot-level graph neural network predictor' in row['method_or_artifact']
    assert 'not demonstrated portable routed-timing improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2048"></span>') == 1
    section = page.split('## Multi-die FPGA floorplanning:', 1)[1].split('## Hardware-aware BEV NAS:', 1)[0]
    for phrase in (
        'HLS', 'multi-die', 'FPGA', 'slot-level', 'graph neural network', 'congestion',
        'Vitis', 'placement', 'routing', 'cross-die', 'timing', 'post-route',
        '84.13%', '0.86', '0.58ms', '11.2%', '23.8%', '30.9%',
        'not demonstrated portable routed-timing improvement',
    ):
        assert phrase in section


def test_bev_nas_explanation_separates_fps_from_end_to_end_realtime_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1878']
    assert 'Hardware-aware neural architecture search' in row['method_or_artifact']
    assert 'not demonstrated universal real-time autonomous-driving suitability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1878"></span>') == 1
    section = page.split('## Hardware-aware BEV NAS:', 1)[1].split('## UNCHARTED:', 1)[0]
    for phrase in (
        'BEV', 'LiDAR', 'camera', 'NAS', 'depth', 'cross-attention', 'nuScenes',
        'mAP', 'Jetson AGX Orin', 'FPS', 'latency', 'power', 'thermal',
        'preprocessing', 'search cost', 'not demonstrated universal real-time autonomous-driving suitability'
    ):
        assert phrase in section


def test_chirm_dse_explanation_separates_surrogate_speed_from_hls_qor() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2083']
    assert 'Hierarchical design-space decomposition' in row['method_or_artifact']
    assert 'not demonstrated portable QoR superiority' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2083"></span>') == 1
    section = page.split('## CHiRM-DSE:', 1)[1].split('## UNCHARTED:', 1)[0]
    for phrase in (
        'HLS', 'pragma', 'FPGA', 'decomposition', 'rule mining', 'CodeLLM', 'surrogate',
        'QoR', 'ranking', 'LUT', 'BRAM', 'DSP', 'Pareto', 'time budget', 'leakage',
        'not demonstrated portable QoR superiority'
    ):
        assert phrase in section


def test_det_trojan_explanation_separates_classifier_scores_from_security_coverage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2179']
    assert 'Functionality-aware feature engineering' in row['method_or_artifact']
    assert 'not demonstrated security coverage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2179"></span>') == 1
    section = page.split('## DeTrojan: a stronger graph classifier', 1)[1].split('## A comparison that explains', 1)[0]
    for phrase in (
        'Trojan', 'gate-level', 'circuit-level', 'GNN', 'functionality', 'edge-aware',
        'community', 'localization', 'false-positive', 'unseen', 'adaptive', 'leakage',
        '16.7%', '47.3%', '16.6%', '2×', 'not demonstrated security coverage'
    ):
        assert phrase in section


def test_atpg_free_tpi_explanation_separates_embeddings_from_fault_coverage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1971']
    assert 'Self-supervised autoencoder on bit sequences' in row['method_or_artifact']
    assert 'not demonstrated production-test improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1971"></span>') == 1
    section = page.split('## ATPG-free test-point insertion:', 1)[1].split('## UNCHARTED:', 1)[0]
    for phrase in (
        'ATPG', 'Test-point', 'controllability', 'observability', 'self-supervised',
        'autoencoder', 'reconvergent', 'fault coverage', 'scan', 'area', 'timing',
        'power', 'pattern count', 'RL', 'not demonstrated production test improvement'
    ):
        assert phrase in section


def test_chipmodeler_explanation_separates_generation_speed_from_oracle_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2319']
    assert 'LLM-assisted hierarchical reference-model generation' in row['method_or_artifact']
    assert 'not demonstrated trusted-oracle quality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2319"></span>') == 1
    section = page.split('## ChipModeler: generating a reference model', 1)[1].split('## A comparison that explains', 1)[0]
    for phrase in (
        'reference model', 'LLM', 'hierarchical', 'building blocks', 'behavioral',
        'oracle', 'RTL', 'protocol', 'reset', 'equivalence', 'corner cases',
        'escaped', 'human', '58.99%', '9.18×', '7.11×',
        'not demonstrated trusted-oracle quality'
    ):
        assert phrase in section


def test_lyra_explanation_separates_fuzzing_throughput_from_processor_coverage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research358']
    assert 'Heterogeneous RISC-V verification framework' in row['method_or_artifact']
    assert 'not demonstrated verification completeness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research358"></span>') == 1
    section = page.split('## Lyra: hardware-accelerated differential fuzzing', 1)[1].split('## vTen:', 1)[0]
    for phrase in (
        'RISC-V', 'DUT', 'reference model', 'FPGA SoC', 'LyraGen', 'ISA-aware',
        'privilege', 'exceptions', 'CSR', 'memory ordering', 'oracle', 'coverage',
        '1.27×', '107×–3343×', 'unique bugs', 'not demonstrated verification completeness',
    ):
        assert phrase in section


def test_rl4hdl_explanation_separates_diverse_generation_from_compiler_defects() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1813']
    assert 'Reinforcement-learning generator guided by HDL code diversity' in row['method_or_artifact']
    assert 'not demonstrated synthesis correctness coverage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1813"></span>') == 1
    section = page.split('## RL4HDL: diverse compiler tests', 1)[1].split('## Vten changes', 1)[0]
    for phrase in (
        'FPGA', 'logic-synthesis compiler', 'RTL', 'reinforcement learning', 'diversity',
        'oracle', 'netlist', 'formal', 'equivalence', 'coverage', 'root cause',
        'false positives', 'three-month', '20 unique defects', '12 previously unreported',
        'not demonstrated synthesis correctness coverage',
    ):
        assert phrase in section


def test_uvmarvel_explanation_separates_code_coverage_from_bug_detection() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2880']
    assert 'LLM-aided UVM generation' in row['method_or_artifact']
    assert 'not demonstrated verification completeness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2880"></span>') == 1
    section = page.split('## UVMarvel: a generated UVM environment', 1)[1].split('## A comparison that explains', 1)[0]
    for phrase in (
        'UVM', 'stimulus', 'protocol', 'intermediate representation', 'signal tracker',
        'scoreboard', 'assertions', 'functional coverage', 'code coverage', 'bug',
        'escaped', 'backpressure', 'reset', '4.5-hour', '95.65%',
        'not demonstrated verification completeness'
    ):
        assert phrase in section


def test_taco_explanation_separates_zero_cost_ranking_from_deployment_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1440']
    assert 'Training-free zero-cost accuracy score' in row['method_or_artifact']
    assert 'not demonstrated accuracy-preserving hardware transfer' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1440"></span>') == 1
    section = page.split('## TACo: a zero-cost score', 1)[1].split('## UNCHARTED:', 1)[0]
    for phrase in (
        'ViT', 'zero-cost', 'Hypervolume', 'gradient', 'Pareto', 'training', 'ranking',
        'CIFAR-10', 'ImageNet-1K', 'latency', 'energy', 'activation memory',
        'hardware', 'leakage', 'GPU-days', 'GPU-hours',
        'not demonstrated accuracy-preserving hardware transfer'
    ):
        assert phrase in section


def test_hybhana_explanation_separates_calibrated_cost_proxy_from_quantum_execution() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research577']
    assert 'Hyb-HANAS' in row['method_or_artifact']
    assert 'not demonstrated quantum advantage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research577"></span>') == 1
    section = page.split('## Hyb-HANAS: a calibrated quantum-cost proxy', 1)[1]
    for phrase in (
        'Quantum machine-learning', 'quantum circuit', 'classical network',
        'native-gate', 'routing', 'shots', 'decoherence', 'NSGA-II',
        'real-device calibration', 'wall-clock', 'fidelity', 'held-out',
        'Pareto', 'accuracy-only NAS', 'quantum advantage',
        'not demonstrated quantum advantage',
    ):
        assert phrase in section


def test_ipclm_explanation_separates_layout_metric_prediction_from_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1859']
    assert 'GEOG' in row['method_or_artifact']
    assert 'not demonstrated transferable or signoff-quality physical-design improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1859"></span>') == 1
    section = page.split('## iPCL-M: a fast layout metric', 1)[1]
    for phrase in (
        'ASIC physical design', 'gate-level netlist', 'GDS-II', 'routing',
        'wirelength', 'delay', 'slew', 'resistance', 'capacitance',
        'GEOG', 'pre-trained', 'iSTA', '336×', 'held-out',
        'design-rule', 'extraction', 'static-timing', 'signoff',
        '10.49%', '13.03%', '14.85%', '10.51%', '6.46%',
        'not demonstrated transferable or signoff-quality physical-design improvement',
    ):
        assert phrase in section


def test_expert_rl_placement_explanation_separates_reward_learning_from_physical_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2560']
    assert 'latent reward' in row['method_or_artifact']
    assert 'not demonstrated expert parity' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2560"></span>') == 1
    section = page.split('## Expert-level RL placement:', 1)[1]
    for phrase in (
        'Placement', 'cells', 'macros', 'routing', 'wirelength', 'density',
        'congestion', 'timing', 'RL', 'expert layouts', 'trajectories',
        'demonstrations', 'preferences', 'reward', 'wirelength-only RL',
        'held-out', 'PDK', 'parasitic', 'signoff', 'single design',
        'not demonstrated expert parity',
    ):
        assert phrase in section


def test_practice_informed_macro_placement_separates_action_masks_from_timing_closure() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research365']
    assert 'practice-informed reinforcement-learning macro-placement framework' in row['method_or_artifact']
    assert 'not demonstrated portable expert parity' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research365"></span>') == 1
    section = page.split('## Practice-informed macro placement:', 1)[1].split('## Expert-level RL placement:', 1)[0]
    for phrase in (
        'macro placement', 'RL', 'action mask', 'peripheral', 'dead-space', 'proximal',
        'hierarchy', 'footprint', 'clusters', 'tiling', 'compaction', 'routing',
        'pin access', 'congestion', 'extraction', 'static timing', 'WNS', 'TNS',
        '25.37%', '39.51%', 'commercial', 'Hold out', 'PDK',
        'not demonstrated portable expert parity',
    ):
        assert phrase in section


def test_slicemoe_explanation_separates_cache_miss_savings_from_end_to_end_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1582']
    assert 'Dynamic Bit-Sliced Caching' in row['method_or_artifact']
    assert 'not demonstrated universal end-to-end on-device efficiency' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1582"></span>') == 1
    section = page.split('## SliceMoE: bit-slice caching', 1)[1].split('## LOHA:', 1)[0]
    for phrase in (
        'MoE', 'expert', 'cache', 'DBSC', 'AMAT', 'PCW', 'precision', 'miss rate',
        'prefill', 'decode', 'latency', 'energy', 'memory', 'bandwidth', 'quality',
        'DeepSeek-V2-Lite', 'Qwen1.5-MoE-A2.7B', '2.37×', '2.85×', '1.81×', '1.64×',
        'not demonstrated universal end-to-end on-device efficiency'
    ):
        assert phrase in section


def test_weaver_explanation_separates_expert_overlap_from_quality_and_tail_latency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2313']
    assert 'Score-stratified expert scheduling' in row['method_or_artifact']
    assert 'not demonstrated robust quality-preserving speedup' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2313"></span>') == 1
    section = page.split('## Weaver: score-stratified MoE', 1)[1].split('## Phantom Walk:', 1)[0]
    for phrase in (
        'MoE', 'expert', 'CPU', 'GPU', 'attention', 'approximation', 'routing',
        'prefetching', 'overlap', 'bandwidth', 'p50', 'p95', 'p99', 'throughput',
        '1.47–3.58×', 'not demonstrated robust quality-preserving speedup',
    ):
        assert phrase in section


def test_maple_explanation_separates_transfer_aware_mapping_from_ndp_execution() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1449']
    assert 'Address-mapping-based mapping exploration' in row['method_or_artifact']
    assert 'not demonstrated portable end-to-end edge-LLM improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1449"></span>') == 1
    section = page.split('## Maple: data-transfer-aware NDP', 1)[1].split('## Phantom Walk:', 1)[0]
    for phrase in (
        'NDP', 'Near-DRAM', 'tensor', 'partition', 'transfer', 'bank', 'queue',
        'synchronization', 'DMA', 'coherence', 'bandwidth', 'energy', '3.34×',
        '1.49×', 'model-quality', 'not demonstrated portable end-to-end edge-LLM improvement',
    ):
        assert phrase in section


def test_phantom_walk_explanation_separates_translation_shortcut_from_coherence_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1938']
    assert 'Proactive dissemination of translations after migration' in row['method_or_artifact']
    assert 'not demonstrated universal multi-GPU improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1938"></span>') == 1
    section = page.split('## Phantom Walk: disseminating translations', 1)[1].split('## LOHA:', 1)[0]
    for phrase in (
        'Unified virtual memory', 'GPU', 'migration', 'PTE', 'TLB', 'page-table',
        'M-miss', 'dissemination', 'invalidation', 'coherence', 'stale', 'metadata',
        'interconnect', 'contention', 'tail latency', '44.37%',
            'not demonstrated universal multi-GPU performance improvement'
    ):
        assert phrase in section


def test_gtx_explanation_separates_parasitic_speed_from_signoff_fidelity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2177']
    assert 'Graph-transformer parasitic surrogate' in row['method_or_artifact']
    assert 'not demonstrated signoff-grade extraction' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2177"></span>') == 1
    section = page.split('## GTX: fast parasitic prediction', 1)[1].split('## UNCHARTED:', 1)[0]
    for phrase in (
        'parasitic', 'analog', 'layout', 'resistance', 'capacitance', 'coupling',
        'graph neural', 'attention', 'PEX', 'PDK', 'corner', 'signoff', 'bandwidth',
        'phase margin', '232.7×', '8.4×', 'not demonstrated signoff-grade extraction'
    ):
        assert phrase in section


def test_pim_busy_explanation_separates_component_speedups_from_full_system_throughput() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1322']
    assert 'Co-designed Channel-Level Burst operand generation' in row['method_or_artifact']
    assert 'not demonstrated hardware-level full throughput' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1322"></span>') == 1
    section = page.split('## Keeping PIM Busy:', 1)[1].split('## LOHA:', 1)[0]
    for phrase in (
        'PIM', 'host', 'memory', 'CL', 'PDMA', 'multi-batch', 'channel', 'bank',
        'request', 'queue', 'synchronization', 'utilization', 'PCIe', 'emulator',
        'GEMM', 'LLM', '6.55%', '9.10×', '29.6×', '102.4×', '145.8×',
        'not demonstrated hardware-level full-throughput'
    ):
        assert phrase in section


def test_pimony_explanation_separates_concurrent_access_from_minimal_interference() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1909']
    assert 'Asynchronous interruptible PIM execution' in row['method_or_artifact']
    assert 'not demonstrated minimal interference' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1909"></span>') == 1
    section = page.split('## PIMony: concurrent PIM and host access', 1)[1].split('## LOHA:', 1)[0]
    for phrase in (
        'PIM', 'DRAM', 'host', 'LLM', 'interrupt', 'preemptible', 'DPSA', 'dual-row',
        'bank', 'channel', 'ordering', 'coherence', 'ECC', 'interference', 'tail',
        'timing', 'energy', 'area', 'not demonstrated minimal interference'
    ):
        assert phrase in section


def test_dart_explanation_separates_shared_execution_from_event_semantic_equivalence() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2011']
    assert 'DAG-driven RTL intermediate representation' in row['method_or_artifact']
    assert 'not demonstrated event-semantic equivalence' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2011"></span>') == 1
    section = page.split('## Dart: shared RTL computation', 1)[1].split('## A comparison that explains', 1)[0]
    for phrase in (
        'RTL', 'DAG', 'stimuli', 'sub-DAG', 'state', 'event', 'delta cycles',
        'nonblocking', 'X/Z', 'waveform', 'debug', 'Verilator', 'RTLflow',
        '136.7×', '4.1×', 'not demonstrated event-semantic equivalence'
    ):
        assert phrase in section


def test_vera_explanation_separates_drift_compensation_from_ten_year_device_resilience() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2298']
    assert 'Lightweight vector compensation' in row['method_or_artifact']
    assert 'not demonstrated ten-year device retention' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/analog-calibration-and-modeling.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2298"></span>') == 1
    section = page.split('## VeRA+: a compact drift compensator', 1)[1].split('## One week measured', 1)[0]
    for phrase in (
        'RRAM', 'in-memory', 'conductance', 'drift', 'vectors', 'scheduling', '1T1R',
        'ADC/DAC', 'temperature', 'variation', 'endurance', 'retraining', 'calibration',
        '99.77%', 'three orders', 'one-week', 'ten years',
        'not demonstrated ten-year device retention'
    ):
        assert phrase in section


def test_voyager_explanation_separates_configurability_from_tapeout_readiness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2884']
    assert 'Configurable HLS accelerator generator' in row['method_or_artifact']
    assert 'not demonstrated tapeout readiness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2884"></span>') == 1
    section = page.split('## Voyager: configurable accelerator generation', 1)[1].split('## UNCHARTED:', 1)[0]
    for phrase in (
        'HLS', 'DNN', 'accelerator', 'compiler', 'datatype', 'quantization', 'PyTorch',
        'tiling', 'synthesis', 'PPA', 'timing', 'signoff', 'utilization', '99.8%',
        '61%', '56%', 'tapeout', 'not demonstrated tapeout readiness'
    ):
        assert phrase in section


def test_rm_cima_explanation_separates_analog_control_speed_from_closed_loop_safety() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1233']
    assert 'Reinforcement learning and model predictive control combined' in row['method_or_artifact']
    assert 'not demonstrated robust UAV flight performance' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/analog-compute-in-memory.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1233"></span>') == 1
    section = page.split('## RM-CIMA: analog control speed', 1)[1].split('## 3D-VRRAM LUT-CiM:', 1)[0]
    for phrase in (
        'UAV', 'reinforcement learning', 'model predictive control', 'analog', 'CIM',
        'wind', 'stability', 'trajectory error', 'ADC/DAC', 'calibration', 'energy',
        '7.9×', '2995.6×', '983.1×', 'not demonstrated robust UAV flight performance',
    ):
        assert phrase in section


def test_analog_flow_explanation_separates_continuous_ode_execution_from_physical_fidelity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1016']
    assert 'Flow-matching MLP-Mixer co-designed' in row['method_or_artifact']
    assert 'not demonstrated physical-solver equivalence' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/neuromorphic-quantum-and-non-von-neumann.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1016"></span>') == 1
    section = page.split('<span id="explanation-dac-2026-research1016"></span>', 1)[1].split('## Optical computation', 1)[0]
    for phrase in (
        'flow generation', 'MLP-Mixer', 'RRAM', 'continuous-time', 'neural ODE',
        'Flow matching', 'physical time', 'generation progress', 'circuit time',
        'conversion', 'noise-aware', 'temperature', 'diversity', 'A100',
        '98.24%', '99.99%', 'not automatically solving the physical equations'
    ):
        assert phrase in section


def test_ai_sar_explanation_separates_graph_optimization_from_end_to_end_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1382']
    assert 'pseudo-transposition operators' in row['method_or_artifact']
    assert 'not demonstrated quality-preserving end-to-end AI+SAR acceleration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/signal-processing-and-sensing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1382"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1382)' in page
    section = page.split('<span id="explanation-dac-2026-research1382"></span>', 1)[1].split('## Numerical equivalence', 1)[0]
    for phrase in (
        'Synthetic-aperture radar', 'SAR', 'echo data', 'PyTorch', 'LiteRT',
        'pseudo-transposition', 'reverse-order', 'FFT', 'tensor shapes',
        'signal fidelity', 'end-to-end', 'memory traffic', '3.45x',
        'not demonstrated quality-preserving end-to-end AI+SAR acceleration',
    ):
        assert phrase in section


def test_hybrid_pim_explanation_separates_dataflow_search_from_llm_system_efficiency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2432']
    assert 'NSGA-II-based multi-objective dataflow-space exploration' in row['method_or_artifact']
    assert 'not demonstrated quality-preserving, hardware-validated end-to-end LLM efficiency' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2432"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2432)' in page
    section = page.split('<span id="explanation-dac-2026-research2432"></span>', 1)[1].split('## COSM:', 1)[0]
    for phrase in (
        'LLM inference', 'DRAM', 'SOT-MRAM', 'NPU', 'PIM', 'dataflow',
        'NSGA-II', 'numerical', 'KV-cache', 'contention', 'p50/p95/p99',
        'Pareto front', '8.72×', '11.74×', '6.24×', '7.76×',
        'not demonstrated quality-preserving, hardware-validated end-to-end LLM efficiency',
    ):
        assert phrase in section


def test_nash_explanation_separates_shared_memory_redirection_from_gpu_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2489']
    assert 'Source Location Table (SLT)' in row['method_or_artifact']
    assert 'not demonstrated cross-GPU, kernel-general or end-to-end AI acceleration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2489"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2489)' in page
    section = page.split('<span id="explanation-dac-2026-research2489"></span>', 1)[1].split('## COSM:', 1)[0]
    for phrase in (
        'GPU AI kernels', 'shared memory', 'global memory', 'neighboring SMs',
        'Source Location Table', 'SLT', 'synchronization', 'false hits',
        'occupancy', 'GEMM', 'attention', 'cycle-accurate simulation',
        '60.2%', '18.3%', '9.8%', '25.3%',
        'not demonstrated cross-GPU, kernel-general or end-to-end AI acceleration',
    ):
        assert phrase in section


def test_gwrite_explanation_separates_replication_offload_from_consistency_and_recovery() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research444']
    assert 'GWrite' in row['method_or_artifact']
    assert 'not demonstrated durable, low-tail-latency distributed-memory scaling' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research444"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research444)' in page
    section = page.split('<span id="explanation-dac-2026-research444"></span>', 1)[1].split('<span id="explanation-dac-2026-research651"></span>', 1)[0]
    for phrase in (
        'Disaggregated memory', 'replication', 'RDMA', 'GWrite', 'GWrap',
        'memory-side RNICs', 'one-sided', 'durability', 'consistency',
        'crash', 'fault', 'p50/p95/p99', '2.18×', '46.7%', '19.7%',
        'not demonstrated durable, low-tail-latency distributed-memory scaling',
    ):
        assert phrase in section


def test_sdm_explanation_separates_soft_sigmoid_tolerance_from_calibrated_edge_efficiency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1308']
    assert 'one-ferroelectric-transistor (1-FeFET) analog content-addressable memory' in row['method_or_artifact']
    assert 'not demonstrated calibrated, process-robust or end-to-end edge efficiency' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/analog-compute-in-memory.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1308"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1308)' in page
    section = page.split('<span id="explanation-dac-2026-research1308"></span>', 1)[1].split('## HP-CIM:', 1)[0]
    for phrase in (
        'soft decision', 'sigmoid', '1-FeFET', 'analog', 'CAM', 'FeFET',
        'calibration', 'device-to-model', '40 mV', 'MNIST', 'decision tree',
        'random forest', '0.54%', '43.86%', '16.06%', 'energy', 'area',
        'not demonstrated calibrated, process-robust or end-to-end edge efficiency',
    ):
        assert phrase in section


def test_hp_cim_explanation_separates_topk_prediction_from_transformer_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2330']
    assert 'hybrid ReRAM–SRAM CIM transformer accelerator' in row['method_or_artifact']
    assert 'not demonstrated quality-preserving' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/analog-compute-in-memory.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2330"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2330)' in page
    section = page.split('## HP-CIM: attention sparsity', 1)[1].split('## HP-CIM: deciding what to skip', 1)[0]
    for phrase in (
        'attention', 'query', 'keys', 'Top-K', 'ReRAM', 'SRAM', 'CIM', 'hash',
        'CAM', 'K-winner', 'softmax', 'false-negative', 'perplexity', 'quality',
        'variation', 'drift', 'ADC/DAC', 'calibration', 'energy/token', 'endurance',
        '9.05–310.04×', '2.48–16.93×', 'not demonstrated quality-preserving',
    ):
        assert phrase in section


def test_reflectbench_explanation_separates_testbench_generation_from_oracle_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1858']
    assert 'ReflectBench' in row['method_or_artifact']
    assert 'not demonstrated reduction in escaped hardware bugs' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1858"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1858)' in page
    section = page.split('<span id="explanation-dac-2026-research1858"></span>', 1)[1].split('## Dart:', 1)[0]
    for phrase in (
        'system-level verification', 'testbench', 'ReflectBench', 'consensus',
        'self-reflection', 'Self-Reflective Domain Knowledge Mining',
        'ReflectVDB', '53', 'oracle', 'false-positive', 'coverage',
        'seeded faults', 'human', 'ConfiBench', '7.6%', '4.5%', '3.8%', '1.2%',
        'not demonstrated reduction in escaped hardware bugs',
    ):
        assert phrase in section


def test_eastpcg_explanation_separates_sparsification_from_solver_validity_and_total_cost() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2131']
    assert 'neural-network-powered self-tuning preconditioned conjugate-gradient' in row['method_or_artifact']
    assert 'not demonstrated solver correctness, general convergence or faster end-to-end circuit simulation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/simulation-and-numerical-methods.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2131"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2131)' in page
    section = page.split('<span id="explanation-dac-2026-research2131"></span>', 1)[1].split('This single record motivates', 1)[0]
    for phrase in (
        'Circuit simulation', 'linear system', 'sparse matrix', 'preconditioner',
        'PCG', 'spectral-probability', 'neural', 'symmetric positive definite',
        'residual', 'b - A x', 'multiple right-hand sides', 'ill-conditioned',
        'setup', 'fallback', 'p50/p95/p99', 'not demonstrated solver correctness',
    ):
        assert phrase in section


def test_pareto_dag_explanation_separates_nondominance_from_deadline_guarantees() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2360']
    assert 'Pareto-prompted metaheuristic' in row['method_or_artifact']
    assert 'not demonstrated probabilistic deadline guarantees' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/real-time-and-networked-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2360"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2360)' in page
    section = page.split('<span id="explanation-dac-2026-research2360"></span>', 1)[1].split('## Cause-effect chains:', 1)[0]
    for phrase in (
        'automotive', 'sensor-to-actuator', 'DAG', 'mapping', 'offset',
        'Pareto', 'metaheuristic', 'LLM', 'deadline', 'resource',
        'p50/p95/p99/p99.9', 'calibrat', 'Orin-N', '12%', '15%',
        'not demonstrated probabilistic deadline guarantees',
    ):
        assert phrase in section


def test_leap_explanation_separates_toggle_prediction_from_power_calibration() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research906']
    assert 'linear-complexity graph transformer' in row['method_or_artifact']
    assert 'not demonstrated transferable signoff-quality power analysis' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research906"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research906)' in page
    section = page.split('<span id="explanation-dac-2026-research906"></span>', 1)[1].split('## G-Power:', 1)[0]
    for phrase in (
        'toggle prediction', 'per-cycle', 'graph transformer', 'self-supervised',
        'LEAP-Power', 'post-synthesis', 'PR-AUC', 'power calibration',
        'MAPE', 'rare', 'clock', 'layout', 'parasitic', 'transfer',
        '7.6×', '0.99', '4.55%', '5.3×',
        'not demonstrated transferable signoff-quality power analysis',
    ):
        assert phrase in section


def test_hyspecpro_explanation_separates_spectral_search_from_partition_validity_and_scaling() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2694']
    assert 'bipartite Laplacian' in row['method_or_artifact']
    assert 'not demonstrated universally scalable, weighted/multiway or downstream-optimal VLSI partitioning' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/graph-and-hypergraph-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2694"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2694)' in page
    section = page.split('<span id="explanation-dac-2026-research2694"></span>', 1)[1].split('## HyperEFs:', 1)[0]
    for phrase in (
        'hypergraph', 'VLSI', 'bipartite', 'Laplacian', 'spectral', 'projection',
        'eigenvectors', 'Lanczos', 'GPU', 'A100', 'balance', 'cut',
        'two-group', 'unit-weight', 'linear', 'weighted', 'multiway',
        'downstream', 'not demonstrated universally scalable, weighted/multiway or downstream-optimal VLSI partitioning',
    ):
        assert phrase in section


def test_hyperefs_explanation_separates_adaptive_sampling_from_resistance_and_cut_fidelity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2887']
    assert 'HyperEFs adaptively samples between star and clique expansions' in row['method_or_artifact']
    assert 'not demonstrated unbiased, universally scalable estimation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/graph-and-hypergraph-optimization.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2887"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research2887)' in page
    section = page.split('<span id="explanation-dac-2026-research2887"></span>', 1)[1].split('## What can be concluded', 1)[0]
    for phrase in (
        'Effective resistance', 'hyperedge', 'clique', 'star', '4,950',
            'Krylov', 'sampling', 'bias', 'variance', 'confidence',
            'CUDA', 'HyperEF 2.0', 'Titan23', 'cut', 'memory', '100×',
        'not demonstrated unbiased, universally scalable estimation',
    ):
        assert phrase in section


def test_etherssd_explanation_separates_in_storage_query_speed_from_proof_and_trust_correctness() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research297']
    assert 'computational storage devices' in row['method_or_artifact']
    assert 'not demonstrated complete blockchain-query correctness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/storage-and-data-movement.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research297"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research297)' in page
    section = page.split('<span id="explanation-dac-2026-research297"></span>', 1)[1].split('## How to compare complete requests', 1)[0]
    for phrase in (
        'authenticated', 'Ethereum', 'Merkle', 'CSD', 'host', 'proof', 'snapshot',
        'root', 'query semantics', 'trust boundary', 'firmware', 'replay',
        'p50/p95/p99', 'wear', 'energy', 'not demonstrated complete blockchain-query correctness',
    ):
        assert phrase in section


def test_trimoe_explanation_separates_three_way_offload_from_moe_correctness_and_tails() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research368']
    assert 'GPU–AMX-enabled CPU–DIMM-NDP architecture' in row['method_or_artifact']
    assert 'not demonstrated quality-preserving universal throughput improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research368"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research368)' in page
    section = page.split('<span id="explanation-dac-2026-research368"></span>', 1)[1].split('## CacheParallel:', 1)[0]
    for phrase in (
        'Mixture-of-Experts', 'hot', 'warm', 'cold', 'GPU', 'AMX', 'DIMM-NDP',
        'routing', 'logits', 'migration', 'relayout', 'coherence', 'NDP',
        'p50/p95/p99', 'prediction', '2.83×',
        'not demonstrated quality-preserving universal throughput improvement',
    ):
        assert phrase in section


def test_crystal_kv_explanation_separates_answer_aware_eviction_from_reasoning_fidelity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research375']
    assert 'answer-first principle' in row['method_or_artifact']
    assert 'not demonstrated reasoning-faithful' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research375"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research375)' in page
    section = page.split('<span id="explanation-dac-2026-research375"></span>', 1)[1].split('## Expertflow:', 1)[0]
    for phrase in (
        'Chain-of-thought', 'CoT', 'KV', 'answer-first', 'SlipKV', 'CrystalKV',
        'Least Recently Frequently Used', 'evict', 'reasoning', 'logit',
        'recompute', 'p50/p95/p99', 'inter-token', 'position', 'long',
        'not demonstrated reasoning-faithful',
    ):
        assert phrase in section


def test_cause_effect_explanation_separates_timing_anomaly_elimination_from_deadline_guarantees() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research378']
    assert 'Deterministic Data Flow (DDF)' in row['method_or_artifact']
    assert 'not demonstrated vehicle-level real-time safety' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/real-time-and-networked-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research378"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research378)' in page
    section = page.split('<span id="explanation-dac-2026-research378"></span>', 1)[1].split('## What the three studies establish together', 1)[0]
    for phrase in (
        'cause-effect', 'producer', 'consumer', 'timing anomaly', 'DDF',
        'buffers', 'one core', 'fixed-priority', 'WCET', 'worst-case',
        'Theorem 5.4', 'multicore', 'networked', 'jitter', 'deadline',
        'not demonstrated vehicle-level real-time safety',
    ):
        assert phrase in section


def test_fuse_tcad_explanation_separates_diffusion_surrogate_speed_from_physical_fidelity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1156']
    assert 'conditional diffusion surrogate' in row['method_or_artifact']
    assert 'not demonstrated PDE-faithful, process-transferable or design-validated near-real-time TCAD' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1156"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1156)' in page
    section = page.split('<span id="explanation-dac-2026-research1156"></span>', 1)[1].split('## LEAP:', 1)[0]
    for phrase in (
        'TCAD', 'PDE', 'device', 'spatial fields', 'diffusion', 'joint',
        'geometry', 'bias', 'Sobolev', 'junction', 'gradient', 'residual',
        'conservation', '20%', '30×', '0.8%', 'transfer', 'extrapolation',
        'not demonstrated PDE-faithful, process-transferable or design-validated near-real-time TCAD',
    ):
        assert phrase in section


def test_lightningfno_explanation_separates_fno_speed_from_photonic_fidelity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2358']
    assert 'inverse Fourier Neural Operator' in row['method_or_artifact']
    assert 'not demonstrated scalable process transfer' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/photonic-and-optical-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2358"></span>') == 1
    section = page.split('## LightningFNO:', 1)[1].split('## Light-Bound Transformers:', 1)[0]
    for phrase in (
        'Fourier neural operators', 'inverse', 'forward', 'topolog', 'Maxwell',
        '4×4', '3×3', 'RMSE', '0.043', 'MNIST', '97.69%', 'fabricated',
        'wavelength', 'polarization', 'feature', 'spacing', 'alignment',
        'calibration', '1,245,550×', 'not demonstrated scalable process transfer',
    ):
        assert phrase in section


def test_sparsee_explanation_separates_encrypted_sparsity_from_privacy_and_fhe_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2265']
    assert 'secure Scatter-Gather-Apply' in row['method_or_artifact']
    assert 'not demonstrated security preservation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/privacy-preserving-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2265"></span>') == 1
    section = page.split('## Sparsee:', 1)[1].split('## Memory is a constraint', 1)[0]
    for phrase in (
        'FHE', 'ciphertext', 'sparsity', 'Scatter-Gather-Apply', 'encrypted indices',
        'Benes', 'Radix-k', 'selector', 'privacy', 'adversary', 'leakage',
        'noise', 'modulus', 'key switching', 'packing', 'decryption',
        '401.8×', '2594.3×', 'not demonstrated security preservation',
    ):
        assert phrase in section


def test_mach_explanation_separates_memory_search_from_fhe_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research897']
    assert 'memory-aware design framework' in row['method_or_artifact']
    assert 'not demonstrated secure, accuracy-preserving end-to-end improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/privacy-preserving-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research897"></span>') == 1
    section = page.split('## MACH:', 1)[1].split('## Less interaction', 1)[0]
    for phrase in (
        'MACH', 'homomorphically encrypted', 'memory', 'static model',
        'latency', 'cryptographic', 'bootstrapping', 'encoding', 'GPU',
        'FHE', 'security', 'accuracy', 'noise', 'packing', 'ResNet-20',
        'ResNet-18', '4.97×', '91.88%', '128-bit', 'RTX 4060 Ti', '16 GB',
        'transfers', 'energy', 'not demonstrated secure, accuracy-preserving end-to-end improvement',
    ):
        assert phrase in section


def test_tami_mpc_explanation_separates_round_reduction_from_tee_security() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research989']
    assert 'one interaction round' in row['method_or_artifact']
    assert 'not demonstrated security-preserving deployment' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/privacy-preserving-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research989"></span>') == 1
    section = page.split('## TAMI-MPC:', 1)[1].split('## What would make', 1)[0]
    for phrase in (
        'TAMI-MPC', 'TEE', 'MPC', 'nonlinear', 'comparison', 'merge',
        'one interaction round', 'synchronized seeds', 'oblivious transfer',
        'correlated randomness', 'streaming', 'log(n)', '4.86×', '7.44×',
        'ResNet-50', 'bert-base', 'communication', 'bytes', 'preprocessing',
        'attestation', 'replay', 'side channels', 'accuracy', 'security proof',
        'not demonstrated security-preserving deployment',
    ):
        assert phrase in section


def test_artemis_explanation_separates_rl_event_search_from_ssd_test_coverage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1138']
    assert 'reinforcement learning' in row['method_or_artifact']
    assert 'not demonstrated device-agnostic verification coverage' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1138"></span>') == 1
    section = page.split('## ARTEMIS:', 1)[1].split('<span id="explanation-dac-2026-research358"></span>', 1)[0]
    for phrase in (
        'ARTEMIS', 'SSD', 'reinforcement learning', 'test-case', 'ensemble',
        'heterogeneous', 'non-stationary', 'Meta Garbage Collection',
        'User Garbage Collection', 'oracle', 'blocking', 'timeout',
        'Deduplicate', 'Hold out', 'firmware', 'NAND', 'coverage',
        'false positives', 'test budget', 'not demonstrated device-agnostic verification coverage',
    ):
        assert phrase in section


def test_wsc_cost_explanation_separates_cost_dimensions_from_yield_and_system_economics() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2230']
    assert 'unified model with a horizontal dimension' in row['method_or_artifact']
    assert 'not demonstrated accurate delivered cost' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/wafer-scale-and-heterogeneous-integration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2230"></span>') == 1
    section = page.split('## WSC-Cost:', 1)[1].split('## Connecting performance', 1)[0]
    for phrase in (
        'mask-stitching', 'metal layers', 'interposer', 'assembly', 'wafer',
        'yield', 'defect', 'repair', 'disabled', 'scrap', 'cost boundary',
        'production volume', 'calibrat', 'prototype', 'sensitivity',
        'throughput', 'bandwidth', 'thermal', 'not demonstrated accurate delivered cost',
    ):
        assert phrase in section


def test_pmtpa_explanation_separates_replica_speed_from_optimization_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2159']
    assert 'elastic replicas' in row['method_or_artifact']
    assert 'not demonstrated optimum-finding probability' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/emerging-and-nonvon-neumann-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2159"></span>') == 1
    section = page.split('## PMTPA:', 1)[1].split('## EHPC:', 1)[0]
    for phrase in (
        'Ising', 'replica', 'tempering', 'momentum', 'local-field',
        'time-division', 'pipeline', '2,048', '2–32', 'Max-Cut',
        'image-segmentation', 'accuracy', 'objective', 'penalty', 'feasible',
        'success probability', 'time-to-target', 'FPGA', '17,000×',
        'not demonstrated optimum-finding probability',
    ):
        assert phrase in section


def test_hyperwafer_explanation_separates_communication_mapping_from_spgemm_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2132']
    assert 'weighted hypergraph for multiway row sharing' in row['method_or_artifact']
    assert 'not demonstrated numerical equivalence' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/wafer-scale-and-heterogeneous-integration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2132"></span>') == 1
    section = page.split('## HyperWafer:', 1)[1].split('## WSC-Cost:', 1)[0]
    for phrase in (
        'SpGEMM', 'hypergraph', 'multiway', 'row sharing', 'reduction',
        'partitioning', 'topology-aware', 'wafer', 'congestion', 'routing',
        'sparse', 'precision', 'residuals', 'messages', 'link utilization',
        'p50/p95/p99', '979.97×', '125.23×', '12.14×', '5.14×',
        'fault', 'not demonstrated numerical equivalence',
    ):
        assert phrase in section


def test_openacmv2_explanation_separates_accuracy_budget_from_circuit_variation() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2014']
    assert 'Accuracy-Constrained Co-Optimization' in row['method_or_artifact']
    assert 'not demonstrated application-safe PPA improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/processing-in-memory-and-memory-centric-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2014"></span>') == 1
    section = page.split('## OpenACMv2:', 1)[1].split('## What would establish', 1)[0]
    for phrase in (
        'approximate', 'compute-in-memory', 'accuracy', 'PPA', 'compressors',
        'SRAM', 'GNN', 'surrogate', 'Monte Carlo', 'PVT', 'variation',
        'parasitics', 'yield', 'Pareto', 'FreePDK45', 'OpenROAD',
        'exact', 'uncoupled', 'not demonstrated application-safe PPA improvement',
    ):
        assert phrase in section


def test_aqr_hnsw_explanation_separates_quantized_speed_from_ann_recall() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1629']
    assert 'density-aware adaptive quantization' in row['method_or_artifact']
    assert 'not demonstrated recall-preserving universal QPS' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1629"></span>') == 1
    section = page.split('## AQR-HNSW:', 1)[1].split('## 3D-DuRA:', 1)[0]
    for phrase in (
        'HNSW', 'nearest neighbors', 'quantization', 'density-aware', 're-ranking',
        'SIMD', '16–64', 'distance', 'recall', 'exact search', 'top-k',
        'codebook', 'candidate', 'memory', 'p50/p95/p99', 'updates',
        '4×', '35%', '2.5–3.3×', '98%+', '75%', '5×',
        'not demonstrated recall-preserving universal QPS',
    ):
        assert phrase in section


def test_n3litho_explanation_separates_3d_field_speed_from_printed_pattern_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1622']
    assert 'GPU-accelerated vectorial Abbe solver' in row['method_or_artifact']
    assert 'not demonstrated process-window robustness' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/manufacturing-and-lithography.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1622"></span>') == 1
    section = page.split('## N3Litho:', 1)[1].split('## Forward modeling:', 1)[0]
    for phrase in (
        '3D', 'aerial image', 'vector field', 'vectorial Abbe', 'hash',
        'mask', 'film-stack', 'electromagnetic', 'resist', 'edge-placement',
        'hotspot', 'process transfer', 'focus/dose', 'polarization',
        'uncertainty', 'fallback', 'orders-of-magnitude', 'OPC/ILT',
        'wafer correlation', 'not demonstrated process-window robustness',
    ):
        assert phrase in section


def test_rosa_explanation_separates_optical_mapping_from_device_and_quality_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research160']
    assert 'optical shift-and-add module' in row['method_or_artifact']
    assert 'not demonstrated process-robust' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/photonic-and-optical-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research160"></span>') == 1
    section = page.split('## ROSA:', 1)[1].split('## LightningFNO:', 1)[0]
    for phrase in (
        'microring', 'optical shift-and-add', 'input-', 'weight-stationary',
        'DAC', 'thermal', 'calibrat', 'detuning', 'insertion loss', 'crosstalk',
        '45-nm', '5 GHz', '8-bit', 'EDP', 'DEAP-CNNs', 'CIFAR-10',
        'ResNet18', '1.531', '1.493', '2.48%', '74.8%', '76.5%',
        'not demonstrated process-robust',
    ):
        assert phrase in section


def test_freebit_explanation_separates_low_bit_pim_speed_from_quality_and_path_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research146']
    assert 'LUT-centric architecture for quantized computation' in row['method_or_artifact']
    assert 'not demonstrated accuracy-preserving LLM inference' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/processing-in-memory-and-memory-centric-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research146"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research146)' in page
    section = page.split('## FreeBit:', 1)[1].split('## What the four records', 1)[0]
    for phrase in (
        'quantiz', '1, 2 or 4 bits', 'roofline', 'memory bandwidth', 'PIM',
        'LUT', 'sparsity', 'static/dynamic', 'parallelism', 'perplexity',
        'accuracy', 'activation/KV', 'dequantization', 'ADC/DAC', 'device variation',
        'metadata', 'host/PIM', 'tail latency', '6.7×', 'NVIDIA A100',
        'not demonstrated accuracy-preserving LLM inference',
    ):
        assert phrase in section


def test_adaptive_mac_explanation_separates_voltage_savings_from_timing_and_dnn_reliability() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2364']
    assert 'adaptive MAC with input-dependent width selection' in row['method_or_artifact']
    assert 'not demonstrated reliable end-to-end DNN quality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/reliable-and-efficient-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2364"></span>') == 1
    section = page.split('## What ADA and ADA-Plus demonstrate', 1)[1]
    for phrase in (
        'ADA', 'ADA-Plus', 'adaptive', 'critical path', 'signed 8-bit',
        '24-bit', '28-nm', 'MNIST', 'CIFAR-10', '16.1%', '12.4%',
        '50.89%', '19.35%', 'timing', 'silicon', 'Process, voltage, and temperature',
        'not demonstrated reliable end-to-end DNN quality',
    ):
        assert phrase in section


def test_rangelfs_explanation_separates_range_mapping_from_durable_filesystem_gain() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2637']
    assert 'flexible ranges that map arbitrary-sized file segments' in row['method_or_artifact']
    assert 'not demonstrated durable end-to-end filesystem improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/storage-and-memory-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2637"></span>') == 1
    section = page.split('## RangeLFS: an application update need not fill a file-system block', 1)[1]
    for phrase in (
        'ZNS', 'RangeLFS', 'range', 'B+ tree', 'page cache', 'partial-page',
        'read-modify-write', '6.95×', 'write bandwidth', 'comparable reads',
        'zone', 'write-pointer', 'metadata', 'durability', 'power loss',
        'write amplification', 'not demonstrated durable end-to-end filesystem improvement',
    ):
        assert phrase in section


def test_crystals_small_modulus_explanation_separates_detection_from_security_acceptance() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2780']
    assert 'dual-modulus residue paths exploit pseudo-Mersenne structure' in row['method_or_artifact']
    assert 'not demonstrated security-preserving correction' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/reliable-and-secure-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2780"></span>') == 1
    section = page.split('## What the CRYSTALS paper reports', 1)[1]
    for phrase in (
        'CRYSTALS', 'NTT', 'modular', 'dual-modulus', 'cross-basis',
        'lookup-table', 'Chinese-remainder', 'Artix-7', '55–78%',
        '100%', '99.01%', 'correction', 'fault', 'TMR', 'recomputation',
        'critical path', 'side-channel', 'not demonstrated security-preserving correction',
    ):
        assert phrase in section


def test_ehpc_explanation_separates_fabricated_device_from_modeled_optimization_gain() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2817']
    assert 'heterogeneous probabilistic computation' in row['method_or_artifact']
    assert 'not demonstrated scalable end-to-end time-to-solution' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/emerging-and-nonvon-neumann-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2817"></span>') == 1
    section = page.split('## EHPC: separate a device demonstration', 1)[1].split('## iADS:', 1)[0]
    for phrase in (
        'EHPC', 'volatile', 'RRAM', 'OxRAM', 'Max-Cut', 'fabricated',
        'hardware simulations', 'within one second', '20×', '1,500×',
        '1.7%', 'floorplanning', 'solution quality', 'probability of reaching the target',
        'time-to-target', 'energy-to-target', 'calibration', 'silicon',
        'not demonstrated scalable end-to-end time-to-solution',
    ):
        assert phrase in section


def test_iads_explanation_separates_pbit_noise_generation_from_full_diffusion_gain() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2975']
    assert 'self-compensating voltage-tunable p-bits' in row['method_or_artifact']
    assert 'not demonstrated full-system diffusion acceleration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/emerging-and-nonvon-neumann-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2975"></span>') == 1
    section = page.split('## iADS: a noise source', 1)[1].split('## Compare time to a useful result', 1)[0]
    for phrase in (
        'iADS', 'p-bit', 'Gaussian', 'MNIST', 'CIFAR10', 'CelebA-HQ',
        '256', '1,048,576', 'FID', '9.96', '8×', '143×', 'pseudorandom-number generators',
        'binary', 'continuous', 'calibration', 'correlation', 'variation',
        'fabricated', 'not demonstrated full-system diffusion acceleration',
    ):
        assert phrase in section


def test_light_bound_explanation_separates_noise_robustness_from_photonic_system_efficiency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3237']
    assert 'Chance-Constrained Training' in row['method_or_artifact']
    assert 'not demonstrated full-system optical efficiency' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/photonic-and-optical-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3237"></span>') == 1
    section = page.split("## Light-Bound Transformers: train for the hardware's uncertainty", 1)[1].split('## SP2RINT:', 1)[0]
    for phrase in (
        'attention', 'microring', 'variance', 'Chance-Constrained Training',
        'LayerNorm', 'Gaussian', 'noise injection', 'hardware-in-the-loop',
        '0.05–0.1', 'Tiny-ImageNet', '65.89%', '79.50%', '86.14%',
        'ten noisy inference runs', '70.7×', '116.7×', '61.4 µJ',
        '54.86 µJ', 'calibration', 'optical loss', 'process-robust Transformer deployment',
    ):
        assert phrase in section


def test_page_explanation_separates_pud_circuit_claims_from_fabricated_gemv_system_gain() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research401']
    assert 'mat-level parallelism across sense amplifiers' in row['method_or_artifact']
    assert 'not demonstrated fabricated PAGE deployment' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/processing-in-memory-and-memory-centric-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research401"></span>') == 1
    section = page.split('## PAGE: co-design the DRAM operation', 1)[1].split('CQ-CiM changes embeddings', 1)[0]
    for phrase in (
        'PAGE', 'GEMV', 'LLM', 'mat-level parallelism', 'sense amplifiers',
        'AP-based', 'adder-tree', 'COTS DRAM–FPGA', 'TSMC 16 nm',
        'system simulator', 'activation', 'restore', 'refresh', 'disturbance',
        'numerical representation', 'signedness', '14×', '3.1×', 'throughput',
        'energy', 'fabricated PAGE deployment', 'numerical equivalence',
    ):
        assert phrase in section


def test_cola_explanation_separates_adaptive_ecc_latency_from_nand_reliability() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research607']
    assert 'selects the ECC code length for each write' in row['method_or_artifact']
    assert 'not demonstrated device-measured reliable low-latency SSD reads' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/storage-and-memory-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research607"></span>') == 1
    section = page.split('## COLA: distinguish code length from storage overhead', 1)[1].split('## WILL:', 1)[0]
    for phrase in (
        'COLA', 'ECC', 'codeword', 'Code rate', 'RBER', 'failure-aware',
        'MQSim', 'Alibaba Cloud', '4 KiB', '68.69%', '71%', '99.9th',
            'latency', 'uncorrectable', 'wear', 'retention', 'read-disturb',
            'decode', 'manufactured', 'not demonstrated device-measured reliable low-latency SSD reads',
    ):
        assert phrase in section


def test_will_explanation_separates_invalidation_skipping_from_ssd_endurance() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research931']
    assert 'predicts page invalidation time' in row['method_or_artifact']
    assert 'not demonstrated durable end-to-end SSD improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/storage-and-memory-systems.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research931"></span>') == 1
    section = page.split('## WILL: skip obsolete QLC programming', 1)[1].split('## The longer-term question', 1)[0]
    for phrase in (
        'WILL', 'QLC', 'NAND', 'two-step', 'invalidation', 'lifespan',
        'wordline', 'fine-step', 'read-hot', '10.0%', '5.03%', '15.9%',
        '2.59%', 'prediction', 'remapping', 'garbage collection',
        'power-loss', 'ECC', 'retention', 'wear', 'write amplification',
        'p50/p95/p99', 'endurance', 'not demonstrated durable end-to-end SSD improvement',
    ):
        assert phrase in section


def test_cq_cim_explanation_separates_embedding_shaping_from_retrieval_quality() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research752']
    assert 'jointly performs compression and quantization' in row['method_or_artifact']
    assert 'not demonstrated robust CiM retrieval quality' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/processing-in-memory-and-memory-centric-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research752"></span>') == 1
    section = page.split('## CQ-CiM: shape the representation', 1)[1].split('## What would establish', 1)[0]
    for phrase in (
        'embedding', 'RAG', 'representation gap', 'compression', 'quantiz',
        'SRAM', 'ReRAM', 'FeFET', '2-bit', '512×512', 'nearest-neighbor',
        'top-k', 'recall', 'NDCG', 'MRR', 'ADC/DAC', 'variation', 'IR drop',
        'calibration', 'index', 'device', 'not demonstrated robust CiM retrieval quality',
    ):
        assert phrase in section


def test_sp2rint_explanation_separates_progressive_inverse_training_from_physical_validation() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research760']
    assert 'banded trainable transfer matrices' in row['method_or_artifact']
    assert 'not demonstrated reproducible training superiority' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/photonic-and-optical-compute.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research760"></span>') == 1
    section = page.split('## SP2RINT: repeatedly bring learned responses', 1)[1].split('## What these papers suggest', 1)[0]
    for phrase in (
        'metasurface', 'PDE', 'banded', 'transfer matrices', 'progressive',
        'adjoint', 'inverse design', 'local patches', '17-element',
        'Fashion-MNIST', 'SVHN', '88.44%', '81.61%', 'Darcy-flow',
        '63.88%', '1825×', '178 hours', 'simulation-in-the-loop',
        'projection', 'approximation', 'fabricated', 'manufacturing',
        'not demonstrated reproducible training superiority',
    ):
        assert phrase in section


def test_dr_opc_explanation_separates_differentiable_rasterization_from_wafer_validated_opc() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research827']
    assert 'fully differentiable OPC pipeline using differentiable rasterization' in row['method_or_artifact']
    assert 'not demonstrated signoff-quality or wafer-validated lithographic improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/manufacturing-and-lithography.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research827"></span>') == 1
    section = page.split('## Inverse optimization: what DR. OPC proposes', 1)[1].split('## Forward modeling:', 1)[0]
    for phrase in (
        'DR. OPC', 'differentiable', 'rasterization', 'curvilinear', 'multi-segment',
        'process-window', 'mask-rule', 'L2', 'PVB', 'EPE', '52.1%', '16.0%',
        '21.1%', 'lithography', 'resist', 'focus/dose', 'writer', 'printability',
        'wafer', 'not demonstrated signoff-quality or wafer-validated lithographic improvement',
    ):
        assert phrase in section


def test_gpu_lu_explanation_separates_kernel_speed_from_numerical_and_spice_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1196']
    assert 'computation-balanced dependency-level partitioning' in row['method_or_artifact']
    assert 'not demonstrated numerical equivalence' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/scientific-and-engineering-computing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1196"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1196)' in page
    section = page.split('## Levelized GPU LU:', 1)[1].split('## Factorization prepares', 1)[0]
    for phrase in (
        'SPICE', 'sparse', 'LU', 'symbolic', 'ordering', 'pivoting', 'fill-in',
        'dependency-level', 'GPU', 'precision', 'residual', 'forward/backward',
        'ill-conditioned', 'triangular solves', 'memory', '2.1×', '5.2×',
        'GLU3.0', 'PARDISO', 'Ngspice', 'Newton', 'transient',
        'not demonstrated numerical equivalence',
    ):
        assert phrase in section


def test_rtl_sequencer_explanation_separates_sequence_encoding_from_timing_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research883']
    assert 'RTL-Sequencer linearizes RTL logic cones by breadth-first traversal' in row['method_or_artifact']
    assert 'not demonstrated scalable timing accuracy' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research883"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research883)' in page
    section = page.split('## RTL-Sequencer:', 1)[1].split('## Stochastic Diffusion Prior:', 1)[0]
    for phrase in (
        'RTL timing', 'logic cones', 'breadth-first', 'sequence models',
        'sequence shuffling', 'bidirectional', 'differentiable',
        'graph-sequence', 'synthesis', 'static-timing', 'fanout',
        'reconvergent', 'slack', 'critical-path', 'STA', 'Hold out',
        'technology', 'timing closure', 'not demonstrated scalable timing accuracy',
    ):
        assert phrase in section


def test_sdp_explanation_separates_expert_prior_from_sizing_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research739']
    assert 'Stochastic Diffusion Prior (SDP)' in row['method_or_artifact']
    assert 'not demonstrated universal sample efficiency' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research739"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research739)' in page
    section = page.split('## Stochastic Diffusion Prior:', 1)[1].split('## Xsearch:', 1)[0]
    for phrase in (
        'analog', 'transistor sizing', 'gm/ID', 'diffusion prior',
        'mutual-information', 'simulation', 'DC', 'AC', 'transient',
        'mismatch', 'stability', 'gain', 'bandwidth', 'noise', 'linearity',
        'power', 'area', 'Bayesian Optimization', 'technology nodes',
        '92.3×', '27.9×', '2.0×', '1.5×',
        'not demonstrated universal sample efficiency',
    ):
        assert phrase in section


def test_xsearch_explanation_separates_multifidelity_search_from_decision_fidelity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1186']
    assert 'multi-fidelity Bayesian optimization' in row['method_or_artifact']
    assert 'not demonstrated quantitative superiority' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1186"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1186)' in page
    section = page.split('## Xsearch: multi-fidelity exploration', 1)[1].split('## FUSE-TCAD:', 1)[0]
    for phrase in (
        'microarchitecture', 'design-space', 'Bayesian', 'low-fidelity',
        'high-fidelity', 'cross-evaluation', 'calibrat', 'uncertainty',
        'rank', 'constraint', 'XiangShan', 'objective', 'acquisition',
        'budget', 'convergence', 'not demonstrated quantitative superiority',
    ):
        assert phrase in section


def test_datapath_gating_explanation_separates_odc_safety_from_power_prediction() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research3154']
    assert 'SAT-based technique to compute valid observability-don\'t-care conditions' in row['method_or_artifact']
    assert 'not demonstrated signoff-power accuracy' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/learned-design-space-exploration.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research3154"></span>') == 1
    section = page.split('## Automated datapath gating:', 1)[1].split('## G-Power:', 1)[0]
    for phrase in (
        'Datapath gating', 'observability', 'ODC', 'SAT', 'enable', 'equivalence',
        'reset', 'clock', 'dynamic', 'power', 'post-place-and-route', 'timing',
        'area', 'prediction', 'calibrat', 'signoff', '-1%', 'not demonstrated signoff-power accuracy',
    ):
        assert phrase in section


def test_escape_explanation_separates_activity_shaping_from_fault_coverage() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1180']
    assert 'programmable low-power LBIST architecture' in row['method_or_artifact']
    assert 'not demonstrated quantitative fault-coverage preservation' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1180"></span>') == 1
    assert '[Read the step-by-step explanation](#explanation-dac-2026-research1180)' in page
    section = page.split('## ESCAPE: activity shaping', 1)[1].split('## TOB-Sched:', 1)[0]
    for phrase in (
        'LBIST', 'scan chain', 'fault', 'activity', 'probability', 'hold registers',
        'two-dimensional AND-gate', 'phase shifter', 'coverage', 'peak', 'average',
        'test-time', 'area', 'timing', 'tester', 'silicon',
        'not demonstrated quantitative fault-coverage preservation',
    ):
        assert phrase in section


def test_prelude_explanation_separates_snapshot_replay_from_state_fidelity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2085']
    assert 'snapshot-based debugging framework' in row['method_or_artifact']
    assert 'not demonstrated universal cycle-accurate reconstruction' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/simulation-emulation-and-testing.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2085"></span>') == 1
    section = page.split('## Prelude: replayed state', 1)[1].split('## GPU-Fuzz changes', 1)[0]
    for phrase in (
        'FPGA', 'processor', 'snapshot', 'architectural state', 'memory',
        'microarchitectural', 'replay', 'warm-up', 'cycle by cycle', 'pipeline',
        'cache', 'interrupts', 'DMA', 'determinism', 'DESSERT', 'ENCORE',
        'BOOM', 'Rocket', '32.88×', '2191.2×', '18.09×', '896.4×',
        'not demonstrated universal cycle-accurate reconstruction',
    ):
        assert phrase in section


def test_3d_dura_explanation_separates_sparse_attention_from_3d_efficiency() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1357']
    assert 'hybrid 3D near-memory and in-memory computing stack' in row['method_or_artifact']
    assert 'not demonstrated quality-preserving' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1357"></span>') == 1
    section = page.split('## 3D-DuRA: sparse attention', 1)[1].split('## CacheParallel:', 1)[0]
    for phrase in (
        'Visual autoregressive', 'resolution', 'token', 'attention', '3D',
        'near-memory', 'in-memory', 'dual-ring', 'sparse', 'quality', 'logits',
        'ring hops', 'synchronization', 'bandwidth', 'ADC/DAC', 'thermal',
        'Infinity2B', 'VAR-d36', '4.1×', '3.5×', '9.1×', '10.1×', '13.1×',
        'not demonstrated quality-preserving',
    ):
        assert phrase in section


def test_dap_explanation_separates_partition_balance_from_distributed_spmm_gain() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1256']
    assert 'two-level partitioning framework' in row['method_or_artifact']
    assert 'not demonstrated portable end-to-end SpMM superiority' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1256"></span>') == 1
    section = page.split('## DAP:', 1)[1].split('<span id="explanation-dac-2026-research1629"></span>', 1)[0]
    for phrase in (
        'DAP', 'sparse-dense', 'distributed', 'two-level', 'partition',
        '2-D', 'multi-chip', 'SPU', 'CSC', 'COO', 'replication',
        'RAW', 'reservation buffer', 'communication', '1.43×', '0.067×',
        '2.69×', 'NVIDIA A100', '500 MHz', 'numerical', 'precision',
        'utilization', 'A100 normalization', 'not demonstrated portable end-to-end SpMM superiority',
    ):
        assert phrase in section


def test_pima_secdb_explanation_separates_pim_speedup_from_fhe_query_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research2294']
    assert 'multi-level, multi-channel high-bandwidth processing-in-memory' in row['method_or_artifact']
    assert 'not demonstrated end-to-end secure query acceleration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/data-movement-and-locality.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research2294"></span>') == 1
    section = page.split('## PIMA-SecDB:', 1)[1].split('<span id="explanation-dac-2026-research1629"></span>', 1)[0]
    for phrase in (
        'PIMA-SecDB', 'FHE', 'database', 'ciphertext', 'PIM', 'multi-level',
        'multi-channel', 'bootstrapping', 'SQL', 'query', 'schema', 'predicate',
        'selectivity', 'noise', 'decryption', 'security', 'ciphertext expansion',
        'memory bandwidth', 'host', '1.98×', '7.93×', 'correctness',
        'not demonstrated end-to-end secure query acceleration',
    ):
        assert phrase in section


def test_bident_explanation_separates_optical_loss_model_from_physical_logic_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1268']
    assert 'binary aggregate model' in row['method_or_artifact']
    assert 'not demonstrated signoff-quality logic' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/neuromorphic-quantum-and-non-von-neumann.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1268"></span>') == 1
    section = page.split('### Bident: optimize how optical signals are combined', 1)[1].split('## Quantum control', 1)[0]
    for phrase in (
        'Bident', 'optical', 'logic', 'binary', 'combiner', 'tree', 'attenuation',
        'receiver', 'Huffman', 'Y-branch', 'directional coupler', 'harmonic mean',
        'greedy', 'input ordering', 'phase', 'wavelength', 'variation', 'manufacturing',
        'schematic-level', 'layout', 'worst-case', 'not demonstrated signoff-quality logic',
    ):
        assert phrase in section


def test_agent_per_qubit_explanation_separates_rl_reward_from_fault_tolerant_execution() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research1312']
    assert 'one reinforcement-learning agent to each logical qubit' in row['method_or_artifact']
    assert 'not demonstrated fault-tolerant execution improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/optimization-and-search-methods.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research1312"></span>') == 1
    section = page.split('## Agent-Per-Qubit:', 1)[1].split('## Compare the result', 1)[0]
    for phrase in (
        'QAgent', 'logical', 'physical', 'placement',
        'reinforcement-learning', 'Breakthrough Return Bonus', 'sparse rewards',
        'routing', 'coupling graph', 'ancilla', 'decoder', 'SWAPs',
        'execution cost', 'success rate', 'logical-error', 'noise',
        '53.9%', 'unseen circuits', 'invalid', 'not demonstrated fault-tolerant execution improvement',
    ):
        assert phrase in section


def test_superconducting_retiming_explanation_separates_jj_count_from_timing_and_interface_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research520']
    assert 'Duplication-aware retiming co-optimizes register placement and polarity assignment' in row['method_or_artifact']
    assert 'not demonstrated portable process yield' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/emerging-device-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research520"></span>') == 1
    section = page.split('## Duplication-aware superconducting retiming:', 1)[1].split('## JSPlace:', 1)[0]
    for phrase in (
        'Superconductor', 'dual-rail', 'Josephson', 'retiming', 'polarity',
        'register', 'amplifier', 'driver', 'receiver', 'fanout', 'SFQ',
        'equivalence', 'pulse', 'cycle', 'cycles per result', 'throughput',
        'critical path', 'process', 'yield', 'cryogenic', '63–71%', '41–66%',
        'not demonstrated portable process yield',
    ):
        assert phrase in section


def test_jsplace_explanation_separates_shape_control_from_pulse_timing_validity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research875']
    assert 'JSPlace folds multi-stage RSFQ placement into three segments' in row['method_or_artifact']
    assert 'not demonstrated clock-safe routed layouts' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/emerging-device-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research875"></span>') == 1
    section = page.split('## JSPlace: control shape', 1)[1].split('## How the two approaches', 1)[0]
    for phrase in (
        'RSFQ', 'aspect ratio', 'three segments', 'mixed-integer linear programming',
        'dynamic programming', 'vertical', 'wirelength', 'ISCAS85', 'EPFL',
        'pulse', 'timing', 'skew', 'fanout', 'routing', 'legalization',
        'process', 'routability', 'not demonstrated clock-safe routed layouts',
    ):
        assert phrase in section


def test_asg_moenn_explanation_separates_sparse_gating_from_rf_linearity() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research656']
    assert 'sparsely gated mixture-of-experts digital predistorter' in row['method_or_artifact']
    assert 'not demonstrated measured RF linearity' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/rf-and-mixed-signal-design.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research656"></span>') == 1
    section = page.split('## ASG-MOENN: sparse adaptive predistortion', 1)[1].split('## The longer-term research question', 1)[0]
    for phrase in (
        'power amplifier', 'nonlinear', 'Digital predistortion', 'SCPA', 'mixture-of-experts',
        'sparse', 'gate', 'confidence', 'EVM', 'ACLR', 'NMSE', 'bandwidth',
        'output power', 'expert-selection', 'switching transients', 'hysteresis',
        'sample throughput', 'worst-case latency', '30-dB', '50%',
        'not demonstrated measured RF linearity',
    ):
        assert phrase in section


def test_credix_explanation_separates_backpressure_from_lossless_switching_gain() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research837']
    assert 'region-based shared pools' in row['method_or_artifact']
    assert 'not demonstrated lossless, deadlock-free or silicon-validated switching improvement' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/interconnect-and-networking.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research837"></span>') == 1
    section = page.split('## Credix: share distributed buffer capacity', 1)[1].split('## Compare the results carefully', 1)[0]
    for phrase in (
        'Credix', 'distributed', 'buffer', 'Regional Credit Allocator',
        'credit', 'VC-to-path', 'packet ordering', '65.6%', 'Hotspot',
        'backpressure', 'realistic', 'throughput', 'latency', 'fairness',
        'losslessness', 'deadlock', 'silicon',
        'not demonstrated lossless, deadlock-free or silicon-validated switching improvement',
    ):
        assert phrase in section


def test_gemir_explanation_separates_joint_prediction_from_power_integrity_signoff() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['dac-2026-research046']
    assert 'cross-layer node-edge attention' in row['method_or_artifact']
    assert 'not replacement of trusted power-integrity and reliability checks' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/observed-subthemes/power-integrity-and-reliability.md').read_text()
    assert page.count('<span id="explanation-dac-2026-research046"></span>') == 1
    section = page.split('## GEMIR: joint EM/IR prediction', 1)[1].split('## Compare the results carefully', 1)[0]
    for phrase in (
        'GEMIR', 'IR drop', 'electromigration', 'node-level', 'edge-level',
        'KCL', 'Korhonen', 'attention', 'boundary conditions', 'temperature',
        'material', 'held-out', 'trusted numerical solver', 'tail', 'percentiles',
        '40.79%', '19.35%', 'signoff', 'lifetime', 'silicon',
        'not replacement of trusted power-integrity and reliability checks',
    ):
        assert phrase in section


def test_adder_dcim_explanation_separates_compression_from_cim_execution() -> None:
    from scripts.build_theme_pages import read_selected_sample
    rows = read_selected_sample(ROOT)
    revised = {r['paper_id']: r for r in apply_editorial_corrections(ROOT, rows)}
    row = revised['iccad-2025-1']
    assert 'Joint model compression and parallel bit-flexible digital CIM' in row['method_or_artifact']
    assert 'does not establish accuracy-preserving end-to-end CIM acceleration' in ' '.join(row['limits'])
    build(ROOT)
    page = (ROOT / 'reports/subtheme-editorial/emerging-memory-and-devices.md').read_text()
    assert page.count('<span id="explanation-iccad-2025-1"></span>') == 1
    section = page.split('## Adder-DCIM: compressed models', 1)[1].split('## Compare useful work', 1)[0]
    for phrase in (
        'AdderNet', 'model compression', 'digital compute-in-memory',
        'bit-flexible', 'minimum-selector', 'ResNet20', 'ResNet50',
        'accuracy', 'dataset', 'bit ordering', 'overflow', 'saturation',
        'utilization', 'TOPS/W', '28-nm', '134 TOPS/W', '6.49 TOPS/mm²',
        '255 TOPS/W', '243 TOPS/W', 'power boundary',
        'not establish accuracy-preserving end-to-end CIM acceleration',
    ):
        assert phrase in section


def test_observed_subtheme_coverage_language_matches_record_count() -> None:
    build(ROOT)
    pages = list((ROOT / 'reports/observed-subthemes').glob('*.md'))
    assert len(pages) == 113
    for page in pages:
        content = page.read_text()
        count = len(re.findall(r'<span id="paper-[^"]+"></span>', content))
        assert count > 0, page.name
        if count == 1:
            assert 'This subject has 1 record in the selected sample.' in content
            assert 'This subject is represented by one paper' in content
        else:
            assert f'This subject has {count} records in the selected sample.' in content
            assert 'Multiple papers in this selected sample permit comparison' in content
            assert 'This subject is represented by one paper' not in content


def test_theme_pages_cover_the_coded_theme_sample() -> None:
    result = build(ROOT)
    assert result["theme_count"] == 10
    assert result["record_count"] == 582
    assert all((ROOT / page["page"]).exists() for page in result["pages"])


def test_theme_pages_keep_source_and_uncertainty_boundaries() -> None:
    index = (ROOT / "reports/themes/README.md").read_text()
    assert "selected coded sample" in index
    for path in (ROOT / "reports/themes").glob("*.md"):
        if path.name == "README.md":
            continue
        text = path.read_text()
        assert "Representative source-backed records" in text
        assert "Paper cards: what changes and where it stops" in text
        assert "Problem:" in text
        assert "Mechanism / artifact:" in text
        assert "source URL" in text
        assert "Missing fields are evidence gaps" in text


def test_authored_subtheme_sections_survive_generation_with_paper_anchors() -> None:
    editorial_paths = list((ROOT / "reports/subtheme-editorial").glob("*.md"))
    assert editorial_paths, "Individual subject explanations must not disappear"
    for path in editorial_paths:
        source = path.read_text()
        generated = ROOT / "reports/observed-subthemes" / path.name
        assert generated.exists(), path.name
        assert source in generated.read_text(), path.name
        for target, anchor in re.findall(
            r"\]\(([^()\s]+\.md)#(paper-[^()\s]+)\)", source
        ):
            destination = (path.parent / target).resolve()
            assert destination.is_relative_to(ROOT), (path.name, target)
            assert destination.exists(), (path.name, target)
            assert f'id="{anchor}"' in destination.read_text(), (
                path.name, target, anchor
            )
