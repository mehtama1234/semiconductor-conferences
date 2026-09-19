"""Readable articles backed by the existing adjudicated evidence, without clipping."""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

try:
    from scripts.research_explanations import explanation_sections
    from scripts.subtheme_explanations import explain
except ModuleNotFoundError:
    from research_explanations import explanation_sections
    from subtheme_explanations import explain


def name(value):
    readable = str(value).replace('_', ' ').replace('-', ' ').capitalize()
    return re.sub(r'\b(ai|eda|llm|rtl|hls|fpga|rf|pim|ecc|dac|isca|iccad)\b', lambda m: m[0].upper(), readable, flags=re.I)


def text(value):
    if value is None or value == '' or value == []:
        return 'Not established in the captured evidence.'
    if isinstance(value, list):
        return '\n\n'.join(text(item) for item in value)
    if isinstance(value, dict):
        return '\n\n'.join(f'**{name(k)}:** {text(v)}' for k, v in value.items())
    return str(value).strip()


CORRECTION_FIELDS = {
    'problem', 'method_or_artifact', 'workload_or_benchmark',
    'hardware_or_process_assumptions', 'baselines', 'metrics', 'limits',
    'evidence_url', 'evidence_locators', '_page_source_tier',
}


def apply_editorial_corrections(root, rows):
    """Update reading cards without overwriting historical adjudication inputs."""
    path = root / 'data/editorial-paper-corrections-v1.json'
    if not path.exists():
        return rows
    register = json.loads(path.read_text())
    if register.get('schema') != 'editorial-paper-corrections.v1':
        raise ValueError('Unsupported editorial correction schema')
    known = {row['paper_id'] for row in rows}
    corrections = {}
    for entry in register['rows']:
        paper_id = entry['paper_id']
        if paper_id not in known or paper_id in corrections:
            raise ValueError(f'Unknown or duplicate correction target: {paper_id}')
        if set(entry['fields']) != CORRECTION_FIELDS:
            raise ValueError(f'Correction must supply a complete evidence card: {paper_id}')
        if not entry.get('review_date') or not entry.get('reason'):
            raise ValueError(f'Correction lacks provenance: {paper_id}')
        corrections[paper_id] = entry
    corrected = []
    for row in rows:
        entry = corrections.get(row['paper_id'])
        if entry is None:
            corrected.append(row)
            continue
        updated = dict(row)
        updated.update(entry['fields'])
        updated['_editorial_correction'] = entry
        updated['_original_evidence'] = row.get('_original_evidence') or {key: row.get(key) for key in sorted(CORRECTION_FIELDS)}
        corrected.append(updated)
    return corrected


