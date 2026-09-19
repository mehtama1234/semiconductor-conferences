# Approximate and precision aware compute

This subject has 14 records in the selected sample. This page explains where it fits, then presents all captured paper evidence without shortening the measurements or limitations.

[Definitions used in the paper records](../reading-guide-v1.md)

## Understand the parent subject first

- [Architecture and accelerators](../themes/architecture-and-accelerators.md)

## Why representing a number is a design decision

This chapter contains fourteen paper records, each now linked to an expanded individual explanation. That is writing coverage, not acceptance: seven explanations are manuscript-backed (HAP, DAPA, Adana, UltraSketchLLM, TopGQ, RESP, BayesCVNN), while seven remain description-backed (CORE, CAPA, CO-MAC, HierPAS, PRISM, MXP, PEACE). Full manuscripts for the latter group and independent comprehension review remain open. UltraSketchLLM has an unresolved compression-rule mismatch, and BayesCVNN has unreconciled dropout conventions in its pseudocode and selected public code. RESP is explained from its public preprint, not a recovered DAC camera-ready version.

A digital machine stores a number as a pattern of bits. A fixed number of bits permits a fixed number of different patterns. Representing a wider numerical range or finer differences between values therefore requires a choice about which values can be represented and how other values are rounded.

Fewer bits can reduce memory capacity requirements, transfer volume, and the cost of arithmetic hardware. The application may then receive a slightly different result. Whether that difference is acceptable depends on the application's required output, rather than on bit count alone.

## Precision, range, and error are different questions

Range describes how small and large a represented value can be. Resolution describes the spacing between representable values in the relevant region. A format may represent large magnitudes while poorly distinguishing small differences, or represent small differences within a limited range.

Quantization maps input values to a chosen finite set. Uniform quantization uses equally spaced levels within the selected range. A nonuniform scheme assigns levels differently, potentially using more levels where values are common or where errors matter most. The scheme also needs an implementation that can store, decode, and operate on those representations.

Consider a constructed unsigned 4-bit code with values 0 through 15 and a scale of 0.1. Decoding code 7 gives 0.7. Rounding 0.73 to code 7 loses 0.03. The scale controls spacing; the four-bit code provides sixteen possible levels. Trying to represent 2.0 exceeds the largest value, 1.5, so clamping to the maximum loses 0.5. The half-step rounding bound applies within the supported interval, not to values clipped outside it.

A zero-point shifts which integer code represents numerical zero. With the decoding rule `x = scale × (q − zero_point)`, a zero-point of 8 and scale 0.1 make code 8 represent zero and code 10 represent 0.2. Large integer codes therefore need not correspond to large real magnitudes. This distinction matters when hardware tries to skip redundant high-order bits.

Weights are model parameters used repeatedly. Activations are intermediate values computed from the current input. Compressing an already quantized integer activation without changing it is different from quantizing the original real-valued activation more coarsely. The first can preserve that integer exactly while the earlier quantization has already introduced error.

## Why one bit width can be wasteful

Different parts of a computation can tolerate different numerical errors. Applying the highest required precision everywhere may spend memory and arithmetic effort on values that do not need it. Applying the lowest precision everywhere can damage the sensitive parts.

Adaptive precision assigns representations according to a criterion such as estimated sensitivity. That introduces its own questions: how the criterion is obtained, what metadata records the choice, whether hardware supports the selected combinations, and whether the criterion remains valid on new inputs.

## What the selected papers distinguish

The HAP record proposes adaptive precision. PRISM focuses on sharing scale information for low-bit values. A scale determines how a stored numerical code maps to a value; sharing it can reduce metadata but couples the representable ranges of the grouped values. DAPA instead concerns approximation of nonlinear activation functions. These are different decisions even when all reduce inference cost.

CAPA concerns conversion between representations used in mixed-precision matrix multiplication. A method can save weight storage yet spend time converting the weights before arithmetic. Measuring only compressed size can therefore miss a cost that controls execution time. CORE and PEACE also connect numerical representation to particular arithmetic organizations. Their captured evidence below must establish the actual supported formats and comparison conditions before numerical benefits can be asserted.

These are different design decisions, not an interchangeable set of low-bit optimizations. The individual explanations below distinguish evidence from full manuscripts, evidence from official descriptions, and constructed examples. Records without individual explanations still need source and writing passes; a numerical claim in a short description alone does not establish a fair comparison.

<span id="explanation-dac-2026-research1999"></span>

## HAP: preserve quantized values while reducing the work needed to process them

### What is preserved, and what can still change

