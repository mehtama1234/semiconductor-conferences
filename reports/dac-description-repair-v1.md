# DAC description extraction repair — 2026-09-06

The original RESEARCH1691 HTML contains the full description. The extractor's
`<[^>]+>` expression consumed text beginning at the literal `<13k` through the
next HTML tag. Replacing tag stripping with HTMLParser preserves the inequality.
Re-extracting all 543 saved DAC 2026 descriptions changes exactly research1691;
no raw captures were missing in this audit. This is a DAC 2026 audit, not proof
that every other collector is free of this defect.

The evidence ledger retains the previous description, original capture date,
raw path and SHA-256 under `extraction_correction`. No source was silently
replaced and no recollection date was substituted for the original capture.
Draft and review packet text/hashes were regenerated. Inventory counts do not
change and no independent verdict is implied.

The [official presentation](https://63dac.conference-program.com/presentation/?id=RESEARCH1691&sess=sess141)
was also checked. It reports 64 nJ/frame and 11 µW at 30 FPS. The first quantity
times frame rate yields 1.92 µW. Idle or additional subsystem power might explain
the difference, but the description supplies no such decomposition. Both source
figures remain qualified; neither is silently corrected. Full-paper evidence is
still needed for power boundaries, evaluation splits and silicon status.
