# Review remediation queue v1

Status as of 2026-09-07: deterministic routing aid only. This queue is not an
independent scientific review and does not create acceptance verdicts.

The preflight contains 0 records marked `review` out of 582 packets. A packet
can be routed here because original source text is absent or unmatched, required
technical fields are incomplete, provenance is outside the accepted source
allow-list, or evidence overlap is below the deterministic threshold. Reviewers
must inspect the original source and apply the independent-review protocol; they
must not treat the preflight label as a substantive judgment.

## Priority order

| Priority | Paper IDs | First remediation action |
|---|---|---|
| 1 | None currently | All previously flagged records now have identity-matched source separation; proceed to independent review and full-paper condition extraction. |

The three previously flagged records now have identity-matched source captures or
artifact evidence and pass deterministic source comparison. Adder-DCIM and the
Panmnesia CXL paper use institutional/company descriptions; ComoPy uses an exact-
URL artifact description with explicitly limited identity. These sources remain
below manuscript-level evidence and do not establish independent acceptance.
`iccad-2025-109` also has the lowest observed evidence overlap and
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
