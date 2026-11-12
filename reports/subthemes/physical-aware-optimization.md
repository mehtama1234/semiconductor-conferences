# Physical-aware optimization

This article groups several related subjects to explain a shared design question.

## The problem

A design choice can look good in an abstract model and fail after wire length, timing, heat, power delivery, or manufacturing rules are included.

## What changes in the design

The papers put physical measurements or models into placement, routing, search, packaging, or process decisions.

## How to establish an improvement

The useful test compares final valid designs, not only proxy scores, and reports technology data, tool settings, runtime, and failed cases.

## A correct connection can still arrive too late once it becomes a wire

A circuit description lists components and their connections. Manufacturing needs real shapes in specified material layers.

1. **Placement** chooses where each component sits.
2. **Routing** chooses each wire's path and layer.

Wires take up space, resist current and store electric charge. Their length and surroundings change how fast a signal switches. So a logically correct connection can still arrive too late.

## Every physical fix pushes on another part of the design

- Moving two communicating components closer shortens a wire, but can crowd another region.
- Adding a buffer can improve signal timing, but adds area and power.
- Manufacturing rules limit widths, spacing and overlaps.
- Changes in fabrication can change how transistors and wires behave.

An optimizer must meet all these conditions together. Improving one score while quietly breaking another does not count.

## The subthemes build geometry, estimate timing, or model manufacturing

- **Placement and routing** methods build the geometry.
- **Timing analysis** estimates whether signals switch in time.
- **Process models** estimate how fabricated devices behave.
- **Manufacturing and yield** methods study defects and variation. Yield is the fraction of manufactured chips that meet requirements.

A faster estimator and a better final layout are different contributions. They need different evidence.

## A fair test uses the same circuits and rules, and counts violations

1. Use the same circuit set, manufacturing rules, timing requirements and implementation tools.
2. Record violations as well as successful outputs.
3. Check the chosen designs with an accurate enough final evaluation, and count all search time.
4. If a method uses a cheaper approximation, check whether its errors change which design is chosen.

## The individual subjects

The grouping contains 27 selected records. Read its individual subjects below; their boundaries can overlap.

- [Process aware design](../observed-subthemes/process-aware-design.md)
- [3d stacking and thermal management](../observed-subthemes/3d-stacking-and-thermal-management.md)
- [Placement routing and timing](../observed-subthemes/placement-routing-and-timing.md)
- [Optimization and search methods](../observed-subthemes/optimization-and-search-methods.md)

## Technical cards

Evidence tier and exact source locations are provided in each linked article. The article preserves full recorded text, including limits and baselines.

- [Differentiable Fill Insertion with Explicit Delay Optimization](../observed-subthemes/process-aware-design.md#paper-dac-2026-research648)
- [From Fluid Dynamics to Chip Design: PDE Foundation Model Address Data Bottleneck in 3D-ICs Thermal Simulation](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research553)
- [IR-Drop Aware Global Placement with PDN Optimization and GPU-Accelerated Analysis for Mitigating Global and Local IR-Drop](../observed-subthemes/placement-routing-and-timing.md#paper-dac-2026-research2297)
- [Design Technology Co-Optimization for Network on Chip in High Performance CPUs at 3nm Node Using Monolithic 3D and Backside Interconnect Technologies](../observed-subthemes/process-aware-design.md#paper-dac-2026-research2290)
- [COPA: A Congestion-Oriented Pin Assignment Framework for Intra-Block Physical Design Optimization](../observed-subthemes/placement-routing-and-timing.md#paper-iccad-2025-1155)
- [Tasa: Thermal-aware 3D-Stacked Architecture Design with Bandwidth Sharing for LLM Inference](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-iccad-2025-1103)
- [Automated Design Space Exploration in High-Level Physical Synthesis](../observed-subthemes/optimization-and-search-methods.md#paper-iccad-2025-109)
- [RSizing: Robust Bayesian Optimization for Analog Circuit Sizing Under Process Variations](../observed-subthemes/process-aware-design.md#paper-iccad-2025-1080)
- [Pushing the Limits of Inverse Lithography with Generative Reinforcement Learning](../observed-subthemes/process-aware-design.md#paper-dac-2026-research209)
- [Seeing Through Silicon: Multimodal Thermal Reconstruction via Physics-Informed Diffusion](../observed-subthemes/3d-stacking-and-thermal-management.md#paper-dac-2026-research1907)

## Limits and next evidence

This is a cross-cutting grouping within the selected sample. Its count measures the records included by the grouping rule. Comparing methods requires the same workload, answer quality, hardware limits, and total evaluation budget. Open the individual records before treating a shared subject as a common result.

[Research directions](../directions/README.md) · [Complete subtheme index](../expanded-taxonomy-v1.md)
