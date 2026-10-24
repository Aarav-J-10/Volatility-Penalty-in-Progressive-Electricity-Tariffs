---
title: "The Volatility Penalty in Progressive Electricity Tariffs: Sharp Finite-Sample Bounds and Constrained Tariff Design"
---

*Author information removed for double-blind review.*

**Abstract**

Under an increasing-block electricity tariff, a household whose monthly use swings between seasons pays more over a year than a household with the same total use spread evenly. We call this difference the volatility penalty and study it for marginal-block tariffs with any number of blocks. Because the tariff is convex, the penalty is never negative. It decomposes exactly by threshold: each threshold contributes its price step multiplied by the energy that the household's atypical months spend on the far side of it. For a fixed price step, the penalty is largest when the threshold equals mean consumption. Classical Scarf-type mean–variance bounds are attained by probability distributions, not by a household's n bills; we derive bounds that are attainable for n bills. One consequence is a certificate: the penalty is zero whenever mean use lies at least the standard deviation times √(n−1) from a threshold. For multi-block tariffs, an exact joint bound follows from enumerating how many periods fall in each block. In a synthetic panel of 300 households priced under the reported Uttar Pradesh urban domestic slabs, the joint bound captured a median 67% of the realised penalty, compared with 43% for the Scarf-type bound. Penalties averaged 0.61% of annual energy charges and were concentrated in the most variable archetypes. In a redesign that held revenue within 1%, the binding revenue and coverage constraints, not the choice of objective, determined the penalty. All numerical results are synthetic; application to observed Indian smart-meter data is pending.

**Keywords:** increasing-block tariff; Jensen gap; distribution-free bounds; nonlinear pricing; electricity affordability; tariff design; India

# 1. Introduction

Many Indian distribution companies bill domestic consumers under increasing-block (telescopic) tariffs: the first units each month are cheap, and units in higher slabs cost more. The aim is to keep small consumers' bills low and to have larger consumers cross-subsidise them, and who actually benefits has been studied for California and India [1–4]. Less attention has gone to a mechanical consequence of applying block prices *period by period*. A household that uses 100 kWh in January and 400 kWh in June reaches the expensive slabs in summer, so its annual bill exceeds that of a neighbour who uses 250 kWh every month, although both consume the same energy. Where cooling appliances concentrate use in the hot months, as in northern India, this timing effect is a feature of ordinary consumption rather than an edge case.

We ask four questions. When is the difference guaranteed to be nonnegative, and can it be split exactly across thresholds? How large can it be when only the mean and standard deviation of a household's consumption are known? Which of those bounds can actually be reached by a household with a fixed number of bills and nonnegative consumption? And how does the penalty change when a regulator redesigns the tariff under revenue, progressivity and affordability constraints?

The first question has a classical answer. The bill is a convex function of monthly use, so by Jensen's inequality [5] the average of the bills is at least the bill on average use; the penalty is a *Jensen gap*. For a single threshold it is a multiple of the expected value of a hinge function, the same function that gives the payoff of a call option and the overage cost of an inventory. Bounds on such expectations given a mean and a variance are therefore available: Scarf's inventory bound [6], Lo's option bound [7], the treatment by Gallego and Moon [8], and the nonnegative-support refinement of Bertsimas and Popescu [9]. Jensen's inequality has also been sharpened in general form [10]. We claim none of these results.

What the paper adds is the following. (i) Section 4 collects the tariff-specific identities: an exact *minority-side* representation of the penalty and a complete description of how it varies with the threshold. (ii) Scarf-type bounds treat consumption as a random variable, but a household has exactly *n* bills, and the distribution that attains Scarf's bound generally cannot be written as *n* equally weighted months. Theorem 1 gives the attainable bound over all *n*-vectors with a given mean and standard deviation; Samuelson's inequality [11] then yields a zero-penalty certificate. Theorem 2 adds nonnegativity. (iii) For tariffs with several blocks, adding per-threshold bounds overstates the worst case, because each threshold's worst case is a different consumption pattern. Theorem 3 gives an exact, attainable joint bound for any convex block tariff by enumerating how many periods fall in each block. (iv) A constrained design analysis, related to moment-based robust optimisation [12], identifies which constraints determine the penalty. The literature search reported in Section 2 did not find Theorems 1–3 in this form. The search was limited, and we do not claim priority.

The empirical scope is limited, and not by design. The intended application is a public smart-meter dataset from about 100 urban households in Mathura and Bareilly, Uttar Pradesh [13, 14], which could not be retrieved in the computing environment used for this study. Every number reported below comes from labelled synthetic data. The code for the observed panel is released so that the analysis can be run once the data are obtained. Sections 2 and 3 cover related work and the model, Section 4 the mathematics, Sections 5–7 the data, results and tariff design, and Sections 8–9 the limitations and conclusions.

