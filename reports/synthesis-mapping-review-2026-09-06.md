# Synthesis mapping reconciliation — 2026-09-06

Status: researcher reconciliation, not independent adjudication.

The prior reference checks established that IDs existed, but did not establish
that the referenced mechanism supported the associated prose. This pass compares
the affected records' methods with the specific subskills named in the synthesis.

| Direction | Prior problem | Correction and scope |
|---|---|---|
| Tool-grounded AI design | DAC research031 is exact quantum synthesis; its record has no LLM design mechanism | Replace with research1110 (LLM/HLS implementation), research865 (LLM HLS exploration), and research535 (evaluated technology-map code evolution) |
| Reliability/security | ICCAD 1080 is RSizing; it does not support the stated telemetry attack example | Use ICCAD 1000, Energon, for the confidentiality attack; retain RSizing under variation-aware search |
| Physical integration | ICCAD 1000 is Energon, not the chiplet design case described in the prose | Use ICCAD 1207, MAHL, for chiplet design-flow integration, with manufacturing readiness unproven |
| Search/modeling | Exact quantum synthesis and multi-fidelity exploration were named without their direct references | Add research031 for exact quantum resource optimization and research1186 (XSearch) for multi-fidelity exploration |

Affected references now carry a mapping rationale and an explicit non-independent
review label. This does not certify all other references or numerical claims.
The combined search direction contains distinct methods: an exact T library is
not itself evidence of learned search, physics awareness, or multi-fidelity
evaluation. Subskill-level interpretation must preserve these distinctions.

The packets and work queue are regenerated from the revised map. Independent
review remains required; neither the reference count nor a successful ID join
is a measure of scientific support.
