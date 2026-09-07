# Review packet workflow

Rebuild with `PYTHONPATH=.:src python3 scripts/build_review_packets.py`.

Each file under `data/review-packets/` is one record's review input. The record's
claims are not the original source. `researcher_summary_not_original_source`
preserves this distinction even when a source has previously been read online.
`original_source_text` is null unless a separate captured description matches
the paper identity. SHA-256 values identify the record, source text, protocol,
and coding guide versions used at preparation time.

Before invoking a reviewer, supply the current protocol and coding guide and
confirm that their hashes match the packet. Recover missing original source text
first. The reviewer must evaluate numerical conditions, assumptions, limitations,
and a neighboring taxonomy category. The packet contains no independent verdict;
do not treat its readiness state as acceptance.

`review-packet-coverage.json` is the scheduling index, including 37 synthesis
anchors. Do not include it in judge input: it reveals which conclusions the
project is trying to support. Generated packets intentionally omit synthesis
conclusions and previous same-model verdicts.

Current coverage: 105 prepared packets; 52 official descriptions, 35 original
abstracts, and three requiring original source capture; zero independent reviews.
The abstracts include 21 arXiv pages, three author PDFs and one HKUST institutional
publication page. HKUST extraction requires matching title and DOI and a unique
scoped abstract block; it does not accept arbitrary page text. Abstract capture does
not complete full-text numerical verification, even when the packet has locators.

Run `PYTHONPATH=.:src python3 scripts/capture_review_sources.py` to capture missing
abstracts. The collector requires exact normalized title identity and records
raw/text hashes, URLs, capture dates, and extraction boundaries. Successful
captures are reused when the source URL and expected title are unchanged; this
is a reproducible snapshot, not a claim that the source has never changed.
`data/review-source-captures.jsonl` preserves normalized abstracts and retrieval
outcomes; downloaded HTML/PDF inputs remain ignored under the raw-data policy.
The collector requires BeautifulSoup4 and pypdf in addition to Python.

The deterministic audit now reports source overlap as null when original text
is absent. All required fields must be populated for its pass result, but field
population and vocabulary overlap still do not establish semantic support.
