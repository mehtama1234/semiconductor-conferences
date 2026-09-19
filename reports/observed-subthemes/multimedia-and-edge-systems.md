# Multimedia and edge systems

This subject has 9 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Systems applications and workloads](../themes/systems-applications-and-workloads.md)

## Begin with the output, not with the word multimedia

An image-processing system can have very different obligations. A codec must represent an existing image with fewer bits. A renderer computes an image from a scene and a viewing position. A search system ranks stored images against a request. A video-language model answers questions about observations. A generator produces new images or video. These outputs need different checks: a convincing generated frame does not prove faithful reconstruction, and a fast search does not prove that it found the requested image.

The nine DAC 2026 papers here concern these distinct tasks. Five matching full manuscripts were inspected; four papers remain supported by official descriptions, with an additional author repository for ExCave. PDF locations refer to the linked versions, not an independently verified final publisher copy. None of the artifacts was executed in this pass.

| Work being changed | Papers | What must remain useful |
|---|---|---|
| Represent screen images with fewer bits | PEL | Reconstructed detail and codec latency |
| Compute scene images | Relay-GS, PipeGS, AdaGScale | Visibility, image quality, frame timing |
| Search an image collection | MIRAGE | Ranking quality at a stated search cost |
| Answer questions about video | LiveVLM | Retention of relevant events and answer accuracy |
| Reuse or reduce generation work | ORBIS, ExCave, GalaxyDiT | Requested changes, retained content, video quality |

The common question is which information must be processed again. Similar input does not necessarily mean interchangeable computation. A slightly changed viewing position can expose a previously hidden surface. A short event may answer a later question. A small edit can change a distant reflection. The following explanations distinguish each paper's intervention from the checks needed to establish its limits.

## Compression: fewer transmitted bits at a stated reconstruction quality

An uncompressed frame stores values for its pixels. Compression replaces those values with a representation from which a decoder reconstructs them. A lossless representation reconstructs the original values exactly. A lossy representation permits differences, assessed with a specified quality measure. Compression ratio alone says nothing about how acceptable those differences are.

Screen content often contains repeated colors and sharp text boundaries. A palette records representative colors and encodes their selections. This can reduce repeated color information, but the palette, indices, and any correction data all occupy bits. A useful comparison therefore includes the entire representation, not only the shortest part of it.

<span id="explanation-dac-2026-research1334"></span>

### PEL: palette assistance improves screen-content rate only if palette overhead and reconstruction quality are counted

#### What screen-content compression is trying to preserve

An image is a grid of pixel samples. A natural image usually changes gradually because of lighting and texture. A screen image often contains large areas of repeated color, text strokes, icons and sharp vertical or horizontal boundaries. These patterns create redundancy, but they also make small errors visible: a one-pixel shift or a slight color change can alter a character edge.

Compression replaces the original samples with a coded representation and a decoder reconstructs an image from that representation. A lossless codec must reproduce the samples exactly. A lossy codec accepts an error in exchange for fewer bits, so its result must be described by a rate–distortion relationship: how many bits are used at a given reconstruction-quality level. A bitrate reduction has no meaning without the quality interval and quality measure used to obtain it.

#### What a palette enhancement changes

The PEL description adds clustering and palette processing around an unchanged JPEG XS core. Clustering groups similar pixel colors. A palette stores representative colors, and each pixel stores an index selecting one representative. Repeated colors can then be represented by short indices rather than repeating full color values.

The representation is not free. The palette itself must be transmitted or stored. Pixel indices, escape values for colors that do not fit the palette, block or tile metadata, and any conversion between the palette representation and the JPEG XS input also consume bits and processing time. The method helps when the savings in repeated color samples exceed these additions. It can be less useful on photographs, gradients, anti-aliased text or frames whose colors change rapidly.

The phrase “around JPEG XS” matters. PEL is an additional representation or preprocessing layer, not evidence that the JPEG XS transform, entropy coder or decoder has been replaced. The comparison must identify whether the reported bitrate includes the palette, indices, side information and all PEL processing, and whether the baseline uses the same JPEG XS settings.

#### What the 5H2V setting tells us

The captured card identifies 5H2V transform levels. This is a configuration of the codec's transform structure, not a complete quality result. A transform reorganizes samples so that later coding can represent their correlations more compactly. Horizontal and vertical transform choices change the spatial support of the calculation, memory access and the way edges are represented. They can also affect how much work the added palette layer sees.

A meaningful evaluation should state the component format, bit depth, chroma sampling, transform configuration, frame dimensions, rate-control settings and whether palette decisions are made per frame, region or sequence. Without those conditions, “5H2V” identifies one tested configuration but does not establish that the same gain holds for other screen resolutions or content types.

#### How to interpret BD-rate

BD-rate is a summary of the average bitrate difference between two rate–distortion curves over a shared quality range. A reported 18.13% BD-rate reduction does not mean that every frame uses 18.13% fewer bits, nor that the reconstructed screen has identical quality at every operating point. The result depends on the anchor codec, selected quality points, interpolation procedure and quality metric.

The comparison should show the curves and identify the anchor JPEG XS configuration. It should separately report text-edge quality, color error, ringing or block artifacts, lossless behavior if supported, and the bitrate of palette metadata. Screen-content tests should include documents, terminals, web pages, slides, flat-color interfaces, anti-aliased text and mixed photographic windows. Sequence identity and temporal behavior matter because a palette or clustering decision can change from frame to frame.

#### What the FPGA numbers establish

The refreshed description reports a tri-core implementation on a Xilinx ZCU106 FPGA, 4K at 120 frames/s, 19.7K lookup tables, and eight additional lines of latency. A sustained 120 frames/s rate means the implementation accepts and produces frames at an average interval of about 8.33 ms under the stated but otherwise unrecovered conditions. It does not by itself give the first-frame delay, worst-case delay, memory bandwidth, power or complete camera-to-display latency.

The eight added lines describe pipeline delay in image rows. Converting that to time requires the pixel clock, line width, blanking and buffering. Three cores may provide parallel throughput, but they also consume resources and may require inter-core buffering. Lookup-table usage is one FPGA logic-resource measure; it is not total FPGA occupancy, external memory use, power or ASIC area.

#### What correctness and deployment validation require

The decoder must reconstruct the same pixel format expected by the JPEG XS core and preserve palette-index associations under all supported blocks and transform levels. Tests should compare decoded images with the JPEG XS anchor and with the original input using the declared quality metric. They should include colors outside the palette, thin text, sharp edges, gradients, palette changes across frames, maximum-resolution frames and error or escape paths.

The evidence establishes a palette-enhancement layer, the refreshed 18.13% BD-rate claim, and the reported ZCU106 throughput/resource/delay figures. It does not establish the sequence identities, quality metric and interval behind the BD-rate number, total codec latency, power, memory traffic, worst-case behavior or generality beyond the captured screen-content conditions. The result is a bounded codec-plus-FPGA report, not a universal claim that screen compression is 18.13% cheaper or that 4K/120 implies end-to-end display responsiveness.

[Observed paper card](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research1334)

### PEL: add a screen-content representation without replacing the core codec

[PEL](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research1334) adds clustering and palette processing around JPEG XS. The refreshed description reports 18.13% BD-rate reduction on screen-content datasets with 5H2V transform levels. It also reports a tri-core implementation on a Xilinx ZCU106: 4K at 120 frames/s, 19.7K lookup tables, and eight additional lines of latency. This corrects the old card's suggestion that the throughput might only be a target. Sequence identities, quality metric, power, and complete codec timing remain missing. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1334&sess=sess130).

BD-rate summarizes the difference between bitrate–quality curves over a comparison interval. It is not a guarantee of 18.13% fewer bits for every frame or every quality setting. A frame rate measures sustained output, whereas an eight-line delay describes added pipeline latency; neither alone gives camera-to-display delay. FPGA lookup-table usage is a logic-resource count, not total memory, power, or manufactured-chip area.

## Rendering: find contributions, order them, then combine them

Gaussian splatting represents a scene with spatially extended elements carrying color, shape, and opacity. Projection determines their image-space locations. The image is divided into small rectangular tiles so work can be organized locally. An element overlapping several tiles produces several element–tile pairs. Pair generation, depth sorting, and pixel-color accumulation can therefore grow faster than the number of stored scene elements.

Opacity makes ordering important. A contribution behind an almost opaque surface has little influence on the final pixel; reversing the order can change the result. There are three separate optimization choices: reuse an earlier ordering, overlap stages of the calculation, or omit contributions judged sufficiently small. They should not be described as interchangeable ways of removing sorting.

<span id="explanation-dac-2026-research2027"></span>

### Relay-GS: reusing a previous depth order is valid only while motion preserves visibility relationships

#### What the renderer normally recomputes

In 3D Gaussian Splatting, a frame is produced from a camera pose and a set of Gaussian scene elements. Each Gaussian is projected into the image, assigned to the tiles it overlaps, ordered by depth within those tiles, and then composited using opacity and accumulated transmittance. The order controls which elements are in front and which are attenuated behind them.

