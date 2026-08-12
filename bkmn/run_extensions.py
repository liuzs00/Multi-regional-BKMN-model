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

from . import (cbam, credit, equity, fx, macro, mixture, oprisk, physical,
               rates, tariff, transition, volatility)
from .regions import load
from .run_fx import (BASE, CONSISTENT_INTENSITY, HORIZONS, OPRISK_INPUT, PHI,
                     TAYLOR_OUTPUT_GAP, warming, xce_annual)
from .scenarios import Scenarios

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The warming baseline and the Taylor output-gap choice live in run_fx.py,
# which this module imports, so the two orchestrators cannot diverge.

# Rate tenors reported, mirroring the paper's Table 11 (Deposit 1D/6M, Swap 1Y..20Y).
RATE_TENORS = {"1D": 1 / 365, "6M": 0.5, "1Y": 1.0, "5Y": 5.0, "10Y": 10.0, "20Y": 20.0}


def chain(m, sc, scenario, M, scope, vl, xce_over=None, dT_over=None,
          dynamic_scope=False, tau=None, theta=1.0, Ltilde=None, A=None):
    """
    One scenario -> all channel outputs (optionally with stressed inputs).

    `dynamic_scope` switches the inflation channel from the frozen 2025 coverage
    to coverage that expands with the scenario's own carbon price (macro.scope_at,
    the §2.6 ΔΩ_XCE reading). Sensitivity only — the headline uses static scope.
    """
    xce = xce_annual(sc, scenario) if xce_over is None else xce_over
    out = {k: {} for k in ("trans", "phys", "dY", "dPi", "dr", "cum", "tariff",
                           "credit")}

    # A tariff is the same object as the carbon charge - an ad-valorem cost wedge
    # in the same units - so it is ADDED TO ct and inherits the whole downstream
    # chain (Taylor -> HW -> FX, equity, op-risk) rather than being computed on
    # the side.  Its price effect comes from the dual (tariff.price_effect); the
    # Moessner relation is carbon-specific and cannot be reused.
    if tau is not None:
        ct_tar, _, _ = tariff.charges(m, A, tau, theta)
        tar_shock = transition.region_shock_from_ct(m, M, ct_tar)
        tar_price = tariff.price_effect(m, Ltilde, ct_tar, tau)
    else:
        ct_tar = None
        tar_shock = {r: 0.0 for r in m.regions_order}
        tar_price = {r: 0.0 for r in m.regions_order}

    def scope_of(r, year):
        return (macro.scope_at(scope[r], xce.loc[year, r]) if dynamic_scope
                else scope[r])

    for t in HORIZONS:
        fac = (sc.intensity_factor(scenario, t)
               if CONSISTENT_INTENSITY else None)
        tr = transition.region_gdp_shock(m, M, xce.loc[t].to_dict(), fac)
        dT = dT_over[t] if dT_over is not None else warming(sc, scenario, t)
        ph = physical.region_damage(m, dT, vl)
        # Credit (2.9, CDS half) needs the SECTOR shock, not the regional
        # aggregate, because a CDS index is a weighted basket of sectors.  Both
        # the carbon charge and the physical cascade reach it: the charge
        # through ct, the damage through Prop 1's VL*alpha add-on, which is the
        # form the reference uses for its market channel.
        ct_all = transition.ct_direct(m, xce.loc[t].to_dict(), fac)
        if ct_tar is not None:
            ct_all = ct_all + ct_tar
        ct_all = ct_all + physical.tax_addon(m, dT, vl)
        for r, d in credit.credit_shift(m, M, ct_all).items():
            out["credit"].setdefault(r, {})[t] = d
        for r in m.regions_order:
            out["trans"].setdefault(r, {})[t] = tr[r]
            out["phys"].setdefault(r, {})[t] = ph[r]
            out["tariff"].setdefault(r, {})[t] = tar_shock[r]
            out["dY"].setdefault(r, {})[t] = tr[r] + ph[r] + tar_shock[r]
            dpi = macro.inflation_dev(xce.loc[t, r] - xce.loc[t - 1, r],
                                      scope_of(r, t))
            out["dPi"].setdefault(r, {})[t] = dpi
            # 2.7's output gap is -Omega: the damage function, not the carbon
            # or tariff charge, which are tax wedges rather than lost output.
            gap = (ph[r] if TAYLOR_OUTPUT_GAP == "physical"
                   else tr[r] + ph[r] + tar_shock[r])
            out["dr"].setdefault(r, {})[t] = macro.taylor_rate_shift(dpi, gap)
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
            out["cum"][r][t] += tar_price[r]
    return out


