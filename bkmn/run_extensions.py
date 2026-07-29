"""
Extension orchestrator (docs/EXT_PLAN.md, Phases P/E/O/M/V).

Runs the full chain with the **physical channel switched on** alongside
transition, then the downstream market/macro channels, then wraps everything in
the scenario mixture and the volatility band:

    ΔY_r(t) = transition (per-region XCE)  +  physical (Ω(ΔT) via Prop 1)
            ─► Taylor Δr_r  ─► HW ΔR  ─► FX vs EUR   (spot PPP + CIP forward)
            ─► equity   ΔS/S = β_r·ΔY_r
            ─► op-risk  ΔU = κ_r·ΔY_r → loss shifts
    mixture  : E[X] and quantiles over NGFS scenarios (3 named priors)
    volatility: ±z·σ on temperature and carbon price → FX-at-risk band

Non-destructive: `bkmn/run_fx.py` and its transition-only `out_fx_*.csv` are
left untouched, so the transition-vs-physical comparison is available directly.

Usage: py -3 -m bkmn.run_extensions
"""
import os

import numpy as np
import pandas as pd

from . import equity, fx, macro, mixture, oprisk, physical, transition, volatility
from .regions import load
from .run_fx import BASE, HORIZONS, PHI, xce_annual
from .scenarios import Scenarios

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Which ΔT the damage function is fed (the paper is ambiguous, so make it explicit):
#   "incremental"    ΔT(t) = GSAT(t) − GSAT(2022) — warming *from today*. Consistent
#                    with §2.1 ("we only need to look at GDP damage from temperature
#                    increases"; market curves already embed pre-damage expectations),
#                    so the output is a shock relative to the market baseline.
#   "preindustrial"  ΔT(t) = GSAT(t) — the literal reading of Prop 1 ("temperature
#                    change, at t, relative to pre-industrial temperature"), which is
#                    also what Eq 13 telescopes to. This charges today's 1.29 K of
#                    warming as if it were a future shock, so damages are ~17x larger.
WARMING_BASELINE = "incremental"


def chain(m, sc, scenario, M, scope, vl, xce_over=None, dT_over=None,
          dynamic_scope=False):
    """
    One scenario -> all channel outputs (optionally with stressed inputs).

    `dynamic_scope` switches the inflation channel from the frozen 2025 coverage
    to coverage that expands with the scenario's own carbon price (macro.scope_at,
    the §2.6 ΔΩ_XCE reading). Sensitivity only — the headline uses static scope.
    """
    xce = xce_annual(sc, scenario) if xce_over is None else xce_over
    out = {k: {} for k in ("trans", "phys", "dY", "dPi", "dr", "cum")}

    def scope_of(r, year):
        return (macro.scope_at(scope[r], xce.loc[year, r]) if dynamic_scope
                else scope[r])

    for t in HORIZONS:
        tr = transition.region_gdp_shock(m, M, xce.loc[t].to_dict())
        if dT_over is not None:
            dT = dT_over[t]
        elif WARMING_BASELINE == "preindustrial":
            dT = float(sc.temp.loc[t, scenario])          # GSAT is already vs 1850-1900
        else:
            dT = sc.delta_T(scenario, t, BASE)
        ph = physical.region_damage(m, dT, vl)
        for r in m.regions_order:
            out["trans"].setdefault(r, {})[t] = tr[r]
            out["phys"].setdefault(r, {})[t] = ph[r]
            out["dY"].setdefault(r, {})[t] = tr[r] + ph[r]
            dpi = macro.inflation_dev(xce.loc[t, r] - xce.loc[t - 1, r],
                                      scope_of(r, t))
            out["dPi"].setdefault(r, {})[t] = dpi
            out["dr"].setdefault(r, {})[t] = macro.taylor_rate_shift(dpi, tr[r] + ph[r])
            # cumulative price-level effect: with static scope this telescopes to
            # k*scope*(XCE_t - XCE_base); with a moving scope it must be summed.
            if dynamic_scope:
                out["cum"].setdefault(r, {})[t] = sum(
                    macro.inflation_dev(xce.loc[u, r] - xce.loc[u - 1, r],
                                        scope_of(r, u))
                    for u in range(BASE + 1, t + 1))
            else:
                out["cum"].setdefault(r, {})[t] = (macro.INFL_PER_USD * scope[r]
                                                   * (xce.loc[t, r] - xce.loc[BASE, r]))
    return out


def derive(m, res, fxregs, betas, kap, u0):
    """FX / equity / op-risk from the macro chain."""
    d = {"spot": {}, "fwd5": {}, "equity": {}, "opConduct": {}, "opExecution": {}}
    for t in HORIZONS:
        gdp_t = {r: res["dY"][r][t] for r in m.regions_order}
        eq = equity.equity_shift(gdp_t, betas)
        op = oprisk.oprisk_shift(gdp_t, kap, u0)
        for r in m.regions_order:
            d["equity"].setdefault(r, {})[t] = eq[r]
            d["opConduct"].setdefault(r, {})[t] = op[r]["Conduct"]
            d["opExecution"].setdefault(r, {})[t] = op[r]["Execution"]
        for r in fxregs:
            d["spot"].setdefault(r, {})[t] = fx.spot_ppp(res["cum"][r][t],
                                                         res["cum"]["EU27"][t])
            d["fwd5"].setdefault(r, {})[t] = fx.forward_total(
                res["cum"][r][t], res["cum"]["EU27"][t],
                res["dr"][r][t], res["dr"]["EU27"][t], 5)
    return d