# 2. Related Literature

*Increasing-block tariffs.* Borenstein [1] shows for California that increasing-block pricing achieves only modest redistribution at substantial efficiency cost. Ito [2] finds that households respond to average rather than marginal price, which bears on whether a period-level penalty changes behaviour. For India, Trimble, Mayer and Banerjee [3] document that residential subsidies delivered through near-universal block tariffs largely reach non-poor households. Chindarkar and Goyal [4] estimate heterogeneous price elasticities of about −0.39 nationally. These studies analyse who benefits from block pricing *on average*. We could not find work that isolates the penalty arising from *within-household variation* across billing periods, although the convexity argument behind it is elementary.

*Moment bounds for hinge functions.* The worst-case expectation of a hinge function given a mean and a variance is Scarf's inventory bound [6]; Lo [7] derived the same expression as an upper bound on call prices, and Gallego and Moon [8] gave a short proof and extensions. Bertsimas and Popescu [9] solved the problem with nonnegative support by semidefinite optimisation. These are statements about *distributions*. The extremal law places probability weights that need not be multiples of 1/*n*. When applied to *n* observed bills, the bounds are valid but generally not attainable. Samuelson [11] showed that no observation can lie more than $s\sqrt{n-1}$ from the mean of *n* observations. Theorem 1 below is the hinge-function analogue of that finite-sample viewpoint. Liao and Berg [10] sharpen Jensen's inequality in general form; we rely only on the elementary bounds of Section 4.

*Robust tariff design.* Distributionally robust optimisation with moment ambiguity [12] provides the language for choosing parameters against worst-case consumption. Our design problem is far simpler, since for a fixed threshold it is a linear programme. We use it mainly to show how degenerate solutions arise and which constraints rule them out.

*Residual contribution.* The convexity, Cauchy–Schwarz and option-bound arguments are standard. What we did not find stated elsewhere is their finite-sample, multi-threshold form for tariffs (Theorems 1–3). The supplementary archive (Research Audit) lists each source, what it covers and where it overlaps with this paper.

# 3. Tariff Model and Assumptions

Let $x\ge 0$ denote energy consumed in a billing period of fixed length (30 days). A *marginal-block* tariff with thresholds $0<K_1<\dots<K_m$ and marginal prices $p_0,p_1,\dots,p_m$ charges

$$B(x)=p_0x+\sum_{j=1}^{m}\Delta p_j\,(x-K_j)_{\text{+}},\qquad \Delta p_j=p_j-p_{j-1},\quad (z)_{\text{+}}=\max(z,0).$$

Equivalently $B(x)=\max_k(p_kx-c_k)$ with $c_k=\sum_{j\le k}\Delta p_jK_j$ whenever all $\Delta p_j\ge0$. This differs from an *all-units* slab tariff, which prices every unit at the rate of the slab reached. All-units tariffs are discontinuous and nonconvex, and the penalty can be negative under them. For example, two months of 140 and 166 kWh under an all-units schedule of Rs 5.50/6.00 at 150 kWh give a penalty of −Rs 70. Fixed monthly charges add the same amount to both sides of the comparison below and cancel.

For consumption $x_1,\dots,x_n$ in $n$ comparable periods with mean $\overline{x}$, define the **volatility penalty**

$$V=\sum_{t=1}^{n}B(x_t)-nB(\overline{x}),$$

and write $s^2=\frac1n\sum_t(x_t-\overline{x})^2$ (the *population* variance), $\operatorname{MAD}=\frac1n\sum_t|x_t-\overline{x}|$ and $d_j=\overline{x}-K_j$. The comparator $nB(\overline{x})$ is a *hypothetical* bill for perfectly smoothed consumption with the same total. It is not an observed bill, and it is not an option that utilities offer. "Budget billing", which smooths *payments* while charging actual consumption, does not remove $V$. We assume telescopic billing, and when periods differ in length we prorate the thresholds. For periods of unequal length $L_t$, the correct comparator uses the perspective $B_L(x)=(L/30)B(30x/L)$, and $V=\sum_tB_{L_t}(x_t)-B_{\sum L_t}(\sum x_t)\ge0$ still holds, because a perspective of a convex function is jointly convex and positively homogeneous [15] (proof in Appendix S2). For one price step it is convenient to write $V=\Delta p\,W(K)$ with $W(K)=\sum_t(x_t-K)_{\text{+}}-n(\overline{x}-K)_{\text{+}}$ (in kWh).

# 4. Mathematical Results

Full proofs, equality cases and counterexamples are in the Supplementary Mathematical Appendix (Sections S2–S11). Here we state the results with proof sketches.

