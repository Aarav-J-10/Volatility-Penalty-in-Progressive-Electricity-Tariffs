"""Publication figures (synthetic results only).  Every figure distinguishes
series by line style / marker as well as colour so it survives grayscale print.
Exports: vector PDF and EPS, 600-dpi TIFF (LZW), 300-dpi PNG preview."""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import simulations as sim
from tariff_models import ILLUSTRATIVE_TWO_TIER as ILL, UP_URBAN_DOMESTIC_FY2019_20 as UP
from theory import hinge_gap, mad, bound_finite, bound_scarf_moments

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "05_Computational_Results" / "synthetic"
FIG = ROOT / "06_Figure_Sources"
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]          # validated categorical slots 1-4
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"

plt.rcParams.update({
    "font.family": "DejaVu Serif", "font.size": 9, "axes.titlesize": 9.5, "axes.labelsize": 9,
    "axes.edgecolor": INK2, "axes.linewidth": 0.6, "xtick.color": INK2, "ytick.color": INK2,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5, "axes.spines.top": False,
    "axes.spines.right": False, "legend.frameon": False, "legend.fontsize": 8, "lines.linewidth": 1.6,
})


def save(fig, folder: str, stem: str):
    d = FIG / folder
    d.mkdir(parents=True, exist_ok=True)
    fig.savefig(d / f"{stem}.pdf")
    fig.savefig(d / f"{stem}.eps")
    fig.savefig(d / f"{stem}.png", dpi=300)
    fig.savefig(d / f"{stem}.tiff", dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)
    return d / f"{stem}.png"


def _X():
    p = pd.read_csv(RES / "Synthetic_Panel.csv")
    return p.pivot(index="household", columns="month", values="kwh30")[sim.MONTHS].to_numpy()


def panel_a(ax):
    x = np.linspace(0, 400, 401)
    ax.plot(x, ILL.bill(x), color=INK, lw=1.6, label="Bill $B(x)$")
    lo, hi = 40.0, 360.0
    m = (lo + hi) / 2
    ax.plot([lo, hi], [ILL.bill(lo), ILL.bill(hi)], color=C[1], ls="--", lw=1.4, label="Average of bills")
    ax.plot([lo, hi], ILL.bill(np.array([lo, hi])), "o", color=C[1], ms=5)
    ax.plot([m], [ILL.bill(m)], "s", color=C[0], ms=6, label="Bill at average use")
    ax.vlines(m, ILL.bill(m), (ILL.bill(lo) + ILL.bill(hi)) / 2, color=C[0], lw=2.2)
    ax.annotate("gap = $V/n$\n(penalty per period)", xy=(m + 3, ILL.bill(m) + 80), xytext=(250, 500),
                fontsize=8, color=INK, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.6))
    ax.axvline(ILL.thresholds[0], color=INK2, lw=0.7, ls=":")
    ax.text(ILL.thresholds[0] + 5, 2200, "$K$", color=INK2)
    ax.set(xlabel="Monthly consumption $x$ (kWh)", ylabel="Energy charge (Rs)",
           title="(a) Tariff convexity and the smoothing gap")
    ax.legend(loc="upper left")


def panel_b(ax, X):
    Ks = np.linspace(0, 700, 701)
    styles = ["-", "--", "-."]
    idx = [int(np.argsort(X.mean(1))[k]) for k in (40, 160, 290)]
    for k, i in enumerate(idx):
        x = X[i]
        W = [hinge_gap(x, K) for K in Ks]
        ax.plot(Ks, W, color=C[k], ls=styles[k], label=fr"household mean {x.mean():.0f} kWh")
        ax.plot([x.mean()], [0.5 * x.size * mad(x)], "o", color=C[k], ms=5)
    ax.set(xlabel="Threshold $K$ (kWh)", ylabel=r"Penalty per Rs/kWh step, $W(K)$ (kWh)",
           title=r"(b) $W(K)$ peaks at $K=\bar{x}$ (dots: $n\,$MAD$/2$)")
    ax.legend(loc="center right", fontsize=7.5)


def panel_c(ax):
    hh = pd.read_csv(RES / "Household_Penalties.csv")
    specs = [("U_sd", "SD bound", ":", C[3]), ("U_scarf", "Scarf-type", "--", C[1]),
             ("U_finite_nonneg", "Thm 2 (per threshold)", "-.", C[2]),
             ("U_exact", "Thm 3 (joint)", "-", C[0])]
    for col, lab, ls, col_ in specs:
        ok = hh[col] > 1e-9
        r = np.sort((hh.loc[ok, "V"] / hh.loc[ok, col]).to_numpy())
        ax.step(r, np.arange(1, r.size + 1) / r.size, where="post", ls=ls, color=col_, label=lab)
    ax.set(xlim=(0, 1), ylim=(0, 1.01), xlabel="Tightness $V_h/U_h$ (1 = bound attained)",
           ylabel="Share of synthetic households", title="(c) Bound tightness (UP-type 4-tier)")
    ax.legend(loc="lower right", fontsize=7.5, frameon=True, facecolor="white", edgecolor=GRID, framealpha=1.0)


