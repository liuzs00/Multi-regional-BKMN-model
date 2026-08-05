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
    priors = ["consensus", "policy-sceptic", "uniform", "ambition"]
    cols = [INK, COOL, TEAL, WARM]
    data = {p: load(f"out_ext_fx_expected_{p}", idx=(0,)) for p in priors}
    order = data["uniform"][H].sort_values().index.tolist()
    y = np.arange(len(order))
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    for k, (p, c) in enumerate(zip(priors, cols)):
        ax.barh(y + (k - 1.5) * 0.21, [data[p].loc[r, H] for r in order],
                height=0.19, color=c, label=p, zorder=3)
    ax.axvline(0, color=MUTED, lw=1)
    ax.set_yticks(y, order, fontsize=8.5)
    ax.invert_yaxis()
    ax.legend(title="scenario prior", loc="lower left", frameon=False, fontsize=8.5,
              title_fontsize=8.5)
    finish(fig, ax, "Expected FX shift under the Bayesian scenario mixture, 2040",
           "Probability-weighted across the seven NGFS scenarios. 'consensus' is anchored on the "
           "published current-policy warming estimate (UNEP/CAT, 2.7 C); the others are conventional or asserted.",
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
    axes[0].set_ylabel("US\$2022 / tCO₂e")
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


# --- 9. sensitivity: scenario drift (Eq 1) ----------------------------------
def fig_drift():
    import sys; sys.path.insert(0, ROOT)
    from bkmn import mixture as mixmod
    from bkmn.regions import load as loadm
    from bkmn.scenarios import Scenarios
    co = Scenarios(loadm().carbon_map).coords()
    fwd = load("out_ext_fx_forward_5y")
    hz = [int(c) for c in fwd.columns]
    priors, cols = ["ambition", "uniform", "policy-sceptic"], [WARM, TEAL, COOL]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), sharey=True)
    for ax, lam, ttl in zip(axes, (5.0, 0.5), ("slow drift  (lambda = 5)",
                                               "fast drift  (lambda = 0.5)")):
        for p, c in zip(priors, cols):
            st = mixmod.expected(fwd, p).loc["IND"].to_numpy(float)
            dr = mixmod.expected_drift(fwd, co, p, lam=lam).loc["IND"].to_numpy(float)
            ax.plot(hz, st, color=c, lw=1.4, ls=":", alpha=.75)
            ax.plot(hz, dr, color=c, lw=2.0, marker="o", ms=3.5, label=p)
        ax.set_title(ttl, fontsize=10, fontweight="600", pad=8)
        ax.set_xlabel("horizon year"); ax.set_xticks(hz)
        ax.grid(color=GRID, lw=0.8, zorder=0); ax.set_axisbelow(True)
    axes[0].set_ylabel("expected 5y forward INR/EUR (%)")
    axes[1].legend(frameon=False, fontsize=8.5, title="prior", title_fontsize=8.5)
    fig.suptitle("Sensitivity: scenario drift erodes the prior (Eq 1 transition matrix)",
                 fontsize=12.5, fontweight="600", x=0.012, ha="left", y=1.085)
    fig.text(0.012, 1.015, "Dotted = static mixture (headline). Solid = with annual drift on "
             "standardised (T2100, carbon price) distance; the three priors converge.",
             fontsize=8.5, color=MUTED, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig9_scenario_drift_sensitivity.png"), dpi=300,
                bbox_inches="tight")
    plt.close(fig); print("  fig9_scenario_drift_sensitivity.png")