def evidence_card(row, level=3, assessments=()):
    lines = [f'<span id="paper-{row["paper_id"]}"></span>', '', f'{"#" * level} {row["title"]}', '',
             f'{row["conference_id"].upper()} {row["analysis_edition"]} · Record: `{row["paper_id"]}`', '']
    if row.get('_explanation_anchor'):
        lines += [f'[Read the step-by-step explanation](#{row["_explanation_anchor"]})', '']
    correction = row.get('_editorial_correction')
    if correction:
        lines += ['**Updated source-backed reading card**', '',
                  f'Reviewed {correction["review_date"]}. {correction["reason"]}', '',
                  'This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.', '',
                  '[Correction register](../../data/editorial-paper-corrections-v1.json)', '']
    for label, key in [('Problem:', 'problem'), ('Mechanism / artifact:', 'method_or_artifact'),
                       ('Workload — the work tested:', 'workload_or_benchmark'),
                       ('Hardware and manufacturing assumptions:', 'hardware_or_process_assumptions'),
                       ('Baseline — the comparison method:', 'baselines'),
                       ('Reported measurements:', 'metrics'), ('Limits on the conclusion:', 'limits')]:
        lines += [f'**{label}**', '', text(row.get(key)), '']
    tier = row.get('_page_source_tier', row.get('classification_confidence', 'unknown'))
    lines += ['**Source and location**', '', f'Evidence tier: {name(tier)}. This is the stored source classification; the location and limits below determine what was actually read.', '']
    if row.get('evidence_url'):
        lines += [f'[Open the recorded source]({row["evidence_url"]})', '']
    else:
        lines += ['A source URL has not been recorded.', '']
    locator = row.get('evidence_locators') or row.get('evidence_locator') or row.get('source_locator')
    lines += [text(locator) if locator else 'An exact page, section, or table location has not been recorded. Page-level verification remains open.', '']
    if correction:
        lines += ['<details markdown="1">', '<summary>Original captured fields — superseded for this reading card</summary>', '',
                  text(row['_original_evidence']), '', '</details>', '']
    for index, assessment in assessments:
        lines += ['#### Additional source assessment', '',
                  f'This separately recorded check is dated {index.get("capture_date", "date unspecified")}. It supplements the original record above and retains its own scope and uncertainty.', '',
                  f'[Assessment record](../../{index["path"]})', '']
        if index.get('source_url'):
            lines += [f'[Assessed source]({index["source_url"]})', '']
        for field in ('extraction_scope', 'identity_status', 'conditions', 'platform', 'metrics', 'interpretation_limits', 'remaining_unknowns', 'headline_metric_status', 'independent_review_status'):
            if assessment.get(field):
                lines += ['**' + name(field) + '**', '', text(assessment[field]), '']
    return lines


def theme_article(theme, label, items, selected, root=None):
    lines = [f'# {label}', '', f'This article explains the subject and then connects it to {len(items)} papers in the selected research sample.', '',
             'A subtheme groups related technical problems. A mechanism describes the particular change proposed by a paper. The discussion below explains the subject; the linked paper records state the available evidence.', '', '[Definitions used in the paper records](../reading-guide-v1.md)', '']
    lines += explanation_sections(theme)
    if root is not None:
        editorial = Path(root) / 'reports/theme-editorial' / f'{theme}.md'
        if editorial.exists():
            lines += [editorial.read_text().strip(), '']
    lines += ['## Subthemes and how to study them', '',
              'Each link opens the subtheme discussion and its captured paper records. Explanatory depth varies: some papers have expanded individual explanations; others still have only brief discussion or evidence cards. Source locations and unresolved conditions remain visible.', '']
    groups = defaultdict(list)
    for row in items:
        groups[row['subtheme_id']].append(row)
    for sub, subset in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        lines += [f'### [{name(sub)}](../observed-subthemes/{sub}.md)', '',
                  f'{len(subset)} selected records in this theme. Start with [{subset[0]["title"]}](../observed-subthemes/{sub}.md).', '']
    lines += ['## Representative source-backed records', '',
              'The following reading set spans the available conferences and uses dated corrections where registered. These corrections improve the current reading view but do not change historical adjudication or establish independent acceptance. Each paper link opens its exact evidence card.', '',
              '## Paper cards: what changes and where it stops', '']
    for row in selected:
        lines += [f'- [{row["title"]}](../observed-subthemes/{row["subtheme_id"]}.md#paper-{row["paper_id"]}) — {row["conference_id"].upper()} {row["analysis_edition"]}.']
    lines += ['', '## What the evidence supports', '',
              'These records identify proposed methods and the conditions recorded for them. A reported improvement should be interpreted with its comparison method, input size, hardware, and result-quality requirement. Missing fields are evidence gaps; a populated field can also state that a detail is unspecified.', '',
              '## Limits and next evidence', '',
              'The selected sample is uneven across conferences and source types. It cannot establish how fast a subject is growing. Repeated observations across comparable years, with the same inclusion rules and source depth, are needed for a time trend.', '',
              'Every linked evidence article preserves the Problem: and Mechanism / artifact: fields, baseline, unshortened limitations, source URL, and recorded location. Primary text and independent review remain necessary where the record says those checks are open.', '',
              '[Research directions](../directions/README.md) · [All observed subthemes](../expanded-taxonomy-v1.md)', '']
    return lines


