# Mathematical audit (adversarial referee notes)

Checked items
* Inequality directions: V ≥ 0 requires convexity; counterexamples for decreasing blocks and all-units slabs included (Appendix S11). ✔
* Population vs sample SD: population used consistently (theory.pop_sd); sample-SD substitution yields valid but non-sharp bounds (Remark S5). ✔
* Cauchy–Schwarz applications: Thm 1 group-wise CS; Thm 3 CS on the sphere ∩ hyperplane with centred coefficient vector. ✔
* Thm 1 edge cases: j = 0 (no minority) → W = 0; j ≤ n−1 when x̄ ≥ K; A_j ≤ 0 for all j ⇒ W = 0 (Cor. 1). ✔ Numerically attained by explicit vectors. ✔
* Thm 3: max over assignments equals sum of maxima (B convex = max of affine) — requires convexity; extension of B to negative x via max-affine form noted. ✔ Reduces to Thm 1 for m = 1 (2,000 random checks, max diff 1.2e-11). ✔
* Sharpness claims: Thm 1, Thm 3 attained over ℝⁿ; under nonnegativity only when extremal vector ≥ 0 (stated). Thm 2 sharpness is a CONJECTURE (148 numerical cases). ✔ not overstated.
* Joint vs componentwise: sum of per-threshold sharp bounds shown non-attainable by exact computation (806.39 vs 565.10). ✔
* Prop. 4 derivative statement: corrected during drafting (an earlier draft misstated the one-sided derivatives of 2W; fixed in manuscript and appendix). ✔
* Optimisation existence: for continuous K the coverage constraint makes the feasible set possibly non-closed; claim restricted to grid optima (Appendix S9, corrected during audit). ✔

Open issues
* Conjecture 1 (Thm 2 sharpness) unproved.
* Thm 3 complexity C(n+m, m) is fine for n = 12, m ≤ 5; large n·m would need a smarter search.
* Billing-period ordering holds only for nested schemes (proved); non-nested comparisons can go either way (counterexample in synthetic data).