HAP applies group-wise minimum subtraction to 8-bit quantized activations, retains the offset, and protects selected weight channels at 8 rather than 4 bits. It combines this with bit-serial computation and reordering. This is the DAC manuscript, not the separately listed DATE paper. [Author-hosted DAC paper, Sections 3–4, PDF pages 2–5](https://www.ece.ualberta.ca/~jhan8/publications/DAC2026_Camera_Ready.pdf#page=2).

The central distinction is between information loss and redundant encoding. Suppose four already quantized values are [100, 103, 101, 102]. Each fits in eight bits, but subtracting their shared minimum gives [0, 3, 1, 2]. Those residuals need only two bits each. Adding 100 back reconstructs every original integer exactly. This is an explanatory example, not the paper's data.

However, if the original real value was 0.73 and the first quantization reconstructed it as 0.7, exact recovery of the integer code does not recover 0.73. “Lossless” at the re-encoding stage is not lossless inference relative to the floating-point model. Weight quantization introduces another possible source of error independently.

### Count offsets and width metadata

The four residuals above require eight payload bits. An eight-bit offset brings the total to sixteen bits before storing the residual width. If we illustratively budget three bits to describe that width, the total is nineteen bits versus the original thirty-two. The actual reduction is 40.6%, not the 75% suggested by comparing two-bit residuals with eight-bit inputs alone.

Larger groups spread metadata over more values but can contain a wider range. Adding an outlier of 250 to a group near 100 creates a residual of 150, requiring eight bits. One exceptional value can therefore raise the width for the entire group. Smaller groups may keep ranges tight while paying more offsets per value. The appropriate group size depends on the data and on the hardware's grouping cost.

HAP selects groups of sixteen and can disable the dynamic offset by layer when its cost outweighs its benefit. [Section 3.1, PDF page 3](https://www.ece.ualberta.ca/~jhan8/publications/DAC2026_Camera_Ready.pdf#page=3). This makes profiling relevant: an encoding that saves bits on calibration inputs should still be checked on different inputs and unusual activation ranges.

### The offset must participate in arithmetic

Changing the representation does not allow the computation to ignore the removed offset. For a simple dot product, let q = [100, 103] and weights w = [2, −1]. The original result is 100×2 + 103×(−1) = 97. After subtracting 100, the residual contribution is 0×2 + 3×(−1) = −3. The offset contribution is 100×(2−1) = 100. Adding both recovers 97.

Using only the residuals would be wrong. The extra work is smaller than restoring every full value only if the implementation can exploit the shared structure. It still consumes operations, data movement, and partial-result storage. The static quantizer zero-point and the dynamic group offset must also remain distinct; they arise at different stages of the representation.

### Why a lower average width does not automatically shorten execution

A bit-serial multiplier processes parts of a number over successive cycles. This can make a narrower operand take fewer cycles than a wider one. But parallel lanes that synchronize after each group wait for the longest-running lane.

Consider four independent jobs with widths [2, 8, 2, 8], processed two at a time. Pairing them in that order takes 8 + 8 = 16 cycles under a simplified one-cycle-per-bit model. Pairing [2, 2] and [8, 8] takes 2 + 8 = 10 cycles. Total useful work remains twenty bit-cycles, but available lane capacity falls from thirty-two to twenty, eliminating idle time in this idealized example.

The improvement requires legally moving work. If an activation contribution changes position, its corresponding weight and output destination must remain associated. For a dot product, swapping both activations and their paired weights preserves the mathematical sum; swapping only one side generally does not. Implementations also need sufficient accumulator range and a defined rounding policy before relying on reordered accumulation.

Perfect matches may not be available in a finite buffer. Waiting indefinitely for equal-width jobs could stop progress. HAP permits nearby widths to share a dispatch and has a fallback when matching cannot proceed. [Sections 4.3–4.4, PDF pages 4–5](https://www.ece.ualberta.ca/~jhan8/publications/DAC2026_Camera_Ready.pdf#page=4). Accepting a little idle time can be preferable to delaying the whole computation. The policy trades matching quality against buffering and forward progress.

### Protecting sensitive weights is a separate choice

Retaining some channels at higher precision can improve output quality at a storage and arithmetic cost. An average width of 4.6 bits is not a literal format in which each weight has 4.6 bits. If only four- and eight-bit values are used and overhead is excluded, `4(1−p) + 8p = 4.6` corresponds to p = 15% of values at eight bits. Channel-size weighting and metadata must be included when translating that arithmetic into a real model's footprint.

Numerical sensitivity is not necessarily determined by weight magnitude alone. A small error can affect a consequential decision; a larger error elsewhere may barely change the final output. Selection criteria are therefore proxies that need task-level evaluation. Calibration or channel ranking on one sample does not establish robustness on every future input.

### Interpret the reported evaluation

The study uses ImageNet-1K and WikiText-2 models, synthesis at 65 nm/500 MHz, and cycle simulation with modeled memory energy. The 2.65× speedup and 55% energy reduction are normalized to Stripes for HAP's 4.6-bit-weight configuration. [Sections 5.1–5.4, PDF pages 5–6](https://www.ece.ualberta.ca/~jhan8/publications/DAC2026_Camera_Ready.pdf#page=5). They are not fabricated-chip measurements or improvements over every compared accelerator by those factors.

Accuracy is not unchanged: Table 1 gives ViT-B top-1 accuracy of 84.54% for floating point and 82.98% for HAP at its more aggressive setting. OPT-1.3B with HAP+LWC has perplexity 16.01 versus 14.62 for floating point. [PDF page 6](https://www.ece.ualberta.ca/~jhan8/publications/DAC2026_Camera_Ready.pdf#page=6).

Top-1 accuracy counts examples whose highest-ranked prediction is correct; higher is better. The ViT-B difference is 1.56 percentage points. Perplexity summarizes how much probability a language model assigns to observed text; lower is better for this comparison. Thus the OPT numbers indicate degradation despite the representation and hardware benefits. Preserving quantized activation resolution must not be rewritten as preserving all model quality.

At 2.65× speedup, elapsed time is about 37.7% of baseline, a 62.3% reduction—not a 165% time reduction. Energy at 45% of baseline is a different measurement. Neither number alone determines average power, and the reported aggregate ratios should not be combined into a power claim without compatible per-workload measurements.

The conceptual result is a linked design: compact integer representations create an opportunity; offset arithmetic maintains the intended value; scheduling turns variable widths into useful parallel work. Each step can add cost. The remaining questions are model-quality tradeoffs, preprocessing and metadata costs, accumulator correctness, and behavior outside the tested workloads. No HAP implementation was executed in this pass.

<span id="explanation-dac-2026-research2094"></span>

## DAPA: approximate a function where the model actually uses it

### Start with the computation being replaced

A neural-network layer first combines numbers using weights and addition. An activation function then changes each resulting value according to a nonlinear rule. Here, nonlinear means that its slope is not constant over the whole input range. This matters because composing only linear maps and offsets produces another linear map with an offset: `W2(W1x + b1) + b2 = (W2W1)x + W2b1 + b2`. Adding more such layers alone does not escape that restriction.

GELU is one activation used in Transformers. Its output depends on both the input value and a smooth, input-dependent multiplier. Evaluating a smooth function directly can require several arithmetic operations. A piecewise-linear approximation divides the input range into intervals and uses a separate rule `y = ax + b` in each. The hardware finds the interval, retrieves its slope a and offset b, then performs one multiplication and addition. The result is cheaper to compute only after counting the interval selection and coefficient storage too.

DAPA chooses intervals using observed input frequencies, fits the lines using distribution-weighted error, and selects fixed-point precision. It also fits a backward function for training. [DAPA v1, Sections 3.1–3.2, PDF pages 3–6](https://arxiv.org/pdf/2603.19338v1#page=3). The examples below are constructed explanations, not additional measurements from the paper.

### Why equal-width intervals need not be equally useful

Suppose almost all inputs fall between −1 and 1, but the supported range extends from −8 to 8. Sixteen equal-width intervals each span one unit; only two cover the frequently used region. The design has spent most of its interval entries on values that occur infrequently.

Instead, sort a calibration sample of input values and choose boundaries at equally spaced fractions of that sample. With four intervals, choose the 25th, 50th, and 75th percentiles. Illustrative boundaries of −0.6, 0, and 0.5 divide the observations into approximately equal-sized groups even though their numerical widths differ. A region containing many observations receives a shorter interval.

This operation uses a cumulative distribution: for each candidate number x, count the fraction of observations less than or equal to x. Finding the number at which that fraction reaches one quarter gives the first boundary. No assumed Gaussian shape is required for this reasoning. Repeated identical observations can complicate exact equal-count partitions and need a tie-handling rule.

Equal population is not an optimality proof. A nearly straight function may need little precision even in a frequently visited region; a sharply bending function may need more. Boundaries based on frequency and coefficients fitted for error are two distinct decisions. Nor does calibration imply runtime adaptation: a table generated from one dataset can remain fixed while new inputs have a different distribution.

### Understand the weighted-error objective before trusting it

Consider two approximation candidates evaluated in a common region containing 90% of inputs and a rare region containing 10%. Candidate A has error magnitude 0.01 in the common region and 0.20 in the rare region. Candidate B has error 0.08 in both.

If the two regions receive equal weight, A's mean squared error is `(0.01² + 0.20²)/2 = 0.02005`; B's is 0.0064. That scoring rule prefers B. Weighting by actual frequency instead gives A `0.9×0.01² + 0.1×0.20² = 0.00409`, below B's 0.0064. The change is not arithmetic precision by itself: it changes which mistakes the fitting process is asked to avoid.

Importantly, an ordinary sample mean computed on actual activation observations already weights frequent regions more heavily through repeated observations. It should not be confused with averaging errors over an equally spaced numerical grid. Weighting observations by their density a second time can overemphasize common regions. The manuscript's sampling wording around Equation 5 leaves this distinction worth checking. [PDF page 5](https://arxiv.org/pdf/2603.19338v1#page=5).

The released vision fitting code resolves the inspected implementation case: `fast_fit_poly` uses equally spaced histogram-bin centers, with density multiplied by bin width, and solves the resulting coefficient equations. This is numerical integration with frequency weights, not density weighting of already frequency-sampled observations. [Pinned fitting implementation, lines 432–458](https://github.com/MayerUser/DAPA_Activation/blob/a2c58e0b83962cb3ea996998722b8ce35b234b5a/src_img_cls/t0_make_pwl.py#L432). Reading that code is not evidence that every experiment was reproduced.

Average function error is still not a bound on model error. Suppose the next operation multiplies an activation error of 0.01 by a weight of 100. Its contribution to the next result changes by 1. An error of 0.20 multiplied by 0.001 changes it by only 0.0002. Frequency alone does not measure downstream sensitivity. A rare input can also determine whether a particular example is classified correctly. Distribution-weighted fitting is a useful objective to test, not a guarantee of retained task quality.

### What fitting a line and quantizing it actually mean

For an interval with input samples x, fitting chooses a and b to minimize the weighted sum of squared differences between the target function and `ax+b`. Changing a rotates the line's slope; changing b shifts every output by the same amount. Neither choice requires storing a separate output for every possible x.

Suppose one fitted interval uses `y = 0.75x + 0.125`. At x = 0.5, its output is 0.5. Both coefficients happen to be exactly representable with fractional steps of 1/8. But rounding an input of 0.53 to that spacing gives 0.5, changing the line output by `0.75×0.03 = 0.0225` before any additional output rounding. A good floating-point fit does not eliminate input, coefficient, product, or output quantization error.

Increasing fractional bits reduces the spacing between representable values but does not extend the range when integer bits stay fixed. Increasing integer bits extends range but leaves fewer fractional bits under a fixed total-width budget. Intermediate products can need more bits than either operand. A hardware implementation must specify rounding, saturation, and intermediate widths, not just its external data type.

DAPA's Algorithm 1 increases fractional precision until its weighted-error threshold is met or the sixteen-bit budget is reached. [PDF page 6](https://arxiv.org/pdf/2603.19338v1#page=6). These are different exit conditions. Reaching the width cap does not logically certify that the error test passed. A reproduction should record the final error and which condition stopped the search.

### A usable training gradient is not automatically the derivative of the forward code

Training adjusts weights using derivatives: numbers describing how a small change at one point affects a later error. Within an interval, the derivative of `ax+b` is the constant a. If two neighboring lines do not meet, the forward function jumps at the boundary. If they meet but have different slopes, it is continuous there but not differentiable there in the ordinary sense.

Now separately fit a line to the derivative of the original smooth function. That new line can vary with x inside the interval, whereas the derivative of the implemented forward line is constant. Both cannot generally be the same function. A separately fitted backward rule can still support useful training, but it should be described as an approximation to the original gradient rather than an exact derivative of the forward approximation.

For a constructed example, let the forward approximation be `0.7x + 0.1` and the separately fitted backward rule be `0.2x + 0.6`. At x = 1, the latter gives 0.8, while differentiating the implemented forward expression gives 0.7. With an incoming gradient of 2, the propagated values are 1.6 and 1.4. That difference affects weight updates; whether it helps or hurts requires training evidence.

Equation 7 specifies the separate derivative fit. The inspected public vision module instead evaluates selected polynomial coefficients through an ordinary `forward` method and does not implement that separate backward rule in this module. [Manuscript, PDF page 6](https://arxiv.org/pdf/2603.19338v1#page=6); [pinned `PWLFunction` implementation](https://github.com/MayerUser/DAPA_Activation/blob/a2c58e0b83962cb3ea996998722b8ce35b234b5a/src_img_cls/m0_udanf.py). The public README scopes the release to vision inference and GPT-2 evaluation. The training result therefore remains manuscript evidence, not a training reproduction established by inspecting this inference code.

### An exponential approximation is only part of softmax

Softmax turns a vector of scores into nonnegative weights whose sum is one. Subtract the largest score from every score, exponentiate, add the exponentials, and divide each by that sum. Subtracting the same value preserves the exact normalized result while preventing large positive exponential inputs.

For scores [2, 1], shifting gives [0, −1]. Their exponentials are approximately [1, 0.368], producing normalized weights [0.731, 0.269]. If an approximation instead produces [1, 0.4], the weights become about [0.714, 0.286]. An error in one exponential affects both outputs through the shared denominator.

This is why replacing exponentiation is not replacing the entire softmax operation. The sum, division, buffering, and vector length still matter. An unconstrained fitted line can also become negative outside the fitted range, unlike the exact exponential. The inspected public `PWLSoftmax` clamps negative approximated exponentials to zero and adds a small constant to the denominator. [Pinned softmax implementation](https://github.com/MayerUser/DAPA_Activation/blob/a2c58e0b83962cb3ea996998722b8ce35b234b5a/src_img_cls/m0_udanf.py).

Those safeguards prevent some numerical failures but are not mathematically identical to exact softmax. If all approximated exponentials were clamped to zero, division with the added constant would return all zeros, not a vector summing to one. That is a boundary case to test, not an observed failure reported here. The fitted value at zero, extreme negative inputs, and masked positions deserve explicit tests.

### Separate hardware latency, resource count, and model quality

Table 4 reports fixed-point GELU latency of 320 ns versus 20 ns for DAPA, while the 16-to-1 DSP comparison uses a prior GELU design. The full DAPA-based softmax is 155 ns. Section 4.5 specifies Vitis HLS 2025.1 at 200 MHz. [PDF pages 9–10](https://arxiv.org/pdf/2603.19338v1#page=9).

A DSP here is a dedicated arithmetic block on an FPGA, not a complete processor. Reducing DSP count can leave more such blocks for other operations, but comparison logic and coefficient storage still consume other resources. The source's latency ratio is `320/20 = 16`; it must not be described as a sixteenfold whole-model speedup. Nor should its sixteenfold DSP reduction be presented as the same baseline comparison: the authors' own fixed-point GELU uses eight DSPs, so that comparison is eightfold.

Suppose activation computation occupies 10 ms of a 100 ms execution and everything else is unchanged. Making that portion sixteen times faster yields `90 + 10/16 = 90.625 ms`, or about 1.10× total speedup. Even infinitely fast activations could not exceed `100/90 ≈ 1.11×` under those assumptions. Actual overlap and data movement can change this model; the example explains why a component result needs an end-to-end measurement.

Latency is the time from an input entering a unit to its result emerging. Throughput is the sustained number of results completed per unit time. A pipelined unit can accept new inputs before earlier results finish, so dividing one by latency does not generally give throughput. At 200 MHz, one clock period is 5 ns; a 20 ns latency represents four periods, not proof that the unit accepts only one value every four periods.

Table 2 reports GPT-2 perplexity of 29.47 with joint quantized approximation versus 29.37 for its baseline. ViT-Tiny changes from 75.42% before quantization of the joint approximation to 75.17% afterward. [PDF page 7](https://arxiv.org/pdf/2603.19338v1#page=7). The first result is close but not identical; lower perplexity is better. The second difference is 0.25 percentage points, which does not match the surrounding prose's stated 0.23. Preserve that discrepancy rather than silently choosing the more favorable wording.

### What this paper adds to the subtheme, and what remains unverified

HAP and DAPA act at different points. HAP can recode an already quantized integer exactly, then exploit its reduced width. DAPA deliberately changes a function's output and asks whether the resulting model still performs adequately. The shared design question is where precision earns its cost, but their correctness arguments are not interchangeable.

A bounded research hypothesis is that measured distributions can guide both numerical representation and function approximation when the implementation exposes the corresponding savings. Testing it requires changed inputs, rare cases, calibration costs, and whole-model timing—not just average function error or a smaller arithmetic block. These two current papers alone do not establish a long-term adoption trend.

This pass inspected the manuscript and selected source files at commit `a2c58e0b83962cb3ea996998722b8ce35b234b5a`. No DAPA model evaluation, training run, or hardware synthesis was executed. Training-code correspondence, device-specific synthesis reproduction, distribution-shift behavior, and independent comprehension review remain open. [Public release and stated scope](https://github.com/MayerUser/DAPA_Activation/tree/a2c58e0b83962cb3ea996998722b8ce35b234b5a).

<span id="explanation-dac-2026-research2184"></span>

## Adana: move the densely spaced values without moving the whole numerical range

### Two different ways a group can be uneven

A group of numbers can have an asymmetric range: for example, values extending from −1 to 4 rather than equally far on either side of zero. Separately, most values can concentrate near one part of that range, such as 0.5. Matching the endpoints and allocating finer spacing near the common values are different requirements.

A uniformly spaced representation can shift its range to cover −1 through 4, but shifting does not change its spacing. A nonuniform representation can place extra levels near zero, but those levels are poorly placed if the group's values concentrate elsewhere. Adana separates a base set of integer levels from a movable set of half-step levels. [Sections 3.1–3.2, PDF pages 2–3](https://www.ece.ualberta.ca/~jhan8/publications/2026Adana.pdf#page=2).

The important concept is not that every small group must have a particular shape. A small group provides fewer observations and can differ substantially from a whole layer. The manuscript's appeal to the central limit theorem in Section 2.3 should not be treated as a proof that individual weights become Gaussian merely by placing more of them in a group. That theorem concerns suitably normalized sums or averages under conditions, not a general transformation of the underlying observations. The observed distribution is something to measure.

### Decode a small example before discussing acceleration

The paper's three-bit example has six integer levels, 0 through 5, and two half-step levels selected by a group mode m. With m = 0, the additional levels are 0.5 and 1.5; with m = 2, they are 2.5 and 3.5. There are eight levels in either case, hence eight possible three-bit codes. [Figure 3 and Algorithm 1, PDF page 3](https://www.ece.ualberta.ca/~jhan8/publications/2026Adana.pdf#page=3).

For this example, codes 0 through 5 decode to those integer levels. Code 6 denotes the first extra half-step level, and code 7 the second. Code order is therefore not numerical order: code 6 can represent a value smaller than the value represented by code 5. Treating stored codes as ordinary integers in multiplication would give the wrong result.

Using m = 2, code 6 first decodes to 2.5. With a group zero-point of 1 and scale 0.2, the reconstructed real value is `0.2×(2.5−1) = 0.3`. Changing the mode to zero makes the same code reconstruct `0.2×(0.5−1) = −0.1`. The code, mode, zero-point, and scale together specify the value. Omitting any of them can change the answer.

This calculation follows Algorithm 1's subtraction convention. The prose immediately before that algorithm says to add the zero-point, whereas the algorithm returns `u−z`. The inconsistency needs resolution in a reproduction; a reader should not infer that both conventions can be mixed within one implementation. [PDF page 3](https://www.ece.ualberta.ca/~jhan8/publications/2026Adana.pdf#page=3).

### Why format selection has to be cheaper for activations

Weights are known before an inference request, so choosing their group formats can be done ahead of execution and reused. Activations depend on the current input. Choosing their formats is part of the work required to answer that input.

A direct selection procedure tries every candidate mode, rounds every value to each mode's levels, sums the squared reconstruction errors, and chooses the smallest. With four modes and sixteen values, that requires assessing sixty-four value/mode combinations, plus the rounding and error arithmetic. Parallel hardware can reduce elapsed time by performing several assessments together, but that consumes extra circuits rather than eliminating the work.

Adana's online rule first rounds to integers and half steps, then counts half-step values absent from each candidate mode. It chooses the mode with the fewest such misses. [Algorithm 2, PDF pages 3–4](https://www.ece.ualberta.ca/~jhan8/publications/2026Adana.pdf#page=3). Counters and comparisons can replace repeated floating-point squared-error calculations because the proxy differences have a simple structure.

Consider already scaled inputs [0.48, 0.52, 1.49, 4.1]. Nearest half-step rounding gives [0.5, 0.5, 1.5, 4]. Mode zero includes both relevant half-step positions, so its miss count is zero. Mode two includes 2.5 and 3.5 instead and misses three observations. Every mode includes the integer 4, so that observation does not distinguish modes. Repeated values count repeatedly; this is a frequency-sensitive choice, not merely a count of distinct levels.

### The cheap score does not preserve every error ranking

The proxy loses information about how close an original value was to its nearest half step. That loss can change the selected mode. Here is a constructed counterexample, not a reported model failure.

Take [0.26, 0.26, 3.49, 5], padded with twelve exact zeros to form a sixteen-value group spanning the full base range 0 through 5. Nearest half-step rounding produces two instances of 0.5 and one of 3.5; the remaining values are integers. Mode zero covers the two 0.5 values and misses 3.5: one miss. Mode two covers 3.5 and misses both 0.5 values: two misses. The counting rule selects mode zero.

Now evaluate error against the first three original values. Mode zero reconstructs [0.5, 0.5, 3], giving squared-error sum `2×0.24² + 0.49² = 0.3553`. Mode two reconstructs [0, 0, 3.5], giving `2×0.26² + 0.01² = 0.1353`. The twelve zeros and the value 5 contribute zero under both modes. Dividing by sixteen gives mean squared errors of approximately 0.02221 and 0.00846. The mode preferred by the cheap score has the larger true error.

Why? Recovering a half-step value counted as one miss can avoid a large error or only a very small extra error. The counter treats those cases alike. This does not make the method useless: a cheaper decision can still deliver a favorable total hardware/quality tradeoff. It does mean that approximate selection must not be described as exact minimization of the original reconstruction error.

### Storage width and arithmetic width are not the same

After decoding and applying the zero-point, the manuscript uses five-bit fixed-point values for three-bit Adana and six-bit values for four-bit Adana. [Section 5, PDF page 4](https://www.ece.ualberta.ca/~jhan8/publications/2026Adana.pdf#page=4). The wider internal representation enables ordinary arithmetic on the decoded levels. A three-bit stored value is not automatically a three-bit multiplier input.

For intuition, represent half-step numbers by doubling them into integers. Then 2.5 becomes 5 and −1.5 becomes −3. Integer multiplication yields −15, corresponding to −15/4 = −3.75 after accounting for both operands' factor of two. The product requires its own range and fractional interpretation. Summing many products needs still more range if overflow is to be avoided.

Shared scales can be applied after a group dot product. If decoded activation values are [1, 2] with scale 0.1 and decoded weights [3, 4] with scale 0.2, the integer-domain sum is `1×3 + 2×4 = 11`; multiplying once by `0.1×0.2` gives 0.22. This avoids applying those same scales separately to both elements before multiplication.

But two groups with different scales cannot generally have their unscaled partial sums added first. If group sums are 11 and 5 with scale products 0.02 and 0.1, the result is `11×0.02 + 5×0.1 = 0.72`. Adding 11 and 5 and using 0.02 gives 0.32, which is wrong. Group boundaries must therefore remain aligned with the computation and its rescaling steps.

### Why keys and values need different grouping directions

In attention, a query is compared with each stored key by a dot product over features. Later, the resulting attention weights combine stored values across token positions. One operation sums along the feature dimension; the other sums along the sequence dimension. A grouping suitable for one need not be suitable for the other.

Adana groups keys within each key vector but groups values across the sequence. It retains an incomplete value group in FP16 and requantizes that partial group as tokens arrive. [Section 4.2, PDF page 4](https://www.ece.ualberta.ca/~jhan8/publications/2026Adana.pdf#page=4).

This creates a cost that a final compressed-cache size does not reveal. For an illustrative group of sixteen arriving values, requantizing prefixes of lengths one through sixteen processes `1+2+…+16 = 136` value instances before the group is complete, rather than sixteen. That is 8.5 times as many quantized value instances for that group's construction under this simplified accounting, not an 8.5× total-runtime claim. Parallelism, reuse, and the surrounding attention work determine actual latency. Keeping the FP16 originals also prevents this process from being confused with repeatedly quantizing previously rounded values.

### Count metadata and the quantization engine

For G values of B bits each and H bits of group metadata, effective storage is `B + H/G` bits per value. With an illustrative sixteen metadata bits and four-bit codes, groups of 128 give 4.125 bits per value, while groups of sixteen give five. The smaller groups can match local distributions better, but spend eight times as much metadata per value. These are illustrative metadata assumptions; a reproduction must verify the actual serialized fields and alignment.

The hardware also buffers incoming FP16 values to obtain the group's minimum and maximum, then scales and rounds them before encoding. A group cannot be finalized before the information needed to select its representation has arrived. Overlapping stages can improve sustained throughput while leaving a startup latency and requiring buffer capacity.

The evaluated design includes a quantization engine rather than treating conversion as free. It uses 28-nm synthesis at 500 MHz, 0.9 V, and 25°C, with modeled SRAM and cycle simulation; accelerator comparisons adjust processing-element counts to hold area constant. [Section 6.2, PDF page 6](https://www.ece.ualberta.ca/~jhan8/publications/2026Adana.pdf#page=6). This is not a measured fabricated-chip result. Equal area also means the compared designs need not have equal arithmetic-unit counts.

### Preserve the baseline and quality conditions

Section 6.2 reports 1.42× speedup and 17.91% energy reduction versus BitMod, but 3.50% higher latency versus INT-Asym. [PDF page 6](https://www.ece.ualberta.ca/~jhan8/publications/2026Adana.pdf#page=6). Thus the accelerator is not faster than every lower-bit baseline. The tradeoff includes reconstruction quality, selection cost, and arithmetic capacity.

Energy is the total expenditure over execution; power is its rate over time. The abstract's power-saving range should not be substituted for the body text's energy-reduction figures. A faster system can consume more average power yet less total energy. To convert between these claims, measurements must refer to the same workload, interval, and system boundary.

The low-bit quality comparisons also adapt earlier formats to common group sizes and joint weight/activation quantization, including attention data. [Section 6.1, PDF page 5](https://www.ece.ualberta.ca/~jhan8/publications/2026Adana.pdf#page=5). These are comparisons under the study's imposed configuration, not necessarily the original papers' best configurations.

Table 2 gives Llama-3.2-1B perplexity of 53.95 at three-bit Adana versus 9.75 at FP16. Table 6 labels its sixteen-value-group configuration “lossless,” despite changed perplexities. [PDF pages 5–6](https://www.ece.ualberta.ca/~jhan8/publications/2026Adana.pdf#page=5). Lower perplexity is better. Beating another three-bit format does not mean retaining the original model's quality, and a small task-score change does not establish exact numerical recovery. The “lossless” label must not be given the exact-integer meaning used in HAP's re-encoding explanation.

### How Adana connects to HAP and DAPA

HAP removes redundant encoding from already quantized activations and schedules variable-width arithmetic. DAPA allocates approximation effort to frequently visited parts of a function. Adana changes which values a short code can represent and makes the choice cheap enough to perform on newly computed activations. These are three separate places where data statistics influence hardware work.

The useful cross-paper hypothesis is conditional: distribution-aware choices save execution cost when their metadata, selection, conversion, and scheduling costs are smaller than the work removed, while task quality stays within an explicit requirement. It would be weakened by distribution changes, expensive partial-group updates, or a quality requirement that forces wider values. It is not yet a demonstrated long-term trend across conference editions.

No Adana model evaluation, quantizer implementation, or hardware synthesis was executed in this pass. The numerical examples check the reasoning, not the reported benchmark results. Exact encoding conventions, full simulation workloads and memory timing, selection-error incidence on real activations, and independent reader comprehension remain open.

<span id="explanation-dac-2026-research1692"></span>

## CORE: move multiplication into a cheaper representation, then count the remaining work

### What is established about this paper

The official description identifies SS-BCQ, which approximates scaling factors with sums of powers of two, and CORE, a pipelined matrix engine with block-wise activation scaling and extra processing for important weights. It reports a 3.14 perplexity reduction on OPT-6.7B relative to prior BCQ, and up to 1.41× area efficiency and 2.18× energy efficiency relative to FP–INT accelerators. It does not name those baselines or give absolute perplexity, process, clock, memory conditions, or page references. [Official CORE description](https://63dac.conference-program.com/presentation/?id=RESEARCH1692&sess=sess142).

A matching full manuscript was not recovered from the title, method-name, author, and laboratory searches in this pass. The explanation below therefore uses explicitly constructed arithmetic to explain the design problem. The examples are not verified CORE encodings, dataflow schedules, or measurements. This evidence level is weaker than the three manuscript-backed discussions above.

### Begin with one output of matrix multiplication

Matrix multiplication repeatedly computes sums of products. One output can be written as `y = x1w1 + x2w2 + … + xKwK`, where x values are activations, w values are weights, and K is the number of paired terms. Different output columns use different weights with the same input activations.

Weight-only quantization stores weights compactly while keeping activations in floating point. The stored weight code is not necessarily the numerical value to multiply. Its decoding rule, scale, and any offset must be accounted for. Small weight storage alone does not prove that multiplication uses a small integer circuit: converting each weight back to floating point can retain substantial arithmetic cost.

Binary coding offers another way to express the weight. In a constructed two-component signed representation, write each weight as `w = αb1 + βb2`, where each b is either −1 or +1. Two sign bits select among four combinations. If α = 0.5 and β = 0.25, the available weights are −0.75, −0.25, 0.25, and 0.75. These are not arbitrary four-level values; their positions are constrained by the shared coefficients.

For example, changing α to 0.6 while keeping β at 0.25 gives −0.85, −0.35, 0.35, and 0.85. Learning or choosing the coefficients changes the representable levels. More components can provide more combinations, but require more stored bits, signed sums, coefficient information, or some combination of those costs. CORE's exact coding convention remains unrecovered.

### Factor the dot product to see what disappears

When the coefficients are shared across a group, the dot product can be rearranged:

`Σ xw = α Σ(xb1) + β Σ(xb2)`.

Multiplying by a sign of +1 or −1 becomes selecting a value or its negation. The repeated general multiplications are replaced by signed additions, but the two final coefficient multiplications remain. Shared coefficients are essential to this rearrangement; arbitrary independently chosen coefficients cannot all be pulled outside one sum.

Take activations [2, 4] and weights [0.75, −0.25]. With the coefficients above, the first weight uses signs [+1, +1] and the second [−1, +1]. The direct answer is `2×0.75 + 4×(−0.25) = 0.5`. The first signed sum is `2−4 = −2`; the second is `2+4 = 6`. Combining them gives `0.5×(−2) + 0.25×6 = 0.5` again.

This two-element example establishes the algebra, not a performance advantage: it barely amortizes the extra structure. For a much longer group, coefficient operations can be shared over more values. But longer groups also constrain more weights to use the same coefficients, potentially making their reconstruction worse. Arithmetic sharing and representational flexibility can pull in opposite directions.

### Why powers of two matter, and why addition remains costly

A coefficient of 0.625 can be expressed exactly as `2^-1 + 2^-3`. Multiplying a value by it can be rewritten as adding one-half and one-eighth of that value. For 8, the result is `4+1 = 5`. In an appropriate binary representation, scaling by a power of two can be simpler than a general multiplication.

Not every desired coefficient has a short exact expansion. Approximating 0.6 by 0.625 changes a product with signed sum 10 from 6 to 6.25. The coefficient error of 0.025 is amplified by the sum. With sum −10 the error reverses sign; with sum zero it vanishes. Consequently, coefficient approximation error alone is not enough to predict the final output error.

Allowing more power-of-two terms can improve the coefficient fit while introducing more additions and more term metadata. A design needs to state the number of terms, allowed exponent range, whether negative terms are permitted, and how terms are selected. None of those details is supplied by CORE's captured description.

Furthermore, a floating-point addition is not just an integer addition on the stored bit patterns. Operands with different exponents need alignment; the result may need normalization and rounding. Power-of-two scaling can also overflow or underflow the supported range. “Shift–add” identifies a promising simplification, not zero-cost or universally exact arithmetic.

### Block scaling changes both range and reuse

A block scale places several activations into a shared numerical range. Illustratively, a signed four-bit integer range of −8 through 7 with scale 1 can represent positive values up to 7. To include 100 without clipping, the positive-side scale must be at least `100/7 ≈ 14.29`. At that scale, small positive values such as 1, 2, and 3 round to zero.

Splitting [1, 2, 3] from [100] permits a much finer scale for the first block, but requires another scale, another block boundary, and potentially another conversion or partial-sum operation. A mapping that minimizes scale operations must therefore be checked against the resolution it gives up. This example explains the tradeoff; it does not establish CORE's optimization objective or block-selection algorithm.

Reuse also depends on the workload. If one prepared activation block feeds many output columns, preparation can be amortized across those columns. If a small operation uses it only once, the same preparation cost is proportionally larger. Matrix dimensions, batch size, and reuse count belong in the evidence for acceleration, not just model parameter count.

### What “important weights” needs to mean operationally

A weight's magnitude is not a complete measure of its effect on an answer. If a weight error δw multiplies activation x, its direct contribution to the output error is `xδw`. A weight error of 0.01 produces an output error of 1 when x = 100, but only 0.0001 when x = 0.01. Correlations, later layers, and the task's decision boundary can change the consequences further.

Allocating extra processing to important weights could protect a sensitive subset without widening every operation. It also introduces selection, routing, and result-merging costs. The reader needs to know how importance is estimated, whether it changes with input, what the extra unit actually computes, and how its outputs merge with the main path. The official description establishes the existence of the extra processing, not these mechanisms.

Nor does a small number of protected weights guarantee a small latency contribution. In a constructed system where a main path processes 98% of operations at 100 operations per cycle and an extra path processes 2% at one operation per cycle, 10,000 operations require 98 cycles on the main path but 200 on the extra path. If both run concurrently and their results are required, the extra path determines completion. Distribution of work across units matters as much as the fraction assigned to them.

### Read the reported efficiency units correctly

Area efficiency divides operation throughput by hardware area. Energy efficiency in TOPS/W divides trillions of operations per second by joules per second, giving trillions of operations per joule. They are not direct measurements of token latency, total model energy, or absolute chip size.

At a fixed operation-count definition and equal throughput, 2.18× operations per joule would correspond to `1/2.18 ≈ 45.9%` as much energy per operation, a 54.1% reduction. It is not a 118% energy reduction. However, that conversion cannot establish whole-model savings when preprocessing, memory transfers, idle periods, or altered operation accounting are excluded.

For binary-coded execution, operation accounting is particularly important: one nominal model multiply may become several signed additions and scaling terms. Comparing reported TOPS requires knowing whether the numerator counts original model operations or physically executed arithmetic. Changing that convention can change the ratio without changing time or energy.

Similarly, the reported 3.14 perplexity improvement is an absolute difference from an unspecified prior BCQ result. Without the starting and ending values, it does not yield a percentage reduction or establish closeness to the unquantized model. The two efficiency figures are reported maxima; they need not occur on the same configuration or workload.

### What this adds, and what still needs evidence

CORE concerns how compressed weights participate in arithmetic while activations remain a separate representation problem. Adana instead describes a jointly low-bit group format with runtime activation selection. DAPA changes nonlinear functions rather than the dot-product representation. These distinctions prevent “low precision” from hiding incompatible execution assumptions.

A useful hypothesis is that removing an expensive arithmetic primitive helps only when its replacement has sufficiently low addition, scaling, routing, and memory costs at the required model quality. CORE's description motivates testing that hypothesis but does not yet establish its full conditions. No CORE implementation, benchmark, or synthesis was executed. A manuscript-backed rewrite still needs exact coefficient rules, activation mapping, important-weight handling, absolute quality, named baselines, and page-located hardware measurements.

<span id="explanation-dac-2026-research2410"></span>

## CAPA: the accumulator and format boundaries matter as much as the multiplier

### What the paper-specific evidence establishes

CAPA's official description identifies Hybrid Delta Block Floating Point (HDBFP), an integer-based format intended to reduce partial-sum overhead while supporting BF16/FP16, and weight decomposition for INT8/INT4 arithmetic. It reports matching GPU accuracy and 3.98× area efficiency and 4.38× power efficiency relative to an FP–FP baseline. Models, accuracy values, hardware conditions, and detailed format rules are absent. [Official CAPA description](https://63dac.conference-program.com/presentation/?id=RESEARCH2410&sess=sess142).

The author's laboratory lists the paper, but a matching full manuscript was not recovered in this pass. [DATES publications](https://sites.google.com/yonsei.ac.kr/dates/publications). The following worked examples explain the underlying engineering questions, not verified HDBFP layouts or CAPA schedules. No PDF-page claims are made from a conference description.

### A partial sum is a value that must survive until the output is complete

To compute one matrix-multiplication output, a machine multiplies pairs of values and adds the products. If it processes only some pairs at a time, it retains their sum and adds subsequent products later. That retained value is a partial sum. An accumulator is the hardware that stores and updates it.

Suppose an output is `2×3 + 4×5 + 6×7`. After the first product the partial sum is 6; after the second it is 26; after the third the completed output is 68. Keeping only the most recent product would lose earlier contributions. Spreading the work across cycles or processing units therefore requires a place to retain or merge partial results.

Short operands do not imply that a short accumulator is safe. Signed four-bit integers range from −8 to 7. The product of −8 and −8 is 64. Summing 256 such products gives 16,384. A signed fifteen-bit accumulator has maximum 16,383, so it overflows even though every input fits in four bits. Sixteen signed bits can hold this particular worst-case sum. Real formats also need to account for fractional precision, scales, and any later accumulation beyond those 256 terms.

Cancellation does not eliminate intermediate-range requirements. Adding a large positive subtotal and an equally large negative subtotal can produce a small final answer, but both subtotals must be represented first. It is unsafe to size the accumulator only from the final output observed on typical inputs.

### Why partial sums can dominate storage and movement

Consider a constructed engine holding a 64-by-64 output tile. It needs 4,096 partial sums. At thirty-two bits each, that is 16 KiB; at sixteen bits each, 8 KiB. This says nothing yet about whether sixteen bits are accurate enough, but it shows why the accumulator representation affects more than the arithmetic circuit.

If those thirty-two-bit partial sums are written to memory and read back between chunks of computation, one full write/read round transfers 32 KiB. Repeating such rounds can consume bandwidth and energy even when weights are stored at four bits. Keeping sums in local registers avoids that memory traffic but spends register capacity and wiring instead. A claimed reduction in partial-sum overhead should identify which of these costs was actually reduced.

Parallel execution adds another issue: each unit may produce its own partial result. Their numerical scales and formats must be compatible at the merge point. Counting only independent multiply throughput omits the work needed to turn those results into one correctly scaled output.

### What sharing an exponent buys, and what it can lose

A floating-point value combines a significand with an exponent: the significand supplies digits, and the exponent sets their numerical scale. A block-floating representation shares one exponent across a group. The individual stored significands can then be handled with common-scale integer arithmetic, provided alignment and range are controlled.

In a deliberately simplified block format, let each signed four-bit integer q reconstruct as `q×16`. This can represent 64 as q = 4, but values 1 and 1.125 both round to zero. A smaller scale would resolve those small values better but might no longer fit 64. The shared exponent makes range and resolution a group-level decision.

Splitting groups by numerical range, recording local exponent differences, or keeping extra precision can reduce that loss in possible designs. Each option adds metadata or conversion work. The words “Hybrid Delta” in HDBFP's name do not establish which fields CAPA uses, how many bits they have, or when they change. Those details must come from its manuscript or implementation, not from interpreting the acronym.

If an accumulator's scale changes during a calculation, its old contents also need conversion. Suppose the retained sum is 12 at scale 1. Changing to scale 4 makes that value integer code 3 exactly. A retained sum of 13 instead rounds to code 3 and reconstructs 12. Later updates now start from a value with error −1. Choosing a new exponent is therefore not just relabeling bits.

### Supporting two floating-point formats is more than accepting sixteen bits

BF16 and FP16 are both sixteen-bit floating-point representations, but allocate their bits differently between range and precision. The same sixteen stored bits cannot generally be reinterpreted as the same numerical value in both formats. Supporting both requires a defined numerical conversion, not merely a sixteen-bit input connection.

An implementation must handle sign, exponent interpretation, significand precision, rounding, overflow, very small values, and exceptional values. It must also state whether multiplication and accumulation use the input format or a wider internal format. A result converted back to sixteen bits can conceal the extra width used while computing it.

For a concrete general rounding example, suppose an internal format resolves increments of 1/8, while an output format resolves increments of 1/2 in the relevant range. Converting 1.125 to the coarser format can produce 1.0. Converting it back cannot restore the lost 0.125. A round trip that is valid as a numerical approximation is not necessarily reversible.

This makes conversion placement important. Converting once at a block boundary and retaining the internal format can cost less than converting after every addition. But delaying conversion may require wider registers and wider interfaces. The efficient location depends on how often data is reused and where the next consumer needs a different format.

### Decomposing an eight-bit weight into smaller pieces

An eight-bit integer can be written using a high part and a low part. For an unsigned example, `45 = 16×2 + 13`, so `x×45 = 16×(x×2) + x×13`. The two smaller products can be computed separately and then combined with the appropriate shift. This illustrates how a smaller multiplier can contribute to a larger-width operation.

Signed values require particular care. For signed eight-bit two's-complement data, a valid decomposition uses a signed high four-bit part and an unsigned low four-bit part. For −19, the high part is −2 and the low part is 13: `16×(−2)+13 = −19`. Treating the low bit pattern 1101 as signed −3 instead gives −35, which is wrong.

If the hardware's small multiplier accepts only signed four-bit operands, the unsigned low part may need a correction or another representation. The description does not specify CAPA's solution. This example establishes why saying “two four-bit multiplies” is incomplete without signedness, shifting, correction, and accumulator rules.

Decomposition also does not double useful capacity for free. If each eight-bit product occupies two smaller multipliers, those multipliers cannot simultaneously serve two independent four-bit products. Mixed-precision scheduling needs to allocate units according to actual decomposition cost, while accounting for the combining additions and output routing.

### Matching a task score does not prove bitwise-identical arithmetic

Two implementations can classify the same examples correctly while producing different intermediate values or final scores. If one predicts scores [0.8, 0.2] and another [0.7, 0.3], both choose the first class, despite their numerical difference. Accuracy can match even when the computation does not match bit for bit.

That distinction matters for the description's GPU-accuracy claim. Its evidence does not specify whether “identical” means a task metric, output agreement within a tolerance, or exact numerical equality. Until the evaluation is recovered, it must not be used as a universal arithmetic-correctness guarantee. A close decision boundary, cancellation-heavy sum, or extreme activation could expose differences that an average task score misses.

The efficiency claims likewise need their denominators. Area efficiency compares useful throughput per area; power efficiency generally relates throughput to power, but the description does not provide its explicit units. A 4.38× improvement is not automatically a 4.38× reduction in whole-model energy or a 4.38× speedup. Weight loading, format conversion, partial-sum movement, and idle cycles must be included consistently before making that inference.

### The cross-paper question this makes visible

CORE focuses on replacing multiplication with structured signed sums and cheaper scales. CAPA focuses on the representation and compatibility of the values being accumulated and on reuse of smaller arithmetic units. Adana explicitly decodes compact codes into wider fixed-point arithmetic. These approaches all challenge the assumption that storage bit width alone predicts compute cost.

A useful hypothesis is that intermediate-state representation becomes increasingly important after operand compression makes weight storage cheaper. To test it, measure accumulator capacity, partial-sum traffic, conversion work, and full-output completion alongside multiplier area. It remains a hypothesis, not a demonstrated historical trend from these descriptions.

No CAPA implementation, benchmark, or synthesis was executed. The open work is to recover HDBFP's exact fields and conversion rules, the signed decomposition mechanism, actual model-quality measurements, baseline configuration, and page-located hardware results. The conceptual explanation is expanded; the paper-level evidence remains incomplete.

<span id="explanation-dac-2026-research2317"></span>

## UltraSketchLLM: share stored values, reconstruct weights, and account for both stages

### Less than one bit is an average, not a fractional physical bit

If every weight independently chooses between two values, its choice requires one bit. A representation can go below one bit per original weight by removing that independence: several original positions share stored information, and a rule reconstructs their values. The resulting model cannot represent every possible independent assignment of the original weights.

For a constructed example, store one four-bit value for every eight original positions and determine the mapping without a per-position index. The payload is four bits divided by eight positions, or 0.5 bit per original weight. This says nothing about metadata, uncompressed parameters, reconstruction buffers, or whether the resulting weights are accurate enough.

UltraSketchLLM combines one-eighth sketch storage with four-bit quantization for its nominal 0.5-bit setting. The DAC version is arXiv v2, not the earlier differently titled v1. [Section 4.1, PDF page 5](https://arxiv.org/pdf/2506.17255v2#page=5); [version history](https://arxiv.org/abs/2506.17255). This is lossy compression, not a way to store arbitrary independent values without losing information.

### What a sketch stores when several weights collide

A sketch maps each original weight position to a smaller table. A hash is a repeatable rule that computes a table location from that position. Two weights collide when their positions map to the same table entry. Compression then needs a rule for deciding what that shared entry retains.

The manuscript's AbsMaxMin rule keeps the signed value with minimum absolute magnitude in each bucket. Multiple independent rows provide different collision patterns, and retrieval chooses among the row candidates. [Section 3.1, PDF page 3](https://arxiv.org/pdf/2506.17255v2#page=3).

Consider a target weight 0.8. In one row it collides with 0.2, so the bucket retains 0.2. In another it collides with 0.6, so the bucket retains 0.6. Choosing the candidate with greatest absolute magnitude gives 0.6, closer to 0.8 than 0.2. If one row has no smaller-magnitude collision, that row can preserve the original value. More rows create more opportunities for such a candidate, but consume more storage or divide a fixed storage budget into narrower rows.

The magnitude property follows directly from the update rule before any later scalar quantization: each bucket containing the target retains a value whose magnitude is no larger than the target's. Choosing any of those candidates cannot exceed the target's magnitude. That is not the same as preserving its sign or guaranteeing small relative error.

For example, a target +0.8 can collide with −0.6 and reconstruct as −0.6. The reconstructed magnitude is smaller, yet the absolute error is 1.4 and the relative error is 175%. Underestimating magnitude is therefore not a task-quality guarantee. Additional quantization can change the bound again if it rounds a stored magnitude upward.

### The paper and loaded kernel disagree on the compression rule

The manuscript's Equation 4 specifies minimum absolute magnitude, but Algorithm 1 on page 4 uses a greater-than comparison that selects a maximum. Equation 7 also mixes a binary-matrix declaration with infinity for unmapped positions. These are consequential implementation details, not merely interchangeable notation. [PDF pages 3–4](https://arxiv.org/pdf/2506.17255v2#page=3).

The public wrapper at commit `ab69c9aeaa60ebc57618bfb66a056fb8eaec18ee` loads `matrix_mul_max.cu`. That kernel starts from zero and retains the candidate with greatest absolute magnitude. It therefore follows a maximum-magnitude rule on the inspected matrix-compression path, not the minimum-magnitude update described in Section 3.1. [Wrapper](https://github.com/suenar/UltraSketchLLM/blob/ab69c9aeaa60ebc57618bfb66a056fb8eaec18ee/src/sketch_matrix_ops.py); [loaded kernel](https://github.com/suenar/UltraSketchLLM/blob/ab69c9aeaa60ebc57618bfb66a056fb8eaec18ee/src/matrix_mul_max.cu).

A two-value bucket makes the difference clear. With [0.2, 0.8], minimum-magnitude compression stores 0.2 and maximum-magnitude compression stores 0.8. Reconstructing the first original position then either preserves 0.2 or increases it to 0.8. The latter is incompatible with the manuscript's underestimation argument for that position.

This is static code evidence, not an executed failure or proof of which revision produced the published results. A reproduction must identify the intended rule, signed retrieval convention, empty-bucket behavior, and matching experimental code before treating the theoretical and implementation claims as one verified result.

### A matrix representation changes access order, not the need to select values

The mapping can be represented as a matrix with one selected destination per input position. Suppose three positions map to buckets [0, 1, 0]. A zero/one mapping matrix has rows [1, 0], [0, 1], and [1, 0]. If bucket values are [0.2, 0.5], multiplying them by the matrix transpose reconstructs [0.2, 0.5, 0.2]. The same stored value is reused at both positions assigned to bucket zero.

That reconstruction uses ordinary selection expressed as multiplication and addition. Compression with a minimum-magnitude rule does not use an ordinary sum: a bucket receiving 0.2 and 0.8 must retain 0.2, not add them to obtain 1.0. It requires a different reduction operator or a custom kernel.

Nor can a minimum reducer simply treat unmapped positions as zeros: zero would beat every nonzero mapped candidate. It must exclude those positions or use a suitable sentinel, with explicit handling for genuine zeros and non-finite values. Conversely, zero-filled selection can work naturally with a maximum-magnitude reduction, which is another reason the min/max discrepancy matters.

Regular matrix operations can execute efficiently on a GPU despite doing more nominal operations than direct indexed loads. They can offer predictable access and parallel work. But a dense mapping matrix still occupies memory even if its values are mostly zero. Its generation and reuse must be included when assessing the system.

### Count the group rounding, projection cache, and temporary weights

For the paper's group size G = 512 and sketch ratio α = 1/8, its formula `K = ceil(αG)+1` gives 65 stored entries per group. If each is actually packed into four bits, the group payload is `65×4/512 = 0.5078125` bits per original weight, before scale and other metadata. The nominal 0.5-bit figure is not an exact accounting of all bytes. [Section 3.3, PDF pages 4–5](https://arxiv.org/pdf/2506.17255v2#page=4).

An illustrative dense 512-by-65 projection matrix stored as four-byte floating-point values occupies 133,120 bytes, or 130 KiB. Sharing it across many layers amortizes that cost; using a different configuration or seed can require another matrix. “Index-free” means avoiding a stored index for every weight, not that the mapping mechanism has zero memory cost.

The paper reconstructs a layer's weights, computes with them, and releases them before continuing. Its weight-memory model includes persistent sketches plus the largest reconstructed layer. [Section 3, PDF page 3](https://arxiv.org/pdf/2506.17255v2#page=3). Activations, cached attention data, framework workspace, and allocator behavior must be added for a full peak-memory measurement.

Suppose original weights occupy 16 GiB across thirty-two equal layers. A nominal 0.5-bit representation of originally sixteen-bit weights occupies 0.5 GiB, but the temporary full layer adds another 0.5 GiB. That is already 1 GiB before the other memory categories—not 0.5 GiB. Unequal layers can raise the temporary maximum, and retaining reconstructed weights across tokens changes the memory/latency tradeoff.

The inspected `SketchLinear.forward` reconstructs `_full_weight`, calls ordinary linear computation, and clears that reference afterward. It also caches projection matrices and includes synchronization and cache-clearing calls. [Pinned inference implementation](https://github.com/suenar/UltraSketchLLM/blob/ab69c9aeaa60ebc57618bfb66a056fb8eaec18ee/src/sketch.py). This supports the existence of reconstruction work; it does not independently verify the paper's peak-memory or latency measurements.

### Four-bit numerical simulation is not necessarily four-bit storage

Fake quantization rounds values to a low-bit grid but can retain them inside ordinary floating-point tensors. Sixteen possible numerical levels do not force a library to pack each element into four physical bits. A floating-point tensor holding those levels can still use four bytes per element.

The public export path applies `fake_quant` and returns stacked sketch tensors; the inspected C++ binding accesses float pointers. These files do not establish a packed four-bit exported representation. [Export path](https://github.com/suenar/UltraSketchLLM/blob/ab69c9aeaa60ebc57618bfb66a056fb8eaec18ee/src/fake_sketch.py#L540); [binding](https://github.com/suenar/UltraSketchLLM/blob/ab69c9aeaa60ebc57618bfb66a056fb8eaec18ee/src/sketch_matrix.cpp).

At 65 float32 entries per 512 weights, that tensor payload would be `65×32/512 = 4.0625` bits per original weight, eight times the corresponding four-bit-packed payload. This is conditional byte accounting for the inspected representation, not a measured checkpoint size or proof that no separate packing path exists. Packing, scales, exported dtype, and load-time unpacking all need verification.

### Why training still retains many more parameters than inference

Compression-aware training computes with reconstructed weights so that updates can adapt to compression error. A straight-through estimator sends an approximate gradient through a discrete operation whose ordinary derivative would not provide useful updates. It does not make the discrete reconstruction exactly differentiable.

For a scalar illustration, a rounded forward output may remain unchanged as the underlying weight moves from 0.21 to 0.22. Its local derivative can be zero, but a straight-through rule can pass the incoming gradient as if the operation had derivative one. This permits updates to the original weight while accepting a biased approximation to the true derivative.

UltraSketchLLM retains the original trainable parameters during fine-tuning and uses activation-based importance to allocate sketch space. [Section 3.2, PDF pages 3–4](https://arxiv.org/pdf/2506.17255v2#page=3). Therefore inference compression must not be advertised as the same reduction in training memory: gradients, optimizer state, and original trainable weights can remain large.

Importance based on mean squared activation has a clear local motivation. If output error from one weight perturbation is `aδw`, its expected square is `E[a²]δw²` when δw is fixed. But multiple errors introduce cross terms involving correlations between activations. Ranking each component independently does not fully predict their combined effect, and a changed input distribution can change that ranking.

### Interpret the evaluation without conflating its metrics

The study evaluates Llama and Qwen models, fine-tunes on two A100 GPUs with context length 512, and compares against AQLM and VPTQ. It reports up to 6.93× peak-memory reduction relative to FP16 and a 14.9× maximum sketch-operator speedup against the hash implementation. [Sections 4–4.2, PDF pages 5–6](https://arxiv.org/pdf/2506.17255v2#page=5).

The 14.9× result is not a 14.9× speedup over an uncompressed language model. Figure 11 labels decompression time, while adjacent prose sometimes says compression; that scope should be retained as an unresolved wording issue. Figure 10 concerns first-token latency overhead, not a complete long-output decoding-throughput curve. [PDF page 6](https://arxiv.org/pdf/2506.17255v2#page=6).

The paper also multiplies perplexity by average bit count into a combined metric. That metric deliberately trades quality against storage. In a constructed comparison, perplexity 40 at 0.5 bit gives product 20, while perplexity 10 at four bits gives product 40. The compressed model wins the product metric despite having four times the perplexity. The product is not evidence that language-model quality improved; perplexity, downstream accuracy, and measured memory must remain separately visible.

### What can be carried into the broader theme

HAP preserves an already quantized integer during re-encoding; UltraSketchLLM ties different weight positions to shared information and reconstructs an approximation. Both can reduce stored bits, but only the former's local exactness argument applies to its integer re-encoding stage. UltraSketchLLM additionally makes reconstruction placement a central memory-system decision.

The testable longer-term hypothesis is that increasingly compressed models shift cost from persistent weight storage toward reconstruction, mapping metadata, and temporary state. Evidence for it requires measured total memory and end-to-end execution at a fixed quality requirement. Nominal bits per weight alone cannot establish that trend.

No UltraSketchLLM model evaluation, CUDA kernel, or training run was executed. This pass inspected the DAC manuscript and selected files at the pinned commit. The min/max mismatch, signed retrieval, packed-storage path, complete workload conditions, and independent reproduction remain unresolved; the arithmetic examples explain why those gaps matter.

<span id="explanation-dac-2026-research3214"></span>

## TopGQ: use graph structure to choose scales without repeatedly scanning activations

### Start with what a graph neural network computes

A graph contains nodes and edges. Each node has a feature vector: numbers describing that node. A graph neural network transforms those numbers and combines information from neighboring nodes. After several layers, a node's representation can depend on increasingly distant parts of the graph.

In a simple layer, first multiply each feature vector by a learned weight matrix. Then aggregate the transformed vectors according to the graph's edges. An adjacency matrix records which nodes contribute to which other nodes and with what coefficient. If one node averages transformed scalar values 2 and 20 from two neighbors, the result is `0.5×2 + 0.5×20 = 11`.

Different neighborhoods can produce very different activation ranges. A node receiving many large positive messages can accumulate a large value. Another may receive smaller values or contributions that cancel. Assigning both the same numerical scale can waste resolution on the smaller range. The graph structure can help predict these differences, but features and learned weights still matter.

TopGQ combines node-sensitive scaling with a graph-derived lookup index, TopPIN. It calibrates an already trained model rather than retraining its weights. [Sections 3–4, PDF pages 3–4](https://arxiv.org/pdf/2608.30394v1#page=3). The examples below explain the method's arithmetic and limitations; they are not additional benchmark results.

### Why the axis of a scale matters

For a dot product `Σ a_j x_j`, a scale shared across all x values can be moved outside the sum. If `x_j = s q_j`, then the result is `s Σ a_j q_j`. One final multiplication restores the scale.

But if every source node has its own scale s_j, the sum becomes `Σ a_j s_j q_j`. Those scales vary with the index being summed. There is no single scale that can generally be factored out. Discarding that variation gives a different computation.

Using the two-neighbor example, represent 2 as code 1 with scale 2, and 20 as code 1 with scale 20. Averaging the two codes gives 1. Applying scale 2 afterward gives 2, while applying scale 20 gives 20. Neither gives the correct result 11. A scheme that is convenient for representing each node can therefore be inconvenient for the aggregation arithmetic.

This is the difference between an inner scale, which varies over the summed dimension, and an outer scale, which is fixed for one output row or column. Standard integer matrix multiplication can sum integer products efficiently; a different floating-point scale for every product interferes with that simple execution path.

### Move the scales into the adjacency values

TopGQ rewrites aggregation as `A X = (A S)(S^-1 X)`, where S is a diagonal matrix of node scales. Multiplying by S scales the columns of A; multiplying X by its inverse scales the rows of X. The two changes cancel in exact arithmetic when the scales are nonzero. [Equations 6–8, PDF page 3](https://arxiv.org/pdf/2608.30394v1#page=3).

For the averaging example, A is [0.5, 0.5], X is [2, 20], and the chosen scales are [2, 20]. The transformed features are [1, 1]. The transformed adjacency coefficients are [1, 10]. Their dot product is still `1×1 + 10×1 = 11`. The unequal scales have not disappeared; their effect has moved into the other operand.

After that exact rearrangement, TopGQ quantizes the transformed adjacency row-wise and the transformed feature matrix feature-wise. These outer scales can be applied after integer multiplication. The representation choice separates local node normalization from the scales needed by the matrix engine.

The exact identity does not make the quantized version exact. If transformed adjacency coefficient 10 rounds to 9 in a constructed coarse representation, the example's answer becomes 10 instead of 11. Improving the feature range can make the adjacency range harder to represent. TopGQ therefore chooses between dual-axis absorption and feature-wise quantization per layer using calibration error. [Sections 4.1–4.2, PDF pages 3–4](https://arxiv.org/pdf/2608.30394v1#page=3).

The edge pattern is preserved when nonzero columns are rescaled: absent edges remain absent. But edge values change, so graph topology and numerical adjacency must not be conflated. Dynamic attention coefficients, changed graphs, zero-valued scale candidates, and numerical overflow need their own implementation rules. The displayed inverse is undefined for a zero scale; reproducing the equations requires checking how the implementation handles that case.

### Why not measure every new node's activation range directly?

For an unseen node, scanning each activation vector can find a suitable minimum and maximum. It also reads every feature and performs reductions each time those parameters are needed. If there are a million nodes with 256 features, even one full scan touches 256 million feature values. At four bytes each, that is approximately one gigabyte of data before counting repeated layers or transfers.

A precomputed lookup can avoid some of that work, but needs a way to decide which stored parameters suit the new node. Using a node identifier alone does not establish anything about its activation distribution. TopGQ instead uses two structural quantities: the node's degree and the mean reciprocal degree of its closed in-neighborhood, including itself. [Equation 9 and Figure 4, PDF page 4](https://arxiv.org/pdf/2608.30394v1#page=4).

For a node with closed-neighborhood degree 3 whose neighborhood degrees are [3, 2, 6], the second quantity is `(1/3 + 1/2 + 1/6)/3 = 1/3`. Its TopPIN pair is therefore `(3, 1/3)`. The reciprocal terms distinguish neighborhoods whose members have different connectivity, even when the target node itself has the same degree.

This is still a compact proxy, not a unique description of a neighborhood. Degrees [3, 3, 3] produce the same pair. More fundamentally, two nodes with identical local structure can carry features differing by a factor of one hundred. Structure alone cannot guarantee equal activation ranges.

### Calibration converts the proxy into a table of numerical parameters

During calibration, nodes sharing a TopPIN value contribute to a combined minimum and maximum. During inference, TopGQ finds nearby TopPIN groups for unseen nodes and interpolates their quantization parameters. [Section 4.2, PDF page 4](https://arxiv.org/pdf/2608.30394v1#page=4).

Combining ranges means accommodating all observed values in that group. If two calibration nodes span [−1, 1] and [−10, 10], the combined range must span [−10, 10]. That avoids clipping those observations but sacrifices resolution for the narrower node. Grouping is a tradeoff between parameter reuse and local fit.

Interpolation can provide a parameter when the exact pair is absent from the table; it cannot establish that the unseen node lies within the calibrated numerical range. Distance normalization also matters: raw degree can be much larger numerically than mean reciprocal degree. A nearest-neighbor implementation must specify its metric, feature normalization, number of neighbors, and behavior beyond the observed range. Those choices were not independently checked in code in this pass.

The motivation connects topology to accumulation variance, but correlations matter. Summing m independent zero-mean values of variance v gives variance mv. Summing m perfectly correlated copies gives m²v. A graph's path counts alone do not determine which situation applies. Learned transformations, nonlinearities, and feature correlations constrain how far the structural approximation can be generalized.

### Preparation time and inference time answer different questions

Quantization time is the work needed to produce the deployable low-precision model and its parameters. Inference time is the work needed to answer with that prepared model. A large reduction in preparation time does not imply an equally large reduction in every inference.

Table 2 reports MAG240M quantization in 58.8 minutes for TopGQ versus 2.06 days for DRA, with accuracies 69.14% and 66.13%; the FP32 reference is 69.66%. [PDF page 5](https://arxiv.org/pdf/2608.30394v1#page=5). Converting units gives `2.06×24×60/58.8 ≈ 50.45×` faster preparation than DRA. The difference from FP32 is 0.52 percentage points, not exact accuracy preservation.

By contrast, Table 4 reports GCN inference on ogbn-products at 20.53 seconds versus FP32's 34.51 seconds on RTX 4090, and 473.25 versus 754.09 seconds on Jetson AGX Orin. These correspond to approximately 1.68× and 1.59×. [PDF page 6](https://arxiv.org/pdf/2608.30394v1#page=6). They are not fiftyfold inference improvements and do not describe MAG240M inference.

Fast preparation can matter even if inference throughput hardly changes. In a constructed update cycle, a model that must be refreshed hourly cannot use a two-day quantization stage without falling far behind. But a 58.8-minute quantization stage would still leave little room in that hour for training, validation, and deployment. The complete refresh process must be timed, not merely one stage.

### Preserve the failures and the experimental setting

The four-bit GCN result on ogbn-products is 39.03% versus FP32's 71.25% in Table 1—a 32.22-percentage-point loss. The same table gives eight-bit TopGQ 71.33%. [PDF page 5](https://arxiv.org/pdf/2608.30394v1#page=5). Thus the method can be useful at one width and inadequate at another. Strong gains against a poorly performing low-bit baseline do not establish acceptable quality relative to FP32.

The manuscript also gives ogbn-products four-bit GraphSAGE accuracy as 61.83% in Table 1 and 63.18% in the ablation table. [Tables 1 and 6, PDF pages 5–6](https://arxiv.org/pdf/2608.30394v1#page=5). The discrepancy remains unresolved; the writeup does not silently substitute either value as if they were interchangeable.

Most evaluations use unseen-node or unseen-graph settings, while MAG240M uses the transductive setting where test-node structure and features can already be present during training, without their labels. [Section 5.1, PDF pages 4–5](https://arxiv.org/pdf/2608.30394v1#page=4). These settings provide different evidence about lookup behavior on genuinely new graph structure. They should not be combined into an unconditional generalization claim.

### What this adds to precision-aware computing

Adana chooses activation representations from current group values. DAPA builds a function approximation from observed input distributions. TopGQ uses structural information to reuse quantization parameters and rearranges scale placement to retain efficient arithmetic. The representation and the method for choosing it are separate sources of cost and error.

A testable longer-term hypothesis is that deployment preparation becomes a first-class systems cost when models or input structures change frequently. Testing that hypothesis requires update frequency, parameter-lookup costs, graph-change behavior, quality thresholds, and full deployment timing. A one-time quantization speedup alone does not establish a trend across applications or conference editions.

No TopGQ model evaluation, inference benchmark, or source-code execution was performed. This explanation uses the DAC manuscript, not the earlier ICLR submission found during discovery. Code-level lookup and scale safeguards, the table discrepancy, and independent reproduction and comprehension remain open.

<span id="explanation-dac-2026-research3029"></span>

## CO-MAC: separate the number represented from the cycles spent computing it

### What is established, and what is not

CO-MAC orders weights by magnitude, reuses magnitude increments, and handles signs after accumulation. Its official description reports up to 54.8% lower MAC latency than prior stochastic designs. [DAC presentation description](https://63dac.conference-program.com/presentation/?id=RESEARCH3029&sess=sess174).

The author laboratory confirms the title and authors but provides no manuscript link in this entry. [Purdue publication list](https://engineering.purdue.edu/neis/publications/). The explanation below develops the arithmetic needed to understand the proposal. Its numerical examples are constructed teaching examples, not recovered CO-MAC measurements or a reconstruction of its circuit. Manuscript pages, exact scheduling rules, and experimental conditions remain unavailable.

### Start with the computation being requested

A multiply-accumulate operation multiplies a pair of values and adds the product to a running sum. A convolution repeats this over a selected input region and its associated weights. For one constructed output, inputs [2, 3, 5, 7] paired with weights [−0.6, 0.1, −0.2, 0.4] give:

`2×(−0.6) + 3×0.1 + 5×(−0.2) + 7×0.4 = 0.9`.

The output is a sum of signed contributions. A different number format must still define how it represents each contribution, combines them, and recovers the final scale. It is insufficient to show that an individual multiplication gate is small.

The inputs in this example exceed one. A representation restricted to [0, 1] would require normalization and later scale recovery. For example, dividing every input by ten makes the intermediate dot product 0.09; multiplying the final result by ten restores 0.9 before any approximation error. Normalization is part of the computation, not an optional change of notation.

### A stream can represent a fraction by counting its ones

In unsigned stochastic representation, the fraction of one bits represents a value between zero and one. An AND gate produces one only when both input bits are one. It therefore represents multiplication when the frequency of simultaneous ones equals the product of the two individual frequencies. Correlation between streams can break that condition. [Alaghi and Hayes, Figure 1 and introduction, PDF page 1](https://homes.cs.washington.edu/~armin/ICCD_2013.pdf#page=1). This background source explains the representation; it is not evidence for CO-MAC's implementation.

Consider these independently constructed four-position examples. Each input contains two ones, so every input represents 0.5.

| First stream | Second stream | Bitwise AND | Decoded result |
| --- | --- | --- | --- |
| 1100 | 1010 | 1000 | 1/4 = 0.25 |
| 1100 | 1100 | 1100 | 2/4 = 0.5 |
| 1100 | 0011 | 0000 | 0/4 = 0 |

Only the first gives the intended product, 0.5×0.5. Correct counts in the inputs do not establish correct overlap between them. Repeating the second pair a thousand times still produces 0.5: extending a systematically unsuitable pattern does not repair it.

There are also two different meanings of precision here. A stream of N positions can represent fractions separated by 1/N. That describes the available count levels. It does not guarantee the result of arithmetic is within 1/N of the desired result; the overlap example violates such a guarantee even when both inputs are represented exactly.

For a separately constructed random experiment, suppose each bit is an independent trial with probability p of being one. The variance of the average of N bits is p(1−p)/N. Its standard deviation is the square root of that quantity. At p = 0.5, N = 256 gives 0.03125; N = 1024 gives 0.015625. Four times as many independent trials halve this measure of random variation. This calculation is not a CO-MAC error model and must not be applied to deterministic sequences without establishing their behavior.

### Why ordering magnitudes can reduce repeated counting

Return to weights [−0.6, 0.1, −0.2, 0.4]. Their sorted magnitudes are [0.1, 0.2, 0.4, 0.6]. Starting at zero, the increments are [0.1, 0.1, 0.2, 0.2]. They sum to 0.6, whereas the four magnitudes sum to 1.3.

To make the difference concrete, construct a counter whose unit represents 0.1. Starting from zero separately for targets [1, 2, 4, 6] requires 1 + 2 + 4 + 6 = 13 forward increments, ignoring reset cost. Visiting those targets in one ascending pass requires 1 + 1 + 2 + 2 = 6 increments. The arithmetic illustrates a possible saving in repeated traversal. It does not establish six CO-MAC cycles, a 13/6 measured speedup, or a complete multiplication algorithm.

The reason for that qualification matters. Four different weights may multiply four different activations. A count associated with one activation cannot simply become the product for another. The hardware must explain what state can be shared, how the activation changes are represented, and when the correct contribution is captured. The description's reference to reused increments motivates these questions but does not answer them at circuit level.

### Reordering must preserve input–weight pairs

Sorting the example's weights by magnitude gives [0.1, −0.2, 0.4, −0.6]. The corresponding input order must become [3, 5, 7, 2]. Their dot product remains:

`3×0.1 + 5×(−0.2) + 7×0.4 + 2×(−0.6) = 0.9`.

Keeping the original input order while sorting only the weights instead gives:

`2×0.1 + 3×(−0.2) + 5×0.4 + 7×(−0.6) = −2.6`.

Thus weight ordering creates an addressing obligation. For convolution, the implementation must fetch the matching input position or retain an equivalent mapping. Fixed weights could permit preparation before inference, but that does not eliminate runtime input-selection cost. This is an implementation requirement derived from the dot product, not a verified account of CO-MAC's memory system.

### Delaying sign handling does not remove signed arithmetic

In the same example, positive contributions total 0.3 + 2.8 = 3.1, and negative magnitudes total 1.2 + 1.0 = 2.2. Their difference is 0.9. Computing nonnegative contributions and subtracting later can therefore be algebraically valid.

But the implementation must retain enough information to distinguish the two totals. Discarding all signs and summing magnitudes produces 5.3, not 0.9. A simplified illustrative organization uses two increasing counters followed by a subtraction; this is not a claim that CO-MAC uses exactly that organization.

Counter range also follows intermediate totals, not just the final answer. A computation with positive total 100 and negative total 99 has final output one. Storage sufficient only for one cannot represent the two totals. Delayed cancellation can require substantial intermediate range even when the output is small.

With approximate totals, cancellation can make relative error large. If the intended totals are 3.1 and 3.0, the difference is 0.1. Errors of +0.01 and −0.01 change the result to 0.12: a 20% relative output error despite small errors in each total. This constructed case explains why a claim about accurate products needs a separate check of accumulated outputs.

### Read the latency result at its actual scope

A 54.8% time reduction leaves 45.2% of baseline time. The equivalent speed ratio is `1/0.452 ≈ 2.21`, not a 54.8× improvement. The description gives a maximum MAC-level reduction, not a whole-network result. It does not identify the baseline names, models, clock, process, stream lengths, accuracy numbers, or sorting and memory costs. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH3029&sess=sess174).

For a constructed 100 ms inference, suppose the affected MAC work takes 40 ms and everything else takes 60 ms. Reducing only that work by 54.8% gives `60 + 40×0.452 = 78.08 ms`, or about 1.28× overall speedup, before new overhead. If input reordering adds 10 ms, total time becomes 88.08 ms, about 1.14×. The missing end-to-end measurements determine which, if either, resembles the implementation.

Maintaining a long effective stream while reducing physical counter activity could distinguish this proposal from simply stopping an approximation early. Establishing that distinction requires a schedule showing how the represented contributions survive skipped work, plus output-error measurements at matched settings. A statement about fewer active counter steps alone is not an accuracy proof.

### What this adds to the subtheme

Low-bit quantization changes which numerical values are available. This proposal instead raises a question about how much physical execution a chosen representation requires. The two decisions should be evaluated separately: representation error can stay fixed while execution improves, or execution can become faster because more error is accepted.

A useful cross-paper comparison would hold output quality fixed, include representation conversion and data selection, and report full inference time and energy. A longer-term hypothesis is that repeated use of fixed model parameters creates opportunities to prepare an execution order once and reuse it. It remains a hypothesis until preparation cost, weight-update frequency, memory access, and repeated-run savings are measured across cases.

No CO-MAC circuit, code, benchmark, or synthesis was executed. This discussion is conceptually expanded but still description-backed. It does not satisfy the requested manuscript-page-backed evidence standard yet.

<span id="explanation-dac-2026-research259"></span>

## HierPAS: decide which attention contributions to keep and how accurately to compute them

### The proposal and the evidence boundary

HierPAS targets attention in video-generation transformers. Its description combines an early estimate of attention patterns, sampled entropy to choose retention by head, progressively lower precision for less important regions, configurable selection of the largest entries, and shared multi-precision matrix-multiplication hardware. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH259&sess=sess127).

The author page confirms the paper but labels its download link “TBD”; following that link returns to the publication list. No manuscript was recovered in this pass. [Author publication page](https://austinliu01.github.io/publication/HierPAS). The following explanation derives the relevant computation and tradeoffs. All numerical examples and error calculations are constructed, not HierPAS results. The exact prediction algorithm, precision levels, selection granularity, and circuit remain unverified.

### What attention computes

A token is a position represented by a vector of numbers. In a video model, the positions may correspond to regions across space and time; the exact grouping depends on the model. Attention computes how information from other positions contributes to the output at each position.

For ordinary scaled dot-product attention, each position supplies a query vector, while positions supplying information have key and value vectors. Query–key dot products form scores. Dividing by the square root of the key dimension controls score scale. Softmax exponentiates these scores and divides by their sum, producing nonnegative weights that sum to one. The output is their weighted sum of value vectors. Multiple heads repeat this with separately learned projections. [Vaswani et al., Sections 3.2.1–3.2.2, PDF pages 4–5](https://arxiv.org/pdf/1706.03762#page=4).

In symbols, `output_i = sum_j a_ij × value_j`, where `a_ij` is the normalized attention weight from position i to position j. A score before softmax and a weight after softmax are not interchangeable. A threshold or error bound must state which quantity it concerns.

For a scalar teaching example, weights [0.8, 0.15, 0.05] and values [2, 4, 10] give `0.8×2 + 0.15×4 + 0.05×10 = 2.7`. Although the last attention weight is small, its contribution is 0.5 because the associated value is large. Importance cannot always be inferred from the attention weight alone.

### Why longer videos can increase work faster than their length

If N positions each compare against all N positions, there are N² scores per head. Doubling N gives four times as many pairs. Holding feature width fixed, both the score dot products and the weighted-value accumulation scale with this number of pairs.

In a constructed case with 4,096 positions, one head has 16,777,216 pair scores. Materializing every score at two bytes requires 32 MiB. At 8,192 positions it requires 128 MiB. These are sizes of hypothetical fully stored matrices, not minimum memory requirements: an implementation can compute and consume sections without keeping the entire matrix at once. Reducing matrix storage and reducing arithmetic are different achievements.

The relationship also depends on tokenization. Doubling both image width and height at fixed spatial patch size gives four times as many spatial positions; global pairwise attention then has sixteen times as many pairs. If an implementation uses local windows or separates spatial and temporal attention, that calculation must be revised. The recovered HierPAS description does not specify enough model detail to apply these example counts to its evaluation.

### Removing entries changes both the numerator and normalization

For the [0.8, 0.15, 0.05] example, dropping the last contribution without renormalizing leaves 2.2. Renormalizing the remaining weights by their sum, 0.95, instead gives `2.2/0.95 ≈ 2.316`. Neither equals the original 2.7. The two pruning policies have different errors.

More generally, suppose the removed weights sum to δ and every value vector has norm at most V. If retained weights are left unchanged, the removed weighted sum has norm at most δV. This follows by bounding each contribution's norm by its weight times V and adding the bounds.

If retained weights are renormalized and δ < 1, their total rescaling changes the retained contribution by at most another δV. The resulting error is therefore at most 2δV under these assumptions. This is an illustrative worst-case bound for a single attention output, not a HierPAS theorem or a guarantee for the final video. It requires the original weights, a value bound, and the specified normalization policy.

Retaining a fraction of entries does not fix δ. Keeping ten of one hundred entries could retain 95% of the attention mass, or only 10% if weights are uniform. Consequently, a retention ratio alone cannot establish accuracy. The distribution of the retained mass and the values it multiplies matter.

### Why entropy can help choose a retention ratio—and why it is insufficient

For normalized nonnegative weights p, entropy is `−sum(p × log2(p))`, with a zero-weight term defined as zero. It measures how spread out the distribution is. A row [1, 0, 0, 0] has entropy zero; [0.25, 0.25, 0.25, 0.25] has entropy two bits.

Keeping one entry preserves all mass in the first case but only one quarter in the second. This explains why concentration information can help select how much of a row or head to retain. A head is one separately parameterized attention computation, so heads need not share the same attention distribution.

However, entropy does not contain the value vectors. In the scalar example, changing values from [2, 4, 10] to [2, 4, 1,000] leaves attention weights and their entropy unchanged. The contribution from the smallest weight increases from 0.5 to 50. An entropy-based decision needs empirical quality checks or additional safeguards; entropy alone is not a bound on the output error.

Aggregating a head can also conceal unusual rows. If most positions concentrate their attention but a small subset uses a broad distribution, a head-wide retention choice may treat those positions too aggressively. This is a failure case to test, not an observed HierPAS failure.

### Sampling reduces decision cost but can miss rare behavior

Computing exact importance from all full-precision scores before skipping those same scores would already pay much of the cost being avoided. A useful predictor must be cheaper than the work it removes. HierPAS's early estimation and sampled entropy are intended to support that decision, but the recovered description does not specify their equations or sampling schedule.

Consider an illustrative independent sample of 32 rows when 1% of rows exhibit a consequential pattern. The probability of missing all such rows is `0.99^32 ≈ 72.5%`. Increasing the sample to 256 reduces that probability to about 7.6%, while increasing sampling work eightfold. Actual structured or correlated sampling may behave differently; these probabilities are not claims about HierPAS's sampler.

An estimate must also rank the right entries. Suppose the two largest true weights are 0.51 and 0.49. Approximation errors of −0.02 and +0.02 reverse their order. Keeping only the predicted largest entry then selects a different value. If the two values differ substantially, a small score-estimation error can cause a much larger output change.

This creates two distinct risks: choosing too few entries and choosing the wrong entries at a given count. Measuring only the average retained fraction cannot distinguish them.

### Precision and sparsity are separate decisions

Sparsity removes selected contributions. Reduced precision retains contributions but represents their operands or arithmetic less accurately. Combining them allows more than a binary keep/drop decision, but it also introduces multiple sources of error.

For a constructed retained scalar product, let attention weight a change by e and value v change by f. The product changes by `e×v + a×f + e×f`. A small error in a is multiplied by v, and an error in v is multiplied by a. Reducing the precision of a small attention weight may be reasonable for some values and inadequate for others.

Errors before softmax require another analysis because changing one score changes the normalization shared by the whole row. The preceding product formula applies after the operands are defined; it cannot by itself certify approximate query–key arithmetic or approximate softmax.

The description does not specify whether each precision tier applies to query/key operands, scores, attention probabilities, values, accumulators, or several of these. Those are distinct design choices. Assigning familiar four-, eight-, or sixteen-bit tiers without the paper would invent the missing method.

### Hardware must turn fewer selected operations into less elapsed work

Selecting the largest k entries requires comparisons and a way to retain their locations. Matrix multiplication over the selected entries then needs the matching values. If the entries are scattered, selection may save arithmetic while creating additional address generation, small memory transfers, or idle arithmetic lanes.

As a constructed scheduling example, two synchronized lanes with jobs requiring two and eight cycles take eight cycles to finish. Their total useful work is ten lane-cycles out of sixteen available. Lowering the short job to one cycle does not shorten the batch: the eight-cycle job still controls completion. Flexible arithmetic must be accompanied by suitable scheduling to realize a latency gain.

Similarly, a dense engine processing a whole tile cannot save proportional work merely because most entries inside that tile are zero. The skip granularity—individual value, group, or tile—determines whether the zero entries are actually omitted. HierPAS mentions configurable selection and a unified multi-precision datapath, but these implementation details remain unrecovered.

In an illustrative 100 ms workload, suppose affected attention computation takes 80 ms. Cutting it to one quarter gives 20 ms, and the unaffected part still takes 20 ms. Adding 15 ms for prediction, selection, and irregular access yields 55 ms total: about 1.82× overall speedup, not the fourfold reduction suggested by the attention arithmetic alone.

### Interpret the efficiency headline without changing its units

The official description reports up to 178× energy efficiency over NVIDIA H20 and 7.7× over other accelerators, with a qualitative claim of little video-quality loss. It does not supply the energy denominator, competing accelerator names, model settings, quality measures, fabrication process, or measurement methodology. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH259&sess=sess127).

If efficiency meant matched completed videos per joule, a 178× ratio would imply 1/178 of the energy per video under those matched conditions. If it instead counts operations per joule, the comparison needs a common operation definition, especially when sparsity removes operations and precision changes their cost. The abstract alone does not resolve this distinction.

Neither ratio is a latency ratio. Nor does a qualitative quality claim establish equal motion consistency, prompt adherence, fine detail, or behavior on difficult prompts. Those evaluation dimensions are requirements for interpreting the claim, not recovered results. Timing and energy must also state whether prediction, selection, memory transfers, and all generation iterations are included.

### How to compare this paper with the others

HAP removes redundant bits from already quantized activations while retaining recovery information. TopGQ changes scale placement and how quantization parameters are selected. HierPAS proposes choosing both the set of attention contributions and their precision. These intervene at different points, so a single “low precision” label is not an adequate explanation.

A testable longer-term hypothesis is that deciding where to spend computation becomes a substantial part of the accelerator itself. The relevant comparison includes the decision cost, the mistakes made by that decision, the granularity the hardware can skip, and the final output quality. It should also test whether the decision remains reliable as video length, content, and generation stage change. One efficiency headline does not establish that trend across conferences or years.

No HierPAS model, circuit, benchmark, or synthesis was executed. The manuscript-page-backed explanation, evaluation conditions, and independent comprehension check remain unfinished.

<span id="explanation-dac-2026-research2207"></span>

## PRISM: the shared scale is also an approximate number

### Identify the part of the representation being changed

PRISM proposes four-bit quantization with one encoded eight-bit scale per group. Its description says the scale representation adapts to the relative importance of values, and reports improved accuracy with 0.62% area and 0.86% energy overhead. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2207&sess=sess145).

This is the shared-scale quantization paper, not another paper called PRISM about forecasting or instruction following. No manuscript was recovered. In particular, the scale encoding, importance measure, group size, decoder, workloads, and evaluation conditions remain unknown. The examples below explain the problem; they are not PRISM bit layouts or reconstructed experiments.

### Two stored quantities jointly represent one value

Write a grouped representation as `decoded_value_i = group_scale × decoded_element_i`. The element code determines a value from a small finite set. The shared scale expands or contracts that set for every element in the group. Storing the element accurately is insufficient if the scale is inaccurate.

For an illustrative group, let the scale be 0.3 and decoded element values be [1, 2, 4]. The represented numbers are [0.3, 0.6, 1.2]. If the scale is stored as 0.25 while these element values remain fixed, the decoded numbers become [0.25, 0.5, 1.0]. Every nonzero value has the same relative scale error, −1/6, although its absolute error differs.

The errors here are linked by the shared scale. They are not independent rounding errors that necessarily cancel in a sum. For instance, summing the three decoded numbers changes 2.1 to 1.75. This example deliberately holds element codes fixed to isolate scale error; a quantizer that reselects codes after rounding the scale can produce a different result.

More generally, changing scale s by e and decoded element q by f changes their product by `e×q + s×f + e×f`. The first term is scale error, the second is element error, and the third is their interaction. Studying only the four-bit element error omits part of the representation.

### A wider range and a finer scale are different benefits

Suppose one scale codebook permits only powers of two. It might represent scale 1 or 2 but not 1.5. Another codebook could represent 1.5 exactly while covering fewer extreme magnitudes with the same number of codes. This is a constructed distinction, not a statement of PRISM's particular codebook.

An eight-bit field has at most 256 distinct codes. Giving more codes to closely spaced values in one region leaves fewer codes elsewhere unless extra context changes the decoding. If context does change decoding, the system must supply that context reliably and account for its storage or computation. An adaptive representation cannot escape this finite-code constraint.

A group of very small values needs an appropriate scale range. A group whose useful scale lies between two available scale values needs finer scale resolution. These are different failure cases, even though both may appear as quantization error. A claim of broader range does not, on its own, prove finer resolution where the model needs it.

### Why importance can change which scale is preferable

An appropriate scale need not minimize the unweighted average error of the stored numbers. The numerical error matters through the computation that consumes those numbers.

Consider the constructed pair [0.14, 3.0], encoded with signed integer element levels −8 through 7. This integer example illustrates scale selection; it is not the paper's four-bit format. With scale 0.2, nearest-level rounding and clipping produce [0.2, 1.4]. With scale 0.4 they produce [0, 2.8].

The sums of squared errors are 2.5636 and 0.0596 respectively, so ordinary squared-error minimization favors scale 0.4. Now assign the first value a sensitivity weight of 1,000 and the second a weight of one. The weighted errors become 6.16 and 19.64. Under this explicitly different objective, scale 0.2 is preferable despite its larger total unweighted error.

This calculation shows why a priority rule must be defined. It does not show how PRISM obtains priorities. A rule based on magnitude, frequency, calibration measurements, or downstream sensitivity may choose different values to protect. We cannot substitute one of these rules for the missing manuscript.

Sensitivity itself has a computational meaning. If output y contains a term c×x, then perturbing x by δ changes that term by c×δ. A small x with large c can matter more than a large x with small c. In a network, later computations and nonlinear operations complicate the relationship further. A local priority estimate needs checks against final task quality and inputs different from those used to choose it.

### Include the scale in the storage budget

For four-bit elements, group size G, and one eight-bit scale, storage is `4 + 8/G` bits per value before alignment and any other metadata. At G = 16 this is 4.5 bits, while G = 32 gives 4.25 bits. These are illustrative group sizes, not recovered PRISM settings.

Using smaller groups makes it easier to choose scales for similar values but pays more scale storage. Group composition matters too: combining small values with a large outlier can force a scale that loses the small values, while separating them can require reordering and additional access information.

Adding a hypothetical shared 32-bit tensor scale would cost another `32/M` bits per value for a tensor of M elements. At one million elements that storage overhead is tiny. Its arithmetic, range, and implementation effects could still matter. Removing an extra scale therefore must not automatically be described as a large memory saving; the sharing granularity determines the saving.

### The scale must remain in the dot product

Within one matching group, products can be written as `sum_i (s×q_i)(t×r_i) = s×t×sum_i q_i×r_i`. This permits scaling a group subtotal rather than each individual product, provided the implementation preserves the required numerical behavior.

Across groups with different scales, one scale pair cannot generally be moved outside the entire sum. For constructed integer subtotals 10 and 20 with scale products 0.1 and 0.01, the output is `10×0.1 + 20×0.01 = 1.2`. Adding the integer subtotals first and multiplying by 0.1 instead produces 3.0.

Consequently, a new scale representation affects decoding, scale multiplication, alignment of group subtotals, and accumulation. A compact encoded field does not establish that all these operations are inexpensive. Fixed weights may permit some preparation before inference; scales for changing activations may need runtime work. The manuscript must specify which tensors are quantized and which costs are included.

### Interpret the small overhead numbers carefully

An area overhead of 0.62% means 1.0062 times the reference area; energy overhead of 0.86% means 1.0086 times the reference energy. They are increases reported alongside an accuracy benefit, not reductions. The description does not identify the reference configuration, accuracy values, process, clock, or measurement method. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2207&sess=sess145).

Whether this is a favorable tradeoff depends on the quality requirement and the alternatives that meet it. Comparing to a configuration that fails the required quality is useful diagnostically, but it is not a complete deployment comparison. Latency, calibration cost, full storage including scales, and task quality at matched settings remain necessary.

The broader question raised by PRISM is whether scale precision deserves its own allocation policy rather than being fixed after choosing element width. Testing that idea requires separating improvements due to the scale codebook from changes in grouping, calibration, element representation, and hardware budget.

No PRISM implementation, model benchmark, or synthesis was executed. The paper-specific mechanism remains description-backed rather than manuscript-page-backed.

<span id="explanation-dac-2026-research2374"></span>

## MXP: spend a value's bits differently at different magnitudes

### What distinguishes MXP from PRISM

MXP combines a group scale with a posit-inspired element representation that changes the allocation of exponent and fraction bits. Its description also introduces a matching accelerator and claims less quality degradation and lower area and power, without numerical results. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2374&sess=sess143). The laboratory publication list confirms the title and authors but supplies no manuscript link for this entry. [SNU VLSI publications](https://vlsi.snu.ac.kr/publications/).

PRISM focuses on the shared scale. MXP focuses on the per-element representation beneath a group scale. The two questions are related but not identical. Neither recovered description establishes that the proposals can be combined without changing their encodings or hardware.

### Exponent bits and fraction bits answer different questions

A simplified normalized floating-point magnitude has the form `2^exponent × (1 + fraction)`. The exponent chooses a magnitude range; the fraction distinguishes values within that range. A sign bit determines whether the value is positive or negative. Zero, very small numbers, exceptional values, and exact encoding conventions require additional rules in a real format.

With four fraction bits, the fractional part can advance in steps of 1/16. With two fraction bits it advances in steps of 1/4. At exponent zero, these give spacings of 0.0625 and 0.25. At exponent three, the spacings become 0.5 and 2.0 because the whole value is multiplied by eight.

More exponent bits allow more exponent codes, subject to reserved encodings and bias rules. At a fixed total width, those bits must come from somewhere else. Increasing range can therefore reduce resolution. No fixed-width format can represent every magnitude with arbitrary accuracy.

### A constructed bit budget illustrates tapered precision

Imagine an eight-bit teaching format with one sign bit and one mode bit. One mode allocates the remaining six bits as two exponent bits and four fraction bits. Another uses four exponent bits and two fraction bits. This is only a bit-budget example, not MXP's encoding or a complete posit definition.

For magnitude 1.1 at exponent zero, four fraction bits round to 1.125, with error 0.025. Two fraction bits round to 1.0, with error 0.1. The second allocation has more exponent codes available but less detail near this value. A tapered format makes this allocation depend on the encoded value or region instead of using the same field lengths everywhere.

The decoder must know where each field ends. In the teaching format, a mode bit supplies that information. Other designs can use a self-delimiting pattern whose length identifies the magnitude region. Whichever rule is used consumes coding capacity and requires decoding logic. We have not recovered MXP's actual rule and do not assign it the toy format's mode bit, widths, or code table.

### The group scale changes where values fall in the element format

With a group scale of eight, input 8.8 becomes normalized element value 1.1. Applying the two teaching allocations above reconstructs 9.0 or 8.0, with absolute errors 0.2 or 0.8. The group scale multiplies the element error as well as the element value.

This means the scale selection and element codebook must be considered together. A scale can move many normalized values into a region with finer spacing, but may move others toward a coarse or unsupported region. Minimizing scale error by itself does not necessarily minimize the decoded tensor error.

Consider a group containing values near one and a value near one hundred. A wider-range element format might allow both without increasing the shared scale as much as a narrower-range format. But that is not a free improvement: the far-from-center value may receive fewer fraction bits, decoding may become more complex, or precision elsewhere may change. The actual codebook is needed to calculate which effect dominates.

### Tapered precision is not automatically importance-aware precision

A representation that gives more detail to a particular magnitude region protects values in that region. That is a statement about numerical location, not necessarily about task importance.

For a constructed linear output, compare a small input 0.01 multiplied by 1,000 with a large input 100 multiplied by 0.001. Their contributions are ten and 0.1. A representation policy that equates magnitude with importance could protect the wrong input. What matters is how representation error propagates through the consuming computation.

Likewise, lower average squared representation error does not guarantee that all tasks improve. Errors concentrated on a few decisive values can change a classification or generated answer. The relevant tests should report model-level quality as well as local quantization error, and should include outliers and changed input distributions.

The official description uses an optimality claim, but does not define the optimization objective, admissible formats, or proof. It cannot establish a universally optimal range–precision balance. The defensible interpretation remains a reported improvement under conditions that have not yet been recovered.

### A matching accelerator must do more than store the format

A matrix multiplier receives two encoded elements, decodes their signs and magnitudes, forms a product, and aligns that product with an accumulated subtotal. Variable field lengths can change decoding and alignment work even when every stored element occupies the same number of bits.

A shorter fraction can make an individual multiplication simpler only if the hardware actually exploits it. A design that decodes every element into the same wider internal representation may save memory but not proportionally reduce arithmetic. A design with several execution modes must account for mode control, routing, accumulation width, and unequal workloads. These are alternatives to inspect, not descriptions of the missing MXP circuit.

Group scales also remain in the arithmetic. If a group's element products sum to u, its contribution includes the product of the operand scales times u. Contributions from groups with different scales must be aligned before they can be combined. Accumulating everything in the narrow storage format can introduce additional errors or overflow even when each input is represented acceptably.

Cancellation provides a simple warning. Products 100 and −99 have final sum one; the intermediate storage still needs to represent the larger values. A format's element range and the accumulator's range are separate requirements. The recovered description does not specify MXP's accumulator.

### Storage and power claims need explicit denominators

If an element uses b bits, its group contains G elements, and the group scale uses h bits, the payload plus scale costs `b + h/G` bits per value. Alignment, exceptional-value handling, padding, and other metadata can increase this. MXP's b, G, and h are not available in the description, so an effective bits-per-value figure cannot yet be calculated for the paper.

Lower power is not the same as lower energy. In a constructed comparison, a reference consuming 10 W for one second uses 10 J. A replacement consuming 8 W for two seconds uses 16 J: lower power but higher energy. The elapsed time and matched amount of completed work determine the interpretation.

The abstract provides no numerical area, power, latency, accuracy, or energy results; it does not name the baselines, model variants, process, or evaluation method. We therefore cannot rank MXP against PRISM, ordinary floating point, or another accelerator on efficiency from the available evidence.

### The comparison this pair of papers motivates

PRISM and MXP suggest separating at least three decisions: which values share a scale, how that scale is represented, and how each scaled element is encoded. A complete comparison changes one decision at a time where possible, or reports the combined design honestly when they cannot be separated.

The longer-term hypothesis is that low-bit formats will increasingly be judged as full numerical systems rather than by element width alone. Evidence would need to include the scale policy, codebook, accumulation, conversion, memory layout, output quality, and hardware cost. Two descriptions establish related research questions, not a demonstrated temporal trend or a winning universal format.

No MXP implementation, model benchmark, or synthesis was executed. The exact encoding, manuscript-page-backed method, experimental conditions, and independent comprehension review remain open.

<span id="explanation-dac-2026-research2650"></span>

## RESP: choose what to remove using the model's generated sequences

### The problem is preserving a computation, not just removing weights

“Think Before You Prune” introduces RESP: self-generated calibration, decode-only gradient importance, and periodic regeneration during structured pruning. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2650&sess=sess176). The inspected manuscript is the December 2025 preprint, not a recovered DAC camera-ready version. [Preprint](https://arxiv.org/pdf/2512.02185v1#page=1).

A model produces its next token from the prompt and the tokens already generated. Removing parameters can change the next-token probabilities. Once the generated token changes, later computations receive a different prefix, so subsequent behavior can diverge further. A pruning rule therefore needs evidence about the computations used during generation, not only about reconstructing intermediate values on unrelated text.

For a constructed two-choice step, suppose the original probabilities are 0.51 and 0.49. A small change reverses them to 0.49 and 0.51. A highest-probability decoder selects a different token, even though the probability vectors are close. Sampling need not choose the same token either. The new prefix changes the inputs to the next step. This example illustrates why local numerical similarity need not preserve a whole generated answer; it is not a measurement from RESP.

### What structured pruning actually removes

Setting scattered individual weights to zero does not automatically shorten dense matrix multiplication. Structured pruning instead removes complete computational units and their dependent parameters. The result can have smaller matrix dimensions, provided the implementation physically removes those dimensions rather than merely masking them.

Consider a teaching network with a first matrix of shape 4×3 and a second of shape 3×2, using row-vector inputs. The first produces three intermediate channels; the second consumes those same three. Removing intermediate channel two requires removing the matching column from the first matrix and row from the second. Their shapes become 4×2 and 2×2. Removing only one side breaks the dimensional relationship.

The two matrices originally contain 12 + 6 = 18 parameters; afterward they contain 8 + 4 = 12. That is a one-third reduction for this simplified pair. It is not necessarily a one-third reduction for a full model with embeddings, other layers, normalization, caches, and temporary storage.

### Calibration chooses which behavior the pruning score sees

A calibration set is a limited collection of inputs used to estimate which parts of a trained model are important. If a unit is useful only on behavior missing from that set, its estimated importance can be misleadingly low.

RESP uses task prompts and the model's generated output as calibration data. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH2650&sess=sess176). The distinction is distributional: generated text supplies prefixes the model actually reaches, whereas a human solution may use a different sequence even when both end with the same answer.

This does not establish that generated text is true, complete, or a faithful account of an internal decision process. It is observable output used to measure sensitivity. A model may generate an incorrect answer confidently; preserving its likelihood preserves that behavior too. Self-generated calibration consequently needs independent evaluation against task answers rather than treating its own output as proof of correctness.

The prompt set still determines the task coverage. Refreshing outputs for the same arithmetic questions does not introduce evidence about programming, unfamiliar languages, or other tasks. Better alignment to one deployment distribution is not a guarantee of general capability preservation.

### Define the loss before interpreting the gradient

The preprint averages negative log-probability over generated tokens while masking prompt-token loss. It sums absolute weight–gradient products over structures, normalizes, and ranks them. [Equations 4–5 and accompanying text, PDF page 5](https://arxiv.org/pdf/2512.02185v1#page=5).

Negative log-probability penalizes assigning low probability to an observed token. If the assigned probability is 0.5, the loss is about 0.693 using the natural logarithm; probability 0.25 gives about 1.386. The latter token is less well predicted and contributes more loss. Averaging over selected generated positions defines the quantity whose sensitivity is measured.

Masking the prompt's direct loss terms does not remove the prompt from the computation. Generated-token predictions still depend on prompt representations, and their gradients can pass through parameters used to process the prompt. Thus “decode-only” should not be read as “prompt processing is irrelevant” or “no prompt computation occurs.”

As a constructed weighting example, a sequence has 100 prompt tokens and ten generated tokens. A uniform full-sequence average gives generated positions only 10/110 of the token weight. Restricting the loss to those ten changes that weighting. It does not necessarily make gradients eleven times larger, because token gradients can differ in magnitude and direction; it changes the objective being differentiated.

### Why multiply a gradient by the weight being removed?

For a scalar weight w, setting it to zero changes it by −w. A first-order expansion predicts loss change approximately `(gradient with respect to w) × (−w)`. The absolute product gives a magnitude estimate of that change.

In a teaching example, weight 2 with gradient 0.01 has absolute product 0.02. Weight 0.1 with gradient 1 has product 0.1. A magnitude-only rule would regard the second weight as smaller; the gradient-weight rule estimates it as more consequential for this particular loss and data.

The estimate is local even though removing a weight may be a large change. For the constructed loss `L(w) = (w−1)^2`, at w = 1 the loss and gradient are both zero. The first-order score is zero, yet setting w to zero increases loss to one. A zero gradient does not prove a weight can safely be deleted.

Removing several weights can also create interactions not captured by summing individual scores. Absolute values avoid cancellation between opposite signed contributions, but can overstate the joint effect when cancellation is real. Normalization and grouping influence which structures rank lowest. These are limitations of the approximation, not observed failures of the specific implementation.

### Why regenerate after part of the model has been removed?

A ranking measured on the dense model describes its current computation. After pruning, previously redundant structures may become important, and generated prefixes can change. Continuing to prune using the original data and sensitivities can therefore become increasingly inappropriate.

RESP replaces calibration outputs at pruning milestones while retaining the prompt set and token budget. [Sections 4.3–5.1, PDF pages 5–6](https://arxiv.org/pdf/2512.02185v1#page=5). Conceptually, the loop is: generate outputs with the current model, measure sensitivity on those outputs, remove the next structures, and repeat.

Regeneration follows the changed model; it does not restore deleted parameters or automatically correct a mistaken answer. It can keep calibration representative while also inheriting the pruned model's new errors. The useful balance is an empirical question, especially when the remaining model already generates poor text.

Pruning milestones require a fixed denominator. If 20% of the original structures have been removed, reaching 30% removes ten percentage points of the original count, or 12.5% of the remaining 80%. Removing another 10% of what remains instead reaches 28%. Structure sizes can differ, so counting structures and counting parameters need not give the same sparsity either. The implementation's exact accounting must be checked before reproducing a target ratio.

### Read the reported accuracy against the dense reference

Table 1 gives dense Qwen3-8B accuracy of 96.74%/87.60% on GSM8K/MathQA. At 40% pruning, RESP gives 81.27%/59.60%, versus GISP's 14.40%/12.60%. [PDF page 6](https://arxiv.org/pdf/2512.02185v1#page=6).

The gains over GISP are 66.87 and 47.00 percentage points. They are not relative gains of 66.87% and 47%. Relative to GISP, the increases would be approximately 464.4% and 373.0%, which are very different quantities. The original paper's percentage wording should not hide the denominator.

Against the dense model, the losses are 15.47 and 28.00 percentage points. Strong improvement over a badly degraded baseline does not make the pruned result equivalent to the original. Whether that loss is acceptable depends on the intended use and its quality threshold.

Regeneration is not uniformly better: at 30% pruning, GSM8K accuracy is 91.36% with regeneration versus 92.65% without it. [Table 1, PDF page 6](https://arxiv.org/pdf/2512.02185v1#page=6). That is a 1.29-percentage-point decline for this comparison. A useful high-sparsity intervention can still have an unfavorable outcome elsewhere.

### Preserve evaluation conditions and unresolved details

The setup uses 500 training prompts per task, 2,048-token calibration caps, temperature 0.6, seed zero, and a separate model to extract final answers. The first 10% of blocks and final block are protected. [Section 5.1, PDF page 6](https://arxiv.org/pdf/2512.02185v1#page=6).

A final-answer extractor is part of the measurement procedure. Holding it fixed helps comparison, but does not make its judgments infallible. A reproduction should examine extraction mistakes, truncated outputs, decoding settings, and variability across seeds. Answer accuracy also does not directly measure whether intermediate text is coherent or correct.

One calibration refresh can generate up to `500×2,048 = 1,024,000` output tokens per task under the stated cap. This is a calculated upper bound, not observed token use or runtime. Gradient calculation adds further computation and memory; not updating weights through training does not make calibration free.

The inspected preprint does not establish an end-to-end hardware speedup. A smaller model can reduce work per token while generating more tokens. For a constructed case, reducing per-token time from 10 ms to 7 ms but increasing output length from 1,000 to 1,600 tokens changes decode time from 10 seconds to 11.2 seconds. Parameter sparsity alone cannot determine latency, energy, or peak memory.

The tables also represent different experimental paths: regeneration-ratio ablations should not silently replace main-table values. A reproducible comparison needs the checkpoint, pruning sequence, normalization, structure dependencies, and exact sparsity denominator, not just the name RESP.

### How this changes the subtheme's conceptual map

PRISM and MXP change how retained numerical values are represented. HierPAS selects attention contributions during computation. RESP removes parameterized structures using a calibration-dependent sensitivity estimate. All can reduce cost, but they act on different objects and have different failure conditions.

The testable longer-term hypothesis is that compression decisions must be refreshed when compression itself changes the behavior used to make those decisions. RESP supplies a concrete example to investigate, not evidence that every compression method needs regeneration. Testing the broader hypothesis requires multiple tasks, controlled refresh budgets, independent quality measurements, and full deployment timing.

No RESP code, model benchmark, or pruning run was executed. Camera-ready reconciliation, implementation-level verification, reproduction, and independent comprehension review remain open.

<span id="explanation-dac-2026-research1610"></span>

## BayesCVNN: estimate prediction variation without discarding complex-valued structure

### Begin with what a complex number stores

A complex number has two real components: `z = a + bi`, with `i² = −1`. Storing both a and b preserves the pair. Replacing z with only a generally loses information, but representing the pair with two real-valued channels does not inherently lose information. The arithmetic and learned constraints, not the word “real,” determine what is preserved.

For example, `(2 + 3i)(4 + 5i) = −7 + 22i`. The direct calculation forms four real products: 2×4, 3×5, 2×5, and 3×4. Subtracting the first pair gives −7; adding the second pair gives 22. Two unrelated real multiplications would omit the cross terms and compute a different operation.

Four products describe this direct implementation, not a universal lower bound. The same example can use `p = 2×4 = 8`, `q = 3×5 = 15`, and `r = (2+3)(4+5) = 45`; then the real result is p−q and the imaginary result is r−p−q. That uses three multiplications with additional additions and different intermediate ranges. This constructed identity is not the paper's accelerator design.

### What the paper adds

BayesCVNN introduces dropout-based uncertainty estimation, searches real/imaginary dropout placements, and generates FPGA accelerators. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1610&sess=sess121). The recovered manuscript carries the DAC DOI and supplies the method and evaluation. [Manuscript, PDF page 1](https://arxiv.org/pdf/2604.19993v1#page=1).

One ordinary forward evaluation returns a prediction for a fixed input and fixed parameters. Introducing dropout masks makes selected intermediate channels vary between evaluations. Repeating the computation produces a collection of predictions rather than a single result. The variation can supply information about sensitivity to those perturbations.

It is not a direct measurement of whether the answer is correct. If every sampled model is confidently wrong in the same way, their predictions can agree. Randomness creates a distribution of outputs; establishing that this distribution usefully represents uncertainty requires separate evaluation.

### Separate average prediction from disagreement

For a constructed binary classifier, suppose three sampled probabilities for class one are [0.2, 0.5, 0.8]. Their mean is 0.5. The mean squared deviation from that mean is `(0.09 + 0 + 0.09)/3 = 0.06`; its square root is about 0.245. This uses the population-style divisor three; an unbiased sample-variance estimate would use divisor two instead. A reproduction must state the convention.

Predictions [0.5, 0.5, 0.5] have the same mean but zero disagreement. The first set varies across sampled networks; the second consistently assigns equal class probabilities. Mean prediction and disagreement therefore describe different properties. Neither alone proves that the model will recognize unfamiliar or dangerous inputs.

The manuscript uses three samples in its evaluated setup. [Section 5.1, PDF page 5](https://arxiv.org/pdf/2604.19993v1#page=5). Three draws can expose variation, but are a limited basis for estimating a distribution. For an illustrative event occurring independently with probability 0.1, the probability that three samples miss it entirely is `0.9³ = 72.9%`. This is a sampling example, not an observed failure rate of BayesCVNN.

### What does dropout on one component mean?

The allowed choices at each specified Bayesian layer are dropout on the real part, imaginary part, or both. For N such layers, the stated search space has 3^N configurations. [Section 3.3, PDF page 3](https://arxiv.org/pdf/2604.19993v1#page=3).

Ignoring rescaling for a moment, independently masking `2 + 3i` can produce zero, 2, 3i, or `2 + 3i`. Using one common mask for the pair permits only zero or the original number. Dropping only the real component permits `3i` or `2 + 3i`. These choices define different perturbation distributions; they are not equivalent ways to implement the same noise.

The counting also depends on what is fixed. For three preselected Bayesian layers there are 27 real/imaginary/both assignments. If “no dropout” were an additional choice at every layer, there would instead be 4³ = 64. The paper's 3^N count must not be described as enumerating every possible network architecture, dropout rate, or layer placement.

Random masks over fixed learned weights are an approximation to a distribution over models. They do not enumerate all plausible weights or solve the full Bayesian posterior exactly. Holding one component deterministic further restricts that approximation. The manuscript's mathematical construction motivates the method; it does not establish calibrated uncertainty for every new task.

### Check dropout scaling before comparing software and hardware

Figure 3 masks channels and then multiplies retained data by the keep rate. [PDF page 4](https://arxiv.org/pdf/2604.19993v1#page=4). Selected public code uses other conventions: the PyTorch complex-dropout module multiplies by the reciprocal keep rate, whereas the inspected Keras layer only applies the mask. [Pinned PyTorch module](https://github.com/zehuanzhang/BayesCVNN/blob/26556cc74ea07fce99e49a1878d4f1f279680d46/Software/Complex-Valued/complex_dropout.py), [pinned Keras layer](https://github.com/zehuanzhang/BayesCVNN/blob/26556cc74ea07fce99e49a1878d4f1f279680d46/Hardeware/converter/keras/BernoulliDropout.py).

These conventions have different means unless compensated elsewhere. Let the input be x = 4 and the keep probability r = 0.5. Multiplying retained values by r produces output two half the time and zero otherwise, for mean one. Applying the mask alone gives mean two. Dividing retained values by r produces eight half the time, for mean four. In general the means are r²x, rx, and x respectively.

The distinction is not cosmetic when comparing trained models, numerical validation, or predicted uncertainty. Compensation in other layers could reconcile a convention, but that must be demonstrated along the actual training-to-hardware path. The selected-file inspection does not establish which convention generated the published hardware results. This remains an unresolved reproduction issue, not a claim that the whole experiment is invalid.

Mask sharing differs too: the inspected PyTorch code makes channel masks per batch example for four-dimensional inputs, while the Keras layer broadcasts one channel mask across the batch. That matters when interpreting independence across examples or batching repeated samples. No end-to-end conversion path was executed or fully traced.

### Search for a stated objective, not an undefined best model

The search evaluates accuracy, expected calibration error, and dropout-component count; mutation and crossover explore configurations. [Section 4.2, PDF page 3](https://arxiv.org/pdf/2604.19993v1#page=3). A mutation changes a candidate; crossover combines parts of two candidates. Repeatedly keeping favorable candidates can find useful designs without proving a global optimum over an unrestricted space.

Accuracy counts correct predictions. Calibration asks whether confidence agrees with empirical correctness. For a constructed bin of 100 predictions with average confidence 0.9 but 70 correct answers, the confidence–accuracy gap is 0.2. Expected calibration error combines such gaps across bins, weighted by their example counts. Bin choices and sample counts affect the estimate.

Lower calibration error need not mean higher accuracy. A model can become less confident on wrong answers and improve calibration without correcting them. Conversely, a classifier can answer more questions correctly while becoming more overconfident on its remaining errors. Both quantities matter, and neither guarantees behavior outside the evaluated distribution.

The CHAR results illustrate this tradeoff: the manual configuration has accuracy 82.81% and ECE 0.59%; the minimum-ECE configuration has 77.06% and 0.53%. [Table 1, PDF page 5](https://arxiv.org/pdf/2604.19993v1#page=5). The calibration improvement accompanies a 5.75-percentage-point accuracy loss. It is not an improvement in every objective.

Counting dropout components is also only a hardware-cost proxy. A component operating on a small tensor need not cost the same as one operating on a much larger tensor. Mask generation, width, parallelism, routing, and buffering affect actual cost. Evidence from the evaluated designs does not make component count universally interchangeable with silicon area or power.

### Why the two hardware mappings trade resources for latency

For complex multiplication, the latency-oriented mapping uses four engines; the resource-oriented mapping reuses two across the real and imaginary inputs. [Section 4.3, PDF page 4](https://arxiv.org/pdf/2604.19993v1#page=4).

In a simplified schedule where each real sub-operation takes one time unit, four engines can finish the four products together. Two engines need two rounds. Both still need the final sum and difference, and the actual layer includes many products, memory reads, and control operations. The toy schedule explains the tradeoff but is not a timing model for the published implementation.

Sharing an engine also changes storage lifetimes. Results from the first round must remain available while the second round runs. Duplicating engines increases simultaneous demand for operands. Whether the faster arithmetic organization improves full latency depends on memory supply and other stages.

Dropout does not eliminate the cost of obtaining an uncertainty estimate. Multiple forward passes must still be produced, either sequentially, in parallel with more resources, or with carefully justified reuse of computation. Any reused state must preserve the intended mask behavior rather than inadvertently make supposedly different samples identical.

### Keep the performance denominators aligned

Table 2 compares RTX 3090 Ti with Kintex XCKU115 at 181 MHz. Small/large-model latency is 9.65/16.73 ms on GPU and 0.70/3.64 ms on FPGA; power is 112 W versus 3.81/4.65 W. Latency covers three samples; energy is labeled per forward pass. [PDF page 6](https://arxiv.org/pdf/2604.19993v1#page=6).

The listed times imply about 13.79× and 4.60× speed ratios, using the displayed rounded values. Those are comparisons to the specified GPU implementation, not all GPUs or all complex-valued models.

For the small FPGA design, `3.81 W × 0.70 ms / 3 = 0.889 mJ` per pass, matching the tabulated 0.89 mJ. Omitting the division by three yields 2.667 mJ, the energy for the three-sample calculation under this constant-power assumption. The same denominator distinction must be applied to the GPU before comparing energy efficiency.

The experimental section uses HLS synthesis reports and FPGA implementation tools. [Section 5, PDF page 4](https://arxiv.org/pdf/2604.19993v1#page=4). The recovered text does not establish a wall-plug measurement boundary or complete host-transfer timing. The writeup therefore does not promote these figures into measured whole-system deployment savings. Reproduction must identify power acquisition, batching, transfers, bit widths, and the aggregation of sample outputs.

### What this contributes to the larger theme

This paper is not primarily a low-bit quantizer. It belongs in the discussion because it couples an approximate statistical representation of model uncertainty to hardware organization. The broader taxonomy must preserve that distinction rather than treating all approximation as reduced numerical precision.

RESP uses sensitivity measurements to remove structures. BayesCVNN deliberately varies selected structures during repeated inference to characterize prediction variation. Both depend on what the measurements actually mean, but their purposes and correctness conditions differ.

A testable longer-term hypothesis is that useful uncertainty estimates need a joint budget for output quality, calibration, sample count, and hardware cost. Faster sampling is valuable only if the sampling procedure remains consistent with the trained model and the required uncertainty behavior. The dropout-convention discrepancy is precisely the kind of implementation boundary that such a comparison must resolve.

No BayesCVNN training, inference, HLS synthesis, or FPGA execution was performed. Selected code at the pinned revision was read only. Dropout-convention reconciliation, measurement provenance, broader uncertainty tests, and independent comprehension review remain open.

<span id="explanation-dac-2026-research1885"></span>

## PEACE: compressed matrices still need a correct execution schedule

### What the available source establishes

PEACE combines column-energy-guided matrix compression with RISC-V extensions, metadata fetching, operand loading, a reconfigurable systolic processing-element array, and partial-sum merging. [Official DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1885&sess=sess175).

No manuscript was recovered. “Column energy” is not defined in the description; it must not automatically be interpreted as either electrical energy or the sum of squared matrix values. Likewise, the description does not establish whether compression preserves every original value or discards some contributions. The following examples explain the requirements such a system faces, not the unrecovered PEACE algorithm.

### Begin with the matrix product that must be preserved

For matrices A and B, output entry `C[i,j] = sum_k A[i,k]×B[k,j]`. The shared index k identifies which input components must be paired. Rearranging stored values is safe only if the implementation preserves this pairing and the correct output destination.

Consider one constructed output row with input [2, 3, 5, 7] and weight columns [4, 0, 0, 6] and [0, 8, 9, 0]. The outputs are `2×4 + 7×6 = 50` and `3×8 + 5×9 = 69`. Zero products need not contribute to the sums.

Storing the first column as the compact list [4, 6] is insufficient by itself. Its original row indices [0, 3] identify input values [2, 7]. Pairing [4, 6] with the first two input values [2, 3] instead produces 26. Compression has removed positions as well as zeros, so metadata must restore their meaning during execution.

The same obligation applies if compression uses tiles, permutations, or groups rather than explicit indices. The representation must tell the loader which operand is required, and tell the accumulator where its product belongs.

### Storage savings depend on metadata, not only zero count

In a toy column with 256 signed eight-bit entries, dense storage is 256 bytes. Suppose a sparse representation stores one eight-bit row index and one eight-bit value for each nonzero entry. At 64 nonzeros, that is 128 bytes before column pointers or alignment. At 192 nonzeros, it is 384 bytes—larger than dense storage.

For this simple encoding, the break-even nonzero fraction is one half before other overhead. It is not a universal sparse-format threshold: run lengths, block indices, shared tables, and compressed indices change the calculation. It demonstrates why a reported matrix-compression ratio needs to include its metadata format.

Metadata also consumes bandwidth. If the arithmetic unit receives a value but its matching index or table entry has not arrived, the multiply cannot safely proceed. A separate metadata fetcher may reduce that delay, but its throughput, cache behavior, and synchronization must be measured.

### Sparse work can be unevenly distributed

A processing element is a small arithmetic unit that performs operations such as multiplication and accumulation. An array contains many such units. A systolic organization moves operands or partial results between neighboring units on a coordinated schedule.

Suppose four lanes receive sparse columns with [8, 1, 1, 2] useful operations and each lane completes one operation per cycle. If all start together and synchronize after their columns, the group takes eight cycles. There are twelve useful operations in 32 available lane-cycles, for 37.5% utilization.

An ideal redistribution could divide twelve independent operations into three per lane, but matrix products are not necessarily freely interchangeable. Moving work can require different inputs, destination tags, and partial-sum merges. A schedule that balances operation counts but doubles operand traffic may lose much of the expected benefit.

This is why compression and scheduling need to be evaluated together. A compact matrix in memory does not prove that an arithmetic array stays busy. Conversely, padding a representation with some redundant work can occasionally improve regular access enough to reduce elapsed time. The right comparison measures the complete execution rather than assuming either choice wins.

### Partial sums must merge without losing identity or precision

Split the first example's output 50 into contributions 8 and 42. Two units can compute them separately, but the merger must add both to the same output and must not count either twice. If a later operation reuses the accumulator before the 42 arrives, the result can be corrupted despite correct individual products.

A hardware implementation therefore needs an ordering or tagging rule, a way to recognize completed outputs, and sufficient buffering when contributors arrive at different times. A dedicated partial-sum adder is a component, not by itself a proof that these conditions hold.

Arithmetic range also matters. One product of signed eight-bit values can be as large as `(−128)×(−128) = 16,384`. Summing 256 such products gives 4,194,304, which exceeds the maximum positive value of a signed 23-bit integer, 4,194,303. At least 24 signed bits are needed for that constructed worst case without saturation or another policy. Eight-bit inputs do not imply an eight-bit accumulator.

If intermediate results are rounded or saturated, reassociating their additions may change the answer. The compression format, execution schedule, and numerical policy must therefore be checked together before describing the transformation as exact.

### Do not confuse small numerical magnitude with small electrical cost

If a hypothetical compression rule drops a column with small squared norm, it is using a numerical importance proxy. That is different from measuring joules consumed when processing that column. Switching activity, memory accesses, operand widths, and control logic affect electrical energy.

Nor does small numerical magnitude guarantee a small output contribution. A discarded weight of 0.001 multiplied by an activation of 1,000 contributes one. Whether that matters depends on other contributions and the task. A rule that drops nonzero values requires an error or quality evaluation; merely repacking existing zeros does not introduce that particular error.

The manuscript must resolve which operation PEACE performs. Until then, the atlas should not classify its compression as lossless, assign it a specific norm formula, or claim task accuracy is preserved. The current subtheme placement remains a routing choice requiring finer mechanism-level reconciliation.

### An instruction extension does not eliminate transfer costs

A processor instruction can request accelerator work through a defined interface. The work still needs operands, metadata, a result destination, and completion handling. If a matrix must first be compressed or copied into a special layout, that preparation may dominate short jobs.

For a constructed recurring workload, suppose compression takes 20 ms and each execution saves 0.2 ms. One hundred executions merely recover the preparation time; more than one hundred are needed for a net time saving, ignoring other overhead. Fixed weights reused many times differ from matrices regenerated for every input.

Similarly, reducing one GEMM operation from 10 ms to 6 ms saves four milliseconds. If new packing and dispatch add five milliseconds, the full operation becomes slower. Timing only the arithmetic array would conceal that reversal.

### Keep the reported metrics in their proper units

The description reports 2.705 mm² at 14 nm, peak INT8 efficiency of 88 GOPS/W, 1.60–1.67× speedup over a RISC-V core across fourteen LLMs, and comparisons of 4.4× PE density, 1.79× average speed, and 2.53× energy efficiency against other designs. Baseline names and full conditions are absent. [DAC description](https://63dac.conference-program.com/presentation/?id=RESEARCH1885&sess=sess175).

GOPS/W divides billions of operations per second by watts. It is an efficiency measure, not throughput alone. Under a consistent operation definition, 88 GOPS/W corresponds to about 11.36 picojoules per counted operation. Without power, it does not establish the number of operations completed per second. Whether a multiply-accumulate counts as one operation or two must also be stated.

A 1.60× speed ratio leaves 62.5% of baseline time, a 37.5% reduction. A 2.53× efficiency ratio corresponds to about 39.5% of baseline energy per matched unit of work if that is the denominator used. These quantities cannot be combined with a density maximum to describe a single operating point unless the evaluation establishes that they belong to the same configuration.

Higher processing-element density means more such units per area under the reported definition. It does not guarantee higher useful throughput if metadata or memory cannot supply them. A 14 nm area report also does not, by itself, establish a fabricated-chip measurement; synthesis, physical design, and measured silicon are different evidence levels.

The missing conditions include model names, matrix sizes, sparsity patterns, clock, memory bandwidth, numerical accuracy, operation counting, and whether preparation is included. The present evidence cannot support a fair ranking against dense GPU inference or all sparse accelerators.

### What PEACE adds to the comparison

RESP removes model structures; CO-MAC changes an execution order; PEACE connects matrix representation to operand supply and partial-result merging. All involve reducing work or its cost, but preserving indices and accumulation is central to matrix compression in a way that a simple bit-width comparison misses.

A testable long-term hypothesis is that metadata processing increasingly determines whether compressed arithmetic delivers a system benefit. Testing it requires the fraction of time and energy spent fetching metadata, selecting operands, waiting for imbalanced work, and merging results across multiple workloads. The hypothesis is not established by this one description.

No PEACE code, model benchmark, circuit, or synthesis was executed. This explanation closes the missing individual-writing slot, not the manuscript, evidence, classification, or independent comprehension requirements.

## When an approximation can stop working

Errors can accumulate through repeated operations, and later operations can be more sensitive to some errors than others. A format tuned to one distribution of values can behave differently when the input distribution changes. Rare values can matter even if they contribute little to an average representation-error score.

Measure both numerical behavior and application output. For a model, use a clearly identified task and quality measure. For another computation, state the error requirement appropriate to its result. Test difficult inputs and cases where the selected range or precision is inadequate. If correction or a higher-precision fallback is used, include how often it runs and what it costs.

## The comparison that establishes an improvement

Hold the required answer quality fixed and compare full execution time, energy, storage, and hardware cost. Include encoding, decoding, scaling, conversion, metadata, and correction. State whether training or calibration is required and whether that work is included.

The useful research conclusion is a conditional one: a particular representation and execution method reduces a stated cost while satisfying a stated output requirement on the tested inputs. Extending that result to new models, workloads, or hardware requires checking which of those conditions still hold.

## Compare the results carefully

First identify the inputs and required output quality. Then identify the limited resource: time, memory, communication, energy, circuit area, or correctness coverage. Ask which part of the method reduces that cost and which new cost it adds. Compare numbers only when the experiments hold these conditions sufficiently similar.

A conference description may explain the proposal while omitting the full experiment. An author preprint link may have been coded from its abstract. The source classification does not by itself establish that every table was read. Missing locations remain visible below.

## Complete captured evidence

These are evidence records, not substitutes for the explanations above. Each record preserves its problem, proposed method, measurements, comparison conditions, and source limits. A populated record does not establish that its mechanism has been fully explained or independently verified.

<span id="paper-dac-2026-research1610"></span>

### Algorithm and Hardware Co-Design for Efficient Complex-Valued Uncertainty Estimation

DAC 2026 · Record: `dac-2026-research1610`

[Read the step-by-step explanation](#explanation-dac-2026-research1610)

**Updated source-backed reading card**

Reviewed 2026-09-07. DAC manuscript and selected pinned code inspected; separates complex arithmetic, sample disagreement, calibration and accuracy; flags unreconciled dropout scaling and batching conventions.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Cost of dropout-based uncertainty estimates in complex-valued neural networks and configuration choices across real/imaginary components.

**Mechanism / artifact:**

BayesCVNN real/imaginary/both dropout placement, evolutionary search, four-engine latency-oriented or two-engine reused complex arithmetic, FPGA generation.

**Workload — the work tested:**

MNIST ComplexLeNet, radar HAR CHAR, Chicago/Houston SAR small/large models; three Bayesian samples.

**Hardware and manufacturing assumptions:**

Kintex XCKU115, 181 MHz, Vivado/HLS 2019.2; synthesis-report latency/resources and implementation flow. Power measurement and full host boundary not established.

**Baseline — the comparison method:**

Manual both-component dropout configuration; RTX3090Ti; selected prior real-Bayesian and complex-network accelerators with differing models.

**Reported measurements:**

Small/large latency GPU 9.65/16.73 ms versus FPGA 0.70/3.64 ms for three samples; power 112 W versus 3.81/4.65 W. Energy table is per forward pass. CHAR minimum-ECE configuration accuracy 77.06% versus manual 82.81%, ECE 0.53% versus 0.59%.

**Limits on the conclusion:**

Figure 3 multiplies kept values by keep rate; pinned PyTorch uses reciprocal, inspected Keras masks without rescaling and shares mask across batch. Full conversion path not traced, results not reproduced. Sample variance is not correctness; three samples and ECE do not establish universal uncertainty reliability.

**Source and location**

Evidence tier: DAC manuscript and selected pinned code; discrepancies unresolved, not reproduced. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2604.19993v1)

PDF p. 3 search space; p. 4 mapping, Figure 3 and setup; p. 5 Table 1; p. 6 Table 2. Selected code at 26556cc74ea07fce99e49a1878d4f1f279680d46 linked in explanation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** software complex uncertainty estimation

real-valued approximation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1610

**Hardware or process assumptions:** Specialized complex arithmetic accelerator; precision and memory assumptions are unspecified.

**Limits:** No calibration, likelihood, latency, area, energy, or precision results are reported.

Complex arithmetic may be workload specific.

Official description only; task and hardware validation is required.

**Method or artifact:** Algorithm and hardware co-design for complex-valued uncertainty estimation.

**Metrics:** Uncertainty-estimation efficiency is claimed qualitatively

**Problem:** Complex-valued models need uncertainty estimates without prohibitive compute and memory cost.

**Workload or benchmark:** Complex-valued neural or signal-processing workloads; datasets and uncertainty metrics are unspecified.

</details>

<span id="paper-dac-2026-research1692"></span>

### CORE: Compact, Optimized, and Resource-Efficient Compute Engine for FP-INT GEMM Acceleration with Binary Coding Quantization

DAC 2026 · Record: `dac-2026-research1692`

[Read the step-by-step explanation](#explanation-dac-2026-research1692)

**Updated source-backed reading card**

Reviewed 2026-09-07. Official description recovered with method and numerical results omitted by earlier card; matching manuscript not recovered.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Residual scaling multiplication and representation error in binary-coded weight-only quantization.

**Mechanism / artifact:**

SS-BCQ power-of-two-sum scales; CORE pipelined GEMM engine, block activation scaling, extra processing for important weights.

**Workload — the work tested:**

OPT-6.7B quality example; hardware workload suite unspecified.

**Hardware and manufacturing assumptions:**

Process, clock, memory, bit widths, synthesis/measurement methodology unspecified in description.

**Baseline — the comparison method:**

Prior BCQ for quality; FP–INT accelerators for efficiency; names not supplied.

**Reported measurements:**

Perplexity reduced by 3.14; up to 1.41× TOPS/mm² and 2.18× TOPS/W; absolute results unspecified.

**Limits on the conclusion:**

Description only; detailed coding, scale selection, importance criterion, operation-count convention, and full-system results unverified. No manuscript pages or reproduction claimed.

**Source and location**

Evidence tier: Official description; matching manuscript not recovered. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH1692&sess=sess142)

Official Description, method and final results sentences; no PDF pages available.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** floating-point GEMM

standard low-bit GEMM

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1692

**Hardware or process assumptions:** Compact mixed-precision accelerator; quantizer, memory, and process assumptions are unspecified.

**Limits:** No accuracy, throughput, area, energy, or precision results are reported.

Binary coding may introduce task-dependent error.

Official description only; model and silicon validation is required.

**Method or artifact:** Resource-efficient GEMM engine using binary coding quantization.

**Metrics:** Resource efficiency is claimed qualitatively

**Problem:** Mixed FP-INT GEMM needs efficient arithmetic and quantization with limited hardware resources.

**Workload or benchmark:** FP-INT GEMM and DNN workloads; models, precision, and hardware platform are unspecified.

</details>

<span id="paper-dac-2026-research1885"></span>

### PEACE: Algorithm–hardware Co-Design for PE-Granular Energy-Aware Compressed GEMM Acceleration

DAC 2026 · Record: `dac-2026-research1885`

[Read the step-by-step explanation](#explanation-dac-2026-research1885)

**Updated source-backed reading card**

Reviewed 2026-09-07. Description inspected; explains index preservation, metadata costs and scheduling while leaving compression exactness and column-energy definition unresolved.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Irregular sparse GEMM can underutilize arithmetic hardware and incur inefficient data supply.

**Mechanism / artifact:**

PEACE-Alg column-energy-guided compression; PEACE-Hw RISC-V extensions, metadata fetcher, operand loader, reconfigurable systolic array and partial-sum adder. Exact algorithm unrecovered.

**Workload — the work tested:**

Fourteen transformer LLMs; names, matrix shapes, sparsity and quality settings not specified.

**Hardware and manufacturing assumptions:**

14 nm ASIC area report of 2.705 mm²; clock, memory boundary and fabrication/measurement evidence unavailable.

**Baseline — the comparison method:**

Unnamed RISC-V core; unnamed state-of-the-art designs with unrecovered comparison conditions.

**Reported measurements:**

Peak INT8 88 GOPS/W is efficiency, not throughput alone. RISC-V speedup 1.60–1.67×; other comparisons report 4.4× PE density, 1.79× average speedup and 2.53× energy efficiency.

**Limits on the conclusion:**

No manuscript recovered; lossless versus approximate compression, column-energy definition, metadata format, accumulation and preparation costs unknown. No execution or synthesis; subtheme classification needs mechanism-level reconciliation.

**Source and location**

Evidence tier: Official description only; manuscript and reproduction missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH1885&sess=sess175)

Official Description and Authors; no manuscript page locators available.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense GEMM accelerator

generic compressed GEMM

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1885

**Hardware or process assumptions:** Processing-element array with compressed operands; memory and process assumptions are unspecified.

**Limits:** No accuracy, energy, throughput, area, or compression results are reported.

PE granularity may be architecture-dependent.

Official description only; model and hardware validation is required.

**Method or artifact:** Algorithm-hardware co-design with PE-granular energy-aware compressed GEMM.

**Metrics:** Energy-aware GEMM efficiency is claimed qualitatively

**Problem:** Compressed GEMM must balance energy, processing-element utilization, and numerical quality.

**Workload or benchmark:** Dense or compressed GEMM and DNN workloads; models, sparsity, and precision are unspecified.

</details>

<span id="paper-dac-2026-research1999"></span>

### HAP: Efficient Quantization Harnessing Adaptive Precision for DNN Hardware Acceleration

DAC 2026 · Record: `dac-2026-research1999`

[Read the step-by-step explanation](#explanation-dac-2026-research1999)

**Updated source-backed reading card**

Reviewed 2026-09-07. DAC manuscript recovered separately from DATE version; distinguishes exact activation re-encoding from weight/model error and modeled hardware results.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Redundant activation coding and load imbalance in variable-width arithmetic.

**Mechanism / artifact:**

Group-wise dynamic offset, 4/8-bit weight-channel protection, and bit-serial reorder engine.

**Workload — the work tested:**

ResNet18, VGG19, ViT-B, DeiT-S on ImageNet-1K; OPT-1.3B/2.7B on WikiText-2.

**Hardware and manufacturing assumptions:**

65-nm synthesis at 500 MHz; cycle simulation and CACTI memory-energy estimates, not fabricated-chip measurements.

**Baseline — the comparison method:**

Hardware: Stripes, ShapeShifter, BitWave. Quality: SQuant, NoisyQuant, SmoothQuant, OmniQuant-LWC.

**Reported measurements:**

HAP_W4.6: 2.65× speedup and 55% energy reduction versus Stripes. ViT-B top-1 82.98% versus floating-point 84.54%.

**Limits on the conclusion:**

Exact re-encoding preserves quantized integers, not original floating-point values. Weight-quality tradeoffs remain; hardware/model reproduction and independent confirmation unverified.

**Source and location**

Evidence tier: Author hosted DAC manuscript; selected method/evaluation inspected, not reproduced. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://www.ece.ualberta.ca/~jhan8/publications/DAC2026_Camera_Ready.pdf)

PDF pp. 2–3 DAR and dataflow; pp. 4–5 reorder engine; pp. 5–6 evaluation and Table 1.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** uniform quantization

post-training quantization

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH1999

**Hardware or process assumptions:** Mixed-precision accelerator or memory system; conversion and control overheads are unspecified.

**Limits:** No accuracy, bit-width, throughput, energy, area, or model-coverage results are reported.

Adaptive precision may add metadata and control overhead.

Official description only; model and silicon validation is required.

**Method or artifact:** Adaptive-precision quantization for hardware acceleration.

**Metrics:** Quantization efficiency is claimed qualitatively

**Problem:** Uniform quantization wastes precision where DNN layers have different sensitivity.

**Workload or benchmark:** DNN inference; models, layer precision, and hardware target are unspecified.

</details>

<span id="paper-dac-2026-research2094"></span>

### DAPA: Distribution Aware Piecewise Activation Functions for On-Device Transformer Inference and Training

DAC 2026 · Record: `dac-2026-research2094`

[Read the step-by-step explanation](#explanation-dac-2026-research2094)

**Updated source-backed reading card**

Reviewed 2026-09-07. Manuscript and pinned public inference/fitting code inspected; separates latency and DSP baselines, forward and backward approximations, and unreproduced training/hardware claims.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Cost of nonlinear activation computation while retaining model quality.

**Mechanism / artifact:**

Distribution-quantile intervals, weighted line fitting, fixed-point selection; separate derivative approximation described for training.

**Workload — the work tested:**

ViT/DeiT/Swin on ImageNet-1K; GPT-2 on WikiText-2; BERT on GLUE; ViT training experiments.

**Hardware and manufacturing assumptions:**

Vitis HLS 2025.1, 200 MHz; FPGA component synthesis, not measured whole-model acceleration.

**Baseline — the comparison method:**

Authors' tanh-based GELU: latency comparison. Prior PEANO-ViT GELU: 16× DSP comparison. PyTorch: model-quality reference.

**Reported measurements:**

Fix16 GELU 320 ns versus DAPA 20 ns (16×); prior GELU 16 DSPs versus DAPA 1; own GELU 8 DSPs. Full softmax 155 ns. GPT-2 PPL 29.47 versus 29.37.

**Limits on the conclusion:**

Training and hardware not reproduced; inspected public module does not establish separate backward rule. ViT-Tiny table implies 0.25-point extra quantization loss versus prose 0.23. Average approximation error does not bound downstream model error.

**Source and location**

Evidence tier: DAC accepted arxiv manuscript and selected public code; not reproduced. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2603.19338v1)

PDF pp. 3–6 methodology; p. 7 Table 2; pp. 8–9 training; pp. 9–10 Table 4 and HLS. Public code commit a2c58e0b83962cb3ea996998722b8ce35b234b5a inspected separately in linked explanation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** standard GELU or ReLU

uniform piecewise approximation

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2094

**Hardware or process assumptions:** Embedded transformer accelerator; arithmetic, memory, and device constraints are unspecified.

**Limits:** No accuracy, approximation error, latency, energy, area, or model results are reported.

Activation distributions may shift after deployment.

Official description only; training and inference validation is required.

**Method or artifact:** Distribution-aware piecewise activation functions for transformers.

**Metrics:** On-device transformer efficiency is claimed qualitatively

**Problem:** Transformer activations have distributions that make on-device nonlinear computation costly.

**Workload or benchmark:** On-device transformer inference or training; models, datasets, and precision are unspecified.

</details>

<span id="paper-dac-2026-research2184"></span>

### Adana: Accelerating Large Language Models via Adaptive Nonuniform Asymmetric Quantization

DAC 2026 · Record: `dac-2026-research2184`

[Read the step-by-step explanation](#explanation-dac-2026-research2184)

**Updated source-backed reading card**

Reviewed 2026-09-07. Manuscript inspected; explains format decoding and approximate online selection, preserves lossy quality and simulation/baseline boundaries.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Small-group range asymmetry and uneven density, with costly runtime activation quantization.

**Mechanism / artifact:**

Integer base grid plus movable half-step levels; count-based online mode selection; decoded fixed-point matrix engine and quantization engine.

**Workload — the work tested:**

WikiText-2 LLM perplexity; Mistral-7B zero-shot tasks; hardware simulation on Llama-3.1-8B, Phi-2-2.7B, Gemma-3-4B, Qwen-3-14B.

**Hardware and manufacturing assumptions:**

28-nm synthesis at 500 MHz, 0.9 V, 25°C; PrimeTime PX power and CACTI SRAM; cycle simulation with iso-area PE counts and equal SRAM/DDR configuration.

**Baseline — the comparison method:**

INT-Asym, ANT, M-ANT, BitMod; quality comparisons adapt formats to common group sizes and joint weight/activation quantization.

**Reported measurements:**

Body: 1.42× speedup and 17.91% energy reduction versus BitMod; 3.50% higher latency versus INT-Asym. Llama-3.2-1B W3/A3 perplexity 53.95 versus FP16 9.75.

**Limits on the conclusion:**

Approximate selection can misrank original reconstruction error. Storage codes decode to wider arithmetic values. Table 6 lossless label does not establish exact recovery. Abstract power and body energy claims are distinct. No implementation or hardware reproduced.

**Source and location**

Evidence tier: Author hosted DAC manuscript; method/evaluation inspected, not reproduced. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://www.ece.ualberta.ca/~jhan8/publications/2026Adana.pdf)

PDF pp. 2–3 numeric type; pp. 3–4 Algorithms 1–2 and KV grouping; pp. 5–6 quality; p. 6 hardware conditions and performance.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** uniform symmetric quantization

floating-point LLM inference

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2184

**Hardware or process assumptions:** Low-bit LLM accelerator or memory system; dequantization and precision assumptions are unspecified.

**Limits:** No perplexity, task accuracy, throughput, energy, memory, or bit-width results are reported.

Quantizer behavior may vary across models and layers.

Official description only; model and hardware validation is required.

**Method or artifact:** Adaptive nonuniform asymmetric quantization for LLMs.

**Metrics:** LLM acceleration is claimed qualitatively

**Problem:** LLM weight and activation distributions are asymmetric and poorly served by uniform quantization.

**Workload or benchmark:** LLM inference; models, bit widths, sequence lengths, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research2207"></span>

### PRISM: Priority Aware Shared Scale Microscaling Format for 4-Bit Quantization

DAC 2026 · Record: `dac-2026-research2207`

[Read the step-by-step explanation](#explanation-dac-2026-research2207)

**Updated source-backed reading card**

Reviewed 2026-09-07. Official description inspected; shared-scale encoding distinguished from element precision. Full manuscript and priority rule remain missing.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Quantization error associated with limited shared-scale precision and range in low-bit grouped formats.

**Mechanism / artifact:**

Four-bit quantization with one eight-bit encoded group scale whose representation adapts to relative value importance; exact codebook and priority rule unknown.

**Workload — the work tested:**

Modern AI models; model names, datasets, quality metrics, group sizes and calibration settings not specified.

**Hardware and manufacturing assumptions:**

Scale-format hardware; process, clock, decoder, accumulation and measurement methodology unavailable.

**Baseline — the comparison method:**

Description discusses MXFP4 and NVFP4; reference configuration for overhead figures is not specified.

**Reported measurements:**

Reported improved accuracy without values; 0.62% area and 0.86% energy overhead, not reductions.

**Limits on the conclusion:**

No manuscript recovered. Scale layout, relative-importance measure, group size and quality conditions unverified. Constructed scale/error examples are not PRISM experiments. No execution or synthesis.

**Source and location**

Evidence tier: Official description only; manuscript and reproduction missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2207&sess=sess145)

Official Description and Authors; no manuscript pages available.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** uniform 4-bit quantization

per-group scaling

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2207

**Hardware or process assumptions:** Low-bit arithmetic and shared-scale hardware; conversion and metadata assumptions are unspecified.

**Limits:** No accuracy, scale overhead, throughput, energy, area, or model results are reported.

Priority definitions may be workload-specific.

Official description only; model and implementation validation is required.

**Method or artifact:** Priority-aware shared-scale microscaling format.

**Metrics:** 4-bit quantization efficiency is claimed qualitatively

**Problem:** Four-bit quantization needs scale allocation that protects important values without excessive metadata.

**Workload or benchmark:** 4-bit neural inference or training; models, priorities, and precision metrics are unspecified.

</details>

<span id="paper-dac-2026-research2317"></span>

### Ultrasketchllm: Sub-1-Bit LLM Compression via Sketch and Hardware-Friendly Operators

DAC 2026 · Record: `dac-2026-research2317`

[Read the step-by-step explanation](#explanation-dac-2026-research2317)

**Updated source-backed reading card**

Reviewed 2026-09-07. DAC v2 manuscript and pinned code inspected; separates nominal payload from peak memory and flags loaded maximum-magnitude kernel versus manuscript minimum rule.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Extreme weight-storage compression with reconstruction error and irregular access costs.

**Mechanism / artifact:**

AbsMaxMin sketch, importance-based allocation, straight-through fine-tuning, matrix reconstruction with projection caching.

**Workload — the work tested:**

Llama3 and Qwen3; Wikitext and downstream tasks; AQLM and VPTQ comparisons; context length 512 for fine-tuning.

**Hardware and manufacturing assumptions:**

Two A100 GPUs for fine-tuning; GPU software implementation with layer-wise reconstructed weights; full inference setup requires further recovery.

**Baseline — the comparison method:**

FP16 memory baseline; hash sketch implementation for operator speedup; AQLM and VPTQ for quality/memory comparisons.

**Reported measurements:**

Nominal 0.5 bits/weight via 1/8 sketch and four-bit quantization; up to 6.93× peak-memory reduction versus FP16; up to 14.9× operator speedup versus hash sketch, not whole-model FP16 speedup.

**Limits on the conclusion:**

Loaded matrix kernel selects maximum magnitude versus manuscript minimum rule; inspected fake-quantized export does not verify packed four-bit storage. Reconstruction buffers remain. No model, kernel, training, or memory reproduction.

**Source and location**

Evidence tier: DAC v2 manuscript and selected pinned code; discrepancies unresolved, not reproduced. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2506.17255v2)

PDF pp. 3–4 method, Algorithms/Equations; pp. 5–6 evaluation. Selected public code at ab69c9aeaa60ebc57618bfb66a056fb8eaec18ee linked in explanation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** 4-bit quantization

floating-point LLM

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2317

**Hardware or process assumptions:** Sub-bit memory/compute accelerator; sketch storage, decoding, and precision assumptions are unspecified.

**Limits:** No perplexity, task accuracy, compression ratio, latency, energy, or hardware results are reported.

Sketch errors may vary by model and layer.

Official description only; model and implementation validation is required.

**Method or artifact:** Sketch-based sub-1-bit compression with hardware-friendly operators.

**Metrics:** Sub-1-bit compression efficiency is claimed qualitatively

**Problem:** LLM memory and bandwidth costs remain high even after conventional low-bit quantization.

**Workload or benchmark:** LLM inference; models, tasks, sequence lengths, and decompression hardware are unspecified.

</details>

<span id="paper-dac-2026-research2374"></span>

### MXP: A Posit-Inspired Microscaling Format for Vision-Language Tasks

DAC 2026 · Record: `dac-2026-research2374`

[Read the step-by-step explanation](#explanation-dac-2026-research2374)

**Updated source-backed reading card**

Reviewed 2026-09-07. Official description and author-laboratory publication identity inspected; distinguishes element-level tapered precision from group-scale representation. Manuscript remains missing.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Low-bit group quantization struggles with differing value distributions and range-resolution requirements.

**Mechanism / artifact:**

Posit-inspired microscaling with element-level exponent/fraction allocation and a tailored accelerator; bit layout, widths and decoder unknown.

**Workload — the work tested:**

Vision-language tasks per title; model names, datasets, quality measures and configurations unavailable.

**Hardware and manufacturing assumptions:**

Proposed accelerator; process, frequency, scale format, accumulator and measurement method unavailable.

**Baseline — the comparison method:**

Existing formats; no named comparison configuration in description.

**Reported measurements:**

Qualitative claims of less degradation and lower area and power; no quantitative results or energy/latency measurements supplied.

**Limits on the conclusion:**

Manuscript missing; author laboratory lists paper without manuscript link. Optimality objective not defined. Teaching format is not MXP encoding. No implementation, benchmark or synthesis executed.

**Source and location**

Evidence tier: Official description and author identity listing; manuscript and reproduction missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2374&sess=sess143)

Official Description and Authors; https://vlsi.snu.ac.kr/publications/ 2026 conference list confirms identity; no manuscript page locators.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** floating point

standard microscaling format

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2374

**Hardware or process assumptions:** Custom low-precision arithmetic and shared-scale hardware; conversion overhead is unspecified.

**Limits:** No task accuracy, perplexity, bit width, throughput, energy, or area results are reported.

Format behavior may depend on model distributions.

Official description only; model and hardware validation is required.

**Method or artifact:** Posit-inspired microscaling numeric format.

**Metrics:** Vision-language quantization efficiency is claimed qualitatively

**Problem:** Vision-language models need compact numeric formats that preserve heterogeneous activation and weight ranges.

**Workload or benchmark:** Vision-language inference or training; models, bit widths, and hardware are unspecified.

</details>

<span id="paper-dac-2026-research2410"></span>

### CAPA: Convertibility-Aware Mixed-Precision Accelerator for Asymmetric GEMM in Weight-Only Quantized LLMs

DAC 2026 · Record: `dac-2026-research2410`

[Read the step-by-step explanation](#explanation-dac-2026-research2410)

**Updated source-backed reading card**

Reviewed 2026-09-07. Official description supplies HDBFP and efficiency results; manuscript not recovered, so format fields and accuracy equivalence remain unresolved.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Partial-sum overhead and precision conversion in weight-only mixed-format matrix multiplication.

**Mechanism / artifact:**

Hybrid Delta Block Floating Point (HDBFP); BF16/FP16 support; weight decomposition to combine INT8/INT4 arithmetic.

**Workload — the work tested:**

Weight-only quantized LLMs; model names, datasets, matrix shapes, and accuracy metrics unspecified.

**Hardware and manufacturing assumptions:**

Process, clock, memory system, internal widths, and measurement methodology unspecified.

**Baseline — the comparison method:**

FP–FP hardware baseline and GPU accuracy reference, neither specifically identified.

**Reported measurements:**

Reported matching GPU accuracy; 3.98× area efficiency and 4.38× power efficiency; absolute values and explicit efficiency units absent.

**Limits on the conclusion:**

Description only; no verified HDBFP encoding, signed decomposition, bitwise-equivalence guarantee, page-located conditions, or reproduction.

**Source and location**

Evidence tier: Official description; matching manuscript not recovered. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH2410&sess=sess142)

Official Description, methods (1)–(2) and final results sentence; no PDF pages available.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** uniform low-bit GEMM

floating-point LLM inference

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2410

**Hardware or process assumptions:** Mixed-precision accelerator with conversion support; dataflow and process assumptions are unspecified.

**Limits:** No accuracy, conversion overhead, throughput, energy, area, or model results are reported.

Convertibility may depend on bit-width combinations.

Official description only; model and hardware validation is required.

**Method or artifact:** Convertibility-aware mixed-precision GEMM accelerator.

**Metrics:** Quantized LLM efficiency is claimed qualitatively

**Problem:** Weight-only quantized LLMs require asymmetric GEMM and costly conversion between precisions.

**Workload or benchmark:** Weight-only quantized LLM inference; models, bit widths, and memory system are unspecified.

</details>

<span id="paper-dac-2026-research259"></span>

### HierPAS: Accelerating Video Generation Models with Hierarchical Precision and Adaptive Sparsity

DAC 2026 · Record: `dac-2026-research259`

[Read the step-by-step explanation](#explanation-dac-2026-research259)

**Updated source-backed reading card**

Reviewed 2026-09-07. Official description and author entry inspected; manuscript download remains TBD. Conceptual explanation separates normalized attention, sampled importance, removed mass, precision, hardware utilization, and energy-efficiency scope.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

High attention computation cost in diffusion-transformer video generation.

**Mechanism / artifact:**

Early attention-pattern estimate, sampled entropy for head-wise retention, hierarchical precision, configurable top-k selection, unified multi-precision GEMM datapath; exact algorithms and formats unrecovered.

**Workload — the work tested:**

Video-generation models; model names, frame counts, resolution, prompts and quality metrics unavailable in description.

**Hardware and manufacturing assumptions:**

Proposed accelerator; process, frequency, memory organization, supported widths and measurement methodology unavailable.

**Baseline — the comparison method:**

NVIDIA H20 and unnamed state-of-the-art accelerators; matched configurations unverified.

**Reported measurements:**

Up to 178× and 7.7× energy-efficiency claims versus H20 and other accelerators respectively; not latency ratios. Qualitative quality preservation without reported metric values in description.

**Limits on the conclusion:**

Author download is TBD and redirects to publication list. No manuscript page evidence; sampling safeguards, selection granularity, normalization policy, precision assignment, full-system costs and quality conditions unverified. Constructed examples are not HierPAS measurements; no execution.

**Source and location**

Evidence tier: Official description and author abstract; full manuscript and reproduction missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH259&sess=sess127)

Official Description and Authors; author https://austinliu01.github.io/publication/HierPAS confirms identity and missing download. No manuscript locators available.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** dense full-precision generation

static sparsity

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH259

**Hardware or process assumptions:** Mixed-precision sparse accelerator; memory and scheduling assumptions are unspecified.

**Limits:** No perceptual quality, temporal consistency, latency, energy, or sparsity results are reported.

Adaptive choices may be content- and timestep-dependent.

Official description only; model and content validation is required.

**Method or artifact:** Hierarchical precision and adaptive sparsity acceleration method.

**Metrics:** Video-generation efficiency is claimed qualitatively

**Problem:** Video-generation models are expensive and have layer- and timestep-varying sensitivity.

**Workload or benchmark:** Video-generation models; resolutions, frames, quality metrics, and accelerator are unspecified.

</details>

<span id="paper-dac-2026-research2650"></span>

### Think Before You Prune: Self-Reflective Structured Pruning for Reasoning Language Models

DAC 2026 · Record: `dac-2026-research2650`

[Read the step-by-step explanation](#explanation-dac-2026-research2650)

**Updated source-backed reading card**

Reviewed 2026-09-07. Public preprint inspected; explains structured deletion and decode-only importance, corrects percentage-point interpretation, retains dense-quality loss and unfavorable regeneration result.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Pruning calibration and sensitivity objectives can mismatch generated reasoning sequences, especially after earlier pruning changes model behavior.

**Mechanism / artifact:**

RESP self-generated task calibration, masked generated-token negative-log-likelihood, absolute weight-gradient structural scoring and progressive regeneration on fixed prompts.

**Workload — the work tested:**

Qwen3-8B; GSM8K and MathQA; 500 training prompts/task and 2048-token calibration cap; sampled decoding temperature 0.6, seed zero; separate model answer extractor.

**Hardware and manufacturing assumptions:**

Structured model pruning; first 10% and final Transformer blocks protected. Preprint does not establish hardware timing, energy or peak memory gains.

**Baseline — the comparison method:**

Main-table Wanda and GISP plus dense Qwen3-8B; RESP without regeneration ablation.

**Reported measurements:**

40% pruning: GSM8K 81.27% versus dense 96.74% and GISP 14.40%; MathQA 59.60% versus dense 87.60% and GISP 12.60%. Gains over GISP are 66.87 and 47 percentage points. At 30%, GSM8K regeneration 91.36% versus 92.65% without.

**Limits on the conclusion:**

December 2025 preprint, not recovered DAC camera-ready. No execution; exact implementation and sparsity denominator need checking. Generated-token likelihood is not answer correctness. No universal regeneration benefit or hardware speedup established.

**Source and location**

Evidence tier: Public preprint; method and tables inspected, not reproduced or reconciled to DAC camera ready. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2512.02185v1)

PDF p. 5 Eqs. 4–5 and regeneration; p. 6 setup and Tables 1–2; p. 7 regeneration-ratio ablation.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** unpruned reasoning LLM

static structured pruning

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH2650

**Hardware or process assumptions:** Structured-sparse LLM accelerator or runtime; hardware support and precision assumptions are unspecified.

**Limits:** No reasoning accuracy, sparsity, latency, energy, or model results are reported.

Self-reflection may add calibration cost or bias.

Official description only; task-diverse validation is required.

**Method or artifact:** Self-reflective structured pruning method for reasoning LLMs.

**Metrics:** Reasoning-model efficiency is claimed qualitatively

**Problem:** Reasoning LLMs need compression that reduces compute without removing capabilities needed for multi-step reasoning.

**Workload or benchmark:** Reasoning language-model tasks; models, pruning units, and quality metrics are unspecified.

</details>

<span id="paper-dac-2026-research3029"></span>

### CO-MAC: A Center-Out Ordered Stochastic MAC for Low-Latency Inference

DAC 2026 · Record: `dac-2026-research3029`

[Read the step-by-step explanation](#explanation-dac-2026-research3029)

**Updated source-backed reading card**

Reviewed 2026-09-07. Official identity checked; expanded conceptual explanation separates stream overlap, pair-preserving ordering, signed accumulation, and MAC versus inference timing. Manuscript remains missing.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Long execution time for stochastic multiply-accumulate operations.

**Mechanism / artifact:**

Center-out magnitude ordering, incremental magnitude reuse, and sign handling after accumulation; exact circuit and schedule unrecovered.

**Workload — the work tested:**

Convolutional neural network workloads; models and datasets not named in description.

**Hardware and manufacturing assumptions:**

Stochastic MAC avoiding bidirectional counters; process, clock, stream lengths, memory system and implementation evidence unavailable.

**Baseline — the comparison method:**

Prior stochastic MAC architectures, not named in the official description.

**Reported measurements:**

Up to 54.8% MAC latency reduction; description asserts maintained accuracy without values or conditions. Not whole-network latency.

**Limits on the conclusion:**

Full manuscript missing; stream correlation, paired-input addressing, signed intermediate range, sorting cost and matched-quality comparisons unverified. Teaching examples are not the recovered CO-MAC algorithm. No execution or synthesis.

**Source and location**

Evidence tier: Official description only; manuscript and reproduction missing. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://63dac.conference-program.com/presentation/?id=RESEARCH3029&sess=sess174)

Official presentation Description and Authors; Purdue laboratory publication entry confirms identity. No manuscript page locators available.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** binary or fixed-point MAC

conventional stochastic MAC

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3029

**Hardware or process assumptions:** Stochastic-computing accelerator; random sources and process assumptions are unspecified.

**Limits:** No accuracy, latency distribution, energy, area, or bitstream results are reported.

Stochastic variance may depend on input distribution.

Official description only; model and hardware validation is required.

**Method or artifact:** Center-out ordered stochastic multiply-accumulate unit.

**Metrics:** Low-latency stochastic inference is claimed qualitatively

**Problem:** Stochastic MACs can incur variable latency while approximating neural inference.

**Workload or benchmark:** Neural inference; models, bitstreams, precision, and accelerator are unspecified.

</details>

<span id="paper-dac-2026-research3214"></span>

### TopGQ: Fast GNN Post-Training Quantization Leveraging Topology Information

DAC 2026 · Record: `dac-2026-research3214`

[Read the step-by-step explanation](#explanation-dac-2026-research3214)

**Updated source-backed reading card**

Reviewed 2026-09-07. DAC manuscript recovered; distinguishes calibration speed from inference and preserves severe INT4 quality loss and conflicting table values.

This editorial correction updates the current reading view and connected dossiers, not the historical adjudication or scientific acceptance status. The original captured fields are preserved below.

[Correction register](../../data/editorial-paper-corrections-v1.json)

**Problem:**

Expensive GNN quantization preparation and incompatible node-wise scales during aggregation.

**Mechanism / artifact:**

Selective dual-axis scale absorption into adjacency; TopPIN degree/neighbor-reciprocal-degree grouping and nearest-group parameter interpolation.

**Workload — the work tested:**

GCN, GraphSAGE, GIN, GAT/R-GAT; node and graph classification; MAG240M transductive, other datasets inductive.

**Hardware and manufacturing assumptions:**

A6000, RTX4090, Xeon Gold 6442Y for experiments; RTX4090 and Jetson AGX Orin for reported inference comparisons.

**Baseline — the comparison method:**

SGQuant, Degree-Quant, A2Q, DRA; FP32 quality/inference reference; on-the-fly PTQ inference comparison.

**Reported measurements:**

MAG240M preparation 58.8 min versus DRA 2.06 days; accuracy 69.14% versus FP32 69.66%. GCN ogbn-products inference 1.68× RTX4090 and 1.59× Orin versus FP32. INT4 GCN accuracy 39.03% versus FP32 71.25%.

**Limits on the conclusion:**

Graph proxy cannot guarantee activation ranges. INT4 GraphSAGE ogbn-products differs between Table 1 (61.83%) and Table 6 (63.18%). No code or benchmark reproduction; lookup and zero-scale safeguards unverified.

**Source and location**

Evidence tier: DAC manuscript; method/evaluation inspected, not reproduced. This is the stored source classification; the location and limits below determine what was actually read.

[Open the recorded source](https://arxiv.org/pdf/2608.30394v1)

PDF p. 3 scale absorption; p. 4 TopPIN and calibration; p. 5 Tables 1–3; p. 6 inference and ablation Tables 4–6.

<details markdown="1">
<summary>Original captured fields — superseded for this reading card</summary>

** page source tier:** medium_official_description

**Baselines:** uniform GNN quantization

full-precision GNN

**Evidence locators:** DAC 2026 official description

**Evidence url:** https://63dac.conference-program.com/?post_type=page&p=16&id=RESEARCH3214

**Hardware or process assumptions:** Low-precision GNN accelerator or runtime; sparse memory assumptions are unspecified.

**Limits:** No accuracy, bit width, latency, energy, memory, or graph-diversity results are reported.

Topology features may be dataset-specific.

Official description only; graph and hardware validation is required.

**Method or artifact:** Topology-aware GNN post-training quantization.

**Metrics:** GNN quantization efficiency is claimed qualitatively

**Problem:** GNN quantization must preserve graph-topology-sensitive behavior while reducing precision and cost.

**Workload or benchmark:** Graph neural networks; graph datasets, bit widths, and hardware are unspecified.

</details>

## What remains to establish

Resolve unspecified workloads, comparison methods, resource budgets, and source locations before generalizing a reported gain. Multiple papers in this selected sample permit comparison of mechanisms, but do not by themselves establish recurrence across years or a long-term trend.

[All subthemes](../expanded-taxonomy-v1.md) · [Research directions](../directions/README.md)
