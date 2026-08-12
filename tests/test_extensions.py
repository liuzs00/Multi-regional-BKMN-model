"""
Validation gates for the extension phases (docs/EXT_PLAN.md).
Run: py -3 tests/test_extensions.py
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from bkmn import equity, mixture, oprisk, physical, transition, volatility  # noqa: E402
from bkmn.regions import load                                              # noqa: E402
from bkmn.scenarios import Scenarios                                       # noqa: E402

m = load()
n = 0


def check(name, cond, detail=""):
    global n
    assert cond, f"FAIL: {name}  {detail}"
    n += 1
    print(f"  PASS  {name}  {detail}")


# --- Phase P: physical risk --------------------------------------------------
vl = physical.vl_vector(m)
check("VL positive & finite", np.all(vl > 0) and np.all(np.isfinite(vl)),
      f"range {vl.min():.2f}-{vl.max():.2f}")
# Eq 11 anchor: the damage function is DEFINED by 1.6768% of GDP at 2.2 C
check("Omega(2.2C) = 1.6768% of GDP (Eq 11 anchor)",
      abs(physical.omega(2.2) - 0.016768) < 1e-12,
      f"Omega(2.2) = {physical.omega(2.2)*100:.4f}%")
# paper quotes 0.003467 in Eq 13; 1.6768e-2/2.2^2 = 0.0034645 (their rounding)
check("damage coefficient ~ 0.003467 (Eq 13)",
      abs(physical.DAMAGE_COEF - 0.003467) < 1e-5,
      f"coef = {physical.DAMAGE_COEF:.6f} vs paper 0.003467")
check("ΔT=0 gives zero damage",
      max(abs(v) for v in physical.region_damage(m, 0.0, vl).values()) == 0.0)

# Prop-1 allocation identity: Σ_i f_i·VL_i·α = Ω(ΔT)
for dT in (0.5, 1.5, 3.0):
    f = m.gva / m.gva.sum()
    lhs = float(np.dot(f, -physical.direct_shock(m, dT, vl)))
    check(f"Prop-1 identity ΔT={dT}", abs(lhs - physical.omega(dT)) < 1e-15,
          f"|Δ|={abs(lhs - physical.omega(dT)):.1e}")

d1, d2 = physical.region_damage(m, 1.0, vl), physical.region_damage(m, 2.0, vl)
check("damage monotone in ΔT", all(d2[r] < d1[r] < 0 for r in m.regions_order))
check("vulnerable regions hit harder", d1["AFR"] < d1["CHE"],
      f"AFR {d1['AFR']*100:.2f}% < CHE {d1['CHE']*100:.2f}%")

# --- 2.8 long-rate term structure (Prop 2) -----------------------------------
from bkmn import rates as _rates                                            # noqa: E402
_rt = pd.read_csv(f"{ROOT}/out_ext_rate_term_structure.csv", index_col=[0, 1, 2])
_dr = pd.read_csv(f"{ROOT}/out_ext_rate_shift.csv", index_col=[0, 1])
_k = ("Net Zero 2050", "EU27")
check("term-structure 1D shift equals the short-rate shift",
      abs(_rt.loc[_k + ("1D",), "2040"] - _dr.loc[_k, "2040"]) < 0.5,
      f"{_rt.loc[_k+('1D',),'2040']:.1f} vs {_dr.loc[_k,'2040']:.1f} bp")
_ten = ["1D", "6M", "1Y", "5Y", "10Y", "20Y"]
_v = [abs(_rt.loc[_k + (t,), "2040"]) for t in _ten]
check("shift decays monotonically with tenor (Prop 2)",
      all(a >= b - 1e-9 for a, b in zip(_v, _v[1:])),
      " > ".join(f"{x:.0f}" for x in _v))
_ratio = _rt.loc[_k + ("20Y",), "2040"] / _rt.loc[_k + ("1D",), "2040"]
_theory = float(_rates.hw_B(20.0)) / 20.0
check("20Y/1D ratio matches B(20)/20 exactly",
      abs(_ratio - _theory) < 2e-3, f"{_ratio:.4f} vs {_theory:.4f}")

# --- Phase E: equity ---------------------------------------------------------
b = equity.betas()
check("betas positive for every region",
      len(b) == len(m.regions_order) and all(v > 0 for v in b.values()),
      f"{len(b)} regions")
eq = equity.equity_shift({r: -0.05 for r in m.regions_order}, b)
check("ΔY<0 ⇒ equity falls", all(v < 0 for v in eq.values()))

# --- Phase O: op-risk --------------------------------------------------------
kap, u0 = oprisk.kappa(), oprisk.base_unemployment()
check("κ negative, U positive", all(kap[r] < 0 for r in m.regions_order)
      and all(u0[r] > 0 for r in m.regions_order))
dU = oprisk.unemployment_change({r: -0.05 for r in m.regions_order}, kap)
check("ΔY<0 ⇒ unemployment rises", all(v > 0 for v in dU.values()))
op = oprisk.oprisk_shift({r: -0.05 for r in m.regions_order}, kap, u0)
check("⇒ op-risk losses rise", all(v["Conduct"] > 0 and v["Execution"] > 0
                                   for v in op.values()))

# --- Sensitivity: dynamic carbon-pricing scope -------------------------------
from bkmn import macro as _macro                                            # noqa: E402
check("scope_at is identity at zero carbon price",
      _macro.scope_at(0.3, 0.0) == 0.3)
check("scope_at bounded in [scope0, 1]",
      all(s0 <= _macro.scope_at(s0, x) <= 1.0
          for s0 in (0.0, 0.3, 0.82) for x in (0, 50, 100, 400)))
check("scope_at monotone in the carbon price",
      all(_macro.scope_at(0.2, a) <= _macro.scope_at(0.2, b)
          for a, b in [(0, 10), (10, 100), (100, 400)]))
check("zero-scope regions are no longer indistinguishable",
      abs(pd.read_csv(f"{ROOT}/out_sens_fx_spot_dynscope.csv", index_col=[0, 1])
          .xs("Net Zero 2050", level=0).loc["IND", "2040"]
          - pd.read_csv(f"{ROOT}/out_sens_fx_spot_dynscope.csv", index_col=[0, 1])
          .xs("Net Zero 2050", level=0).loc["TUR", "2040"]) > 1e-4,
      "IND vs TUR differ under dynamic scope (identical under static)")

# --- Phase M: mixture --------------------------------------------------------
tbl = pd.read_csv(f"{ROOT}/out_ext_fx_forward_5y.csv", index_col=[0, 1])
tbl.columns = [int(c) for c in tbl.columns]
scen = list(tbl.index.get_level_values(0).unique())
for prior in mixture.PRIORS:
    w = mixture.weights(prior, scenarios=scen)
    check(f"weights sum to 1 [{prior}]", abs(sum(w.values()) - 1) < 1e-12)
conc = {p: sum(mixture.PRIORS[p].values()) for p in mixture.PRIORS}
check("priors share one concentration Σα",
      max(conc.values()) - min(conc.values()) < 1e-9,
      f"Σα = {mixture.ALPHA0} for all {len(conc)} priors")
ev = {"Current Policies": 3}
for p in mixture.PRIORS:
    w0, w1 = mixture.weights(p), mixture.weights(p, ev)
    assert w1["Current Policies"] > w0["Current Policies"], p
check("event counts shift the posterior toward the counted scenario",
      True, "+3 Current Policies raises its weight under all priors")

# every scenario present in a result table must receive strictly positive
# weight — this catches a label mismatch silently dropping a scenario
for prior in mixture.PRIORS:
    w = mixture.weights(prior, scenarios=scen)
    assert len(w) == 7 and all(v > 0 for v in w.values()), (prior, w)
check("all 7 scenarios carry positive weight in the mixture", True,
      "guards against label drift, e.g. 'Below 2?C' vs 'Below 2°C'")

# consensus prior: citable anchor (UNEP/CAT current-policy warming)
from bkmn.scenarios import Scenarios as _Sc                                 # noqa: E402
_co = _Sc(m.carbon_map).coords()
_cshape = mixture.consensus_shape(_co)
check("consensus prior has the same concentration as the others",
      abs(sum(_cshape.values()) - mixture.ALPHA0) < 1e-9,
      f"Sigma-alpha = {sum(_cshape.values()):.1f}")
_cw = mixture.weights(_cshape, scenarios=scen)
_tmax = max(_co["T"].items(), key=lambda kv: kv[1])[0]
check("consensus puts most weight on the scenario nearest the 2.7C anchor",
      max(_cw, key=_cw.get) == _tmax,
      f"{_tmax[:14]} at {_cw[_tmax]*100:.1f}% (T2100 = {_co.loc[_tmax,'T']:.2f}C)")
check("consensus weight falls monotonically with distance from the anchor",
      all(b <= a + 1e-12 for a, b in zip(
          [_cw[s] for s in _co.assign(d=(_co["T"] - mixture.CONSENSUS_T).abs())
                          .sort_values("d").index],
          [_cw[s] for s in _co.assign(d=(_co["T"] - mixture.CONSENSUS_T).abs())
                          .sort_values("d").index][1:])))

one = {s: (1 if s == "Net Zero 2050" else 0) for s in scen}
deg = mixture.expected(tbl, one)
check("degenerate prior reproduces scenario",
      np.allclose(deg.to_numpy(float), tbl.xs("Net Zero 2050", level=0).to_numpy(float)))
e = mixture.expected(tbl, "uniform")
lo = tbl.groupby(level=1).min().reindex(e.index)[e.columns]
hi = tbl.groupby(level=1).max().reindex(e.index)[e.columns]
check("E[X] within scenario range",
      bool(((e >= lo - 1e-9) & (e <= hi + 1e-9)).all().all()))

# --- Sensitivity: Eq-1 transition matrix -------------------------------------
_scen, _Q = mixture.transition_matrix(_co, 2.0)
check("Q rows are probabilities", np.allclose(_Q.sum(1), 1) and (_Q >= 0).all(),
      f"{_Q.shape[0]}x{_Q.shape[1]}")
check("Q diagonal is the mode (staying is likeliest)",
      all(_Q[i, i] == _Q[i].max() for i in range(len(_scen))))
_d = mixture.expected_drift(tbl, _co, "ambition", lam=500.0, base_year=2022)
_s0 = mixture.expected(tbl, "ambition")
check("lambda -> inf reproduces the static mixture",
      float((_d - _s0).abs().to_numpy().max()) < 1e-12,
      "drift collapses to Q = I")
_p = mixture.drifted_weights("ambition", _co, 18, 2.0)
check("drifted weights still sum to 1", abs(sum(_p.values()) - 1) < 1e-12)

# --- CBAM sensitivity ---------------------------------------------------------
from bkmn import cbam as _cb                                                # noqa: E402
_A = transition.technical_matrix(m)
_ap = m.carbon_map.set_index("region").applied_price_usd.to_dict()
_tau = _cb.tariff_rate(m, _ap)
check("CBAM rate is zero for the levying region itself",
      float(np.abs(_tau[m.region_of == "EU27"]).max()) == 0.0)
check("CBAM rate is zero outside covered industries",
      all(_tau[k] == 0 for k in range(len(_tau))
          if m.industry_of[k] not in _cb.COVERED))
# A region already paying more than the EU gets no charge and no rebate.  Under
# the 13-region calibration this is live rather than hypothetical: Switzerland
# levies CHF 120/t (~$133) against the EU's $86 CBAM certificate price, so CHE
# satisfies the condition on the real data.  (The 20-region build had to perturb
# the price map to test it, because the EU was then the highest payer.)
check("no rebate where the origin already pays more than the EU",
      _ap["CHE"] > _ap["EU27"]
      and float(np.abs(_cb.tariff_rate(m, _ap)[m.region_of == "CHE"]).max()) == 0.0,
      f"CHE ${_ap['CHE']:.0f}/t vs EU ${_ap['EU27']:.0f}/t")

# statutory phase-in: CBAM is 2.5% of notional in 2026, reaching full rate in
# 2034, so results reported at 2040 see the fully phased-in charge.
check("CBAM phase-in rises to full rate by 2034 and holds",
      _cb.phase_in(2025) == 0.0 and _cb.phase_in(2026) == 0.025
      and _cb.phase_in(2034) == 1.0 and _cb.phase_in(2040) == 1.0
      and all(_cb.phase_in(y) <= _cb.phase_in(y + 1) for y in range(2026, 2040)),
      "2026 2.5% -> 2030 48.5% -> 2034 100%")
check("phase-in scales CBAM revenue linearly",
      abs(_cb.revenue(m, _A, _ap, year=2030)
          - 0.485 * _cb.revenue(m, _A, _ap)) < 1e-6)

_g = pd.read_csv(f"{ROOT}/out_sens_cbam_gva.csv", index_col=[0, 1])
_rev_div = _g.loc[("applied-divergence", "theta=1"), "revenue_bn"]
_rev_uni = _g.loc[("ngfs-uniform", "theta=1"), "revenue_bn"]
check("CBAM shrinks when carbon prices converge", _rev_uni < _rev_div,
      f"${_rev_uni:.1f}bn uniform vs ${_rev_div:.1f}bn divergent")
check("incidence flips with theta",
      _g.loc[("applied-divergence", "theta=1"), "EU27"]
      < _g.loc[("applied-divergence", "theta=0"), "EU27"]
      and _g.loc[("applied-divergence", "theta=0"), "TUR"]
      < _g.loc[("applied-divergence", "theta=1"), "TUR"],
      "theta=1 burdens the EU importer, theta=0 the exporter")

# --- generic tariff machinery -------------------------------------------------
from bkmn import tariff as _tf                                              # noqa: E402
_t0 = _tf.empty(m)
check("empty schedule has shape (sectors, regions)",
      _t0.shape == (len(m.x), len(m.regions_order)), str(_t0.shape))
_t1 = _tf.add_rule(m, _tf.empty(m), 0.25, origin="CHN", destination="USA")
_iusa = list(m.regions_order).index("USA")
_ichn = list(m.regions_order).index("CHN")
check("add_rule targets only the named origin and destination",
      _t1[m.region_of == "CHN", _iusa].min() == 0.25
      and _t1[m.region_of != "CHN", _iusa].max() == 0.0
      and _t1[:, _ichn].max() == 0.0)
_t2 = _tf.add_rule(m, _tf.empty(m), 0.10)          # universal
check("a tariff never applies to intra-regional supply",
      all(_t2[m.region_of == r, list(m.regions_order).index(r)].max() == 0.0
          for r in m.regions_order))
_tot, _imp, _exp = _tf.charges(m, _A, _t1, theta=1.0)
check("theta=1 charges the importer only",
      _imp[m.region_of == "USA"].sum() > 0 and abs(_exp).max() == 0.0)
_tot0, _imp0, _exp0 = _tf.charges(m, _A, _t1, theta=0.0)
check("theta=0 charges the exporter only",
      _exp0[m.region_of == "CHN"].sum() > 0 and abs(_imp0).max() == 0.0)
check("revenue is invariant to the incidence split",
      abs(_tf.revenue(m, _A, _t1) - _tf.revenue(m, _A, _t1)) < 1e-9)
check("final-demand imports raise revenue",
      _tf.revenue(m, _A, _t1, True) > _tf.revenue(m, _A, _t1, False),
      f"${_tf.revenue(m,_A,_t1,True)/1e3:,.1f}bn vs "
      f"${_tf.revenue(m,_A,_t1,False)/1e3:,.1f}bn intermediate-only")

# --- tariff reaches the FX chain ---------------------------------------------
_tfx = pd.read_csv(f"{ROOT}/out_sens_tariff_fx.csv", index_col=[0, 1])
_glob = _tfx.xs("Global 10% on all imports", level=0)
check("a tariff moves FX through the price level (it once stopped at GVA)",
      float(_glob.spot_pct.abs().max()) > 0.1,
      f"max |spot| = {_glob.spot_pct.abs().max():.2f}%")
# A tariff must NOT move the policy rate: like the carbon charge it is a tax
# wedge, and 2.7's output gap is -Omega(dT).  Its route to FX is the price
# level, not the output gap.  This gate is the inverse of the one it replaced.
check("a tariff does NOT move the policy rate (it is a transfer, not an output gap)",
      float(_glob.rate_bp.abs().max()) < 1e-9,
      f"max |dr| = {_glob.rate_bp.abs().max():.2e} bp")
_us = _tfx.xs("USA 25% on CHN manufactures", level=0)
check("a tariff weakens the levying currency (PPP: prices rise at home)",
      _us.loc["USA", "spot_pct"] > 0,
      f"USD spot {_us.loc['USA','spot_pct']:+.3f}% vs EUR")
_op = {}
for r in m.regions_order:
    _isr = m.region_of == r
    _col = _A[:, _isr] * m.x[_isr]
    _op[r] = _col[~_isr].sum() / _col.sum()
_c = np.corrcoef([_op[r] for r in _glob.index], _glob.spot_pct)[0, 1]
check("the FX response tracks import dependence", _c > 0.8,
      f"corr = {_c:.3f}")

# calibrated scenario must reproduce the published US effective tariff rate
_us26 = _tf.add_rule(m, _tf.empty(m), 0.044, destination="USA")
_us26 = _tf.add_rule(m, _us26, 0.234 - 0.044, origin="CHN", destination="USA")
_iu = list(m.regions_order).index("USA")
_isus = m.region_of == "USA"
_impv = (_A[:, _isus] * m.x[_isus]).sum(1) + m.fd[:, _iu]
_eff = float(_us26[~_isus, _iu] @ _impv[~_isus] / _impv[~_isus].sum())
check("calibrated schedule reproduces the published US effective rate",
      abs(_eff - 0.072) < 0.002,
      f"{_eff*100:.2f}% vs Penn Wharton 7.2% (May 2026)")

# China-share sweep: the calibration constraint must hold at every point, the
# headline FX number must be robust to it, and the attribution must not be.
_cs = pd.read_csv(f"{ROOT}/out_sens_china_share.csv", index_col=0)
check("sweep reproduces the published 7.2% at every China share",
      float((_cs.effective_pct - 7.2).abs().max()) < 1e-4)
check("revenue is invariant to the China share (the total is pinned)",
      float(_cs.revenue_bn.max() - _cs.revenue_bn.min()) < 1e-6)
check("headline USD/EUR is robust to the base-year China share",
      float(_cs.USD_spot_vs_EUR_pct.max() - _cs.USD_spot_vs_EUR_pct.min()) < 0.05,
      f"{_cs.USD_spot_vs_EUR_pct.min():.3f}..{_cs.USD_spot_vs_EUR_pct.max():.3f}%")
check("but the attribution to China is NOT robust",
      float(_cs.CHN_share_of_revenue_pct.max()
            - _cs.CHN_share_of_revenue_pct.min()) > 20.0,
      f"{_cs.CHN_share_of_revenue_pct.min():.0f}.."
      f"{_cs.CHN_share_of_revenue_pct.max():.0f}% of revenue")

# every scenario label the figure code asks for must resolve against the data.
# fig7 listed five series and silently plotted four for several commits, because
# the IIASA API returns 'Below 2?C' where the published name has a degree sign.
import importlib.util as _ilu                                              # noqa: E402
_mf = _ilu.module_from_spec(_ilu.spec_from_file_location(
    "mf", f"{ROOT}/tools/make_figures.py"))
_names = Scenarios(m.carbon_map).names
_ilu.spec_from_file_location("mf", f"{ROOT}/tools/make_figures.py").loader.exec_module(_mf)
for _lab in [_mf.NZ, _mf.CP, _mf.NDC, "Low demand", "Below 2C",
             "Delayed transition", "Fragmented World"]:
    _mf.scen(_lab, _names)          # raises if it cannot be matched
check("every figure scenario label resolves against the data",
      len({_mf.scen(x, _names) for x in
           [_mf.NZ, _mf.CP, _mf.NDC, "Low demand", "Below 2C",
            "Delayed transition", "Fragmented World"]}) == 7,
      "all 7 NGFS narratives matched, incl. the degree-sign case")

# spot is near-perfectly a rescaled carbon-pricing scope vector, because 20
# regions map onto only 5 NGFS R5 zones.  Gated so the claim cannot silently
# become false (or be quoted as an exact 1.000) if the zone mapping changes.
_spf = pd.read_csv(f"{ROOT}/out_fx_spot_ppp.csv",
                   index_col=[0, 1]).xs("Net Zero 2050", level=0)["2045"]
_cmf = m.carbon_map.set_index("region")
_scf = _cmf.loc[list(_spf.index), "carbon_scope"].astype(float)
_c = float(_spf.corr(_scf))
check("spot is near-exactly a rescaled carbon-pricing scope vector",
      0.999 < _c < 1.0,
      f"corr = {_c:.4f} (not 1.0000 - the residual is the R5 price variation)")

# --- 2.7 output gap and the damage temperature (the paper's specification) ---
from bkmn.run_fx import TAYLOR_OUTPUT_GAP, WARMING_BASELINE, warming  # noqa: E402
_sc2 = Scenarios(m.carbon_map)
check("Taylor output gap is the damage function, not the tax wedge",
      TAYLOR_OUTPUT_GAP == "physical",
      "A.6 step 6: dr = market + phi_Pi*dPi - phi_Y*Omega; 2.7: output gap == -Omega")
check("damage uses warming vs pre-industrial, not since the base year",
      WARMING_BASELINE == "preindustrial"
      and abs(warming(_sc2, "Net Zero 2050", 2040)
              - float(_sc2.temp.loc[2040, "Net Zero 2050"])) < 1e-12,
      f"dT(2040) = {warming(_sc2,'Net Zero 2050',2040):.3f} K vs 1850-1900")
# the rate shift must reconstruct from dPi and the PHYSICAL shock alone
_rs = pd.read_csv(f"{ROOT}/out_ext_rate_shift.csv", index_col=[0, 1])
_pi2 = pd.read_csv(f"{ROOT}/out_inflation_shift.csv", index_col=[0, 1])
_ph2 = pd.read_csv(f"{ROOT}/out_ext_gdp_physical.csv", index_col=[0, 1])
_kk = ("Net Zero 2050", "CHN")
_pred = 0.5 * _pi2.loc[_kk, "2040"] + 0.5 * _ph2.loc[_kk, "2040"] * 100
check("rate shift reconstructs from inflation + physical damage only",
      abs(_rs.loc[_kk, "2040"] - _pred) < 0.05,
      f"{_rs.loc[_kk,'2040']:.2f} bp vs {_pred:.2f} bp predicted")
# and must NOT reconstruct if the transition shock were included
_tr2 = pd.read_csv(f"{ROOT}/out_ext_gdp_transition.csv", index_col=[0, 1])
check("the transition shock is absent from the rate shift",
      abs(_rs.loc[_kk, "2040"]
          - (_pred + 0.5 * _tr2.loc[_kk, "2040"] * 100)) > 100.0,
      f"including it would give {_pred + 0.5*_tr2.loc[_kk,'2040']*100:.0f} bp")

# --- 2.11 op-risk takes the same output measure as 2.7 -----------------------
# Okun's law maps real output to employment, so the tax wedge must be excluded
# here for exactly the reason it is excluded from the Taylor rule.  Applying the
# argument to one and not the other was an inconsistency, found by re-reading
# the single-region reference: it calls oprisk.shift(omega, ...) and never
# passes it the carbon shock.
from bkmn.paper_tables import OPRISK_BETA                             # noqa: E402
from bkmn.run_fx import OPRISK_INPUT                                  # noqa: E402
check("op-risk takes the same output measure as the Taylor rule",
      OPRISK_INPUT == TAYLOR_OUTPUT_GAP == "physical",
      "a tax wedge destroys no output, so it drives no unemployment")
_opc = pd.read_csv(f"{ROOT}/out_ext_oprisk_conduct.csv", index_col=[0, 1])
_ope = pd.read_csv(f"{ROOT}/out_ext_oprisk_execution.csv", index_col=[0, 1])
# it must reconstruct from the PHYSICAL shock alone
_pred_op = (OPRISK_BETA["Conduct"] * (oprisk.kappa()["CHN"]
                                      * _ph2.loc[_kk, "2040"] / 100)
            / float(oprisk.base_unemployment()["CHN"])) * 100
check("op-risk reconstructs from the physical shock alone",
      abs(_opc.loc[_kk, "2040"] - _pred_op) < 0.05,
      f"{_opc.loc[_kk,'2040']:.2f} % vs {_pred_op:.2f} % predicted")
# The single-region reference uses a SATURATING form, m*(-kappa)*Omega/(off+Omega),
# bounded by m*(-kappa): 23.77 % Conduct, 28.52 % Execution.  Ours is the
# linearisation of the same Table-10 regression and is unbounded, so it can in
# principle exceed that ceiling -- it did, at 37.1 %, before this correction.
# The gate records the bound as a sanity ceiling rather than a hard identity.
for _nm, _tbl, _cap in (("Conduct", _opc, 1.306037776 * 0.182 * 100),
                        ("Execution", _ope, 1.566813512 * 0.182 * 100)):
    _mx = float(_tbl.abs().to_numpy().max())
    check(f"op-risk {_nm} stays inside the reference's saturating bound",
          _mx < _cap, f"max {_mx:.1f} % vs the reference asymptote {_cap:.1f} %")

# --- 2.9 credit: the CDS half -----------------------------------------------
from bkmn import credit as _cr                                        # noqa: E402
from bkmn.paper_tables import (CDS_BETA, CDS_WEIGHTS,                 # noqa: E402
                               EQUITY_BETA as _EQB)

# Tables 7-8 are index compositions, so each column must be a partition of 1
_wsum = {j: sum(CDS_WEIGHTS[s][k] for s in CDS_WEIGHTS)
         for k, j in enumerate(_cr.CDS_SECTORS)}
check("CDS index weights sum to 1 for every index",
      all(abs(v - 1.0) < 5e-3 for v in _wsum.values()),
      f"max |sum-1| = {max(abs(v-1) for v in _wsum.values()):.4f}")
check("every ICIO industry maps to a SIC section",
      set(m.industry_of) <= set(_cr.ICIO_TO_SIC),
      f"{len(set(m.industry_of))} industries covered")

_M5 = transition.gva_operator(m, 0.5)
_ct5 = transition.ct_direct(m, {r: 100.0 for r in m.regions_order})
_syn = _cr.synthetic_shock(m, _cr.rel_dgva_sectors(m, _M5, _ct5))
_cs = _cr.spread_shift(_syn)

# the transfer is exactly beta * synthetic (2.9), no hidden scaling
check("spread shift is exactly beta x the synthetic index shock",
      max(abs(_cs[r][j] - CDS_BETA[j] * _syn[r][j])
          for r in m.regions_order for j in _syn[r]) < 1e-18)
# a charge lowers GVA, so a NEGATIVE beta must WIDEN the spread
_neg = [j for j, b in CDS_BETA.items() if b < 0]
check("negative-beta indices widen when GVA falls",
      all(_cs[r][j] > 0 for r in m.regions_order for j in _neg),
      f"{len(_neg)} of {len(CDS_BETA)} indices have beta < 0")
# and the paper's two positive-beta indices must move the other way
_pos = [j for j, b in CDS_BETA.items() if b > 0 and j != "FTSE"]
check("the paper's positive-beta indices move against the rest",
      all(_cs[r][j] < 0 for r in m.regions_order for j in _pos),
      f"{_pos} - a property of the UK sample, not of the extension")
# zero charge, zero spread
_z = _cr.spread_shift(_cr.synthetic_shock(m, np.zeros(len(m.sectors))))
check("no charge means no spread move",
      max(abs(v) for d in _z.values() for v in d.values()) == 0.0)
# linear in the charge, like every other channel
_cs2 = _cr.credit_shift(m, _M5, 2 * _ct5)
check("the credit channel is exactly linear in the charge",
      max(abs(2 * _cs[r][j] - _cs2[r][j])
          for r in m.regions_order for j in _syn[r]) < 1e-15)
# the FTSE column is the equity index, so it must agree with equity.py's beta
check("the FTSE column carries the same beta as the equity channel",
      abs(CDS_BETA["FTSE"] - _EQB) < 1e-12,
      f"{CDS_BETA['FTSE']} = paper Table 9 FTSE 100 slope")
# output vs GVA weighting changes the answer -- the reference's gap 9b
_syn_g = _cr.synthetic_shock(m, _cr.rel_dgva_sectors(m, _M5, _ct5), size="gva")
_dev = max(abs(_syn_g[r][j] / _syn[r][j] - 1)
           for r in m.regions_order for j in _syn[r] if abs(_syn[r][j]) > 1e-12)
check("output- vs GVA-weighting materially changes the synthetic index",
      _dev > 0.05,
      f"max relative difference {_dev*100:.1f} % (SIZE switch; paper uses output)")

# --- scenario-consistent carbon intensities ----------------------------------
_scn = Scenarios(m.carbon_map)
check("intensity factor is exactly 1 at the base year",
      max(abs(_scn.intensity_factor(s_, 2022) - 1.0).max() for s_ in _scn.names) < 1e-12)
_fnz = _scn.intensity_factor("Net Zero 2050", 2040)
_fcp = _scn.intensity_factor("Current Policies", 2040)
check("mitigation scenarios abate; Net Zero abates most",
      bool((_fnz < _fcp).all()) and bool((_fnz < 1.0).all()),
      f"NZ {_fnz.min():.2f}-{_fnz.max():.2f} vs CP {_fcp.min():.2f}-{_fcp.max():.2f}")
check("factor falls monotonically with horizon under Net Zero",
      all(_scn.intensity_factor("Net Zero 2050", y)["CHN"]
          > _scn.intensity_factor("Net Zero 2050", y + 5)["CHN"]
          for y in (2025, 2030, 2035, 2040)))

# consistent intensities must lower the charge, by the factor, exactly
_Mp = transition.gva_operator(m, 0.5)
_x40 = _scn.xce_by_region("Net Zero 2050", 2040).to_dict()
_stat = transition.region_gdp_shock(m, _Mp, _x40)
_cons = transition.region_gdp_shock(m, _Mp, _x40, _fnz)
check("scenario-consistent intensities reduce the transition shock",
      all(_cons[r] > _stat[r] for r in m.regions_order),
      f"CHN {_stat['CHN']*100:.2f}% -> {_cons['CHN']*100:.2f}%")
# a region's shock is NOT its own factor times the static shock: the Leontief
# dual propagates cost-push across regions, so every region's charge enters.
# The exact property is linearity, checked with a uniform factor.
_half = _fnz.copy(); _half[:] = 0.5
_uni = transition.region_gdp_shock(m, _Mp, _x40, _half)
check("charge is exactly linear in a uniform intensity factor",
      max(abs(_uni[r] - 0.5 * _stat[r]) for r in m.regions_order) < 1e-15)
check("per-region reduction reflects trade partners, not just own factor",
      any(abs(_cons[r] - _stat[r] * _fnz[r]) > 1e-6 for r in m.regions_order),
      "cross-region cost-push means the scaling is not separable")
# sanity vs NGFS's own NiGEM Net Zero GDP impacts (roughly -1% to -4% by 2050)
check("Net Zero GDP shock is now the order of NGFS's own macro estimates",
      abs(min(_cons.values())) < 0.08,
      f"worst region {min(_cons.values())*100:.2f}% (was {min(_stat.values())*100:.2f}%)")

# --- the worked illustration in docs/TARIFF_METHOD.md 5 -----------------------
_ig = pd.read_csv(f"{ROOT}/out_illus_eu_tariff_gva.csv", index_col=0)
_if = pd.read_csv(f"{ROOT}/out_illus_eu_tariff_fx.csv", index_col=0)
check("illustration: a tariff weakens the currency that levies it",
      bool((_if.spot_pct < 0).all()),
      f"all {len(_if)} currencies strengthen vs EUR "
      f"({_if.spot_pct.min():.3f}..{_if.spot_pct.max():.3f}%)")
check("illustration: a tariff leaves the policy rate untouched",
      abs(_ig.loc["EU27", "rate_bp"]) < 1e-9,
      "a tariff is a tax wedge; 2.7's output gap is -Omega(dT)")
check("illustration: incidence moves the burden from levier to exporters",
      _ig.loc["EU27", "theta=1.0"] < _ig.loc["EU27", "theta=0.0"]
      and all(_ig.loc[r, "theta=0.0"] < _ig.loc[r, "theta=1.0"]
              for r in ("TUR", "RASIA", "RUS", "CHE")),
      f"EU27 {_ig.loc['EU27','theta=1.0']:.4f}% -> "
      f"{_ig.loc['EU27','theta=0.0']:.4f}%, TUR the reverse")

# --- Phase V: volatility -----------------------------------------------------
ts, ps = volatility.temperature_sigma(), volatility.carbon_price_sigma()
check("temperature σ > 0", float(ts.loc[2040, "Net Zero 2050"]) > 0,
      f"σ_T 2040 = {ts.loc[2040,'Net Zero 2050']:.3f} K")
check("carbon-price σ > 0 (cross-model)",
      float(ps.loc[2040, ("Net Zero 2050", "R5.2OECD")]) > 0,
      f"σ_XCE 2040 OECD = ${ps.loc[2040,('Net Zero 2050','R5.2OECD')]:.0f}/t")
q95 = pd.read_csv(f"{ROOT}/out_ext_fx_forward_q95.csv", index_col=[0, 1])
cen = tbl.xs("Net Zero 2050", level=0)
q95c = q95.xs("Net Zero 2050", level=0)
q95c.columns = [int(c) for c in q95c.columns]
check("q95 band wider than central",
      bool((q95c[2040].abs() >= cen[2040].abs() - 1e-9).mean() > 0.7),
      f"{int((q95c[2040].abs() >= cen[2040].abs()).sum())}/{len(cen)} currencies")

# The stress must be a stress in EVERY narrative, not just the one the band was
# originally written for.  A 1.64-sigma upward shock cannot make a currency's
# move smaller, and it did: the stressed path built its warming off the 2022
# base while the central path uses the pre-industrial level, so the damage leg
# ran ~50x too small and the tail inverted wherever the carbon-price leg was
# quiet (every low-price narrative).  Assert the widening scenario by scenario.
# The invariant is dispersion, not per-currency magnitude: a currency whose
# central value sits near zero (GBP, CHF under the low-price narratives) can
# pass through zero under stress and end up smaller in absolute terms without
# the stress being any milder.  What must hold everywhere is that the stress
# spreads the cross-section, which is what the chapter claims of it.
_q = pd.read_csv(f"{ROOT}/out_ext_fx_forward_q95.csv", index_col=[0, 1])["2040"]
_c = pd.read_csv(f"{ROOT}/out_ext_fx_forward_5y.csv", index_col=[0, 1])["2040"]
_tight = [s for s in _c.index.get_level_values(0).unique()
          if (_q.xs(s, level=0).max() - _q.xs(s, level=0).min())
          <= (_c.xs(s, level=0).max() - _c.xs(s, level=0).min())]
check("q95 widens the cross-section in every scenario", not _tight,
      f"{len(_c.index.get_level_values(0).unique())} scenarios" +
      (f", tight in {_tight}" if _tight else ""))

# and the stressed warming must exceed the central warming, which is the
# property the bug actually violated
_sc = Scenarios(m.carbon_map)
_ts = volatility.temperature_sigma()
_z = 1.6448536269514722
_bad = [(s, t) for s in _sc.names for t in (2030, 2040, 2050)
        if warming(_sc, s, t) + _z * float(_ts.loc[t, s] - _ts.loc[2022, s])
        <= warming(_sc, s, t)]
check("stressed warming exceeds central warming", not _bad,
      f"{len(_sc.names)*3} scenario-years checked")

# --- non-regression: transition core untouched -------------------------------
ref = pd.read_csv(f"{ROOT}/out_gva_shock_by_region_phi.csv", index_col=0)
M = transition.gva_operator(m, 0.5)
got = transition.region_gdp_shock(m, M, {r: 70.0 for r in m.regions_order})
err = max(abs(got[r] * 100 - ref.loc[r, "50%"]) for r in m.regions_order)
check("non-regression: transition core", err < 1e-9, f"max|Δ|={err:.1e} pp")

print(f"\nALL {n} GATES PASSED")