**Proposition 1 (nonnegativity and decomposition).** $V=\sum_j\Delta p_jW(K_j)$ and each $W(K_j)\ge0$. Hence $V\ge0$ for every consumption vector if and only if all $\Delta p_j\ge0$. $W(K)=0$ exactly when no two periods lie strictly on opposite sides of $K$.

*Sketch.* Linear terms cancel. $W(K)\ge 0$ is Jensen's inequality for the convex hinge [5]. If some $\Delta p_j<0$, two periods straddling $K_j$ closely enough to avoid the other thresholds give $V<0$.

**Proposition 2 (exact identities).**
(a) $W(K)=\tfrac12\big[\sum_t|x_t-K|-n|\overline{x}-K|\big]$.
(b) Minority-side form: $W(K)=\sum_t(K-x_t)_{\text{+}}$ if $\overline{x}\ge K$, and $W(K)=\sum_t(x_t-K)_{\text{+}}$ if $\overline{x}\le K$.

*Sketch.* (a) follows from $(z)_{\text{+}}=(z+|z|)/2$. (b) follows from $(z)_{\text{+}}-z=(-z)_{\text{+}}$. Form (b) states that the penalty equals the price step times the energy that the household's *minority-side* periods spend across the threshold. A household that is usually above a slab pays for the months it dips below, and vice versa.

**Proposition 3 (moment bounds; known).** $W(K)\le\frac n2\min\{\operatorname{MAD},\ \sqrt{s^2+d^2}-|d|\}\le\frac n2 s$.

*Sketch.* $\sum_t|x_t-K|\le\sum_t|x_t-\overline{x}|+n|d|$ gives the MAD term. Cauchy–Schwarz, $\frac1n\sum_t|x_t-K|\le\sqrt{s^2+d^2}$, gives the second term, which is the Scarf–Lo bound [6–8] written as a Jensen gap.

**Proposition 4 (threshold sensitivity).** For fixed data that are not all equal, $W$ is zero for $K\le\min_tx_t$ and $K\ge\max_tx_t$. It is strictly increasing for $K$ between the smallest reading and $\overline{x}$, and strictly decreasing for $K$ between $\overline{x}$ and the largest reading. Hence $K=\overline{x}$ is the unique maximiser, with $\max_KW(K)=\frac n2\operatorname{MAD}$.

*Sketch.* By Proposition 2, when $K$ lies strictly between the smallest reading and $\overline{x}$, the one-sided derivatives of $W$ are the numbers of periods with $x_t<K$ and with $x_t\le K$, both at least 1. When $K$ lies strictly between $\overline{x}$ and the largest reading, they are minus the numbers of periods with $x_t\ge K$ and with $x_t>K$, both at most −1. The MAD bound is therefore the sharp bound *uniformly in K*. This result holds the price step fixed; in a design problem, moving $K$ also changes the revenue-neutral prices (Section 7).

**Theorem 1 (finite-sample sharp bound).** Let $n\ge2$. For every real vector with mean $\overline{x}$ and population standard deviation $s$,

$$W(K)\le\max\Big\{0,\ \max_{1\le j\le n-1}A_j\Big\},\qquad A_j=s\sqrt{j(n-j)}-j\,|\overline{x}-K|,$$

with equality attained by a two-valued vector: $j^{\text{*}}$ minority-side periods at $K\mp A_{j^{\text{*}}}/j^{\text{*}}$, and the remaining periods equal to one another on the other side.

*Sketch.* Take $\overline{x}\ge K$ (the other case is symmetric) and let $j$ be the number of periods below $K$, with total deficit $D=W(K)$. The periods above $K$ then have total excess $D+n d$. Cauchy–Schwarz within each group gives $n(s^2+d^2)=\sum_t(x_t-K)^2\ge D^2/j+(D+nd)^2/(n-j)$. Solving this quadratic for $D$ gives $D\le s\sqrt{j(n-j)}-jd$. Equality holds when the values within each group are equal.

**Corollary 1 (zero-penalty certificate).** Because $A_j/j$ decreases in $j$, $W(K)=0$ whenever $|\overline{x}-K|\ge s\sqrt{n-1}$. This is Samuelson's inequality [11]: no period can then cross the threshold. The Scarf-type bound is strictly positive whenever $s>0$, so it never certifies a zero penalty. Theorem 1 is always at most that bound, because it restricts the continuous weight $p=j/n$ of the Scarf extremal law to multiples of 1/*n*.

**Theorem 2 (nonnegative consumption).** If also $x_t\ge0$, then $W(K)\le\max_j\min\{A_j,c_j\}$ with $c_j=jK$ if $\overline{x}\ge K$ and $c_j=n\overline{x}-jK$ otherwise.

