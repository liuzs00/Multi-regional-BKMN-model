"""
The four measures in force in mid-2026, applied together, and decomposed.

docs/TARIFF_CALIBRATION.md reports each schedule on its own.  This driver runs
them as one stack, alongside the carbon charge, and attributes the combined
result back to its components.

    1  US applied tariffs, May 2026        4.4% on all origins into the US,
                                           23.4% on China (Penn Wharton / USAFacts)
    2  EU-US framework, Jul 2026           the US caps EU goods at an all-inclusive
                                           15%; the EU drops its MFN on US industrials
    3  EU steel safeguard 2026/1384        out-of-quota duty 50%, ~39% above quota
                                           -> 19.5% average on EU steel imports
    4  CBAM (EU, applied prices)           carbon-price differential on embedded
                                           carbon, EU certificate price $86/t

AVOIDING DOUBLE COUNTING.  Only one pair genuinely overlaps.  Measures 1 and 2
both price the EU->US flow, and the framework's 15% is *all-inclusive* -- it caps
the total, it does not sit on top of the existing rate.  Adding the schedules
naively would charge 4.4 + 15 = 19.4% on EU goods entering the US.  Measure 2 is
therefore entered as the INCREMENT over measure 1 on that flow, 15 - 4.4 = 10.6
pp, so the stack totals exactly 15% and the four schedules remain additive.
`check_no_double_count()` asserts this on the assembled matrix.

The other pairs do not overlap:
  * safeguard x CBAM  -- both hit EU steel, but they are separate instruments and
    stack in law; CBAM's double-protection rule concerns ETS free allocation, not
    trade defence.
  * carbon x CBAM     -- structurally disjoint: the carbon charge is levied on a
    sector's own Scope-1 production (diagonal blocks), CBAM on imported inputs
    (off-diagonal).  Asserted numerically.

DECOMPOSITION.  The charge channel is exactly linear in ct (validation gate C8)
and shocks superpose exactly (C9), so the stack decomposes into its components
with no residual and no ordering dependence.  The script reports the residual as
evidence rather than assuming it.

Writes out_stack_{gva,fx,decomp}.csv.
Run: py -3 tools/run_tariff_stack.py
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")
os.makedirs(RESULTS, exist_ok=True)
sys.path.insert(0, ROOT)

from bkmn import cbam, equity, oprisk, physical, tariff, transition     # noqa: E402
from bkmn.regions import load                                           # noqa: E402
from bkmn.run_extensions import PHI, chain, derive                      # noqa: E402
from bkmn.scenarios import Scenarios                                    # noqa: E402

YEAR = 2040
SCENARIO = "Current Policies"          # carbon baseline the tariffs sit on
MFG = ["C10T12", "C13T15", "C16", "C17_18", "C19", "C20", "C21", "C22", "C23",
       "C24A", "C24B", "C25", "C26", "C27", "C28", "C29", "C301", "C302T309",
       "C31T33"]

US_ALL, US_CHN = 0.044, 0.234          # [DATA] Penn Wharton, USAFacts
EU_US_CAP, EU_MFN = 0.15, 0.0133       # [DATA] EU-US framework; World Bank MFN
STEEL_DUTY, STEEL_ABOVE_QUOTA = 0.50, 0.39   # [DATA]/[ESTIMATE] Reg 2026/1384


def build(m, applied):
    """The four schedules, constructed so that they are additive."""
    z = tariff.empty
    us = tariff.add_rule(m, z(m), US_ALL, destination="USA")
    us = tariff.add_rule(m, us, US_CHN - US_ALL, origin="CHN", destination="USA")

    # increment over `us` on the EU->US flow, so the stack totals the 15% cap
    eu_us = tariff.add_rule(m, z(m), EU_US_CAP - US_ALL, origin="EU27",
                            destination="USA")
    eu_us = tariff.add_rule(m, eu_us, -EU_MFN, origin="USA",
                            destination="EU27", industries=MFG)

    steel = tariff.add_rule(m, z(m), STEEL_DUTY * STEEL_ABOVE_QUOTA,
                            destination="EU27", industries=["C24A"])
    cb = cbam.schedule(m, applied)
    return {"US applied tariffs, May 2026": us,
            "EU-US framework, Jul 2026": eu_us,
            "EU steel safeguard 2026/1384": steel,
            "CBAM (EU, applied prices)": cb}


def check_no_double_count(m, shocks, stack, applied):
    """Assert the overlaps are handled, and report the numbers that show it."""
    reg = np.asarray(m.region_of)
    regs = list(m.regions_order)
    d_us, d_eu = regs.index("USA"), regs.index("EU27")
    eu_rows = reg == "EU27"

    # 1. EU->US totals the all-inclusive cap, not cap + existing rate
    tot = stack[eu_rows, d_us]
    naive = (shocks["US applied tariffs, May 2026"][eu_rows, d_us]
             + EU_US_CAP)
    print("no-double-count checks")
    print(f"  EU->US stacked rate      {tot.max():.4f}   (cap {EU_US_CAP:.4f})")
    print(f"  naive sum would have been {naive.max():.4f}   "
          f"-> {(naive.max()-tot.max())*100:.1f} pp of double counting avoided")
    assert abs(tot.max() - EU_US_CAP) < 1e-12

    # 2. CBAM and the carbon charge never touch the same cell: CBAM is zero on
    #    the EU's own supply, the carbon charge is levied only there.
    cb = shocks["CBAM (EU, applied prices)"]
    assert abs(cb[eu_rows, d_eu]).max() == 0.0
    print(f"  CBAM on EU's own supply   {abs(cb[eu_rows, d_eu]).max():.1e} "
          f"(carbon charge territory -- disjoint)")

    # 3. safeguard and CBAM do overlap on EU steel, deliberately
    st = shocks["EU steel safeguard 2026/1384"]
    steel_rows = np.asarray(m.industry_of) == "C24A"
    both = ((st[:, d_eu] > 0) & (cb[:, d_eu] > 0)).sum()
    print(f"  cells carrying both safeguard and CBAM  {both}  "
          f"(separate instruments, stack in law)")
    return True


def main():
    m = load()
    sc = Scenarios(m.carbon_map)
    cm = m.carbon_map.set_index("region")
    scope, vl = cm.carbon_scope, physical.vl_vector(m)
    applied = cm.applied_price_usd.to_dict()
    fxregs = [r for r in m.regions_order if cm.loc[r, "fx_role"] == "analytical"]
    M = transition.gva_operator(m, PHI)
    Lt = transition.price_operator(m, PHI)
    A = transition.technical_matrix(m)
    betas, kap, u0 = equity.betas(), oprisk.kappa(), oprisk.base_unemployment()

    shocks = build(m, applied)
    stack = sum(shocks.values())
    check_no_double_count(m, shocks, stack, applied)

    # carbon-only baseline, and the same chain with each schedule added
    base_c = chain(m, sc, SCENARIO, M, scope, vl)
    base_d = derive(m, base_c, fxregs, betas, kap, u0)

    runs = {}
    for name, tau_ in list(shocks.items()) + [("ALL FOUR COMBINED", stack)]:
        c = chain(m, sc, SCENARIO, M, scope, vl, tau=tau_, theta=1.0,
                  Ltilde=Lt, A=A)
        runs[name] = (c, derive(m, c, fxregs, betas, kap, u0))

    # ---- GVA decomposition -------------------------------------------------
    gva = pd.DataFrame({
        name: {r: c["tariff"][r][YEAR] * 100 for r in m.regions_order}
        for name, (c, _) in runs.items()}).rename_axis("region")
    gva.insert(0, "carbon charge",
               [base_c["trans"][r][YEAR] * 100 for r in gva.index])
    parts = list(shocks)
    gva["sum of four"] = gva[parts].sum(axis=1)
    gva["residual"] = gva["ALL FOUR COMBINED"] - gva["sum of four"]
    gva["carbon + tariffs"] = gva["carbon charge"] + gva["ALL FOUR COMBINED"]

    # ---- FX decomposition --------------------------------------------------
    def fxcol(key, d, base, scale):
        return {r: (d[key][r][YEAR] - base[key][r][YEAR]) * scale for r in fxregs}

    spot = pd.DataFrame({n: fxcol("spot", d, base_d, 100)
                         for n, (_, d) in runs.items()}).rename_axis("region")
    spot["sum of four"] = spot[parts].sum(axis=1)
    spot["residual"] = spot["ALL FOUR COMBINED"] - spot["sum of four"]

    rate = pd.DataFrame({
        n: {r: (c["dr"][r][YEAR] - base_c["dr"][r][YEAR]) * 1e4 for r in fxregs}
        for n, (c, _) in runs.items()}).rename_axis("region")
    rate["sum of four"] = rate[parts].sum(axis=1)
    rate["residual"] = rate["ALL FOUR COMBINED"] - rate["sum of four"]

    # ---- revenue and consumer prices --------------------------------------
    rows = {}
    for name, tau_ in list(shocks.items()) + [("ALL FOUR COMBINED", stack)]:
        rev = tariff.revenue(m, A, tau_)
        rev_i = tariff.revenue(m, A, tau_, include_final_demand=False)
        ct, _, _ = tariff.charges(m, A, tau_, 1.0)
        px = tariff.price_effect(m, Lt, ct, tau_)
        rows[name] = {"revenue_bn": rev / 1e3,
                      "intermediate_bn": rev_i / 1e3,
                      "px_USA_pct": px["USA"] * 100,
                      "px_EU27_pct": px["EU27"] * 100}
    rev = pd.DataFrame(rows).T.rename_axis("shock")
    rev.loc["sum of four"] = rev.loc[parts].sum()
    rev.loc["residual"] = rev.loc["ALL FOUR COMBINED"] - rev.loc["sum of four"]

    # ---- price-level decomposition: carbon vs each tariff -----------------
    # chain() adds the two into out["cum"]: a cumulative carbon price level
    # k*scope*(XCE_t - XCE_base), plus the tariff price effect from the dual.
    # Both are level effects in the same units, so they decompose additively.
    px = pd.DataFrame({
        name: tariff.price_effect(m, Lt, tariff.charges(m, A, t_, 1.0)[0], t_)
        for name, t_ in list(shocks.items()) + [("ALL FOUR COMBINED", stack)]
    }) * 100
    px = px.reindex(m.regions_order).rename_axis("region")
    px["tariffs total"] = px["ALL FOUR COMBINED"]
    for scen in (SCENARIO, "Net Zero 2050"):
        c = chain(m, sc, scen, M, scope, vl)
        px[f"carbon ({scen})"] = [c["cum"][r][YEAR] * 100 for r in px.index]
    px["carbon+tariff (CP)"] = px[f"carbon ({SCENARIO})"] + px["tariffs total"]
    px["carbon+tariff (NZ)"] = px["carbon (Net Zero 2050)"] + px["tariffs total"]

    gva.to_csv(f"{RESULTS}/out_stack_gva.csv", float_format="%.6f")
    spot.to_csv(f"{RESULTS}/out_stack_fx.csv", float_format="%.6f")
    rev.to_csv(f"{RESULTS}/out_stack_decomp.csv", float_format="%.6f")
    px.to_csv(f"{RESULTS}/out_stack_prices.csv", float_format="%.6f")

    pd.set_option("display.width", 200)
    print(f"\n=== revenue and consumer prices ({YEAR}, phi={PHI}, theta=1) ===")
    print(rev.round(3).to_string())
    print(f"\n=== GVA effect by region (%), {YEAR} ===")
    print(gva.round(4).to_string())
    print(f"\n=== spot FX vs EUR (%), {YEAR} ===")
    print(spot.round(4).to_string())
    print(f"\n=== policy-rate shift (bp), {YEAR} ===")
    print(rate.round(3).to_string())
    print(f"\n=== consumer price LEVEL (%), {YEAR}: carbon vs tariffs ===")
    print(px.round(4).to_string())
    print(f"\nmax |residual|  GVA {gva.residual.abs().max():.2e} pp   "
          f"spot {spot.residual.abs().max():.2e} pp   "
          f"rate {rate.residual.abs().max():.2e} bp")


if __name__ == "__main__":
    main()
