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


def scen(label, available):
    """
    Match a scenario label against what the data actually holds.

    The IIASA API returns 'Below 2?C' (ASCII 0x3f) where the published name has
    a degree sign, so an exact lookup silently drops that series -- which is
    what fig7 did for several commits, plotting 4 of the 5 curves its code
    listed.  bkmn.mixture solves this with the same normalisation; raise rather
    than drop, so the failure can never be silent again.
    """
    norm = lambda t: "".join(ch for ch in t.lower() if ch.isalnum())
    for a in available:
        if norm(a) == norm(label):
            return a
    raise KeyError(f"scenario {label!r} not in {sorted(available)}")


def pick_regions(wanted, available, need=4):
    """
    Keep the requested regions that exist in the data, in the order asked.

    The region set is derived (docs/CHAPTER_REGION_SELECTION.md), so it changes
    when the selection changes: figures must not hard-code a list that silently
    empties.  Dropping a name is allowed -- it means that region no longer
    exists -- but ending up with too few series to make the point is not, so
    that raises.  Same principle as `scen()`: never fail silently.
    """
    keep = [r for r in wanted if r in set(available)]
    if len(keep) < need:
        raise KeyError(f"only {keep} of {wanted} exist in {sorted(available)}; "
                       f"need at least {need} series for this figure")
    return keep


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
    # Two panels, not seven: these are the transition EXTREMES (Net Zero has the
    # largest mean transition cost at -2.04%, Current Policies the smallest at
    # -0.06%).  Physical damage is deliberately not the selection criterion --
    # it varies only 0.08pp across all seven scenarios, which is the point the
    # figure makes.  All seven inputs are in fig7.
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 6.4), sharey=True)
    span, phmean = {}, {}
    for ax, s in zip(axes, (NZ, CP)):
        t = [tr.loc[(s, r), H] for r in order]
        p = [ph.loc[(s, r), H] for r in order]
        span[s] = min(min(t), min(p))
        phmean[s] = float(np.mean(p))
        ax.barh(y - 0.19, t, height=0.36, color=TEAL, label="transition (carbon price)", zorder=3)
        ax.barh(y + 0.19, p, height=0.36, color=WARM, label="physical (warming)", zorder=3)
        ax.axvline(0, color=MUTED, lw=1)
        ax.set_title(s, fontsize=10, fontweight="600", color=INK, pad=8)
        ax.set_xlabel("GDP shock at 2040 (%)")
        ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
        ax.set_axisbelow(True)
        # independent x-scales: on a shared scale the Current Policies panel is
        # a blank column, because after the damage-function correction physical
        # damage is ~100x smaller than the Net Zero transition cost.  The point
        # of the figure is which channel dominates WITHIN each scenario, so the
        # scales are per-panel and the difference is stated in the subtitle.
        lo = min(min(t), min(p)) * 1.35
        ax.set_xlim(lo, abs(lo) * 0.06)
    axes[0].set_yticks(y, order, fontsize=8.5)
    axes[0].invert_yaxis()
    axes[0].legend(loc="lower left", frameon=False, fontsize=8.5)
    fig.suptitle("Transition cost is a policy choice; physical cost is not",
                 fontsize=12.5, fontweight="600", x=0.012, ha="left", y=1.075)
    fig.text(0.012, 1.012,
             "The two transition extremes of the seven NGFS narratives. Transition cost swings "
             f"{abs(span[NZ])/abs(span[CP]):.0f}x between them, while mean physical damage barely moves "
             f"({phmean[NZ]:.2f}% vs {phmean[CP]:.2f}%) — warming to 2040 is largely locked in. "
             "NOTE per-panel x-scales.",
             fontsize=8.5, color=MUTED, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig1_transition_vs_physical.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("  fig1_transition_vs_physical.png")


# --- 2. FX forward ranking ---------------------------------------------------
def fig_fx_rank():
    """
    Headline is the mixture, not one narrative.

    The chapter reports every channel as a probability-weighted expectation over
    the seven NGFS narratives and shows the single-narrative value as a labelled
    component; this figure has the same shape, so bars are the uniform-prior
    expectation and the tick is Net Zero.  Reading only the tick overstates
    every move, because Net Zero is the most transition-intensive of the seven.
    """
    mix = load("out_mix_fx_forward_uniform", idx=(0,))
    nz = load("out_ext_fx_forward_5y").xs(NZ, level=0)
    order = mix[H].sort_values().index.tolist()
    v = [mix.loc[r, H] for r in order]
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    barh_signed(ax, order, v, fmt="{:+.2f}%")
    ticks = [nz.loc[r, H] for r in order]
    ax.scatter(ticks, np.arange(len(order)), marker="|", s=90, color=INK,
               zorder=4, label="Net Zero 2050 component")
    # barh_signed sizes the axis from the bars alone; the Net Zero component is
    # larger than every mixture value, so widen or the ticks fall off the edge
    lo, hi = ax.get_xlim()
    ax.set_xlim(min(lo, min(ticks) * 1.12), max(hi, max(ticks) * 1.12))
    ax.legend(loc="lower left", frameon=False, fontsize=8.5)
    finish(fig, ax, "Climate FX shifts against the euro, 2040 (scenario mixture)",
           "5-year forward, uniform prior over the seven NGFS narratives; negative = strengthens vs EUR.",
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
    # all seven NGFS narratives, not a subset: 'Low demand' in particular
    # carries the second-largest FX dispersion (FX_REPORT 4) and was omitted.
    want = [NZ, "Low demand", "Below 2C", "Delayed transition", NDC,
            "Fragmented World", CP]
    scens = [scen(w, sc.names) for w in want]
    labs = ["Net Zero 2050", "Low demand", "Below 2°C", "Delayed transition",
            "NDCs", "Fragmented World", "Current Policies"]
    cols = [TEAL, "#2f6f6b", "#4b9aa4", COOL, "#d08b5c", "#a8703f", WARM]
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
    show = pick_regions(["IND", "TUR", "USA", "CHN", "GBR", "CHE"],
                        fwd.index.get_level_values(-1))
    cols = [WARM, "#d08b5c", "#c9a227", TEAL, COOL, "#3f5f8a", "#0e7c86"]
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
    show = pick_regions(["IND", "CHN", "TUR", "RASIA", "USA", "EU27", "CHE"],
                        d.index.get_level_values(1))
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

    show2 = pick_regions(["EU27", "TUR", "RUS", "IND", "CHN", "AFR", "RASIA"],
                         g.columns)
    x = np.arange(len(show2))
    for k, (th, c, lbcl) in enumerate([("theta=1", COOL, "EU importer pays (statutory)"),
                                       ("theta=0", WARM, "exporter absorbs")]):
        axes[1].bar(x + (k - 0.5) * 0.36,
                    [g.loc[("applied-divergence", th), r] for r in show2],
                    width=0.34, color=c, label=lbcl, zorder=3)
    axes[1].axhline(0, color=MUTED, lw=1)
    axes[1].set_xticks(x, show2, fontsize=9)
    axes[1].set_title("Who bears it: GVA effect by incidence assumption",
                      fontsize=10, fontweight="600", pad=8)
    axes[1].set_ylabel("GVA change at applied prices (%)")
    axes[1].legend(frameon=False, fontsize=8.5, loc="lower right")
    for ax in axes:
        ax.grid(axis="x" if ax is axes[0] else "y", color=GRID, lw=0.8, zorder=0)
        ax.set_axisbelow(True)
    fig.suptitle("CBAM as a carbon tariff: enormous sector rates, small macro effect",
                 fontsize=12.5, fontweight="600", x=0.012, ha="left", y=1.075)
    # read the price and revenue from the data rather than hardcoding them, so
    # the caption cannot drift from the bars when the calibration changes
    eu_px = pd.read_csv(os.path.join(ROOT, "DATA_20R/region_carbon_map.csv"),
                        index_col="region").loc["EU27", "applied_price_usd"]
    rev = g.loc[("applied-divergence", "theta=1"), "revenue_bn"]
    fig.text(0.012, 1.012,
             rf"EU price \${eu_px:.0f}/t (published CBAM certificate price) against "
             rf"the price each origin already pays. Revenue \${rev:.1f}bn/yr.",
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
    ratio = fw.abs().max() / sp.abs().max()
    corr = sp.corr(fw)
    axa.set_title(f"(a) the same shock, two channels {ratio:.1f}x apart "
                  f"(corr {corr:.2f})",
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
    share = (0.5 * pi.abs() / (0.5 * pi.abs() + 0.5 * gy.abs()) * 100).median()
    axb.set_title("(b) the output term dominates the policy-rate move",
                  fontsize=10, fontweight="600", loc="left", pad=24)
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


# --- 13. credit: CDS spread shifts by sector and region ----------------------
def fig_credit():
    d = load("out_ext_credit_spread", idx=(0, 1, 2)).xs(NZ, level=0)[H].unstack()
    # drop FTSE (it is the equity column) and order sectors by median widening
    d = d.drop(columns=["FTSE"], errors="ignore")
    order = d.median().sort_values(ascending=False).index.tolist()
    d = d[order]
    regs = pick_regions(["IND", "CHN", "RUS", "RASIA", "TUR", "AFR", "EU27",
                         "USA", "CHE"], d.index, need=5)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.2),
                             gridspec_kw={"width_ratios": [1.35, 1]})

    # panel a: heat-map-free grouped bars, sector on x, a line per region
    x = np.arange(len(order))
    cols = [WARM, "#c9755a", "#d9a441", TEAL, "#3f8f8f", "#5b8bb5", COOL,
            "#6f7f96", "#9aa6b5"]
    for r, c in zip(regs, cols):
        axes[0].plot(x, d.loc[r, order].to_numpy(float), marker="o", ms=4,
                     lw=1.7, color=c, label=r, zorder=3)
    axes[0].axhline(0, color=MUTED, lw=1)
    axes[0].set_xticks(x, order, fontsize=7.5, rotation=38, ha="right")
    axes[0].set_ylabel("CDS spread change at 2040 (%)")
    # how much of the spread is sector vs region?  read it from the data
    _st = d.stack().rename("v").reset_index()
    _st.columns = ["region", "index", "v"]
    _sec = _st.groupby("index").v.mean().var() / _st.v.var() * 100
    _reg = _st.groupby("region").v.mean().var() / _st.v.var() * 100
    axes[0].set_title(f"Sector explains {_sec:.0f} % of the spread, region "
                      f"{_reg:.0f} %",
                      fontsize=10, fontweight="600", pad=8)
    axes[0].legend(frameon=False, fontsize=8, ncol=3, loc="upper right")
    axes[0].grid(axis="y", color=GRID, lw=0.8, zorder=0)
    axes[0].set_axisbelow(True)

    # panel b: the driver -- each index's beta against its median widening
    from bkmn.paper_tables import CDS_BETA
    b = [CDS_BETA[s] for s in order]
    med = d[order].median().to_numpy(float)
    axes[1].scatter(b, med, s=46, color=[WARM if v > 0 else COOL for v in med],
                    zorder=3)
    for s, bi, mi in zip(order, b, med):
        axes[1].annotate(s, (bi, mi), fontsize=7, color=INK,
                         xytext=(4, 3), textcoords="offset points")
    axes[1].axhline(0, color=MUTED, lw=1)
    axes[1].axvline(0, color=MUTED, lw=1)
    axes[1].set_xlabel("paper Table 9 regression slope β")
    axes[1].set_ylabel("median widening across regions (%)")
    rho = float(np.corrcoef(b, med)[0, 1])
    _signs_ok = all((bi < 0) == (mi > 0) for bi, mi in zip(b, med))
    axes[1].set_title(f"β fixes the sign{' exactly' if _signs_ok else ''}; "
                      f"size is β and composition together (corr {rho:.2f})",
                      fontsize=10, fontweight="600", pad=8)
    axes[1].grid(color=GRID, lw=0.8, zorder=0)
    axes[1].set_axisbelow(True)

    fig.suptitle("Credit: CDS spread shifts at 2040 under Net Zero 2050",
                 fontsize=12.5, fontweight="600", x=0.012, ha="left", y=1.06)
    fig.text(0.012, 1.005,
             "Positive = spread widens. Financials and UK Real Estate carry "
             "positive β in the paper's own UK estimates and therefore move "
             "against the rest — a property of that sample, not of this model.",
             fontsize=8.5, color=MUTED, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig13_credit_spreads.png"), dpi=300,
                bbox_inches="tight")
    plt.close(fig)
    print("  fig13_credit_spreads.png")


# --- 14. cost pass-through sensitivity ---------------------------------------
def fig_phi():
    tr = load("out_phi_transition", idx=(0,))
    cr = load("out_phi_credit", idx=(0,))
    inv = load("out_phi_invariance", idx=(0,))
    phis = tr.index.to_numpy(float)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.0))

    # panel a: every region's GVA shock crosses zero as phi rises
    show = pick_regions(["IND", "CHN", "AFR", "TUR", "RUS", "EU27", "USA",
                         "GBR", "CHE"], tr.columns, need=5)
    cols = [WARM, "#c9755a", "#d9a441", TEAL, "#3f8f8f", COOL, "#5b8bb5",
            "#6f7f96", "#9aa6b5"]
    for r, c in zip(show, cols):
        y = tr[r].to_numpy(float)
        axes[0].plot(phis, y, lw=1.8, color=c, label=r, zorder=3)
        s = np.where(np.diff(np.sign(y)) != 0)[0]
        if len(s):
            i = s[0]
            root = phis[i] + (phis[i + 1] - phis[i]) * (-y[i]) / (y[i + 1] - y[i])
            axes[0].plot([root], [0], marker="o", ms=4, color=c, zorder=4)
    axes[0].axhline(0, color=MUTED, lw=1)
    axes[0].axvline(0.5, color=MUTED, lw=0.9, ls="--")
    axes[0].text(0.505, axes[0].get_ylim()[0] * 0.92, "reporting value φ = 0.5",
                 fontsize=7.5, color=MUTED)
    axes[0].set_xlabel("cost pass-through φ")
    axes[0].set_ylabel("transition GVA shock at 2040 (%)")
    axes[0].set_title("The charge changes sign, and near the same φ everywhere",
                      fontsize=10, fontweight="600", pad=8)
    axes[0].legend(frameon=False, fontsize=7.5, ncol=3, loc="upper left")
    axes[0].grid(color=GRID, lw=0.8, zorder=0)
    axes[0].set_axisbelow(True)

    # panel b: everything as a deviation from the reporting value at phi = 0.5,
    # so a channel that does not depend on phi sits exactly on zero
    def dev(v):
        v = np.asarray(v, float)
        mid = v[np.argmin(abs(phis - 0.5))]
        return (v - mid) / abs(mid) * 100

    for lbl, v, c, ls in (
            ("transition GVA", tr["IND"], WARM, "-"),
            ("credit spread", cr["IND"], "#d9a441", "-"),
            ("policy rate", inv["rate_IND_bp"], COOL, "--"),
            ("5y forward FX", inv["fwd5_IND_pct"], TEAL, ":")):
        axes[1].plot(phis, dev(v), lw=2.4 if ls != "-" else 2.0, color=c,
                     ls=ls, label=lbl, zorder=3)
    axes[1].axhline(0, color=MUTED, lw=1)
    axes[1].set_xlabel("cost pass-through φ")
    axes[1].set_ylabel("India: % change from the value at φ = 0.5")
    rng = float(inv["rate_IND_bp"].max() - inv["rate_IND_bp"].min())
    axes[1].set_title("φ moves value added and credit; rates and FX sit exactly "
                      "on zero", fontsize=10, fontweight="600", pad=8)
    axes[1].annotate("policy rate and FX: identical at every φ\n"
                     f"(range {rng:.0e} bp)", xy=(0.30, 0), xytext=(0.18, 120),
                     fontsize=7.5, color=MUTED,
                     arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
    axes[1].legend(frameon=False, fontsize=8, loc="upper left")
    axes[1].grid(color=GRID, lw=0.8, zorder=0)
    axes[1].set_axisbelow(True)

    fig.suptitle("Cost pass-through is the model's widest single uncertainty — "
                 "for two channels only",
                 fontsize=12.5, fontweight="600", x=0.012, ha="left", y=1.05)
    fig.text(0.012, 1.0,
             "Net Zero 2050 at 2040. At φ = 0 a sector absorbs the whole carbon "
             "charge in its own value added; at φ = 1 it passes all of it "
             "downstream. Markers show where each region's shock changes sign.",
             fontsize=8.5, color=MUTED, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig14_pass_through.png"), dpi=300,
                bbox_inches="tight")
    plt.close(fig)
    print("  fig14_pass_through.png")


# --- 15. how much the scenario prior matters, by channel ---------------------
PRIORS = ["uniform", "policy-sceptic", "ambition", "consensus"]


def _mix(channel, prior, idx=(0,)):
    return load(f"out_mix_{channel}_{prior}", idx=idx)


def fig_prior_sensitivity():
    """
    The chapter's organising result: which channels survive the prior.

    Every headline is an expectation under an assumed scenario distribution,
    and NGFS publishes no probabilities, so the honest summary statistic is how
    far a number travels when that assumption changes.  Channels are split by
    what they carry: the carbon charge inherits the narratives' disagreement
    about policy, physical damage does not, because warming to 2040 is already
    largely determined.
    """
    def spread(vals):
        v = [abs(float(x)) for x in vals]
        return max(v) / min(v)

    def med_credit(p):
        c = _mix("credit", p, idx=(0, 1))[H].unstack().drop(columns=["FTSE"])
        return c.median(axis=1)["IND"]

    rows = [
        ("Spot FX (rupee)", spread(_mix("fx_spot", p).loc["IND", H] for p in PRIORS), "carbon price"),
        ("Transition GVA (mean)", spread(_mix("gdp_transition", p)[H].mean() for p in PRIORS), "carbon price"),
        ("Credit (India median)", spread(med_credit(p) for p in PRIORS), "carbon price"),
        ("Total GDP (mean)", spread(_mix("gdp_total", p)[H].mean() for p in PRIORS), "both"),
        ("Equity (mean)", spread(_mix("equity", p)[H].mean() for p in PRIORS), "both"),
        ("Forward FX (rupee)", spread(_mix("fx_forward", p).loc["IND", H] for p in PRIORS), "both"),
        ("Policy rate (mean)", spread(_mix("rate", p)[H].mean() for p in PRIORS), "physical damage"),
        ("Operational risk", spread(_mix("oprisk_conduct", p).loc["RASIA", H] for p in PRIORS), "physical damage"),
        ("Physical damage (mean)", spread(_mix("gdp_physical", p)[H].mean() for p in PRIORS), "physical damage"),
    ]
    rows.sort(key=lambda r: -r[1])
    labs = [r[0] for r in rows]
    vals = [r[1] for r in rows]
    hue = {"carbon price": WARM, "both": "#d9a441", "physical damage": COOL}

    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    y = np.arange(len(labs))
    ax.barh(y, vals, color=[hue[r[2]] for r in rows], height=0.66, zorder=3)
    ax.set_xscale("log")
    ax.set_xlim(0.9, max(vals) * 2.2)
    ax.axvline(1, color=MUTED, lw=1)
    ax.set_yticks(y, labs, fontsize=8.5)
    ax.invert_yaxis()
    for i, (v, r) in enumerate(zip(vals, rows)):
        ax.text(v * 1.07, i, f"{v:.2f}×" if v < 2 else f"{v:.1f}×", va="center",
                fontsize=8, color=INK)
    ax.set_xticks([1, 2, 5, 10, 20], ["1×", "2×", "5×", "10×", "20×"])
    for k, c in hue.items():
        ax.barh([0], [0], color=c, label=k)
    ax.legend(title="driven by", loc="lower right", frameon=False, fontsize=8.5,
              title_fontsize=8.5)
    finish(fig, ax, "How much does the scenario prior matter? It depends on the channel",
           "Ratio of largest to smallest headline at 2040 across the four priors. "
           "Note the log scale: 1× means the prior is irrelevant.",
           "fig15_prior_sensitivity.png", "range across the four priors (max ÷ min)")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ROOT)
    os.makedirs(FIG, exist_ok=True)
    print("writing figures/")
    fig_tradeoff(); fig_fx_rank(); fig_mixture(); fig_band()
    fig_vuln(); fig_equity_oprisk(); fig_inputs(); fig_term(); fig_drift(); fig_term_structure(); fig_cbam()
    fig_two_channels(); fig_credit(); fig_phi(); fig_prior_sensitivity()
    print("done.")