For a moving camera or a changing scene, the projected position and depth of a Gaussian can change. Two elements that were separated in depth can approach or cross. A previously computed order is therefore a cached result with a validity condition; “the next frame” is not itself evidence that the order remains correct.

#### What selective reuse changes

Relay-GS reuses previous sorted results when it expects them to remain useful, selectively sorts when they do not, and periodically performs correction. This can avoid repeating the full sorting work for every frame. The method also overlaps sorting with other rendering work and shares parameters during parallel pixel processing. These are separate sources of benefit: reuse reduces repeated work, overlap hides waiting, and sharing can reduce duplicated data or arithmetic. They should be measured separately before being combined into one speedup.

The central design decision is the reuse test. It must detect enough change in projected location, depth, opacity or tile membership to decide whether an old order is still safe. A threshold that is too strict causes unnecessary sorting. A threshold that is too loose allows an invalid order to reach compositing. Periodic correction limits how long an error can persist, but it also creates extra sorting work and can produce a high-latency frame when the correction is triggered.

#### Why adjacent frames are not a sufficient condition

Small camera motion can cause a large visibility change near a depth crossing, a thin object, a disocclusion or a high-opacity boundary. A cut to a new camera pose can invalidate nearly every cached order even though it is only one frame later. Fast object motion can do the same in a dynamic scene. Conversely, a large numerical pose change in a region with no overlapping Gaussians may not require much new sorting.

The useful state variable is therefore the change in the visibility relations that the renderer relies on, not frame index or average camera displacement alone. Evaluation should include smooth motion, abrupt camera cuts, fast object motion, depth crossings, newly exposed surfaces, dense overlap and sparse scenes. It should report the fraction of orders reused, selectively resorted and corrected, along with the image-quality and frame-time consequences of each case.

#### What the performance and energy numbers mean

The official description reports 1.55–1.64× speedup and up to 16.5% energy savings against an unnamed baseline design. A 16.5% saving means energy is reduced by 0.165 of the reference amount; it is not a 16.5-fold efficiency improvement. The speedup also cannot be attributed to reuse alone unless the evaluation separates sorting, correction, overlap, shared parameters and the remaining rasterization work.

The comparison must state whether the baseline fully sorts every frame, whether both systems render the same trained scene and views, and whether the timing includes projection, tile assignment, sorting, correction, compositing, memory traffic and output. Energy must include the work used to detect invalidity and perform correction. Average frame time is insufficient for an interactive system: the worst frame and deadline-miss rate matter when correction creates bursts of work.

#### What correctness requires

Compare every reused frame with a reference that performs full sorting under the same camera, scene, precision and rendering settings. Report the numerical image difference and a task-relevant image-quality measure, not only the number of skipped sorts. The evaluation should identify whether the stated “small quality loss” is an average, maximum, perceptual or task-specific quantity, and over which scenes and views it was calculated.

The captured record supports selective sort reuse, periodic correction, pipeline overlap and parameter sharing as the proposed mechanisms. It supports the reported speed and percentage energy claims only at the level of the official description. It does not establish the reuse predicate, correction interval, scene set, quality loss, implementation process, power boundary or behavior under abrupt visibility changes. The method is a conditional temporal-reuse proposal, not evidence that sorting can generally be removed from dynamic rendering.

[Observed paper card](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research2027)

### Relay-GS: reuse ordering across nearby frames, with correction

[Relay-GS](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research2027) reuses previous sorted results through selective sorting and periodic correction. Its architecture overlaps sorting and shares parameters during parallel pixel processing. The description reports 1.55–1.64× speedup and up to 16.5% energy savings against an unnamed baseline design. It does not quantify the stated small quality loss or identify the implementation process and scene conditions. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2027&sess=sess143).

The reuse condition depends on motion and visibility, not merely on adjacent frame numbers. A useful test includes camera cuts, fast motion, and depth crossings. Correction frequency has a cost and can affect the worst frame delay. These are proposed tests, not recovered failures. The energy figure is a percentage reduction, not a 16.5-fold efficiency improvement.

<span id="explanation-dac-2026-research2036"></span>

### PipeGS: overlapping rendering stages helps only when dependencies, buffers and pipeline balance are preserved

#### What the 3DGS pipeline has to do

A 3D Gaussian Splatting renderer does not start with one rectangular matrix operation. It projects scene Gaussians into the current view, determines which image tiles each Gaussian can affect, creates element–tile work, orders overlapping elements by depth, and composites their colors and opacities into pixels. Later stages need data produced by earlier stages: rasterization cannot consume a tile before its relevant work exists, and ordered compositing cannot safely proceed before the visibility information it depends on is available.

If one stage finishes before the next can consume its output, the hardware waits. If the stages are placed in a pipeline, different frames or tiles can occupy different stages at the same time. This can increase steady-state throughput, but it does not automatically reduce the work needed for one frame or remove the storage and synchronization required between stages.

#### What a pipeline bubble means

A pipeline bubble is a time interval in which a stage has no valid work to process. Bubbles arise when a producer is late, a consumer has no buffer space, a dependency prevents safe execution, or the workload is too unevenly partitioned. “Fewer bubbles” means that more cycles contain useful stage work under the measured schedule. It does not mean that the omitted idle cycles were useful computation that has been eliminated, and it does not by itself establish a proportional reduction in frame latency.

For a pipeline with stages of durations (t_1, t_2, \ldots, t_k), the steady-state interval is constrained by the slowest stage and by any extra dependency or transfer delay. Balancing the stages can improve the interval between completed outputs. The first output still pays pipeline fill time, and a frame can still be delayed by a long tile, an empty or overloaded partition, a visibility dependency, or a buffer stall. Throughput and per-frame deadline behavior must therefore be reported separately.

#### What hierarchical reuse contributes

The PipeGS description combines hierarchical reuse with dynamic partitioning. Hierarchical reuse can preserve work or intermediate information at more than one spatial or temporal level, while dynamic partitioning assigns work to stages or processing units according to the current load. The exact hierarchy, reuse validity rule, partition granularity and hardware schedule are not exposed in the captured description.

Every reused intermediate needs a validity condition. A changed camera, scene element, tile assignment or depth relationship can invalidate data that a later stage would otherwise consume. Dynamic partitioning also has overhead: it must inspect work, decide boundaries, move or index data, and keep producers and consumers synchronized. If the decision and movement cost is large, fewer bubbles can coexist with higher total energy or lower performance on small or irregular scenes.

#### Why the reported ratios are not frame-speed ratios

The official description reports 76.2% fewer pipeline bubbles and 63% of preprocessing latency hidden. It also reports 1.96–3.34× area efficiency and 1.20–2.77× energy efficiency for a 28 nm design. Area efficiency is a performance quantity divided by area; energy efficiency is useful work divided by energy. Neither number is the same as a 1.96–3.34× or 1.20–2.77× reduction in frame time.

To interpret those ratios, the evaluation must provide the performance numerator, area denominator, energy boundary, frequency, memory system, precision, scene set and comparator implementation. It must state whether “hidden preprocessing” still consumes power while overlapping with another stage, whether external memory and control are included, and whether the 28 nm design was fabricated or only modeled. An area-efficiency gain can result from a smaller design, a larger performance numerator, or both.

#### What a complete pipeline evaluation requires

Measure first-frame latency, steady-state frame interval, tail latency, deadline misses, stage utilization, buffer occupancy, memory traffic and synchronization stalls. Break the result into projection, tile generation, sorting, rasterization, compositing, reuse checks, partitioning and output movement. Use scenes with balanced and highly uneven tile workloads, different Gaussian counts, camera motion, disocclusions and cases that invalidate reused data.

Correctness must be checked against a reference renderer using the same scene, camera, precision and visibility rule. If hierarchical reuse approximates or omits work, report image-quality error and identify whether the result is exact, bounded or empirical. A pipeline that produces frames faster but changes visibility or image quality is a different operating point, not an equivalent implementation.

The captured record supports hierarchical reuse, dynamic partitioning and concurrent 3DGS stages as a proposed pipeline design, plus the reported bubble, area-efficiency and energy-efficiency figures. It does not establish frame-time speedup, fabrication, full energy accounting, exact comparators, scene diversity, quality preservation or worst-case deadline behavior. The defensible claim is improved overlap under an incompletely specified schedule, not that the rendering computation has become proportionally cheaper.

[Observed paper card](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research2036)

### PipeGS: reduce waiting between dependent rendering stages

[PipeGS](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research2036) combines hierarchical reuse with dynamic partitioning to overlap preprocessing, sorting, and rasterization. Its description reports 76.2% fewer pipeline bubbles and 63% of preprocessing latency hidden. The 28 nm design's headline ratios are 1.96–3.34× area efficiency and 1.20–2.77× energy efficiency, not those factors of rendering speedup. Fabrication status, exact comparators, quality, and workload conditions remain unresolved. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2036&sess=sess143).

A pipeline bubble is an interval when a stage cannot perform useful work. Hiding a stage's latency means doing some of it concurrently with other work; it does not mean that the operations or energy disappear. Area efficiency needs both a performance numerator and an area denominator. A smaller design can improve that ratio without shortening one frame's latency by the same factor.

<span id="explanation-dac-2026-research2845"></span>