*Sketch.* Each of the $j$ minority-side deficits is at most $K$. In the other case, the $j$ periods above $K$ consume at most the household's total consumption, $n\overline{x}$. The bound was attained in all 148 adversarial numerical tests (Appendix S7). A general proof of sharpness remains open, so we state that sharpness as a conjecture.

**Theorem 3 (exact joint bound for multi-block tariffs).** Let $B$ be convex with $m+1$ blocks. For counts $N=(n_0,\dots,n_m)$ summing to $n$, let $\overline{p}_N$ and $\sigma_N$ be the mean and standard deviation of the marginal prices when $n_k$ periods are assigned to block $k$. Then

$$V\le\max_{N}\Big[n\overline{x}\,\overline{p}_N+n s\,\sigma_N-\sum_kn_kc_k\Big]-nB(\overline{x}),$$

over all real vectors with mean $\overline{x}$ and standard deviation $s$, and the bound is attained.

*Sketch.* Since $B=\max_k(p_kx-c_k)$, $\sum_tB(x_t)$ is a maximum over assignments of periods to pieces. The supremum of a maximum is the maximum of the suprema. For a fixed assignment the objective is linear, and its maximum on the set $\{\sum_tx_t=n\overline{x},\ \sum_t(x_t-\overline{x})^2=ns^2\}$ follows from Cauchy–Schwarz. The value depends only on the counts, giving $\binom{n+m}{m}$ cases (455 for twelve months and four blocks). For $m=1$, Theorem 3 reduces to Theorem 1. For the reported Uttar Pradesh schedule with $n=12$, $\overline{x}=280$ and $s=160$ kWh, the joint bound is Rs 565.1. The sum of the three per-threshold sharp bounds is Rs 806.4, which therefore *cannot* be attained jointly.

**Worked example.** Consider a stylised two-season household with twelve 30-day readings: 80, 85, 90, 95, 400, 420, 410, 390, 85, 80, 90 and 95 kWh. The mean is $\overline{x}=193.3$ kWh, the population standard deviation is $s=149.9$ kWh and $\operatorname{MAD}=141.1$ kWh. Under the reported Uttar Pradesh schedule (price steps of Rs 0.50 at 150, 300 and 500 kWh), the twelve energy charges total Rs 13,480. Smoothed use would cost $12\,B(193.3)$ = Rs 13,020, so $V$ = Rs 460. Proposition 2(b) reproduces this by hand. At $K=150$ the mean lies above the threshold, so the minority side is *below*: the eight low months fall short of 150 kWh by a total of 500 kWh, contributing $0.5\times500$ = Rs 250. At $K=300$ the mean lies below, so the four summer months, which exceed 300 kWh by 420 kWh in total, contribute Rs 210. No month exceeds 500 kWh, so the third term is zero. The summed standard-deviation bound is Rs 1,349 and the summed Scarf-type bound Rs 674. The summed per-threshold finite-sample bounds give Rs 660, while the joint bound of Theorem 3 gives Rs 468.4, within 2% of the realised penalty. The joint bound is close here because a household that alternates between two regimes resembles the two-valued worst cases of Theorems 1 and 3. The summed bounds are loose because each assumes a different worst case, and no single consumption vector realises all of them.


# 5. Data and Methods

*Intended observed data.* The target dataset [14] records three-minute smart-meter readings for about 100 urban households in Mathura and Bareilly from May 2019 to October 2021 (Harvard Dataverse, version 2.0, CC0). Its companion report gives an average consumption of about 280 kWh per month over May–October 2019. Fan-only homes used up to about 200 kWh, and homes with coolers or air conditioners used 200–1,000 kWh [13]. The dataset host was not reachable from the computing environment, so **no observed household data were analysed**. The released pipeline (Appendix S13) inspects column semantics before use and distinguishes interval from cumulative-register energy. It treats device resets and incomplete days as missing rather than zero, retains household-months with at least 90% valid days, and anonymises meter identifiers. It also prorates thresholds for unequal months and stratifies a household-cluster bootstrap [16] by district.

*Synthetic panel.* To exercise the theory, we generated a stylised panel of 300 households over twelve 30-day billing cycles. Households were drawn from three appliance archetypes (fan 40%, cooler 35%, air-conditioner 25%). Base load was lognormal with median 115 kWh, a cooling component was scaled by an assumed north-Indian seasonal profile, and monthly noise was multiplicative (lognormal SD 0.10); the seed was 20261024. The design was *informed by*, not estimated from, the published summary statistics. The panel mean over May–October was 255.5 kWh, of the same order as the reported 280 kWh. No empirical claim rests on these data.

