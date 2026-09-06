# ISCA 2026 company-source evidence batch 7

This batch adds two exact ISCA 2026 CXL papers using official company/author
sources. These are useful because they expose silicon and deployment context that
ordinary program metadata does not, but they are not equivalent to captured full
papers and are labeled `medium_company_author_source`.

## Panmnesia: silicon-proven CXL controller and fabric switch

Panmnesia’s official announcement describes a unified CXL controller that shares
buffers across physical, link, and transaction layers, reducing synchronization
overhead inherited from PCIe-derived controller organization. Its fabric switch
supports port-based routing in addition to hierarchy-based routing, allowing more
flexible topologies. The announcement reports stable performance with as many as
64 nodes, similar latency while expanding memory connectivity, and improved total
system bandwidth. It also places the work in a productization context involving
pre-release PCIe 6.4-CXL 3.2 switch silicon and PCIe 7.0-CXL 4.0 controller IP.
[Official company announcement](https://panmnesia.com/news/en/2026-06-24-panmnesia-isca2026-eng/)

The detailed subskill is silicon-level interconnect integration: layer-buffer
organization, routing topology, node scale, and latency are co-designed rather
than evaluated as isolated protocol features. The source does not provide full
latency distributions, power, area, process, or workload tables.

## Meta: Vistara’s end-to-end CXL deployment path

The lead author’s presentation post describes Vistara as a path from ASIC and
firmware through OS memory tiering to hyperscale deployment. It names
disaggregated ML inference, big-data processing, databases, distributed caches,
and software build/test pipelines as production workload classes. The post claims
up to 25% fewer servers for disaggregated inference, tiering overhead below 0.5%,
and reuse of decommissioned DIMMs as CXL memory.
[Lead-author presentation post](https://www.linkedin.com/posts/neha-gholkar-4897b445_isca2026-activity-7477033922183458816-o8FC)

The detailed subskill is productionization across layers: CXL value depends on
silicon, firmware, OS policy, workload diversity, tail latency, capacity
planning, and operations. These are company-reported claims and require full-
paper and independent deployment verification before being used for quantitative
industry conclusions.

## Why this batch matters

The two records complement the academic CXL/PIM cases. CANNON, CtxMem, and COSM
focus on architecture and memory behavior; these company-source records expose
the implementation and deployment path needed to make composable memory useful
at scale. The evidence still does not establish broad CXL adoption or a general
economic advantage.