### AdaGScale: contribution-guided culling saves rasterization work by accepting a measurable image error

#### What a Gaussian–pixel contribution means

In 3D Gaussian Splatting, a projected Gaussian affects a region of the image rather than one pixel. For a pixel, the Gaussian's opacity depends on its projected distance from the Gaussian center and its covariance. During front-to-back compositing, the contribution is also multiplied by the transmittance left by Gaussians in front of it. A Gaussian can therefore have a nonzero mathematical contribution while having a very small practical effect on the final pixel.

The renderer still has to discover candidate Gaussian–tile or Gaussian–pixel pairs, evaluate their contribution, update transmittance and accumulate color. Large projected footprints create many candidate pairs. AdaGScale targets this work by reducing the projected extent used for tile intersection when the contribution is expected to be small.

#### What the method removes and what it keeps

Contribution-guided extent reduction is different from geometric culling. A geometrically impossible intersection can be removed without changing the rendering result. AdaGScale can remove a pair that is geometrically possible but judged too weak to matter. That is an approximation decision.

For pairs that survive, the method retains the original Gaussian parameters for the pixel calculation. This preserves the original formula for the retained work, but it cannot restore the contributions that were omitted. The total error is determined by the omitted contributions, their colors, their transmittance position and how those errors accumulate across pixels and views.

#### Why one threshold cannot have one universal meaning

A contribution threshold interacts with Gaussian scale, opacity, depth order, camera position, image resolution, tile size, scene density and background contrast. A small contribution repeated across many Gaussians can become visible. A contribution behind an already opaque surface may be safely negligible, while the same numerical contribution at a thin silhouette can alter an edge. A threshold that gives a small average error on one scene can produce a concentrated error on another.

The threshold also controls a direct tradeoff. A stricter threshold retains more pairs, increasing intersection and blending work while reducing approximation error. A looser threshold skips more pairs, reducing work while increasing the risk of missing visible structure. The evaluation should report the retained-pair fraction and error as a curve, not only the fastest selected point.

#### What the manuscript evaluation measures

The recovered manuscript evaluates five scene datasets and multiple Gaussian models on CUDA using an NVIDIA A6000. It reports up to 13.8× speedup on city-scale scenes with approximately a 0.5 dB PSNR drop. “Up to” identifies the best reported case, not the expected result for every scene. The useful comparison needs scene-by-scene latency, retained work, image quality, Gaussian count, resolution, camera views and the exact baseline configuration.

PSNR is a logarithmic measure derived from mean squared pixel error. A 0.5 dB change is not a 0.5% change in pixel error, and the same PSNR can hide different spatial error patterns. A small average error can still damage thin objects, text-like edges, high-contrast silhouettes or task-relevant regions. Report SSIM or other perceptual measures where appropriate, plus error maps and region-specific results.

#### Why the calibration boundary matters

Section 3.4 calibrates the method on training views, but Section 4.3 fine-tunes the threshold using the test dataset for equal-quality speed comparisons. This makes the reported speed point a test-view-tuned comparison rather than an untouched-test generalization result. The test images have influenced the choice of operating point, even if the final PSNR is then reported on those same views.

A deployment evaluation must choose the threshold using training or validation views only, freeze it, and evaluate previously unused viewpoints and scenes. It should separately report the threshold-selection cost, whether the threshold is global or scene-specific, and how performance changes under camera motion, higher resolution, dense overlap, thin geometry and different Gaussian optimization quality.

#### What the evidence establishes and where it stops

The manuscript supports contribution-guided reduction of the Gaussian intersection extent, exact original-parameter evaluation for surviving pairs, the A6000 implementation and the reported best-case speed/PSNR tradeoff. It does not establish lossless rendering, a universal threshold, untouched-test generalization, equal task quality or end-to-end performance beyond the evaluated rasterization path. AdaGScale is a quality-controlled approximation: its value is the measured work/error tradeoff, not the claim that low-contribution pairs are free to remove in every scene.

[Observed paper card](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research2845)

### AdaGScale: omit small contributions, with an explicit quality cost