*Planned inference for observed data.* When the observed panel is analysed, households (not household-months) will be the resampling unit, because the twelve readings of one household are dependent. Confidence intervals for the mean penalty share will use a percentile cluster bootstrap stratified by district [16] (2,000 replicates). Sensitivity analyses will vary the month-completeness rule (90% versus 100% of days), the treatment of partially observed months (scaling versus exclusion), and the twelve-month window. The sample of instrumented urban households is not a probability sample of Uttar Pradesh or of India, so any estimate will describe only the observed households.


*Tariff scenario.* The reference schedule is the Uttar Pradesh urban domestic metered energy charge for FY2019–20: Rs 5.50 for 0–150 kWh, Rs 6.00 for 151–300 kWh, Rs 6.50 for 301–500 kWh and Rs 7.00 above 500 kWh, with a fixed charge of Rs 110/kW. These rates are as reported in the trade press [17]; the primary regulatory order could not be retrieved. Telescopic application is assumed, and the dataset does not identify households' tariff categories, so the schedule is used only as a counterfactual scenario.

*Computations.* For each household we computed $V$, its threshold decomposition, and the ratios $V/U$ for every bound $U>0$. We also computed (a) threshold-sensitivity curves on a 1-kWh grid, (b) penalties under bimonthly and quarterly billing with thresholds scaled as $B_k(E)=kB(E/k)$, (c) adversarial tests of every bound by multistart constrained optimisation, and (d) the design problems of Section 7. All 26 unit tests pass, including a hand-worked bill (420 kWh gives Rs 2,505). Independent block-by-block recomputation reproduced every reported penalty and design (Appendix S12).

# 6. Results (Synthetic Panel)

*Size of the penalty.* Under the reference schedule, the mean annual penalty was Rs 108 per household (median Rs 53, 90th percentile Rs 309, maximum Rs 808). As a share of annual energy charges, it averaged 0.61% (median 0.42%, maximum 2.2%); 44 of 300 households had no penalty because they never crossed a threshold. The share rose with the coefficient of variation (correlation 0.84). Median shares were 0.10% for fan-only, 0.50% for cooler and 1.34% for air-conditioned archetypes (Figure S1). For the air-conditioned archetype, most of the penalty came from the 300 and 500 kWh thresholds (Figure S2). Across 20 independent synthetic panels, the mean share ranged from 0.54% to 0.72%. These figures describe the synthetic design only.

*Tightness of the bounds.* Table 1 (Panel A) and Figure 1(c) compare the bounds. The standard-deviation bound captured a median of only 12% of the realised penalty. The Scarf-type and nonnegative-support distributional bounds captured 43%. The per-threshold finite-sample bounds (Theorems 1–2) raised this to 50%, and the joint bound (Theorem 3) to 67%, cutting the median slack from Rs 77 to Rs 30. Among 900 household–threshold pairs, 530 had a zero penalty term. Corollary 1 certified 342 of these in advance from the mean and standard deviation alone; the Scarf-type bound certified none. No bound was violated in any computation.

*Threshold and billing period.* For every household, the penalty per unit price step peaked exactly at $K=\overline{x}$ with value $n\,\operatorname{MAD}/2$, confirming Proposition 4 (Figure 1b). Lengthening the billing period with proportionally scaled thresholds lowered the mean penalty from Rs 108 (monthly) to Rs 96 (bimonthly) and Rs 87 (quarterly). It fell to zero under annual settlement, which coincides with the smoothed comparator (Figure S3). Applying unprorated monthly thresholds to calendar months shifted the mean penalty from Rs 109 to Rs 114, so incorrect proration distorts the estimate.

# 7. Constrained Tariff Design

*Formulation.* Consider a two-block schedule $\theta=(p_1,p_2,K)$, chosen to minimise either the mean household penalty, the maximum household penalty (minimax), or the maximum of the Theorem 2 bound (a moment-robust objective). The constraints are: minimum progressivity $p_2-p_1\ge\delta_{\min}=0.5$; prices between Rs 3 and Rs 9; revenue within ±1% of the reference schedule; an affordability cap that the bill for 100 kWh not exceed the reference bill (Rs 550); and coverage of both blocks, with 10–60% of household-months above $K$. For fixed $K$, the penalty equals $(p_2-p_1)W_h(K)$, and revenue and affordability are linear in $(p_1,p_2)$. Each subproblem is therefore a two-variable linear programme, solved exactly with HiGHS on a 1-kWh grid of thresholds. On the grid, each feasible subproblem has a minimiser, so the reported optima are global on the grid. Because the coverage share is a step function of $K$, we do not claim existence for a continuous threshold (Appendix S9).