# --- 10. rate term structure (Prop 2) ---------------------------------------
def fig_term_structure():
    d = load("out_ext_rate_term_structure", idx=(0, 1, 2))
    ten = ["1D", "6M", "1Y", "5Y", "10Y", "20Y"]
    tau = [1/365, 0.5, 1, 5, 10, 20]
    show = ["IND", "CHN", "TUR", "KOR", "USA", "EU27", "NOR"]
    cols = [WARM, "#d08b5c", "#c9a227", TEAL, COOL, "#0e7c86", "#3f5f8a"]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), sharey=True)
    for ax, s, ttl in zip(axes, (NZ, NDC), ("Net Zero 2050", "NDCs")):
        for r, c in zip(show, cols):
            y = [d.loc[(s, r, t), H] for t in ten]
            ax.plot(tau, y, color=c, lw=1.9, marker="o", ms=3.5, label=r)
        ax.axhline(0, color=MUTED, lw=1)
        ax.set_xscale("log"); ax.set_xticks(tau); ax.set_xticklabels(ten)
        ax.set_title(ttl, fontsize=10, fontweight="600", pad=8)
        ax.set_xlabel("tenor")
        ax.grid(color=GRID, lw=0.8, zorder=0); ax.set_axisbelow(True)
    axes[0].set_ylabel("zero-rate shift at 2040 (bp)")
    axes[1].legend(frameon=False, fontsize=8, ncol=2)
    fig.suptitle("Long-rate term structure: the shift decays with maturity (Prop 2)",
                 fontsize=12.5, fontweight="600", x=0.012, ha="left", y=1.085)
    fig.text(0.012, 1.015, "Hull-White 1F with a = 0.04: dR(t,T) = B(tau)/tau . dr(t), "
             "sigma-independent. 20Y/1D ratio = 0.688 by construction.",
             fontsize=8.5, color=MUTED, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig10_rate_term_structure.png"), dpi=300,
                bbox_inches="tight")
    plt.close(fig); print("  fig10_rate_term_structure.png")


