"""
Phase 3 — FX orchestrator.

For each NGFS scenario and horizon year it runs the full chain
    XCE_r(t)  ─► transition GDP shock ΔY_r(t)      (bkmn.transition)
    ΔXCE_r(t) ─► inflation deviation ΔΠ_r(t)       (bkmn.macro)
              ─► Taylor short-rate shift Δr_r(t)   (bkmn.macro)
              ─► FX vs EUR: spot (PPP) + forward points (CIP)   (bkmn.fx)
and writes the result tables.  φ = 0.5, base year 2022.

Outputs (out_fx_*.csv), rows = (scenario, region), cols = horizon year:
  out_fx_spot_ppp.csv       spot FX log-shift vs EUR (%)   [+ = depreciates vs EUR]
  out_fx_forward_5y.csv     total 5y forward FX shift (%)  (spot + CIP points)
  out_rate_shift.csv        Taylor short-rate shift (bp)
  out_inflation_shift.csv   annual inflation deviation (bp)
  out_gdp_shock_fx.csv      transition GDP shock (%)

Usage: py -3 -m bkmn.run_fx
"""
import os

import numpy as np
import pandas as pd

from . import fx, macro, transition
from .regions import load
from .scenarios import Scenarios

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 2022
HORIZONS = [2025, 2030, 2035, 2040, 2045]
TENORS = [1, 5, 10]
PHI = 0.5
HEADLINE = ["Net Zero 2050", "Delayed transition",
            "Nationally Determined Contributions (NDCs)", "Current Policies"]


def xce_annual(sc, scenario):
    """DataFrame index=year, columns=region — per-region carbon price ($2022/t)."""
    zones = {r: sc._zone(r) for r in sc.cm.index}
    px = sc.px[scenario]
    return pd.DataFrame({r: px[zones[r]].values for r in sc.cm.index},
                        index=px.index)


def run_scenario(m, sc, scenario, M, scope, fxregs):
    xce = xce_annual(sc, scenario)
    dr, dPi, dY, cum = {}, {}, {}, {}
    for t in HORIZONS:
        gdp = transition.region_gdp_shock(m, M, xce.loc[t].to_dict())
        for r in m.regions_order:
            dY.setdefault(r, {})[t] = gdp[r]
            dpi = macro.inflation_dev(xce.loc[t, r] - xce.loc[t - 1, r], scope[r])
            dPi.setdefault(r, {})[t] = dpi
            dr.setdefault(r, {})[t] = macro.taylor_rate_shift(dpi, gdp[r])
            cum.setdefault(r, {})[t] = macro.INFL_PER_USD * scope[r] * \
                (xce.loc[t, r] - xce.loc[BASE, r])

    spotfx = {r: {t: fx.spot_ppp(cum[r][t], cum["EU27"][t]) for t in HORIZONS}
              for r in fxregs}
    fwd5 = {r: {t: fx.forward_total(cum[r][t], cum["EU27"][t],
                                    dr[r][t], dr["EU27"][t], 5) for t in HORIZONS}
            for r in fxregs}
    return dict(dr=dr, dPi=dPi, dY=dY, spotfx=spotfx, fwd5=fwd5)


def _tbl(results, key, regs, scale):
    rows = {}
    for sc_name, res in results.items():
        for r in regs:
            rows[(sc_name, r)] = {t: res[key][r][t] * scale for t in HORIZONS}
    df = pd.DataFrame(rows).T
    df.index = pd.MultiIndex.from_tuples(df.index, names=["scenario", "region"])
    return df[HORIZONS]


def main():
    m = load()
    sc = Scenarios(m.carbon_map)
    cm = m.carbon_map.set_index("region")
    scope = cm.carbon_scope
    fxregs = [r for r in m.regions_order if cm.loc[r, "fx_role"] == "analytical"]
    M = transition.gva_operator(m, PHI)                 # one inversion
    print(f"FX model: {len(fxregs)} currencies vs EUR | φ={PHI} | base {BASE} | "
          f"scenarios {len(sc.names)}")

    results = {s: run_scenario(m, sc, s, M, scope, fxregs) for s in sc.names}

    _tbl(results, "spotfx", fxregs, 100).to_csv(f"{ROOT}/out_fx_spot_ppp.csv")
    _tbl(results, "fwd5", fxregs, 100).to_csv(f"{ROOT}/out_fx_forward_5y.csv")
    _tbl(results, "dr", m.regions_order, 1e4).to_csv(f"{ROOT}/out_rate_shift.csv")
    _tbl(results, "dPi", m.regions_order, 1e4).to_csv(f"{ROOT}/out_inflation_shift.csv")
    _tbl(results, "dY", m.regions_order, 100).to_csv(f"{ROOT}/out_gdp_shock_fx.csv")

    pd.set_option("display.width", 200, "display.float_format", lambda v: f"{v:6.2f}")
    for s in HEADLINE:
        if s not in results:
            continue
        sp = _tbl({s: results[s]}, "spotfx", fxregs, 100).loc[s]
        print(f"\n=== Spot FX vs EUR (%), {s}  [+ = depreciates vs EUR] ===")
        print(sp.sort_values(2040).to_string())
    print("\nsaved: out_fx_spot_ppp.csv, out_fx_forward_5y.csv, out_rate_shift.csv,"
          " out_inflation_shift.csv, out_gdp_shock_fx.csv")


if __name__ == "__main__":
    main()