*Degeneracy.* Without constraints, the minimum penalty is zero and trivially attained: set $p_2=p_1$, or place $K$ below or above all observed consumption. The progressivity and coverage constraints exclude these solutions.

*Results.* All three objectives selected the same design: $K=151$ kWh, $p_1$ = Rs 5.50 and $p_2$ = Rs 6.00. The binding constraints were the progressivity floor, the lower revenue limit and the coverage ceiling, which held the threshold at the lowest admissible level; the affordability cap was just slack (Table 1, Panel B). Because the penalty is proportional to the price gap at a fixed threshold, the penalty–progressivity frontier is linear (Figure 1d). At a top-to-bottom gap of Rs 1.50, equal to the reference schedule's, a single threshold at 152 kWh gave a maximum household penalty of Rs 583, against Rs 808 for the reference four-block schedule. Its mean penalty was Rs 103, against Rs 108. The objectives diverged only when constraints were relaxed. With no affordability cap and at most 30% of months above $K$, the mean-penalty design moved the threshold to 348 kWh, raising the maximum penalty to Rs 463; the minimax design chose 244 kWh, with a maximum of Rs 299 (Table S7). Minimising the average penalty can thus concentrate the burden on the most variable households.

These are statements about billing arithmetic under fixed consumption. A lower penalty is a transfer between consumer groups and the utility, not a welfare gain. Demand responses [2, 4], cost of supply and subsidy targeting [3] are outside the model.

# 8. Discussion and Limitations

The penalty is what a period-by-period block tariff charges for *timing*. Proposition 2(b) makes it concrete: a household pays for the energy its atypical months spend on the far side of a threshold. Theorems 1–3 are useful when only summary statistics are available, as in surveys or aggregated billing reports. They give the largest penalty consistent with a household's mean and variability over its actual number of bills, and they identify households for which no penalty is possible.

Three practical implications follow, each conditional on the assumptions above. First, billing rules that look administrative are distributional: the length of the billing cycle, whether thresholds are prorated when meter-reading intervals vary, and whether slabs are applied monthly or over a longer settlement period all change the penalty mechanically (Section 6). Second, for a given price step, the penalty is largest for households whose mean consumption sits near a threshold and whose use swings across it. A threshold placed at the typical consumption of seasonal households therefore maximises their penalty, unless the price step is adjusted. Third, because the bounds of Section 4 use only the mean and the standard deviation, a regulator could screen a billing database for households where the penalty might be material without reconstructing every bill, and use Corollary 1 to rule out households for which it must be zero.


The limitations are substantial. First, and most important, no observed Indian household data were analysed, so the magnitudes in Section 6 are properties of an assumed synthetic design, and the results should not be read as estimates for Mathura, Bareilly, Uttar Pradesh or India. Second, the tariff schedule comes from a secondary source, and telescopic application and household category are assumed. Third, consumption is held fixed. If households respond to marginal or average price [2], both the penalty and any redesign would change. Fourth, sharpness under nonnegativity (Theorem 2) is supported numerically but not proved, and Theorem 3 does not impose nonnegativity. Fifth, the design analysis uses a two-block family, a stylised affordability proxy and revenue on a synthetic sample. It is an illustration of structure, not a tariff proposal.

# 9. Conclusions

Under convex block tariffs, variable consumption never costs a household less than smooth consumption of the same total, and it costs more whenever its months fall on both sides of a threshold. The extra cost decomposes exactly by threshold and, for a fixed price step, peaks when a threshold sits at the household's mean. For a fixed number of bills, attainable bounds follow from the mean and standard deviation alone; for multi-block schedules, the exact joint bound is substantially tighter than the sum of per-threshold bounds. In the synthetic illustration, the penalty was small on average but concentrated among high-variability households. Once the revenue and coverage constraints bound, the required price gap and the admissible threshold range, not the choice of objective, determined it. The next step is to apply these tools to observed smart-meter data.

**Declarations.** *Funding:* non**Declarations**

*Author contributions.* The author is the sole named author and takes responsibility for the submitted work, its interpretations and final claims.

*Funding.* This research received no external funding.

*Conflicts of interest.* The author declares no conflicts of interest.

*Data and code availability.* Source data [14] are available under CC0 via Harvard Dataverse. The code, synthetic data, and numerical results are in the supplementary archive. No observed household records were analysed in this study.

*Ethics approval and informed consent.* The analysis used synthetic data and publicly available documentation of a de-identified dataset. No identifiable household data or human participants were directly studied. Institutional ethics approval and informed consent were not sought.

*Use of generative AI.* Generative AI (Claude, Anthropic) was used extensively to search literature, derive and check proofs, write and test code, run simulations, and draft text. The author reviewed the work and assumes responsibility for all claims.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

