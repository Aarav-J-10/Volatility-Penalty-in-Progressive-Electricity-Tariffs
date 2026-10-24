# Notation and assumptions

| Symbol | Meaning |
|---|---|
| x_t | energy consumed in billing period t (kWh); periods are 30-day cycles unless stated |
| n | number of comparable periods (12 in the experiments) |
| x̄ | mean consumption, (1/n) Σ x_t |
| s | **population** standard deviation, sqrt((1/n) Σ (x_t − x̄)²) |
| MAD | mean absolute deviation about the mean, (1/n) Σ |x_t − x̄| |
| K, K_j | block thresholds (kWh per 30-day period) |
| p_0..p_m | marginal prices by block (Rs/kWh); Δp_j = p_j − p_{j−1} |
| B(x) | energy charge p_0 x + Σ_j Δp_j (x − K_j)_+ ; equals max_k (p_k x − c_k) when convex |
| c_k | intercepts Σ_{j≤k} Δp_j K_j |
| V | volatility penalty Σ_t B(x_t) − n B(x̄) (Rs) |
| W(K) | Σ_t (x_t − K)_+ − n (x̄ − K)_+ (kWh); V = Σ_j Δp_j W(K_j) |
| d, d_j | x̄ − K, x̄ − K_j |
| A_j | s sqrt(j(n−j)) − j|d|, j = 1..n−1 (Theorem 1) |
| B_L(x) | (L/30) B(30x/L): charge for a period of L days with prorated thresholds |

Assumptions: (A1) telescopic billing; (A2) fixed charges cancel; (A3) consumption fixed — no behavioural response;
(A4) thresholds defined per 30 days and prorated for other lengths; (A5) the smoothed bill n B(x̄) is a hypothetical comparator, not an available billing option.