def table(per_scen, key, regs, scale):
    rows = {(s, r): {t: v[key][r][t] * scale for t in HORIZONS}
            for s, v in per_scen.items() for r in regs}
    df = pd.DataFrame(rows).T
    df.index = pd.MultiIndex.from_tuples(df.index, names=["scenario", "region"])
    return df[HORIZONS]


def main():
    m = load()
    sc = Scenarios(m.carbon_map)
    cm = m.carbon_map.set_index("region")
    scope, vl = cm.carbon_scope, physical.vl_vector(m)
    fxregs = [r for r in m.regions_order if cm.loc[r, "fx_role"] == "analytical"]
    M = transition.gva_operator(m, PHI)
    betas, kap, u0 = equity.betas(), oprisk.kappa(), oprisk.base_unemployment()
    print(f"extensions: physical+transition | {len(fxregs)} currencies | "
          f"{len(sc.names)} scenarios | φ={PHI}")

    chains = {s: chain(m, sc, s, M, scope, vl) for s in sc.names}
    dv = {s: derive(m, c, fxregs, betas, kap, u0) for s, c in chains.items()}

    # --- per-scenario channel tables ---------------------------------------
    allreg = m.regions_order
    table(chains, "trans", allreg, 100).to_csv(f"{ROOT}/out_ext_gdp_transition.csv")
    table(chains, "phys", allreg, 100).to_csv(f"{ROOT}/out_ext_gdp_physical.csv")
    table(chains, "dY", allreg, 100).to_csv(f"{ROOT}/out_ext_gdp_total.csv")
    table(chains, "dr", allreg, 1e4).to_csv(f"{ROOT}/out_ext_rate_shift.csv")
    spot = table(dv, "spot", fxregs, 100)
    fwd = table(dv, "fwd5", fxregs, 100)
    spot.to_csv(f"{ROOT}/out_ext_fx_spot.csv")
    fwd.to_csv(f"{ROOT}/out_ext_fx_forward_5y.csv")
    table(dv, "equity", allreg, 100).to_csv(f"{ROOT}/out_ext_equity.csv")
    table(dv, "opConduct", allreg, 100).to_csv(f"{ROOT}/out_ext_oprisk_conduct.csv")
    table(dv, "opExecution", allreg, 100).to_csv(f"{ROOT}/out_ext_oprisk_execution.csv")

    # --- Phase M: mixture over scenarios ------------------------------------
    for prior in mixture.PRIORS:
        mixture.expected(fwd, prior).to_csv(f"{ROOT}/out_ext_fx_expected_{prior}.csv")
    mixture.quantile(fwd, 0.95, "uniform").to_csv(f"{ROOT}/out_ext_fx_q95_scen.csv")

    # --- Sensitivity: scenario drift under the Eq-1 transition matrix --------
    # NOT part of the headline: it needs two assumptions the static mixture does
    # not (λ, and a distance metric over narratives). See docs/PAPER_AUDIT.md §E.
    coords = sc.coords()
    for lam in (5.0, 2.0, 0.5):
        for prior in mixture.PRIORS:
            mixture.expected_drift(fwd, coords, prior, lam=lam, base_year=BASE) \
                   .to_csv(f"{ROOT}/out_sens_fx_drift_{prior}_lam{lam:g}.csv")

    # --- Sensitivity: dynamic carbon-pricing scope (§2.6 dOmega reading) -----
    dyn = {s_: derive(m, chain(m, sc, s_, M, scope, vl, dynamic_scope=True),
                      fxregs, betas, kap, u0) for s_ in sc.names}
    table(dyn, "spot", fxregs, 100).to_csv(f"{ROOT}/out_sens_fx_spot_dynscope.csv")
    table(dyn, "fwd5", fxregs, 100).to_csv(f"{ROOT}/out_sens_fx_forward_dynscope.csv")

    # --- Phase V: volatility band (95th pct of inputs, Net Zero) -------------
    tsig, psig = volatility.temperature_sigma(), volatility.carbon_price_sigma()
    s = "Net Zero 2050"
    z = 1.6448536269514722                                    # Φ⁻¹(0.95)
    xce_hi = xce_annual(sc, s).copy()
    for r in m.regions_order:
        zone = sc._zone(r)
        if (s, zone) in psig.columns:
            xce_hi[r] = volatility.stress(xce_hi[r], psig[(s, zone)], z)
    dT_hi = {t: sc.delta_T(s, t, BASE) + z * float(tsig.loc[t, s] - tsig.loc[BASE, s])
             for t in HORIZONS}
    hi = derive(m, chain(m, sc, s, M, scope, vl, xce_hi, dT_hi), fxregs, betas, kap, u0)
    table({s: hi}, "fwd5", fxregs, 100).to_csv(f"{ROOT}/out_ext_fx_forward_q95.csv")

    # --- report --------------------------------------------------------------
    pd.set_option("display.width", 200, "display.float_format", lambda v: f"{v:7.2f}")
    tr40 = table(chains, "trans", allreg, 100)
    ph40 = table(chains, "phys", allreg, 100)
    print("\n=== transition vs physical GDP shock (%), 2040 ===")
    cmp = pd.DataFrame({
        "trans NZ": tr40.xs("Net Zero 2050", level=0)[2040],
        "phys NZ": ph40.xs("Net Zero 2050", level=0)[2040],
        "trans CP": tr40.xs("Current Policies", level=0)[2040],
        "phys CP": ph40.xs("Current Policies", level=0)[2040]})
    print(cmp.round(2).to_string())
    print("\n=== 5y-forward FX vs EUR (%), 2040, Net Zero ===")
    print(fwd.xs("Net Zero 2050", level=0)[2040].sort_values().to_string())
    print("\nsaved: out_ext_*.csv (channels, mixture x3 priors, q95 band)")


if __name__ == "__main__":
    main()
