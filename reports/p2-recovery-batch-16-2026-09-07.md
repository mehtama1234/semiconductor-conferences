# P2 recovery routing batch 16 — 2026-09-07

This tranche routes ten ISCA records across RISC-V GPU/ASIP co-design, DRAM
reliability and RowHammer defenses, chiplet PHY/package simulation, and
heterogeneous chiplet execution.

| Priority | Paper ID | Title | Evidence needed before quantitative use |
|---:|---|---|---|
| 1 | `isca-2026-program-095` | sCROOGe: Circuit-level Design and Optimization Framework for RISC-V Out-of-Order GPUs | ISA/microarchitecture, GPU workloads, synthesis/process, PPA metrics, compiler/toolchain, and GPU baseline |
| 2 | `isca-2026-program-096` | æSIP: μArch-aware ASIP-ISA Co-Design via Program Synthesis, Equality Saturation, and External Don’t Cares | ISA search space, synthesis/equality-saturation setup, workloads, formal correctness, area/timing/energy, and fixed-ISA baseline |
| 3 | `isca-2026-program-097` | ColumnKeeper: Efficient Solutions to the ColumnDisturb Vulnerability in DRAM-based Systems | DRAM generation, attack pattern, vulnerability definition, mitigation coverage, performance/area/energy, and prior defenses |
| 4 | `isca-2026-program-098` | PVAC: A RowHammer Mitigation Architecture Exploiting Per-victim-row Counting | Threat model, row activation conditions, counter storage/update cost, attack coverage, false positives, and baseline defense |
| 5 | `isca-2026-program-099` | Loaded Dice: Solving the Non-Selection Problem for Scalable Probabilistic RowHammer Defense | Probabilistic model, attack/refresh workload, selection guarantee, security probability, storage/energy, and deterministic baseline |
| 6 | `isca-2026-program-100` | PRowhammer: Propagating Bit-flips from CPU to GPU | CPU/GPU platform, propagation path, attack privilege, observed bit flips, mitigation, and cross-device baseline |
| 7 | `isca-2026-program-101` | DejaVu: Why You Should Write to Your DRAM Rows Twice, Carefully | DRAM device/process, write pattern, reliability/security mechanism, workload, retention/latency/energy, and conventional write baseline |
| 8 | `isca-2026-program-102` | DICE: Detailed Inter-Chiplet End-to-End PHY Modeling for Accurate Chiplet Simulation | PHY/link model, process/package, calibration traces, workloads/topologies, accuracy/runtime, and existing simulator baseline |
| 9 | `isca-2026-program-103` | Omelet: A Packaging-Aware Hierarchical Interconnect Simulator for 2.5D/3D Chiplet Architectures | Package/interposer assumptions, hierarchy, traffic patterns, thermal/power/link models, validation target, and simulator baseline |
| 10 | `isca-2026-program-104` | PhaseWeave: Phase-Aware Execution on Heterogeneous Chiplet Architectures for Datacenters | Chiplet types/topology, phase detector, datacenter workloads, migration/reconfiguration cost, throughput/SLO/energy, and static scheduler baseline |

These are recovery priorities and condition checklists, not technical rankings or
temporal trend evidence.