def subtheme_article(spec, items, selected):
    lines = [f'# {spec["label"]}', '', 'This article groups several related subjects to explain a shared design question.', '']
    for heading, paragraph in zip(['The problem', 'What changes in the design', 'How to establish an improvement'], spec['plain']):
        lines += ['## ' + heading, '', paragraph, '']
    # Include the complete foundational explanation for the principal parent.
    lines += explanation_sections(spec['theme_ids'][0])
    lines += ['## The individual subjects', '', f'The grouping contains {len(items)} selected records. Read its individual subjects below; their boundaries can overlap.', '']
    for sub in spec['subtheme_ids']:
        if any(r['subtheme_id'] == sub for r in items):
            lines += [f'- [{name(sub)}](../observed-subthemes/{sub}.md)']
    lines += ['', '## Technical cards', '', 'Evidence tier and exact source locations are provided in each linked article. The article preserves full recorded text, including limits and baselines.', '']
    for row in selected:
        lines += [f'- [{row["title"]}](../observed-subthemes/{row["subtheme_id"]}.md#paper-{row["paper_id"]})']
    lines += ['', '## Limits and next evidence', '',
              'This is a cross-cutting grouping within the selected sample. Its count measures the records included by the grouping rule. Comparing methods requires the same workload, answer quality, hardware limits, and total evaluation budget. Open the individual records before treating a shared subject as a common result.', '',
              '[Research directions](../directions/README.md) · [Complete subtheme index](../expanded-taxonomy-v1.md)', '']
    return lines


def build_observed(root, rows):
    out = root / 'reports/observed-subthemes'
    out.mkdir(parents=True, exist_ok=True)
    groups = defaultdict(list)
    assessments = defaultdict(list)
    index_path = root / 'data/supplementary-assessment-index-v1.json'
    if index_path.exists():
        for index in json.loads(index_path.read_text())['rows']:
            assessment = json.loads((root / index['path']).read_text())
            assessments[index['paper_id']].append((index, assessment))
    for row in apply_editorial_corrections(root, rows):
        groups[row['subtheme_id']].append(row)
    for sub, items in sorted(groups.items()):
        themes = sorted({r['theme_id'] for r in items})
        record_label = 'record' if len(items) == 1 else 'records'
        coverage_limit = (
            'This subject is represented by one paper and supports a case study, not evidence of recurrence or a long-term trend.'
            if len(items) == 1 else
            'Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.'
        )
        lines = [f'# {name(sub)}', '',
                 f'This subject has {len(items)} {record_label} in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.', '',
                 '[Definitions used in the paper records](../reading-guide-v1.md)', '', '## Understand the parent subject first', '']
        for theme in themes:
            lines += [f'- [{name(theme)}](../themes/{theme}.md)']
        editorial = root / 'reports/subtheme-editorial' / f'{sub}.md'
        editorial_text = editorial.read_text() if editorial.exists() else ''
        lines += [''] + (editorial_text.splitlines() + [''] if editorial_text else explain(sub))
        lines += ['## Compare the results carefully', '',
                  'First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.', '',
                  'A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.', '',
                  '## Complete captured evidence', '',
                  'These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.', '']
        for row in items:
            card_row = dict(row)
            anchor = f'explanation-{row["paper_id"]}'
            if f'<span id="{anchor}"></span>' in editorial_text:
                card_row['_explanation_anchor'] = anchor
            lines += evidence_card(card_row, assessments=assessments[row['paper_id']])
        lines += ['## What remains to establish', '',
                  'Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. ' + coverage_limit, '',
                  '[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)', '']
        (out / f'{sub}.md').write_text('\n'.join(lines))
    return len(groups)