# --- 11. CBAM ---------------------------------------------------------------
def fig_cbam():
    rates = pd.read_csv(os.path.join(ROOT, "out_sens_cbam_rates.csv"))
    g = load("out_sens_cbam_gva", idx=(0, 1))
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.2))

    top = rates.nlargest(12, "cbam_rate_pct").iloc[::-1]
    lab = [f"{r.region} {r.industry}" for r in top.itertuples()]
    y = np.arange(len(top))
    axes[0].barh(y, top.cbam_rate_pct, color=WARM, height=0.68, zorder=3)
    axes[0].set_yticks(y, lab, fontsize=8)
    for i, v in enumerate(top.cbam_rate_pct):
        axes[0].text(v + 2, i, f"{v:.0f}%", va="center", fontsize=8, color=INK)
    axes[0].axvline(100, color=MUTED, lw=1, ls="--")
    axes[0].text(102, 0.6, "charge exceeds the good's value",
                 fontsize=7.5, color=MUTED)
    axes[0].set_xlim(0, 175)
    axes[0].set_title("Ad-valorem CBAM rate by origin and sector",
                      fontsize=10, fontweight="600", pad=8)
    axes[0].set_xlabel("CBAM charge as % of import value")

    regs = ["EU27", "TUR", "RUS", "KAZ", "IND", "CHN", "AFR"]
    x = np.arange(len(regs))
    for k, (th, c, lbcl) in enumerate([("theta=1", COOL, "EU importer pays (statutory)"),
                                       ("theta=0", WARM, "exporter absorbs")]):
        axes[1].bar(x + (k - 0.5) * 0.36,
                    [g.loc[("applied-divergence", th), r] for r in regs],
                    width=0.34, color=c, label=lbcl, zorder=3)
    axes[1].axhline(0, color=MUTED, lw=1)
    axes[1].set_xticks(x, regs, fontsize=9)
    axes[1].set_title("Who bears it: GVA effect by incidence assumption",
                      fontsize=10, fontweight="600", pad=8)
    axes[1].set_ylabel("GVA change at applied prices (%)")
    axes[1].legend(frameon=False, fontsize=8.5, loc="lower right")
    for ax in axes:
        ax.grid(axis="x" if ax is axes[0] else "y", color=GRID, lw=0.8, zorder=0)
        ax.set_axisbelow(True)
    fig.suptitle("CBAM as a carbon tariff: enormous sector rates, small macro effect",
                 fontsize=12.5, fontweight="600", x=0.012, ha="left", y=1.075)
    fig.text(0.012, 1.012, r"EU price \$80/t against the price each origin already pays. "
             r"Revenue on covered intermediate imports ~\$8.4bn/yr.",
             fontsize=8.5, color=MUTED, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig11_cbam.png"), dpi=300, bbox_inches="tight")
    plt.close(fig); print("  fig11_cbam.png")


# --- 12. the two FX channels disagree ---------------------------------------
def fig_two_channels():
    """
    Spot (relative PPP, inflation-driven) against forward (CIP, rate-driven).

    The paper derives FX from "the difference in the changes of yield curves",
    which in practice splits into two channels of very different size that rank
    regions differently.  This figure is the argument for reporting both.
    """
    Y = "2045"
    sp = load("out_fx_spot_ppp").xs(NZ, level=0)[Y]
    fw = load("out_fx_forward_5y").xs(NZ, level=0)[Y]
    pi = load("out_inflation_shift").xs(NZ, level=0)[Y]
    gy = load("out_gdp_shock_fx").xs(NZ, level=0)[Y] * 100
    regs = list(sp.index)

    fig, (axa, axb) = plt.subplots(1, 2, figsize=(11.6, 5.4),
                                   gridspec_kw={"width_ratios": [1.25, 1]})
    o = list(fw.loc[regs].sort_values().index)
    y = np.arange(len(o))
    axa.barh(y - 0.2, sp[o], height=0.38, color=COOL, zorder=3,
             label="spot (relative PPP)")
    axa.barh(y + 0.2, fw[o], height=0.38, color=WARM, zorder=3,
             label="5y forward (CIP)")
    flip = [r for r in o if np.sign(sp[r]) != np.sign(fw[r])]
    axa.set_yticks(y, [f"{r} *" if r in flip else r for r in o], fontsize=8.5)
    axa.axvline(0, color=MUTED, lw=1)
    axa.invert_yaxis()
    axa.legend(frameon=False, fontsize=8.5, loc="lower left", ncol=2,
               bbox_to_anchor=(0, 1.0), handlelength=1.4, columnspacing=1.4)
    axa.set_xlabel("% vs EUR   (negative = strengthens against the euro)", fontsize=9)
    axa.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    axa.set_axisbelow(True)
    axa.set_title("(a) the same shock, two channels, 9x apart",
                  fontsize=10, fontweight="600", loc="left", pad=24)
    axa.text(0.015, 0.055, "*  spot and forward disagree in sign",
             transform=axa.transAxes, fontsize=7.8, color=INK)

    o2 = list(gy.reindex(gy.abs().sort_values().index).index)
    axb.barh(np.arange(len(o2)), 0.5 * gy[o2], height=0.62, color=TEAL, zorder=3,
             label="output term  0.5 x GVA")
    axb.barh(np.arange(len(o2)), 0.5 * pi[o2], height=0.62, color=WARM, zorder=4,
             label="inflation term  0.5 x dPi")
    axb.set_yticks(np.arange(len(o2)), o2, fontsize=7.6)
    axb.axvline(0, color=MUTED, lw=1)
    axb.set_xlabel("contribution to the policy-rate shift (bp)", fontsize=9)
    axb.legend(frameon=False, fontsize=8.5, loc="lower left", ncol=2,
               bbox_to_anchor=(0, 1.0), handlelength=1.4, columnspacing=1.4)
    axb.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    axb.set_axisbelow(True)
    axb.set_title("(b) the inflation channel is invisible next to output",
                  fontsize=10, fontweight="600", loc="left", pad=24)
    share = (0.5 * pi.abs() / (0.5 * pi.abs() + 0.5 * gy.abs()) * 100).median()
    axb.text(0.015, 0.055, f"inflation is a median {share:.1f}% of each rate move",
             transform=axb.transAxes, fontsize=7.8, color=INK)

    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.suptitle("Two FX channels, and why they diverge", fontsize=12.5,
                 fontweight="600", x=0.006, ha="left", y=1.00)
    fig.text(0.006, 0.945, f"Net Zero 2050 at {Y}, vs EUR. Spot moves with the "
             "inflation differential; the forward adds the rate differential, "
             "which the output term dominates.",
             fontsize=8.5, color=MUTED, ha="left", va="bottom")
    fig.savefig(os.path.join(FIG, "fig12_two_fx_channels.png"), dpi=300,
                bbox_inches="tight")
    plt.close(fig)
    print("  fig12_two_fx_channels.png")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ROOT)
    os.makedirs(FIG, exist_ok=True)
    print("writing figures/")
    fig_tradeoff(); fig_fx_rank(); fig_mixture(); fig_band()
    fig_vuln(); fig_equity_oprisk(); fig_inputs(); fig_term(); fig_drift(); fig_term_structure(); fig_cbam()
    fig_two_channels()
    print("done.")