def panel_d(ax):
    fr = pd.read_csv(RES / "Pareto_Progressivity.csv")
    opt = pd.read_csv(RES / "Optimisation_Results.csv")
    ax.plot(fr["dp_min"], fr["V_max"], "-o", color=C[0], ms=4, label="Max household penalty")
    ax.plot(fr["dp_min"], fr["V_mean"], "--s", color=C[1], ms=4, label="Mean household penalty")
    ref = opt.iloc[0]
    ax.plot([1.5], [ref["V_max"]], marker="^", color=C[0], ms=7, ls="none", mfc="white", mew=1.4,
            label="Reference 4-tier: max")
    ax.plot([1.5], [ref["V_mean"]], marker="v", color=C[1], ms=7, ls="none", mfc="white", mew=1.4,
            label="Reference 4-tier: mean")
    ax.set(xlabel=r"Minimum price gap $\delta_{\min}$ (Rs/kWh)", ylabel="Annual penalty (Rs)",
           title="(d) Penalty vs. progressivity frontier")
    ax.legend(loc="upper left")


def main_figure():
    X = _X()
    fig, axs = plt.subplots(2, 2, figsize=(7.0, 7.4), constrained_layout=True)
    panel_a(axs[0, 0]); panel_b(axs[0, 1], X); panel_c(axs[1, 0]); panel_d(axs[1, 1])
    return save(fig, "Figure_01", "Figure1_main")


def supp_figures():
    hh = pd.read_csv(RES / "Household_Penalties.csv")
    out = []
    # S1 penalty share by type
    fig, ax = plt.subplots(figsize=(6, 3.6), constrained_layout=True)
    types = ["fan", "cooler", "ac"]
    data = [hh.loc[hh.type == t, "V_share_pct"] for t in types]
    ax.boxplot(data, tick_labels=["Fan only", "Cooler", "Air-conditioner"], widths=0.45,
               medianprops=dict(color=INK), boxprops=dict(color=INK2), whiskerprops=dict(color=INK2), capprops=dict(color=INK2), flierprops=dict(marker="o", ms=3, mec=INK2))
    ax.set(ylabel="Penalty as % of annual energy charge", title="Figure S1. Synthetic household penalty share by appliance archetype")
    out.append(save(fig, "Figure_02", "FigureS1_penalty_by_type"))
    # S2 decomposition by threshold
    fig, ax = plt.subplots(figsize=(6, 3.6), constrained_layout=True)
    g = hh.groupby("type")[["V_K150", "V_K300", "V_K500"]].mean().loc[types]
    bottom = np.zeros(3)
    hatches = ["", "//", ".."]
    for k, (col, lab) in enumerate(zip(g.columns, ["K=150", "K=300", "K=500"])):
        ax.bar(range(3), g[col], bottom=bottom, color=C[k], edgecolor="white", linewidth=2, hatch=hatches[k], label=lab, width=0.55)
        bottom += g[col].to_numpy()
    ax.set_xticks(range(3), ["Fan only", "Cooler", "Air-conditioner"])
    ax.set(ylabel="Mean annual penalty (Rs)", title="Figure S2. Exact threshold decomposition of the penalty")
    ax.legend(title="Threshold term")
    out.append(save(fig, "Figure_03", "FigureS2_threshold_decomposition"))
    # S3 billing period
    bp = pd.read_csv(RES / "Billing_Period_Results.csv").iloc[:4]
    fig, ax = plt.subplots(figsize=(6, 3.4), constrained_layout=True)
    ax.bar(bp["period"], bp["V_mean"], color=C[0], width=0.5, label="Mean")
    ax.plot(bp["period"], bp["V_median"], "D", color=C[1], label="Median")
    ax.set(ylabel="Annual penalty vs. full smoothing (Rs)", title="Figure S3. Longer billing periods with scaled thresholds")
    ax.legend()
    out.append(save(fig, "Figure_04", "FigureS3_billing_period"))
    # S4 sensitivity of design to coverage cap
    se = pd.read_csv(RES / "Optimisation_Sensitivity.csv")
    se = se[(se.afford_cap == "1.00x ref") & (se.revenue_band == "0.99-1.01")]
    fig, ax = plt.subplots(figsize=(6, 3.4), constrained_layout=True)
    for k, (obj, ls, mk) in enumerate([("mean", "-", "o"), ("minimax", "--", "s")]):
        s = se[se.objective == obj].sort_values("cover_hi")
        ax.plot(s["cover_hi"], s["V_max"], ls=ls, marker=mk, color=C[k], label=f"{obj} objective: max penalty")
    ax.set(xlabel="Maximum share of household-months above K", ylabel="Max household penalty (Rs)",
           title="Figure S4. Targeting (coverage) constraint drives the design")
    ax.legend()
    out.append(save(fig, "Additional_Figures", "FigureS4_design_coverage"))
    # S5 finite-sample vs Scarf as function of distance to threshold
    fig, ax = plt.subplots(figsize=(6, 3.4), constrained_layout=True)
    d = np.linspace(0, 400, 401)
    for k, n in enumerate([3, 6, 12]):
        r = [bound_finite(n, 150 + dd, 100, 150, 1) / max(bound_scarf_moments(n, 150 + dd, 100, 150, 1), 1e-12) for dd in d]
        ax.plot(d / 100, r, ls=["-", "--", "-."][k], color=C[k], label=f"n = {n}")
    ax.set(xlabel=r"Standardised distance $|\bar{x}-K|/s$", ylabel="Theorem 1 / Scarf bound",
           title="Figure S5. Finite-sample bound relative to the Scarf bound", ylim=(0, 1.05))
    ax.legend()
    out.append(save(fig, "Additional_Figures", "FigureS5_finite_vs_scarf"))
    return out


if __name__ == "__main__":
    print(main_figure()); print(supp_figures())
