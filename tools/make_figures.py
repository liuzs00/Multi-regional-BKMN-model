"""
Publication figures for the multi-regional BKMN results -> figures/*.png (300 dpi).

Reads the committed result tables (no model re-run) and draws the eight figures
used in the write-up. Colour rules follow the project's chart conventions:
diverging orange<->blue for signed quantities (CVD-safe pair), one sequential
teal for magnitudes, categorical hues only where series identity matters, and a
value label on every bar so colour is never the sole encoding.

Usage: py -3 tools/make_figures.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "figures")
NZ, CP = "Net Zero 2050", "Current Policies"
NDC = "Nationally Determined Contributions (NDCs)"
H = "2040"

WARM, COOL, TEAL, INK, MUTED, GRID = "#c6522e", "#2a7db0", "#0e7c86", "#16202b", "#8b95a1", "#e4e8ec"
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Segoe UI", "DejaVu Sans"],
    "font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "savefig.facecolor": "white",
})


def load(name, idx=(0, 1)):
    d = pd.read_csv(os.path.join(ROOT, f"{name}.csv"), index_col=list(idx))
    return d


def finish(fig, ax, title, sub, path, xlabel=None):
    ax.set_title(title, fontsize=12, fontweight="600", loc="left", pad=30)
    if sub:
        ax.text(0, 1.012, sub, transform=ax.transAxes, fontsize=8.5, color=MUTED,
                va="bottom")
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=9)
    ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, path), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  {path}")


def barh_signed(ax, labels, vals, fmt="{:+.1f}%", pad=0.35):
    y = np.arange(len(labels))
    cols = [WARM if v > 0 else COOL for v in vals]
    ax.barh(y, vals, color=cols, height=0.68, zorder=3)
    ax.set_yticks(y, labels, fontsize=8.5)
    ax.axvline(0, color=MUTED, lw=1)
    span = max(abs(np.array(vals))) or 1
    for i, v in enumerate(vals):
        ax.text(v + np.sign(v) * span * 0.02, i, fmt.format(v), va="center",
                ha="left" if v > 0 else "right", fontsize=8, color=INK)
    ax.set_xlim(min(0, min(vals)) - span * pad, max(0, max(vals)) + span * pad)
    ax.invert_yaxis()


# --- 1. transition vs physical trade-off ------------------------------------
def fig_tradeoff():
    tr, ph = load("out_ext_gdp_transition"), load("out_ext_gdp_physical")
    regs = list(tr.xs(NZ, level=0).index)
    order = sorted(regs, key=lambda r: tr.loc[(NZ, r), H])
    y = np.arange(len(order))
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 6.4), sharey=True)
    for ax, s in zip(axes, (NZ, CP)):
        t = [tr.loc[(s, r), H] for r in order]
        p = [ph.loc[(s, r), H] for r in order]
        ax.barh(y - 0.19, t, height=0.36, color=TEAL, label="transition (carbon price)", zorder=3)
        ax.barh(y + 0.19, p, height=0.36, color=WARM, label="physical (warming)", zorder=3)
        ax.axvline(0, color=MUTED, lw=1)
        ax.set_title(s, fontsize=10, fontweight="600", color=INK, pad=8)
        ax.set_xlabel("GDP shock at 2040 (%)")
        ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
        ax.set_axisbelow(True)
        ax.set_xlim(-12.5, 0.6)
    axes[0].set_yticks(y, order, fontsize=8.5)
    axes[0].invert_yaxis()
    axes[0].legend(loc="lower left", frameon=False, fontsize=8.5)
    fig.suptitle("The transition/physical trade-off — the scenario ranking flips by channel",
                 fontsize=12.5, fontweight="600", x=0.012, ha="left", y=1.075)
    fig.text(0.012, 1.012, "Ambitious policy maximises transition cost and minimises warming damage; "
             "Current Policies does the reverse.", fontsize=8.5, color=MUTED, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig1_transition_vs_physical.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("  fig1_transition_vs_physical.png")


# --- 2. FX forward ranking ---------------------------------------------------
def fig_fx_rank():
    fwd = load("out_ext_fx_forward_5y").xs(NZ, level=0)
    spot = load("out_ext_fx_spot").xs(NZ, level=0)
    order = fwd[H].sort_values().index.tolist()
    v = [fwd.loc[r, H] for r in order]
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    barh_signed(ax, order, v)
    ax.scatter([spot.loc[r, H] for r in order], np.arange(len(order)),
               marker="|", s=90, color=INK, zorder=4, label="spot only (relative PPP)")
    ax.legend(loc="lower left", frameon=False, fontsize=8.5)
    finish(fig, ax, "Climate FX shifts against the euro, 2040 (Net Zero 2050)",
           "5-year forward, per-currency; negative = strengthens vs EUR. Tick = spot-only component.",
           "fig2_fx_forward_ranking.png", "5y forward FX shift vs EUR (%)")


# --- 3. mixture: expected FX by prior ----------------------------------------
def fig_mixture():
    priors = ["policy-sceptic", "uniform", "ambition"]
    cols = [COOL, TEAL, WARM]
    data = {p: load(f"out_ext_fx_expected_{p}", idx=(0,)) for p in priors}
    order = data["uniform"][H].sort_values().index.tolist()
    y = np.arange(len(order))
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    for k, (p, c) in enumerate(zip(priors, cols)):
        ax.barh(y + (k - 1) * 0.27, [data[p].loc[r, H] for r in order],
                height=0.25, color=c, label=p, zorder=3)
    ax.axvline(0, color=MUTED, lw=1)
    ax.set_yticks(y, order, fontsize=8.5)
    ax.invert_yaxis()
    ax.legend(title="scenario prior", loc="lower right", frameon=False, fontsize=8.5,
              title_fontsize=8.5)
    finish(fig, ax, "Expected FX shift under the Bayesian scenario mixture, 2040",
           "Probability-weighted across the seven NGFS scenarios; the prior is a narrative choice.",
           "fig3_mixture_expected_fx.png", "expected 5y forward FX vs EUR (%)")


# --- 4. volatility band ------------------------------------------------------
def fig_band():
    cen = load("out_ext_fx_forward_5y").xs(NZ, level=0)
    hi = load("out_ext_fx_forward_q95").xs(NZ, level=0)
    order = cen[H].sort_values().index.tolist()
    y = np.arange(len(order))
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    for i, r in enumerate(order):
        ax.plot([cen.loc[r, H], hi.loc[r, H]], [i, i], color=WARM, lw=3.2,
                solid_capstyle="round", zorder=3, alpha=.75)
    ax.scatter(cen[H][order], y, s=26, color=TEAL, zorder=4, label="central path")
    ax.scatter(hi[H][order], y, s=26, color=WARM, zorder=4, label="95th-percentile inputs")
    ax.axvline(0, color=MUTED, lw=1)
    ax.set_yticks(y, order, fontsize=8.5)
    ax.invert_yaxis()
    ax.legend(loc="lower left", frameon=False, fontsize=8.5)
    finish(fig, ax, "Climate FX-at-risk: central vs 95th-percentile inputs, 2040",
           "Net Zero 2050. Inputs stressed by 1.64σ — temperature (MAGICC fan) and carbon price (cross-model spread).",
           "fig4_fx_at_risk_band.png", "5y forward FX vs EUR (%)")


# --- 5. damage vs vulnerability ---------------------------------------------
def fig_vuln():
    ph = load("out_ext_gdp_physical").xs(CP, level=0)
    sc = pd.read_csv(os.path.join(ROOT, "data", "physical", "vl_scale_20R.csv"),
                     index_col=0)["scale"]
    regs = [r for r in ph.index if r in sc.index]
    x = [sc[r] for r in regs]
    y = [ph.loc[r, H] for r in regs]
    fig, ax = plt.subplots(figsize=(7.6, 5.4))
    ax.scatter(x, y, s=54, color=TEAL, zorder=3, edgecolor="white", lw=.8)
    for r, xi, yi in zip(regs, x, y):
        ax.annotate(r, (xi, yi), fontsize=7.5, color=INK,
                    xytext=(4, 3), textcoords="offset points")
    b, a = np.polyfit(x, y, 1)
    xs = np.linspace(min(x), max(x), 20)
    ax.plot(xs, a + b * xs, color=WARM, lw=1.4, ls="--", zorder=2,
            label=f"fit: slope {b:.1f}")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    ax.grid(color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_ylabel("physical GDP damage at 2040 (%)")
    finish(fig, ax, "Physical damage tracks ND-GAIN vulnerability",
           "Current Policies (highest warming). Scale is normalised so the GDP-weighted world mean = 1.",
           "fig5_damage_vs_vulnerability.png", "ND-GAIN vulnerability scale (world mean = 1)")


# --- 6. equity & op-risk -----------------------------------------------------
def fig_equity_oprisk():
    eq = load("out_ext_equity").xs(NZ, level=0)
    op = load("out_ext_oprisk_conduct").xs(NZ, level=0)
    order = eq[H].sort_values().index.tolist()
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 5.8))
    barh_signed(axes[0], order, [eq.loc[r, H] for r in order])
    axes[0].set_title("Equity index shift", fontsize=10, fontweight="600", pad=8)
    axes[0].set_xlabel("ΔS/S at 2040 (%)")
    barh_signed(axes[1], order, [op.loc[r, H] for r in order], fmt="{:+.0f}%")
    axes[1].set_title("Operational-risk losses (Conduct)", fontsize=10, fontweight="600", pad=8)
    axes[1].set_xlabel("relative change at 2040 (%)")
    for ax in axes:
        ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
        ax.set_axisbelow(True)
    fig.suptitle("Downstream channels under Net Zero 2050",
                 fontsize=12.5, fontweight="600", x=0.012, ha="left", y=1.075)
    fig.text(0.012, 1.012, "Equity via β·ΔGVA/GVA (§2.9); op-risk via Okun → unemployment → loss frequency (§2.11).",
             fontsize=8.5, color=MUTED, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig6_equity_oprisk.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("  fig6_equity_oprisk.png")


# --- 7. scenario inputs ------------------------------------------------------
def fig_inputs():
    from bkmn.regions import load as loadm
    from bkmn.scenarios import Scenarios
    m = loadm()
    sc = Scenarios(m.carbon_map)
    scens = [NZ, "Below 2°C", "Delayed transition", NDC, CP]
    labs = ["Net Zero 2050", "Below 2°C", "Delayed transition", "NDCs", "Current Policies"]
    cols = [TEAL, "#4b9aa4", COOL, "#d08b5c", WARM]
    yrs = np.arange(2022, 2051)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6))
    for s, lab, c in zip(scens, labs, cols):
        if s not in sc.px.columns.get_level_values("scenario"):
            continue
        axes[0].plot(yrs, [sc.px.loc[y, (s, "R5.2OECD")] for y in yrs], color=c, lw=1.9, label=lab)
        axes[1].plot(yrs, [sc.temp.loc[y, s] for y in yrs], color=c, lw=1.9, label=lab)
    axes[0].set_title("Carbon price, OECD zone", fontsize=10, fontweight="600", pad=8)
    axes[0].set_ylabel("US$2022 / tCO₂e")
    axes[1].set_title("Global mean warming (GSAT)", fontsize=10, fontweight="600", pad=8)
    axes[1].set_ylabel("K vs 1850–1900")
    for ax in axes:
        ax.grid(color=GRID, lw=0.8, zorder=0)
        ax.set_axisbelow(True)
        ax.set_xlabel("year")
    axes[0].legend(frameon=False, fontsize=8)
    fig.suptitle("Model inputs: NGFS Phase 5 scenario paths",
                 fontsize=12.5, fontweight="600", x=0.012, ha="left", y=1.085)
    fig.text(0.012, 1.015, "MESSAGEix-GLOBIOM R12. The two channels are driven by these: carbon price → transition, warming → physical.",
             fontsize=8.5, color=MUTED, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig7_scenario_inputs.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("  fig7_scenario_inputs.png")


# --- 8. FX term structure ----------------------------------------------------
def fig_term():
    fwd = load("out_ext_fx_forward_5y")
    hz = [int(c) for c in fwd.columns]
    show = ["IND", "CHN", "TUR", "KOR", "USA", "NOR"]
    cols = [WARM, "#d08b5c", "#c9a227", TEAL, COOL, "#3f5f8a"]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), sharey=True)
    for ax, s, t in zip(axes, (NZ, NDC), ("Net Zero 2050", "NDCs")):
        d = fwd.xs(s, level=0)
        for r, c in zip(show, cols):
            ax.plot(hz, d.loc[r].to_numpy(float), color=c, lw=1.9, marker="o", ms=3.5, label=r)
        ax.axhline(0, color=MUTED, lw=1)
        ax.set_title(t, fontsize=10, fontweight="600", pad=8)
        ax.set_xlabel("horizon year")
        ax.grid(color=GRID, lw=0.8, zorder=0)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("5y forward FX vs EUR (%)")
    axes[1].legend(frameon=False, fontsize=8, ncol=2)
    fig.suptitle("FX impact grows with horizon as carbon prices and warming build",
                 fontsize=12.5, fontweight="600", x=0.012, ha="left", y=1.005)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig8_fx_term_structure.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("  fig8_fx_term_structure.png")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ROOT)
    os.makedirs(FIG, exist_ok=True)
    print("writing figures/")
    fig_tradeoff(); fig_fx_rank(); fig_mixture(); fig_band()
    fig_vuln(); fig_equity_oprisk(); fig_inputs(); fig_term()
    print("done.")