def derive(m, res, fxregs, betas, kap, u0):
    """FX / equity / op-risk from the macro chain."""
    d = {"spot": {}, "fwd5": {}, "equity": {}, "opConduct": {}, "opExecution": {}}
    for t in HORIZONS:
        gdp_t = {r: res["dY"][r][t] for r in m.regions_order}
        # Equity takes the TOTAL shock: a tax wedge still reduces the value
        # added accruing to firms.  Op-risk takes the physical shock only:
        # Okun's law maps real output to employment, and a wedge destroys no
        # output.  See OPRISK_INPUT in run_fx.py.
        op_t = ({r: res["phys"][r][t] for r in m.regions_order}
                if OPRISK_INPUT == "physical" else gdp_t)
        eq = equity.equity_shift(gdp_t, betas)
        op = oprisk.oprisk_shift(op_t, kap, u0)
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

    # --- 2.9 credit: CDS spread shift, scenario x region x index -------------
    crows = {}
    for s_, c in chains.items():
        for r in allreg:
            for idx in credit.CDS_SECTORS:
                crows[(s_, r, idx)] = {t: c["credit"][r][t][idx] * 100
                                       for t in HORIZONS}
    cdf = pd.DataFrame(crows).T
    cdf.index.names = ["scenario", "region", "index"]
    cdf.to_csv(f"{ROOT}/out_ext_credit_spread.csv")

    # --- §2.8 long-rate term structure (Prop 2), paper Table 11 layout -------
    rows = {}
    for s_, c in chains.items():
        for r in allreg:
            for lbl, tau in RATE_TENORS.items():
                rows[(s_, r, lbl)] = {
                    t: float(rates.zero_rate_shift(c["dr"][r][t], tau)) * 1e4
                    for t in HORIZONS}
    rt = pd.DataFrame(rows).T
    rt.index = pd.MultiIndex.from_tuples(rt.index,
                                        names=["scenario", "region", "tenor"])
    rt[HORIZONS].to_csv(f"{ROOT}/out_ext_rate_term_structure.csv")

    # --- Phase M: mixture over scenarios ------------------------------------
    # `consensus` is the citable prior (UNEP/CAT current-policy warming anchor);
    # the other three are uninformative + asserted bookends.
    #
    # The mixture is applied to EVERY channel, not only FX.  A per-scenario table
    # is a component of the answer; the expectation over the scenario
    # distribution is the answer, and reporting one narrative as though it were
    # the result overstates the transition channel by a factor of 37 (Net Zero
    # against Current Policies).  Expectation is linear, so E[X] over scenarios
    # commutes with every downstream transform that is itself linear.
    priors = dict(mixture.PRIORS)
    priors["consensus"] = mixture.consensus_shape(sc.coords())
    channels = {
        "fx_forward": fwd, "fx_spot": spot,
        "gdp_transition": table(chains, "trans", allreg, 100),
        "gdp_physical": table(chains, "phys", allreg, 100),
        "gdp_total": table(chains, "dY", allreg, 100),
        "rate": table(chains, "dr", allreg, 1e4),
        "inflation": table(chains, "dPi", allreg, 1e4),
        "equity": table(dv, "equity", allreg, 100),
        "oprisk_conduct": table(dv, "opConduct", allreg, 100),
        "credit": cdf,
        "rate_term_structure": rt[HORIZONS],
    }
    for prior, shape in priors.items():
        for name, tbl in channels.items():
            mixture.expected(tbl, shape).to_csv(
                f"{ROOT}/out_mix_{name}_{prior}.csv")
        # keep the legacy FX filename, which the figures and docs already use
        mixture.expected(fwd, shape).to_csv(
            f"{ROOT}/out_ext_fx_expected_{prior}.csv")
    mixture.quantile(fwd, 0.95, "uniform").to_csv(f"{ROOT}/out_ext_fx_q95_scen.csv")
    pd.DataFrame({p: mixture.weights(s, scenarios=list(sc.names))
                  for p, s in priors.items()}).to_csv(f"{ROOT}/out_mix_weights.csv")

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

    # --- Tariff shocks carried through to FX (project stretch goal) ----------
    # Same chain as the carbon tax: tariff -> ct -> GVA + prices -> Taylor -> FX.
    Lt = transition.price_operator(m, PHI)
    MFG = ["C10T12", "C13T15", "C16", "C17_18", "C19", "C20", "C21", "C22",
           "C23", "C24A", "C24B", "C25", "C26", "C27", "C28", "C29", "C301",
           "C302T309", "C31T33"]
    A_ = transition.technical_matrix(m)
    applied_ = cm.applied_price_usd.to_dict()
    # Calibrated to observed policy: Penn Wharton Budget Model (13 Jul 2026)
    # reports a US average effective tariff rate of 7.2% as of May 2026, with
    # China the highest major partner at 23.4%.  With China at 14.7% of US
    # imports in this table, those two pin the residual rate on other origins at
    # 4.4% (0.147*23.4 + 0.853*4.4 = 7.2).  [DATA]
    us_2026 = tariff.add_rule(m, tariff.empty(m), 0.044, destination="USA")
    us_2026 = tariff.add_rule(m, us_2026, 0.234 - 0.044, origin="CHN",
                              destination="USA")
    # EU steel safeguard, Regulation (EU) 2026/1384, applying from 1 Jul 2026:
    # the out-of-quota duty doubles to 50% and the tariff-free quota falls to
    # 18.3 Mt.  A tariff-rate quota is not an ad-valorem rate, so it is converted
    # to the average rate paid on the flow: 50% times the share of imports that
    # exceed quota.  EUROFER puts 2025 EU steel imports near 30 Mt, which leaves
    # about 39% above the new quota and an average rate of ~19.5%.  Under the
    # model's fixed demand nothing re-sources, so this is an upper bound: the
    # measure's purpose is to push imports back toward the quota, which would cut
    # the out-of-quota share and hence the average rate.  Swept below.  [ESTIMATE]
    STEEL_ABOVE_QUOTA = 0.39
    eu_steel = tariff.add_rule(m, tariff.empty(m), 0.50 * STEEL_ABOVE_QUOTA,
                               destination="EU27", industries=["C24A"])
    # EU-US framework in force 1 Jul 2026: the US caps most EU goods at an
    # all-inclusive 15%, and the EU eliminates tariffs on US industrial goods.
    # Schedules here are increments from a zero-tariff baseline, so the EU-side
    # liberalisation enters as a NEGATIVE wedge equal to the MFN rate it removes
    # (World Bank weighted applied mean for the EU, 1.33%).  [DATA/ESTIMATE]
    eu_us = tariff.add_rule(m, tariff.empty(m), 0.15, origin="EU27",
                            destination="USA")
    eu_us = tariff.add_rule(m, eu_us, -0.0133, origin="USA",
                            destination="EU27", industries=MFG)
    SHOCKS = {
        "CBAM (EU, applied prices)": cbam.schedule(m, applied_),
        "US applied tariffs, May 2026": us_2026,
        "EU-US framework, Jul 2026": eu_us,
        "EU steel safeguard 2026/1384": eu_steel,
        "USA 25% on CHN manufactures":
            tariff.add_rule(m, tariff.empty(m), 0.25, origin="CHN",
                            destination="USA", industries=MFG),
        "Global 10% on all imports": tariff.add_rule(m, tariff.empty(m), 0.10),
    }
    # Report the tariff's INCREMENTAL effect: the same scenario with and without
    # the schedule, differenced, so the underlying carbon baseline cancels.
    base_c = chain(m, sc, "Current Policies", M, scope, vl)
    base_d = derive(m, base_c, fxregs, betas, kap, u0)
    fxrows, gvarows = {}, {}
    for name, tau_ in SHOCKS.items():
        c = chain(m, sc, "Current Policies", M, scope, vl, tau=tau_, theta=1.0,
                  Ltilde=Lt, A=A_)
        d = derive(m, c, fxregs, betas, kap, u0)
        for r in fxregs:
            fxrows[(name, r)] = {
                "spot_pct": (d["spot"][r][2040] - base_d["spot"][r][2040]) * 100,
                "fwd5y_pct": (d["fwd5"][r][2040] - base_d["fwd5"][r][2040]) * 100,
                "rate_bp": (c["dr"][r][2040] - base_c["dr"][r][2040]) * 1e4}
        for r in allreg:
            gvarows[(name, r)] = {"gva_pct": c["tariff"][r][2040] * 100}
    pd.DataFrame(fxrows).T.rename_axis(["shock", "region"]).to_csv(
        f"{ROOT}/out_sens_tariff_fx.csv")
    pd.DataFrame(gvarows).T.rename_axis(["shock", "region"]).to_csv(
        f"{ROOT}/out_sens_tariff_gva.csv")

    # --- Sensitivity: CBAM as a carbon tariff (project stretch goal) ---------
    # Needs no new data: MRIO gives bilateral trade, CARBON_INTENSITY gives
    # embodied carbon by origin, region_carbon_map gives the price already paid.
    A = transition.technical_matrix(m)
    applied = cm.applied_price_usd.to_dict()
    rows, sect = {}, {}
    for label, prices in [("applied-divergence", applied),
                          ("ngfs-uniform", sc.xce_by_region("Net Zero 2050", 2040).to_dict())]:
        for theta in (1.0, 0.5, 0.0):
            tot, imp, exp = cbam.charges(m, A, prices, theta=theta)
            dV = m.x * (M @ tot)
            rows[(label, f"theta={theta:g}")] = {
                **{r: dV[m.region_of == r].sum() / m.gva[m.region_of == r].sum() * 100
                   for r in allreg},
                "revenue_bn": cbam.revenue(m, A, prices) / 1e3}
    pd.DataFrame(rows).T.rename_axis(["prices", "incidence"]).to_csv(
        f"{ROOT}/out_sens_cbam_gva.csv")
    # ad-valorem rates by origin x covered sector
    tau = cbam.tariff_rate(m, applied)
    cov = [k for k in range(len(tau)) if m.industry_of[k] in cbam.COVERED
           and m.region_of[k] != cbam.BASE_REGION]
    pd.DataFrame({"region": [m.region_of[k] for k in cov],
                  "industry": [m.industry_of[k] for k in cov],
                  "carbon_intensity_t_per_musd": [m.ci[k] for k in cov],
                  "cbam_rate_pct": [tau[k] * 100 for k in cov]})       .sort_values("cbam_rate_pct", ascending=False)       .to_csv(f"{ROOT}/out_sens_cbam_rates.csv", index=False)

    # --- Phase V: volatility band (95th pct of inputs, Net Zero) -------------
    # Stress every narrative, not just Net Zero: the chapter reports the tail
    # as a mixture like everything else, and a tail computed on one scenario
    # cannot be weighted against a central case computed on seven.
    tsig, psig = volatility.temperature_sigma(), volatility.carbon_price_sigma()
    z = 1.6448536269514722                                    # Φ⁻¹(0.95)
    his = {}
    for s in sc.names:
        xce_hi = xce_annual(sc, s).copy()
        for r in m.regions_order:
            zone = sc._zone(r)
            if (s, zone) in psig.columns:
                xce_hi[r] = volatility.stress(xce_hi[r], psig[(s, zone)], z)
        # `warming`, NOT sc.delta_T(..., BASE): the damage function is evaluated
        # on the pre-industrial level (WARMING_BASELINE in run_fx), and the
        # central path uses that.  Building the stressed path off the 2022 base
        # instead fed the damage function ~0.2 K where the central run sees
        # ~1.5 K and, since Omega is quadratic, made the "stressed" run milder
        # than the central one -- the tail was inverted for the physical leg.
        dT_hi = {t: warming(sc, s, t)
                 + z * float(tsig.loc[t, s] - tsig.loc[BASE, s])
                 for t in HORIZONS}
        his[s] = derive(m, chain(m, sc, s, M, scope, vl, xce_hi, dT_hi),
                        fxregs, betas, kap, u0)
    q95 = table(his, "fwd5", fxregs, 100)
    q95.to_csv(f"{ROOT}/out_ext_fx_forward_q95.csv")
    # the spot leg too: the stress perturbs the carbon price and the temperature
    # at once, and those reach the forward through different terms, so the two
    # legs are needed to say which one drives the tail under a given narrative
    q95s = table(his, "spot", fxregs, 100)
    q95s.to_csv(f"{ROOT}/out_ext_fx_spot_q95.csv")
    for prior in priors:
        mixture.expected(q95, priors[prior]).to_csv(
            f"{ROOT}/out_mix_fx_forward_q95_{prior}.csv")
        mixture.expected(q95s, priors[prior]).to_csv(
            f"{ROOT}/out_mix_fx_spot_q95_{prior}.csv")

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