[AdaGScale](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research2845) reduces the projected extent used for tile intersection while retaining the original Gaussian parameters for surviving pixel calculations. It is approximate, not lossless. Section 3.4 calibrates on training views, but Section 4.3 fine-tunes the threshold using the test dataset for equal-quality speed comparisons. The A6000 evaluation reports up to 13.8× on city-scale scenes around a 0.5 dB PSNR drop. That comparison is not an untouched-test-set guarantee. [Version-1 manuscript, Sections 3.3–4.3, PDF pages 4–6](https://arxiv.org/pdf/2604.18980v1#page=5).

Removing small nonzero contributions differs from removing geometrically impossible intersections. Retaining the original formula for surviving pairs does not recover omitted pairs. PSNR measures pixel error on a logarithmic scale; a dB change is not the same percentage change in error. For deployment, select the threshold without using the evaluation views, then measure both image error and frame-time distribution on previously unused viewpoints.

## Image retrieval: use spatial detail only where it helps ranking

An image embedding is a vector of learned numerical features. Text can be mapped into a compatible feature space so a similarity calculation ranks images against a request. A single vector summarizes the whole image. Several vectors can represent different image regions, helping distinguish a small requested object from the dominant background. This also multiplies comparisons and storage.

The image collection and the request are separate inputs. Work done once to prepare a largely unchanged collection is different from work repeated for each request. A complete service comparison must account for both, including any language model used to split a request into smaller descriptions.

<span id="explanation-dac-2026-research2243"></span>

### MIRAGE: use several image scales, then avoid paying for scales that no longer change the ranking

[MIRAGE](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research2243) addresses a specific conflict in multi-vector image retrieval. A whole-image vector is cheap but can hide a small object inside the dominant visual content. Splitting an image into segments exposes local objects, but each query sub-part must then be compared with many image segments. If a query has `Nq` sub-queries and an image is represented at granularity `g` by `Ng` segments, the fine-grained work grows with the number of sub-query/segment pairs. More detail therefore improves the representation while directly increasing the amount of similarity computation.

The paper's baseline multi-vector procedure uses one global query/image comparison plus one fixed image segmentation level. MIRAGE adds intermediate segmentation levels. Its score keeps the global term and, for every query sub-part, retains the largest similarity found at any examined level and segment. In plain terms, a sub-query is allowed to use the image scale at which its object is represented most usefully. A “chair” may align at a coarser level while a “keyboard” may need a finer level. The method is not claiming that one segmentation count is optimal; it searches a hierarchy because object scales vary within and across images.

### The hierarchy creates three different opportunities to remove work

First, low-ranked images can be removed as the search becomes finer. Early, coarse segments preserve enough global information for many irrelevant images to remain far below the candidates that matter. MIRAGE keeps the highest-ranked fraction after each level and does not compute later, more expensive segment comparisons for the discarded tail. This is a candidate-recall assumption: the relevant image must stay near the retained prefix while the representation is still coarse.

Second, a query need not traverse every level. Once each query sub-part has found a sufficiently good matching segment, later levels may not change the accumulated score. MIRAGE compares consecutive top-`k` lists with Kendall's tau, a statistic that measures whether two rankings preserve the same ordering. When the rank ordering exceeds a chosen threshold, the runtime exits. A stable ranking is evidence that this particular search has stopped changing under the tested representations; it is not a proof that the ranking is correct, nor does it protect against a relevant object that every examined scale represented poorly.

Third, some intermediate levels are redundant. MIRAGE calls a level “hollow” when neighboring levels capture nearly the same objects and therefore produce little new ranking information. It starts with a stride between granularities and removes levels that cause the least accuracy loss, while preventing adjacent removals so that the remaining hierarchy still provides opportunities for runtime pruning and early exit. This is an offline configuration step performed with a fixed image database and a separate validation-query split. It must not be confused with an online claim that every database can use the same hierarchy.

### The automated configuration is part of the measured method

The tunable quantities are the initial hierarchy stride, the fraction of images retained at each level, its decay rate, and the Kendall-tau early-exit threshold. MIRAGE searches these settings under latency constraints. Its simple latency model is proportional to the number of query sub-parts, the number of segments at each level, the fraction of images retained at that level, and the database size. The model treats the cost of one similarity operation as constant, so it is a search guide, not a replacement for device timing. The implementation uses PyTorch, Faiss, CUDA-event profiling, SLIC image segmentation, black padding for irregular segments, and a local Qwen3-8B model for query decomposition.

### What the reported table actually compares

The version-3 experiment uses an Intel Xeon 4410T and one NVIDIA A100-PCIE-40G. It evaluates CREPE, MSCOCO, NoCaps and Flickr after cleaning; the listed image counts are 1K, 40K, 2K and 2K, with a sampled MSCOCO subset. CLIP embeds text and images, and NDCG@10 measures how high relevant images appear in the first ten ranked positions. QPS measures retrieval throughput. The test treats each image caption as a query whose relevant image is its paired image, so the metric does not establish open-ended semantic correctness for arbitrary user questions.

On MSCOCO, POQD reaches 27.8 QPS and NDCG@10 of 68.44. The full MIRAGE configuration reaches 93.3 QPS and 70.27. Across the four datasets, the table labels the average speed comparison as 3.5× relative to POQD and the average accuracy improvement as 1.43×, or +5.03 in the paper's notation. The ablations explain the mechanism: hierarchical retrieval without optimizations is expensive; hollow-level elimination approximately doubles throughput with little accuracy loss; tail pruning increases throughput further; and early exit adds another improvement. These are results of the combined configuration and its tuned parameters, not isolated speedups attributable to one component.

The timing boundary is essential. MIRAGE does not include the Qwen3-8B query-decomposition process in its performance comparison. It measures retrieval after the query has been decomposed, while a deployed multimodal RAG request may need to pay that cost. Single-vector retrieval is still faster in the table, so the result is a tradeoff between the accuracy of global-only retrieval and the cost of the richer retrieval path. The reported scheduler overhead for rank comparison and sorting is under 0.1 ms per query in the manuscript's setup; that does not include model inference, database updates, network transfer, or downstream answer generation.

### What this establishes and what remains open

The paper supports a bounded claim: for the selected datasets, embeddings, database sizes, A100 platform, and validation-tuned parameters, multiple image granularities can improve the recorded NDCG@10 while candidate pruning and ranking-stability exit recover much of the throughput lost by multi-vector matching. It does not establish that ranking stability detects correctness, that pruning preserves recall for rare or small objects outside these datasets, or that the same thresholds transfer when the image database changes. A stronger deployment evaluation would include held-out databases or database updates, query decomposition in end-to-end latency, adversarial small-object and compositional queries, recall under aggressive pruning, memory/storage cost for all segment embeddings, and repeated runs with dispersion rather than only the reported averages.

[Version-3 manuscript, Sections 2–6, PDF pages 2–6, Algorithm 1, Algorithm 2 and Table 1](https://arxiv.org/pdf/2510.08976v3#page=5)

## Online video understanding: retention happens before the question is known

A video-language model converts visual observations into internal features and generates an answer. Attention lets a current token use information from earlier tokens. Cached keys help select relevant past information; cached values supply the associated content. Keeping every frame's cache indefinitely consumes increasing memory. Deleting features bounds memory but can discard the only evidence for a later question.

Retention and retrieval solve different problems. Retention decides what remains available before knowing the question. Retrieval chooses which retained information to use once the question arrives. Better retrieval cannot recover information already discarded. A frame-sampling rate also limits which events were observed in the first place.

<span id="explanation-dac-2026-research670"></span>

### LiveVLM: bounded video memory requires separating what is retained from what can later be retrieved

#### Why a streaming video-language model needs a cache policy

A video-language model processes visual tokens from a stream and later uses them to answer a question. Transformer attention commonly stores key and value states from earlier tokens. Keys help a new query decide which earlier positions are relevant; values contain the information that is read after those keys are selected.

If the model keeps every frame's states, memory grows with stream length. If it deletes states to maintain a fixed budget, a later question may ask about an event that was discarded. The system must therefore make a retention decision before it knows the future question. This is a different problem from retrieval, which happens after the question or current reasoning state provides a query.

#### Retention is a coverage problem, not only an importance ranking

LiveVLM balances attention scores with position-based coverage when retaining information. An attention score can identify frames or cache pages that were useful for recent model computation. Position-based coverage prevents the policy from concentrating the whole budget in one temporal region and losing the rest of a long stream.

The two signals encode different risks. Attention-only retention can discard a rare event that was not important at the time it arrived but becomes essential for a later question. Uniform position coverage can retain many frames that are irrelevant to the question. The cache budget, frame sampling rate, grouping rule and retention score jointly determine what evidence remains available. A retrieval method cannot recover an event that was never sampled or was removed from the cache.

#### What retrieval changes and what it does not change

For retrieval, LiveVLM temporarily removes positional encoding from keys, scores groups of retained information, and restores positions for subsequent reasoning. This makes the retrieval score less tied to the original position representation, so content relevance can be compared across grouped cache pages. Restoring positions before reasoning preserves the temporal information used by the model; removing it during one scoring operation is not the same as discarding temporal order from the model.

The method must preserve the association between a selected value and its original time, frame, page and spatial location. A retrieval score that finds relevant content but attaches the wrong position can change temporal interpretation. Evaluation should compare content-only retrieval, position-aware retrieval and the full restoration path, including the cost of grouping, scoring and reapplying positions.

#### What the reported experiment measures

Version 2 evaluates LLaVA-OneVision-Qwen2-7B on a 24 GB NVIDIA 4090D with a 12k-token cache. At 256 frames, the reported 1.73× improvement against ReKV concerns time to first token. Time to first token is the delay before answer generation begins; it is not the time to finish the answer, process the complete stream or meet a sustained online deadline.

The quality comparison is not uniformly favorable. Table 3 reports average accuracy of 55.6 for LiveVLM and 59.0 for CPU-offloaded ReKV. The faster first token therefore comes with a lower measured average accuracy in that comparison. A fair reading must retain both numbers and identify whether the systems use the same frame sampling, cache budget, offload policy, model precision, question set and answer-generation settings.

#### Why long-stream and rare-event tests are necessary

Average question-answering accuracy can hide the failure that matters most in a stream: a short event that occurs once and is never repeated. Evaluation should vary stream length, frame rate, event duration, event position, cache budget and question delay. It should include questions about early events, late events, transient interactions, small objects and events that were initially irrelevant to the model's running computation.

The system should report retention recall for annotated events, retrieval recall among retained events, answer accuracy, time to first token, full answer latency, memory usage and tail latency. These measurements separate three failure points: the camera or sampler never observed the event, retention discarded it, or retrieval failed to select it. They also separate a memory-saving policy from a language-model reasoning improvement.

The evidence establishes attention-plus-position retention, grouped retrieval with temporary key-position removal and restoration, the LLaVA-OneVision-Qwen2-7B/4090D/12k-token configuration, and the reported first-token and accuracy comparison. It does not establish full-answer latency, continuous-stream behavior, event retention under long horizons, equal memory/offload conditions or a quality-preserving speedup. LiveVLM is a bounded memory/latency tradeoff, not proof that a fixed cache preserves all future video evidence.

[Observed paper card](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research670)

### LiveVLM: preserve coverage, then retrieve question-relevant cache pages

[LiveVLM](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research670) balances attention scores with position-based coverage during retention. For retrieval it temporarily removes positional encoding from keys, scores groups, then restores positions for reasoning. Version 2 uses LLaVA-OneVision-Qwen2-7B, a 24 GB 4090D, and a 12k-token cache. At 256 frames, its 1.73× latency improvement against ReKV concerns time to first token. Table 3 shows lower average accuracy than CPU-offloaded ReKV: 55.6 versus 59.0. [Version-2 manuscript, Sections 3–5, PDF pages 3–6, Table 3 and Figure 8](https://arxiv.org/pdf/2505.15269v2#page=5).

Time to first token is the delay until answer generation begins, not the time to finish the answer or process a complete camera stream. Removing position information for retrieval does not mean abandoning temporal order during reasoning. A meaningful comparison needs the same sampling policy and memory/offload rules. Rare-event retention should be tested separately from average question-answering accuracy.

## Generation: decide what can be reused without assuming identical outputs

Diffusion generation repeatedly updates a noisy representation toward an output. A diffusion transformer divides that representation into tokens and applies attention and other transformations across many steps. Two opportunities differ: processing fewer tokens within a step, and reusing previous transformations across steps. Both alter computation and need output checks.

Similarity to a full-compute generated video and quality as an answer to a prompt are separate measurements. A full-compute model can itself produce an incorrect object, action, or physical interaction. High pixel agreement with that output would preserve the mistake. Conversely, a plausible alternative output can have low pixel agreement despite satisfying the request.

<span id="explanation-dac-2026-research2495"></span>

### ORBIS: token reduction helps only when the matching decision is cheaper than the attention work it removes

#### What repeated video attention computes

A diffusion transformer generates a video by repeatedly transforming a sequence of tokens. A token represents a spatial or spatio-temporal part of the noisy video representation. At each diffusion step, attention compares tokens, forms weights from those comparisons, and uses the weights to mix information. The number of comparisons grows with the number of query and key tokens, so reducing the token pairs can reduce arithmetic and data movement.

The reduction is not automatically safe. A token that appears unimportant in one step can carry a small object, a motion boundary or a detail needed several steps later. A reduced attention operation must preserve enough of the important interactions for the final video, not merely produce a similar intermediate tensor at one step.

#### What ORBIS prepares during full steps

ORBIS uses attention outputs from fully computed steps to prepare token pairs for three subsequent reduced steps. Its distribution-aware matching selects representative tokens rather than assigning each token to an arbitrary destination. The full step therefore acts as both model computation and information used to decide which later interactions can be represented more cheaply.

This creates a validity interval. The prepared pairs are useful only while the token distribution and the attention relationships remain sufficiently stable. The interval may depend on the diffusion step, the prompt, the model, the current noise state and the video content. Reusing the same pairs for three steps is a measured design choice, not a general property of diffusion transformers. A stronger evaluation would vary the reuse interval and show how matching cost, token coverage and video quality change together.

#### Why the matching engine is part of the result

Finding representative pairs requires work. The system must inspect token features or attention outputs, compute or approximate similarity, choose destinations, store pair metadata and deliver the pairs to the reduced attention hardware. That decision process can be overlapped with other work only if its inputs are ready early enough and the hardware has spare resources and buffering.

The reported negative configuration is therefore central evidence. Without the dedicated matching engine, one configuration runs at 0.3–0.6× of the reference speed. In other words, the matching work and its data movement can cost more than the attention arithmetic removed. A complete comparison must include the full-step computation used to prepare pairs, matching, pair storage, reduced attention, synchronization, token movement and output projection. Quoting only the reduced attention kernel would omit the decision that makes the reduction possible.

#### What the hardware comparison actually means

The manuscript evaluates CogVideoX at 49×480×720 and HunyuanVideo at 129×544×960. Its modeled custom hardware uses 28 nm synthesis at 1 GHz and 38 instances matched to A100 peak compute and bandwidth. The reported 3.5–4.5× speedups are therefore modeled-system comparisons against measured A100 execution, not measurements from a fabricated ORBIS chip. Matching peak compute and bandwidth does not establish equal area, memory capacity, interconnect, control cost, manufacturing cost or measured energy.

The comparison should report absolute latency and energy for the entire generation, including all full steps, reduced steps, matching, transfers and synchronization. It should state how the A100 baseline is measured, what precision and batch size are used, how many diffusion steps are run, and whether both systems produce the same number of frames at the same resolution.

#### What the quality change means

The reported CogVideoX VBench score falls from 63.95 to 63.66. That is a difference of 0.29 VBench points, not evidence of unchanged quality. The number also does not identify which VBench dimensions changed or whether the change is statistically stable across prompts and random seeds. Pixel similarity to a fully computed video is not sufficient: the full model can itself fail to follow the prompt, while a different video can satisfy it better.

Evaluation should report prompt adherence, temporal consistency, motion quality and visual quality under fixed prompts, seeds, step counts, precision and resolution. It should compare several matching intervals and token-retention levels, include prompts with small objects and rapid motion, and show the distribution of quality changes rather than only one average score.

The evidence establishes output-guided, distribution-aware token pairing for three subsequent reduced diffusion steps, the two model workloads, the modeled hardware boundary, the 3.5–4.5× modeled speed claim and the 0.3–0.6× negative configuration. It does not establish a fabricated-chip measurement, lossless token reduction, universal reuse interval, unchanged quality or measured whole-system energy advantage. ORBIS is best understood as a co-designed selection-and-attention system whose benefit depends on paying for selection efficiently.

[Observed paper card](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research2495)

### ORBIS: prepare matching decisions during full steps

[ORBIS](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research2495) uses full-step attention outputs to prepare token pairs for three subsequent reduced steps. Its distribution-aware matching chooses representative tokens rather than arbitrary destinations. Section 4 evaluates CogVideoX and HunyuanVideo. The reported 3.5–4.5× speedups compare modeled custom hardware against measured A100 execution. Without the dedicated matching engine, one configuration slows to 0.3–0.6×. Quality is not unchanged: CogVideoX VBench falls from 63.95 to 63.66. [Version-1 manuscript, Sections 3–4, PDF pages 4–6, Tables 1–2 and Figure 7](https://arxiv.org/pdf/2605.22015v1#page=6).

This negative configuration matters: a more accurate selection rule can cost more than the arithmetic it removes. Overlap depends on available execution resources, memory traffic, and when results are needed. Matching peak arithmetic throughput and bandwidth to a GPU does not establish equal chip area, manufacturing cost, or measured device energy. The software and hardware contributions need separate comparisons.

<span id="explanation-dac-2026-research2778"></span>

### ExCave: shared inversion and background-feature reuse help only when the edit does not invalidate the reused computation

#### Why image editing repeats expensive work

A diffusion image editor does not usually transform the input image directly into the edited image in one operation. It first maps the input into a latent or noisy state that the generator can continue from. The denoising process then applies many transformations conditioned on the requested edit. If every edit request starts by repeating the same inversion and recomputing features for the whole image, repeated work can dominate the time for a sequence of related edits.

The useful unit of reuse is not simply an unchanged rectangle in the output image. A feature at one position can depend on other positions through attention, convolutional receptive fields, normalization, cross-attention or later denoising steps. A region that looks unchanged may still need a new internal representation when the requested edit changes a connected object, lighting, geometry or global context.

#### What shared inversion changes

ExCave shares one inversion across multiple edits. The inversion is the computation that connects the existing image to the generator's internal trajectory. Reusing it can amortize that setup cost when the same source image receives several requests. The reuse is valid only if the starting image, preprocessing, model, latent representation and inversion settings are the same, and if the later edit procedure can safely branch from the shared state.

Sharing the starting state does not make the edits independent. Each request still changes the conditioning and may change the denoising trajectory. The evaluation must distinguish time saved in inversion from time saved in the later denoising computation, and must show whether all edits use the same number of steps, precision, resolution and guidance settings.

#### What CacheDiff is trying to reuse

The captured card describes CacheDiff as reusing features for unchanged regions, together with GPU-oriented execution changes. The intended saving is to avoid recomputing feature transformations where the edit is expected not to matter. The cache needs a dependency rule: it must identify which feature values are affected by the edit and invalidate those values, including values whose dependency is indirect.

If invalidation is too broad, the system loses the performance benefit. If it is too narrow, stale features can leak into the edited result or prevent the requested change from propagating. Cache metadata, region tests, feature copies, invalidation and cache misses are part of the method's cost. A comparison that times only the reused feature path does not measure the complete editor.

#### Preservation and successful editing are separate obligations

An editor has at least two correctness requirements. The requested change must occur, and content that the request did not target should remain sufficiently consistent. Improving one can harm the other. Reusing too much background computation may preserve pixels while suppressing a necessary global change. Recomputing everything may achieve the edit but introduce unnecessary changes elsewhere.

Evaluation should therefore partition the image into the requested edit region, protected regions and boundary regions. It should measure edit success, identity or content preservation outside the edit, boundary consistency, prompt adherence and temporal or multi-edit consistency. A single PSNR value cannot show whether the requested object changed correctly or whether the error is concentrated at an important boundary.

#### How to read the repository performance table

The author repository's Performance section reports RF-Solver/ExCave latency of 108.58/26.62 seconds and PSNR of 8.22/8.39 dB. The captured record does not establish the platform, model configuration, image set, edit prompts, number of samples, timing boundary, quality reference or whether the table corresponds exactly to the DAC manuscript. The apparent latency reduction and PSNR increase are therefore repository-reported observations with unresolved experimental scope, not independently reproducible end-to-end claims.

The official description provides no quantitative experiment. An anonymous same-title manuscript was discovered, but its identity as the DAC paper is unverified. The explanation can use the repository table as located evidence while keeping source identity and conditions open; it must not silently promote that table to a verified manuscript result.

#### What stronger validation would require

Use the same source image, edit request, model, seed, precision and output resolution for independent editing, shared-inversion editing and CacheDiff editing. Measure inversion, feature extraction, cache construction, invalidation, denoising, decoding and output transfer separately. Include edits that are local, global, overlapping, sequential and contradictory, plus changes near protected regions and edits that alter illumination or object relationships.

Compare the outputs with a full-recomputation reference and report both edit success and protected-region preservation. Report median and tail latency, memory use, cache hit and invalidation rates, and energy if an efficiency claim is made. Reproduce the repository table from a named environment before treating the numbers as a hardware or deployment result.

The evidence establishes the proposed shared-inversion and unchanged-region feature-reuse direction, the repository's located latency/PSNR table, and the source-identity limitations. It does not establish that unchanged visual regions have unchanged internal features, that edits remain faithful under global dependencies, that the repository table is the DAC result, or that the artifact provides a general latency or quality improvement. ExCave is a conditional reuse mechanism for multi-step image editing, not a guarantee that background computation can be skipped safely.

[Observed paper card](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research2778)

### ExCave: share initial inversion and unchanged background features

Editing an existing image first requires connecting it to the generator's internal trajectory. Repeating that reconstruction for every edit can introduce additional changes even in regions the user wanted to retain.

[ExCave](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research2778) shares one inversion across edits and uses CacheDiff to reuse unchanged-region features, with GPU-oriented execution changes. The [official description](https://63dac.conference-program.com/presentation/?id=RESEARCH2778&sess=sess177) gives no quantitative experiment. Its [author repository, Performance section](https://github.com/ACA-Lab/ExCave), reports RF-Solver/ExCave latency of 108.58/26.62 seconds and PSNR of 8.22/8.39 dB, but does not establish the platform and evaluation scope for that table. The repository was inspected, not run. An anonymous same-title submission was discovered; its equivalence to the DAC manuscript remains unverified.

An unchanged pixel region need not have unchanged internal features: attention can connect it to edited content. Evaluation should separate preservation outside the edit, successful modification inside it, and consistency across a sequence of user requests. More faithful preservation is not useful if the requested change never occurs. The official mechanism is therefore not a general guarantee that all background computation is unnecessary.

<span id="explanation-dac-2026-research999"></span>

### GalaxyDiT: guidance reuse must preserve the relationship between conditioned and unconditioned predictions

#### What classifier-free guidance computes

In classifier-free guidance, the diffusion model produces two predictions from the same noisy state and diffusion step. One prediction is conditioned on the text or other request, and the other is unconditioned. A guided prediction is formed by combining them, commonly as

`prediction = unconditioned + scale × (conditioned − unconditioned)`.

The difference between the two branches is therefore part of the signal that controls prompt adherence. Reusing one branch from an earlier step while freshly computing the other does not merely save one model evaluation. It changes the difference used by guidance and can change the denoising trajectory.

#### What GalaxyDiT reuses

GalaxyDiT synchronizes reuse decisions for the conditioned and unconditioned guidance calculations. It uses a model-specific proxy based on the first block to estimate whether the full transformation has changed enough to require recomputation. The first 20% of diffusion steps remain fully computed, which provides an initial reference before reuse begins. Proxy selection is calibrated with 16 prompts in the inspected manuscript.

The proxy is a cheaper measurement used to decide whether an expensive transformation can be reused. Its validity depends on correlation between first-block change and full-network change. That correlation can vary with the model, layer, diffusion step, prompt, noise state, spatial content and guidance scale. A proxy threshold that is safe for one model or prompt family is not automatically safe for another.

Synchronizing the two guidance branches avoids one obvious inconsistency, but it does not prove that reusing both branches produces the same guided prediction. The cached values can still be stale relative to the current noisy state. The evaluation must compare the guided result and final video against a full recomputation under the same seed, step count, precision and guidance scale.

#### Why the first 20% and calibration prompts matter

Keeping the first 20% of steps fully computed imposes a fixed cost and gives the system a warm-up interval. The remaining steps are not equally interchangeable: early denoising establishes broad structure, while later steps can determine fine detail and temporal consistency. The reuse interval and threshold must therefore be evaluated by step position, not only as one average over the full generation.

Calibration with 16 prompts can reveal a model-specific relationship between the proxy and full output changes, but it can also overfit the selected prompts. If calibration prompts overlap the evaluation prompts or share their distribution too closely, the measured quality loss may not represent unseen requests. A defensible protocol uses disjoint calibration, validation and evaluation prompt sets and reports proxy error across prompt types and step positions.

#### What the manuscript reports

The manuscript evaluates Wan2.1 with 1,330 VBench-2.0 prompts and Cosmos with 1,118 image/prompt pairs. Section 4 uses one A100 for the 1.3B model and Cosmos, and eight A100s for the 14B model. For the 1.3B slow configuration, Table 2 reports 1.85× while the conclusion reports 1.87×. That discrepancy should remain visible until reconciled; it is not valid to silently choose the larger number.

The VBench score changes from 56.65 to 55.68, a decrease of 0.97 percentage points. It is not a 0.97% relative decrease. The score should be accompanied by its component metrics, prompt/seed protocol, generation steps, resolution, batch size and timing boundary. A speedup measured for model execution does not by itself include prompt processing, data transfer, decoding or display.

#### What correctness and cost validation require

For every reuse decision, compare the proxy's decision with the full-network change and report false reuse and missed-reuse cases. Compare conditioned and unconditioned outputs separately, then compare their guided combination. Measure proxy computation, cache storage, invalidation, synchronization and recomputation cost as well as the denoising work saved.

Quality evaluation should include prompt adherence, motion and temporal consistency, object identity, spatial detail and VBench components. It should test different prompt complexity, camera or motion patterns, random seeds, guidance scales and reuse schedules. Pixel agreement with the full-compute output is useful for diagnosing numerical drift, but it is not an independent measure of whether the generated video follows the request.

The evidence establishes synchronized guidance reuse, a first-block model-specific proxy, the 20% full-compute warm-up, the 16-prompt calibration description, the reported workloads and A100 configurations, and the bounded speed/quality claims. It does not establish a universal proxy, exact output equivalence, a reconciled 1.85×/1.87× value, or prompt correctness from pixel agreement. GalaxyDiT is a calibration-dependent reuse method whose benefit depends on both branches remaining mutually consistent.

[Observed paper card](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research999)

### GalaxyDiT: synchronize reuse for the two guidance calculations

Classifier-free guidance combines a prediction conditioned on the request with one not conditioned on it. Reusing one from an earlier step while freshly computing the other changes the relationship between the predictions.

[GalaxyDiT](../observed-subthemes/multimedia-and-edge-systems.md#paper-dac-2026-research999) synchronizes both reuse decisions and selects a model-specific, first-block proxy for changes in the full transformation. The first 20% of steps remain fully computed; proxy selection uses 16 prompts. Section 4 times the 1.3B model on one A100 and 14B on eight. Table 2 gives the 1.3B slow variant 1.85×, whereas the conclusion says 1.87×. Its VBench score falls 56.65→55.68: 0.97 percentage points, not 0.97% relative. [Version-1 manuscript, Sections 3–4, PDF pages 3–6, Algorithm 1 and Table 2](https://arxiv.org/pdf/2512.03451v1#page=6).

A proxy is a cheaper measured quantity used to guide a decision about expensive work. Correlation with full-compute changes does not prove a bound on final video error. Evaluation should hold prompts, random seeds, step counts, and precision fixed, report proxy-calibration cost, and identify whether calibration prompts overlap evaluation. Agreement with baseline-generated pixels is not independent proof of prompt correctness.

## What these papers suggest, and what they do not establish over time

The defensible shared interpretation is that a multimedia system can save substantial work by identifying which parts of a representation remain useful. The important object differs: palette entries, sort orders, element–tile pairs, retrieval candidates, retained video features, token matches, or generation residuals. Their validity conditions also differ. Grouping all of them as caching would hide those conditions.

One long-term hypothesis is that selection quality and the cost of making selections will become as important as raw arithmetic throughput. This would be supported by comparable experiments showing that better retention, pruning, or reuse consistently improves full-task cost at fixed quality. It would be weakened by selection overhead, distribution changes, or adverse cases that erase the benefit. ORBIS's slower matching configuration already supplies a bounded example of the overhead problem; it does not establish a field-wide trajectory.

Another hypothesis is that selection decisions will need explicit lifetimes: when to refresh a sort order, invalidate an edited feature, recalibrate a ranking rule, or recompute a generation step. Useful evidence would report abrupt changes and worst cases, not only average savings on smoothly varying inputs. These are research directions derived from the mechanisms, not measured growth in adoption between conference editions.

For related mechanisms, continue to [specialized AI accelerators](../observed-subthemes/specialized-ai-accelerators.md), especially GEMM-GS, MASQ, and geometry-guided rendering; [memory and data movement](../observed-subthemes/memory-and-data-movement.md) for the cost of retaining values; and [edge, embedded, and mobile systems](../observed-subthemes/edge-embedded-and-mobile-systems.md) for the distinction between throughput and deadline behavior. The [temporal-comparison protocol](../longitudinal-protocol-v1.md) explains why this DAC-heavy selected sample cannot establish an ISCA–DAC–ICCAD trend by itself.

## Evidence still needed

This 2026-09-07 pass recovered five matching manuscripts and refreshed four official descriptions. Title/author searches did not recover matching full texts for PEL, Relay-GS, or PipeGS. ExCave's author repository and anonymous same-title discovery do not resolve final manuscript identity. Page numbers are therefore deliberately absent for those description-backed claims.

All nine reading cards below receive dated corrections, with original captured fields preserved separately. This does not reconcile the original coding used by other analyses. Final-version matching, source discrepancies, artifact execution, independent review, and comparable historical evidence remain open. The article and its formatting checks are not scientific acceptance.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1334"></span>

### PEL: A 4K@120FPS Palette-Based Enhancement Layer Validated with JPEG XS Achieving 18.13% Bdrate Reduction

DAC 2026 · Record: `dac-2026-research1334`

[Read the step-by-step explanation](#explanation-dac-2026-research1334)

**Updated source-backed reading card**

Reviewed 2026-09-07. Refreshed official description establishes reported FPGA throughput, not merely a title-level target.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Compress text-rich screen images efficiently.

**Mechanism / artifact:**

Palette enhancement around unchanged JPEG XS core.

**Workload — the work tested:**

Screen content; 5H2V transform levels.

**Hardware and manufacturing assumptions:**

Tri-core ZCU106 FPGA implementation.

**Baseline — the comparison method:**

JPEG XS; detailed anchor missing.

**Reported measurements:**

18.13% BD-rate reduction; 4K/120 FPS; 19.7K LUTs; eight added lines.

**Limits on the conclusion:**

Sequences, quality metric, power, and complete codec timing unresolved.

**Source and location**

Evidence tier: Refreshed official description. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH1334&sess=sess130)

Description, paragraphs 1–3; manuscript unrecovered.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** JPEG XS baseline

conventional enhancement layer

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1334

**Hardware or process assumptions:** Real-time video codec pipeline; memory bandwidth and implementation process are unspecified.

**Limits:** The Bdrate anchor, quality constraint, sequence set, and decoder cost are not specified.

4K@120FPS may be a target rather than a measured implementation.

Official description only; codec and hardware reproducibility is required.

**Method or artifact:** Palette-based enhancement layer integrated with JPEG XS.

**Metrics:** 18.13% Bdrate reduction is reported in the title

**Problem:** High-resolution high-frame-rate video needs compression efficiency without excessive decoding cost.

**Workload or benchmark:** 4K 120FPS video; content set, quality metric, and hardware platform are unspecified.

</details>

<span id="paper-dac-2026-research2027"></span>

### Relay-GS: Reusing Temporal Sort Information for 4D Gaussian Splatting Acceleration

DAC 2026 · Record: `dac-2026-research2027`

[Read the step-by-step explanation](#explanation-dac-2026-research2027)

**Updated source-backed reading card**

Reviewed 2026-09-07. Refreshed source supplies numerical claims while leaving implementation and quality conditions missing.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Repeated sorting in dynamic rendering.

**Mechanism / artifact:**

Selective sort reuse, periodic correction, overlapped pipeline, shared parameters.

**Workload — the work tested:**

4D Gaussian splatting; scenes unspecified.

**Hardware and manufacturing assumptions:**

Accelerator; technology and realization unknown.

**Baseline — the comparison method:**

Unnamed baseline design; full sorting for quality.

**Reported measurements:**

1.55–1.64× speed; up to 16.5% energy savings.

**Limits on the conclusion:**

No numerical quality loss or correction-frequency conditions recovered.

**Source and location**

Evidence tier: Refreshed official description. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2027&sess=sess143)

Description, paragraphs 1–3; manuscript unrecovered.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** full resort per frame

standard Gaussian splatting

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2027

**Hardware or process assumptions:** GPU or graphics accelerator with temporal scene access; memory and precision assumptions are unspecified.

**Limits:** No frame rate, image quality, memory, energy, or motion-diversity results are reported.

Sort reuse may fail under abrupt motion.

Official description only; dynamic-scene validation is required.

**Method or artifact:** Temporal sort reuse for 4D Gaussian-splatting acceleration.

**Metrics:** Rendering efficiency is claimed qualitatively

**Problem:** Dynamic Gaussian-splatting rendering repeatedly sorts temporally related primitives.

**Workload or benchmark:** 4D Gaussian-splatting scenes; sequence length, quality metric, and renderer are unspecified.

</details>

<span id="paper-dac-2026-research2036"></span>

### Pipegs: Unlocking 3DGS Pipeline Parallelism via Hierarchical Reuse and Dynamic Partitioning

DAC 2026 · Record: `dac-2026-research2036`

[Read the step-by-step explanation](#explanation-dac-2026-research2036)

**Updated source-backed reading card**

Reviewed 2026-09-07. Source distinguishes pipeline overlap from area and energy efficiency.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Rendering stages wait on dependencies.

**Mechanism / artifact:**

Hierarchical reuse, dynamic partitioning, concurrent stages.

**Workload — the work tested:**

3DGS; scenes unspecified.

**Hardware and manufacturing assumptions:**

28 nm; fabrication status unresolved.

**Baseline — the comparison method:**

Unnamed 3DGS accelerators.

**Reported measurements:**

1.96–3.34× area efficiency; 1.20–2.77× energy efficiency.

**Limits on the conclusion:**

These are not elapsed-time speedups; quality and exact comparator conditions missing.

**Source and location**

Evidence tier: Refreshed official description. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2036&sess=sess143)

Description, paragraphs 1–3; manuscript unrecovered.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** sequential 3DGS pipeline

static partitioning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2036

**Hardware or process assumptions:** Multi-stage GPU or heterogeneous pipeline; interconnect and memory assumptions are unspecified.

**Limits:** No frame rate, quality, scaling, memory, communication, or energy results are reported.

Dynamic partitioning may add synchronization overhead.

Official description only; scene- and device-diverse validation is required.

**Method or artifact:** Hierarchical reuse and dynamic partitioning for pipelined 3DGS.

**Metrics:** Pipeline efficiency is claimed qualitatively

**Problem:** 3D Gaussian-splatting pipelines have dependencies and load imbalance that limit parallelism.

**Workload or benchmark:** 3D Gaussian-splatting rendering or training; scenes, devices, and scaling are unspecified.

</details>

<span id="paper-dac-2026-research2243"></span>

### MIRAGE: Runtime Scheduling for Multi-Vector Image Retrieval with Hierarchical Decomposition

DAC 2026 · Record: `dac-2026-research2243`

[Read the step-by-step explanation](#explanation-dac-2026-research2243)

**Updated source-backed reading card**

Reviewed 2026-09-08. Reconciles the updated reading card with arXiv version 3; explains hierarchical granularity, candidate pruning, ranking-stability exit, offline hierarchy selection and the excluded query-decomposition timing boundary.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Multi-vector image retrieval improves fine-grained alignment but multiplies similarity work because each query sub-part is matched against many image segments; a fixed segmentation level also misaligns with objects of different sizes.

**Mechanism / artifact:**

MIRAGE adds intermediate image granularities, keeps the best sub-query/segment score across the hierarchy, prunes low-ranked images at later levels, exits when consecutive top-k rankings stabilize under Kendall's tau, removes redundant hollow levels offline, and tunes the hierarchy and thresholds by latency-guided search.

**Workload — the work tested:**

CREPE, MSCOCO, NoCaps and Flickr after cleaning; CLIP image/text embeddings, Qwen3-8B query decomposition, SLIC segmentation, PyTorch/Faiss implementation; Xeon 4410T with one NVIDIA A100-PCIE-40G; 1K/40K/2K/2K image counts with a sampled MSCOCO subset and caption-to-image relevance.

**Hardware and manufacturing assumptions:**

CUDA-event retrieval timing on the stated Xeon/A100 platform; image database is treated as sufficiently static for validation-query profiling and offline hierarchy selection; query decomposition by Qwen3-8B is excluded from the reported performance comparison; similarity-operation cost is simplified in the latency search model.

**Baseline — the comparison method:**

Vanilla single-vector retrieval

POQD one-shot multi-vector retrieval

MIRAGE ablations without optimization, without O1/O2, and without O1

**Reported measurements:**

MSCOCO Table 1: POQD 27.8 QPS and NDCG@10 68.44; full MIRAGE 93.3 QPS and NDCG@10 70.27.

Across CREPE, MSCOCO, NoCaps and Flickr, the table reports 3.5× average speed relative to POQD and 1.43× average accuracy improvement (+5.03 in the paper's notation); vanilla single-vector retrieval remains faster but less accurate on the reported metric.

The manuscript reports under 0.1 ms/query scheduling overhead for rank comparison and per-iteration sorting in the stated setup; this excludes query decomposition, database updates, network and downstream generation.

**Limits on the conclusion:**

NDCG@10 with caption-paired relevance is a ranking metric, not proof of open-ended semantic correctness or answer quality; stable top-k ordering is a stopping signal, not a correctness certificate.

Pruning assumes relevant images remain in the retained prefix at coarse levels; small objects, compositional queries, distribution shift and database updates may violate that assumption.

The configuration is tuned on a validation-query split with a mostly static database, and the reported retrieval timing excludes Qwen3-8B query decomposition. Storage for all segment embeddings, end-to-end service latency, repeated-run dispersion and deployment update cost remain open.

The combined result and ablations are selected-manuscript evidence; no code execution or independent reproduction was performed here.

**Source and location**

Evidence tier: Primary arxiv preprint v3 and official DAC record; selected manuscript reading, execution and independent acceptance not performed. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2510.08976v3)

Version 3: Sections 2–3 pages 2–3 for global/one-shot versus hierarchical decomposition and Eq. 3; Sections 4.1–4.4 pages 3–4 and Algorithm 1 for tail pruning, Kendall-tau early exit and hollow-level removal; Section 5 pages 4–5 and Algorithm 2 for automated configuration and latency model; Section 6 pages 5–6 and Table 1 for platform, datasets, excluded Qwen3-8B timing, QPS/NDCG results and ablations; DAC DOI 10.1145/3770743.3804297.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** static retrieval scheduling

single-vector retrieval

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2243

**Hardware or process assumptions:** CPU/GPU or memory-centric retrieval system; index and interconnect assumptions are unspecified.

**Limits:** No recall, latency, throughput, memory, update, or query-diversity results are reported.

Scheduling may depend on vector count distribution.

Official description only; workload-diverse validation is required.

**Method or artifact:** Runtime scheduler using hierarchical decomposition for multi-vector retrieval.

**Metrics:** Retrieval scheduling efficiency is claimed qualitatively

**Problem:** Multi-vector image retrieval creates irregular query work and scheduling imbalance.

**Workload or benchmark:** Multi-vector image-search queries; databases, recall targets, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research2495"></span>

### ORBIS: Output-Guided Token Reduction with Distribution-Aware Matching for Video Diffusion Acceleration

DAC 2026 · Record: `dac-2026-research2495`

[Read the step-by-step explanation](#explanation-dac-2026-research2495)

**Updated source-backed reading card**

Reviewed 2026-09-07. Full text distinguishes simulated hardware gains, slower matching ablation, and quality losses.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Video attention processes redundant tokens.

**Mechanism / artifact:**

Output-guided pairing for reduced attention steps.

**Workload — the work tested:**

CogVideoX 49×480×720; HunyuanVideo 129×544×960; VBench.

**Hardware and manufacturing assumptions:**

28 nm synthesis, 1 GHz; cycle simulation; 38 instances matched to A100 peak compute/bandwidth.

**Baseline — the comparison method:**

Measured A100-80GB; AsymRnR.

**Reported measurements:**

3.5–4.5× modeled speed; unsupported matching configuration 0.3–0.6×.

**Limits on the conclusion:**

Not fabricated-chip measurements or lossless reduction.

**Source and location**

Evidence tier: Recovered manuscript; cited sections inspected. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2605.22015v1)

Sections 3–4, PDF pages 4–6; Tables 1–2, Figure 7.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** full-token diffusion

static token pruning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2495

**Hardware or process assumptions:** GPU or specialized video-generation accelerator; memory and precision assumptions are unspecified.

**Limits:** No video quality, temporal consistency, latency, energy, or token-retention results are reported.

Output guidance may add analysis overhead.

Official description only; content-diverse validation is required.

**Method or artifact:** Output-guided, distribution-aware token reduction.

**Metrics:** Video diffusion efficiency is claimed qualitatively

**Problem:** Video diffusion has redundant tokens but token reduction can damage temporal and visual quality.

**Workload or benchmark:** Video diffusion generation; models, resolutions, frame counts, and quality metrics are unspecified.

</details>

<span id="paper-dac-2026-research2778"></span>

### Excavating Consistency Across Editing Steps for Effective Multi-Step Image Editing

DAC 2026 · Record: `dac-2026-research2778`

[Read the step-by-step explanation](#explanation-dac-2026-research2778)

**Updated source-backed reading card**

Reviewed 2026-09-07. Refreshed description resolves inversion sharing; author repository adds an explicitly underconditioned experiment.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Repeated image inversion adds error and work.

**Mechanism / artifact:**

Shared inversion, CacheDiff background reuse, GPU optimizations.

**Workload — the work tested:**

Multi-step image editing; repository uses FLUX.

**Hardware and manufacturing assumptions:**

GPU; repository timing platform unspecified.

**Baseline — the comparison method:**

RF-Solver in author README.

**Reported measurements:**

README: 108.58→26.62 s; PSNR 8.22→8.39 dB.

**Limits on the conclusion:**

Metric scope and platform missing; artifact not run; anonymous manuscript identity unresolved.

**Source and location**

Evidence tier: Author repository and refreshed official description; no verified matching full text. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://github.com/ACA-Lab/ExCave)

README Overview/Performance; DAC official Description linked in article.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** independent editing steps

single-step editing

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2778

**Hardware or process assumptions:** GPU image-generation inference; precision and memory assumptions are unspecified.

**Limits:** No visual quality, consistency metric, latency, energy, or prompt results are reported.

Consistency may trade against edit fidelity.

Official description only; content-diverse validation is required.

**Method or artifact:** Consistency-aware multi-step image-editing method.

**Metrics:** Editing consistency is claimed qualitatively

**Problem:** Iterative image editing can accumulate inconsistencies across generation steps.

**Workload or benchmark:** Multi-step image-editing models and prompts; datasets, quality metrics, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research2845"></span>

### Adagscale: Viewpoint-Adaptive Gaussian Scaling in 3D Gaussian Splatting to Reduce Gaussian-Tile Pairs

DAC 2026 · Record: `dac-2026-research2845`

[Read the step-by-step explanation](#explanation-dac-2026-research2845)

**Updated source-backed reading card**

Reviewed 2026-09-07. Full text reveals approximate omission and test-dataset tuning in speed comparisons.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Low-contribution Gaussian–tile pairs consume work.

**Mechanism / artifact:**

Contribution-guided intersection extent reduction.

**Workload — the work tested:**

Five scene datasets; multiple Gaussian models.

**Hardware and manufacturing assumptions:**

CUDA on A6000.

**Baseline — the comparison method:**

Original 3DGS, AdR-Gaussian, FlashGS.

**Reported measurements:**

Up to 13.8× city-scale speed, approximately 0.5 dB PSNR loss.

**Limits on the conclusion:**

Section 4.3 tunes on test views; not lossless or untouched-test generalization.

**Source and location**

Evidence tier: Recovered manuscript; cited sections inspected. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2604.18980v1)

Sections 3.3–4.3, PDF pages 4–6; Tables III–IV, Figure 8.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** fixed Gaussian scaling

standard 3DGS

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2845

**Hardware or process assumptions:** GPU or graphics accelerator for 3DGS; memory and precision assumptions are unspecified.

**Limits:** No rendering quality, tile count, frame rate, memory, energy, or view-diversity results are reported.

Scaling may create view-dependent artifacts.

Official description only; scene and viewpoint validation is required.

**Method or artifact:** Viewpoint-adaptive Gaussian scaling.

**Metrics:** Gaussian-tile reduction is claimed qualitatively

**Problem:** 3D Gaussian splatting can generate excess Gaussian-tile intersections from viewpoint-independent scale choices.

**Workload or benchmark:** 3D Gaussian-splatting scenes; viewpoints, quality metrics, and renderer are unspecified.

</details>

<span id="paper-dac-2026-research670"></span>

### LiveVLM: Efficient Online Video Understanding via Streaming-Oriented KV Cache and Retrieval

DAC 2026 · Record: `dac-2026-research670`

[Read the step-by-step explanation](#explanation-dac-2026-research670)

**Updated source-backed reading card**

Reviewed 2026-09-07. Revised manuscript replaces older headline and distinguishes first-token latency from answer completion.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Streaming visual cache grows without bound.

**Mechanism / artifact:**

Coverage-aware retention and position-decoupled retrieval.

**Workload — the work tested:**

Offline/online VideoQA; LLaVA-OneVision-Qwen2-7B.

**Hardware and manufacturing assumptions:**

4090D 24 GB; FP16; 12k cache, 16-token pages, 40% retrieval.

**Baseline — the comparison method:**

ReKV, Dispider, StreamMem.

**Reported measurements:**

256 frames: 1.73× first-token speedup over ReKV.

**Limits on the conclusion:**

Not full-answer latency; offloaded ReKV is more accurate on RVS average.

**Source and location**

Evidence tier: Recovered version 2 manuscript; cited sections inspected. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2505.15269v2)

Sections 3–5, PDF pages 3–6; Table 3, Figure 8.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** full-history video inference

windowed video inference

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH670

**Hardware or process assumptions:** GPU or edge video-language inference; memory and bandwidth assumptions are unspecified.

**Limits:** No task accuracy, memory, latency, energy, or stream-length results are reported.

Retrieval may omit rare but relevant events.

Official description only; long-stream validation is required.

**Method or artifact:** Streaming-oriented KV cache and retrieval for online VLMs.

**Metrics:** Online VLM efficiency is claimed qualitatively

**Problem:** Online video-language models must process continuous streams without unbounded KV-cache growth.

**Workload or benchmark:** Continuous video understanding; models, frame rates, context windows, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research999"></span>

### Galaxydit: Efficient Video Generation with Guidance Alignment and Adaptive Proxy in Diffusion Transformers

DAC 2026 · Record: `dac-2026-research999`

[Read the step-by-step explanation](#explanation-dac-2026-research999)

**Updated source-backed reading card**

Reviewed 2026-09-07. Full text exposes a speedup discrepancy and percentage-point quality changes.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Repeated video denoising is costly.

**Mechanism / artifact:**

Model-specific proxy and synchronized guidance reuse.

**Workload — the work tested:**

Wan2.1: 1330 VBench-2.0 prompts; Cosmos: 1118 image/prompt pairs.

**Hardware and manufacturing assumptions:**

One A100 for 1.3B/Cosmos; eight for 14B.

**Baseline — the comparison method:**

Full computation; TeaCache.

**Reported measurements:**

1.3B slow: Table 2 1.85×, conclusion 1.87×; VBench −0.97 percentage points.

**Limits on the conclusion:**

Pixel agreement is not prompt correctness; calibration/evaluation overlap unresolved.

**Source and location**

Evidence tier: Recovered manuscript; cited sections inspected. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2512.03451v1)

Sections 3–4, PDF pages 3–6; Algorithm 1, Table 2.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** full diffusion-transformer sampling

static proxy guidance

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH999

**Hardware or process assumptions:** GPU or video-generation accelerator; memory and precision assumptions are unspecified.

**Limits:** No visual quality, temporal consistency, latency, energy, or proxy results are reported.

Adaptive proxies may fail on unusual prompts.

Official description only; content-diverse validation is required.

**Method or artifact:** Guidance alignment and adaptive proxy for diffusion-transformer video generation.

**Metrics:** Video-generation efficiency is claimed qualitatively

**Problem:** Diffusion-transformer video generation is expensive while guidance and proxy choices affect quality.

**Workload or benchmark:** Video generation models; resolutions, frame counts, prompts, and hardware are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
