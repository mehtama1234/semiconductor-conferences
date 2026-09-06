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

`review-packet-coverage.json` is the scheduling index, including 33 synthesis
anchors. Do not include it in judge input: it reveals which conclusions the
project is trying to support. Generated packets intentionally omit synthesis
conclusions and previous same-model verdicts.

Current coverage: 72 prepared packets; 49 captured official descriptions and
23 requiring original source capture; zero independent reviews. The latter
includes primary-paper records such as MTIA: a primary source label and source
locators do not mean original text is already embedded in a reproducible packet.

The deterministic audit now reports source overlap as null when original text
is absent. All required fields must be populated for its pass result, but field
population and vocabulary overlap still do not establish semantic support.
