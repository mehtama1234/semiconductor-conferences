# Review remediation queue v1

Status as of 2026-09-06: deterministic routing aid only. This queue is not an
independent scientific review and does not create acceptance verdicts.

The preflight contains 19 records marked `review` out of 581 packets. A packet
can be routed here because original source text is absent or unmatched, required
technical fields are incomplete, provenance is outside the accepted source
allow-list, or evidence overlap is below the deterministic threshold. Reviewers
must inspect the original source and apply the independent-review protocol; they
must not treat the preflight label as a substantive judgment.

## Priority order

| Priority | Paper IDs | First remediation action |
|---|---|---|
| 1 | `isca-2026-program-044`, `iccad-2025-1`, `iccad-2025-1137` | Capture and identity-match original source text; do not review researcher summaries as substitutes. |
| 2 | `isca-2026-program-058`, `iccad-2025-105`, `iccad-2025-109`, `iccad-2025-1094`, `iccad-2025-1109`, `iccad-2025-1111`, `iccad-2025-1117`, `iccad-2025-114`, `iccad-2025-1142`, `iccad-2025-1155`, `iccad-2025-1144` | Fill missing problem/method/metric/limitation fields from source passages and record section/table locators; reconcile provenance where needed. |

The first group has no comparable captured original text in the preflight and
therefore cannot be accepted from the current packet. The second group has
captured text but needs field-level reconciliation before independent review can
resolve it. `iccad-2025-109` also has the lowest observed evidence overlap and
an invalid preflight provenance URL, so it should be handled first within that
group.

`iccad-2025-105` (Squat) is a distinct metric-reconciliation case: the original
preprint and PDF table are captured, but two displayed latency/speedup ratios are
incompatible under the recorded rounding analysis. Keep the abstract's maximum
speedup as a withheld author claim, reconcile the raw timings or final version,
and do not convert it into an accepted metric merely to satisfy the required
field checklist.

## Completion condition

For each row, add source capture or corrected locators, preserve unresolved
unknowns, regenerate the packet, and obtain two independent verdicts. A
deterministic pass after remediation still does not count as acceptance.