![**Figure 1. Volatility penalty: geometry, threshold sensitivity, bound tightness and design trade-off.** (a) Under a convex two-block tariff (illustrative: Rs 5/kWh up to K = 200 kWh, Rs 7 above), the average of bills for two periods (40 and 360 kWh) exceeds the bill at average use; the vertical gap is the penalty per period, V/n. (b) Penalty per Rs/kWh price step, W(K), as a function of threshold position for three synthetic households; each curve peaks at the household mean, at height n·MAD/2 (dots), as in Proposition 4. (c) Cumulative distribution of tightness V/U over 300 synthetic households under the reported Uttar Pradesh four-block schedule, for the standard-deviation bound, the summed Scarf-type bound, the summed per-threshold finite-sample bound (Theorem 2) and the joint bound (Theorem 3); curves further right are tighter; households with U = 0 are excluded. (d) Revenue-neutral two-block designs (minimax objective; constraints in Section 7): maximum and mean household penalty against the required price gap; open triangles mark the reference four-block schedule (top-to-bottom gap Rs 1.50). Source: author's computations on synthetic data (seed 20261024); code in the supplementary archive. No observed household data are shown.](../../06_Figure_Sources/Figure_01/Figure1_main.png){width=6.3in}

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

**Table 1. Bound performance and constrained designs on the synthetic panel (UP-type tariff).**

*Panel A. Bounds on the annual volatility penalty (300 synthetic households, reported Uttar Pradesh four-block schedule)*

| Bound | Inputs | Sharpness | Median V/U | 90th pct. V/U | Median slack (Rs) |
|:-----------------------|:---------------|:-------------------------------|-------:|-------:|--------:|
| SD bound  nΔp·s/2 | n, s | Only if x̄ = K and half the periods sit at K ± s | 0.12 | 0.28 | 412 |
| MAD bound  nΔp·MAD/2 | n, MAD | Yes, uniformly over K: equals max over K of V (Prop. 4) | 0.14 | 0.31 | 355 |
| Scarf-type moment bound | n, x̄, s, K | Sharp over distributions; not for fixed n | 0.43 | 0.63 | 77 |
| Nonnegative-support moment bound | n, x̄, s, K, x ≥ 0 | Sharp over nonnegative distributions | 0.43 | 0.64 | 77 |
| Finite-sample bound (Thm 1) | n, x̄, s, K | Sharp over real n-vectors (attained) | 0.49 | 0.76 | 65 |
| Finite-sample bound, x ≥ 0 (Thm 2) | n, x̄, s, K, x ≥ 0 | Valid; attained in all numerical tests | 0.50 | 0.76 | 65 |
| Joint multi-tier bound (Thm 3) | n, x̄, s, whole tariff | Sharp over real n-vectors (attained) | 0.67 | 0.87 | 30 |

*Panel B. Two-block designs (revenue within ±1%, price gap ≥ Rs 0.50, bill at 100 kWh ≤ Rs 550, 10–60% of months above K)*

| Design | K (kWh) | p₁ (Rs) | p₂ (Rs) | Revenue ratio | Mean V (Rs) | Max V (Rs) | Binding |
|:---------------------|---------:|-------:|---------:|--------:|--------:|--------:|:--------------|
| A. Reference 4-block (reported FY2019–20) | 150/300/500 | 5.50 | 7.00 (top) | 1.000 | 108.1 | 807.7 | — |
| B. Minimise mean penalty | 151 | 5.50 | 6.00 | 0.990 | 33.8 | 191.9 | G, R, C |
| C. Minimax penalty | 151 | 5.50 | 6.00 | 0.990 | 33.8 | 191.9 | G, R, C |
| D. Moment-robust minimax | 151 | 5.50 | 6.00 | 0.990 | 33.8 | 191.9 | G, R, C |
| E. Minimax, price gap ≥ Rs 1.50 | 152 | 5.17 | 6.67 | 0.990 | 102.9 | 583.3 | G, R, C |

*Notes:* V = annual volatility penalty; U = bound; ratios are computed over households with U > 0 (300 for distributional bounds, 287 for finite-sample bounds, which certify V = 0 for the remaining 13). Multi-block bounds in rows 1–6 are sums of per-threshold bounds; row 7 is the joint bound of Theorem 3. Reference schedule: Rs 5.50/6.00/6.50/7.00 per kWh with thresholds 150/300/500 kWh (as reported in [17]); telescopic application assumed; fixed charges cancel. Sharpness refers to a single threshold. Designs B–D coincide because the constraints bind (Section 7); their objective values differ. Design E uses a 2-kWh threshold grid. Binding constraints: G = minimum price gap; R = lower revenue limit; C = upper coverage limit (share of household-months above K). Source: author's computations on synthetic data; all values regenerate from the supplementary code.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# References

1. Borenstein S. (2012). The redistributional impact of nonlinear electricity pricing. *Am Econ J Econ Policy*, 4(3), 56–90. doi:10.1257/pol.4.3.56. Available at: https://doi.org/10.1257/pol.4.3.56
2. Ito K. (2014). Do consumers respond to marginal or average price? Evidence from nonlinear electricity pricing. *Am Econ Rev*, 104(2), 537–563. doi:10.1257/aer.104.2.537. Available at: https://doi.org/10.1257/aer.104.2.537
3. Trimble C., Mayer K., Banerjee S.G. (2015). *Elite Capture: Residential Tariff Subsidies in India*. World Bank Study. Washington, DC: World Bank. Available at: http://hdl.handle.net/10986/20538
4. Chindarkar N., Goyal N. (2019). One price doesn't fit all: an examination of heterogeneity in price elasticity of residential electricity in India. *Energy Econ*, 81, 765–778. doi:10.1016/j.eneco.2019.05.021. Available at: https://doi.org/10.1016/j.eneco.2019.05.021
5. Jensen J.L.W.V. (1906). Sur les fonctions convexes et les inégalités entre les valeurs moyennes. *Acta Math*, 30, 175–193. doi:10.1007/BF02418571. Available at: https://doi.org/10.1007/BF02418571
6. Scarf H. (1958). A min-max solution of an inventory problem. In: Arrow K.J., Karlin S., Scarf H. (eds.), *Studies in the Mathematical Theory of Inventory and Production*, pp. 201–209. Stanford, CA: Stanford University Press.
7. Lo A.W. (1987). Semi-parametric upper bounds for option prices and expected payoffs. *J Financ Econ*, 19(2), 373–387. doi:10.1016/0304-405X(87)90010-9. Available at: https://doi.org/10.1016/0304-405X(87)90010-9
8. Gallego G., Moon I. (1993). The distribution free newsboy problem: review and extensions. *J Oper Res Soc*, 44(8), 825–834. doi:10.1057/jors.1993.141. Available at: https://doi.org/10.1057/jors.1993.141
9. Bertsimas D., Popescu I. (2002). On the relation between option and stock prices: a convex optimization approach. *Oper Res*, 50(2), 358–374. doi:10.1287/opre.50.2.358.424. Available at: https://doi.org/10.1287/opre.50.2.358.424
10. Liao J.G., Berg A. (2019). Sharpening Jensen's inequality. *Am Stat*, 73(3), 278–281. doi:10.1080/00031305.2017.1419145. Available at: https://doi.org/10.1080/00031305.2017.1419145
11. Samuelson P.A. (1968). How deviant can you be? *J Am Stat Assoc*, 63(324), 1522–1525. doi:10.1080/01621459.1968.10480944. Available at: https://doi.org/10.1080/01621459.1968.10480944
12. Delage E., Ye Y. (2010). Distributionally robust optimization under moment uncertainty with application to data-driven problems. *Oper Res*, 58(3), 595–612. doi:10.1287/opre.1090.0741. Available at: https://doi.org/10.1287/opre.1090.0741
13. Agrawal S., Mani S., Ganesan K., Jain A. (2020). *What Smart Meters Can Tell Us: Insights on Electricity Supply and Use in Mathura and Bareilly Households*. New Delhi: Council on Energy, Environment and Water. Available at: https://www.ceew.in/publications/what-smart-meters-can-tell-us (accessed 24 October 2026)
14. Agrawal S., Mani S., Ganesan K., Jain A. (2021). High frequency smart meter data from two districts in India (Mathura and Bareilly), version 2.0 [dataset]. Harvard Dataverse. doi:10.7910/DVN/GOCHJH. Available at: https://doi.org/10.7910/DVN/GOCHJH
15. Boyd S., Vandenberghe L. (2004). *Convex Optimization*. Cambridge: Cambridge University Press. ISBN 978-0-521-83378-3. doi:10.1017/CBO9780511804441
16. Cameron A.C., Gelbach J.B., Miller D.L. (2008). Bootstrap-based improvements for inference with clustered errors. *Rev Econ Stat*, 90(3), 414–427. doi:10.1162/rest.90.3.414. Available at: https://doi.org/10.1162/rest.90.3.414
17. Power Line (2020). No power tariff hike, slabs unchanged in Uttar Pradesh. *Power Line*, 12 November 2020. Available at: https://powerline.net.in/2020/11/12/no-power-tariff-hike-slabs-unchanged-in-uttar-pradesh/ (accessed 24 October 2026)
