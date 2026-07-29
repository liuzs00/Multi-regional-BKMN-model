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
check("vulnerable regions hit harder", d1["AFR"] < d1["NOR"],
      f"AFR {d1['AFR']*100:.2f}% < NOR {d1['NOR']*100:.2f}%")

# --- Phase E: equity ---------------------------------------------------------
b = equity.betas()
check("betas positive for all 20 regions",
      len(b) == 20 and all(v > 0 for v in b.values()))
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

# --- Phase M: mixture --------------------------------------------------------
tbl = pd.read_csv(f"{ROOT}/out_ext_fx_forward_5y.csv", index_col=[0, 1])
tbl.columns = [int(c) for c in tbl.columns]
scen = list(tbl.index.get_level_values(0).unique())
for prior in mixture.PRIORS:
    w = mixture.weights(prior, scenarios=scen)
    check(f"weights sum to 1 [{prior}]", abs(sum(w.values()) - 1) < 1e-12)
one = {s: (1 if s == "Net Zero 2050" else 0) for s in scen}
deg = mixture.expected(tbl, one)
check("degenerate prior reproduces scenario",
      np.allclose(deg.to_numpy(float), tbl.xs("Net Zero 2050", level=0).to_numpy(float)))
e = mixture.expected(tbl, "uniform")
lo = tbl.groupby(level=1).min().reindex(e.index)[e.columns]
hi = tbl.groupby(level=1).max().reindex(e.index)[e.columns]
check("E[X] within scenario range",
      bool(((e >= lo - 1e-9) & (e <= hi + 1e-9)).all().all()))

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

# --- non-regression: transition core untouched -------------------------------
ref = pd.read_csv(f"{ROOT}/out_gva_shock_by_region_phi.csv", index_col=0)
M = transition.gva_operator(m, 0.5)
got = transition.region_gdp_shock(m, M, {r: 70.0 for r in m.regions_order})
err = max(abs(got[r] * 100 - ref.loc[r, "50%"]) for r in m.regions_order)
check("non-regression: transition core", err < 1e-9, f"max|Δ|={err:.1e} pp")

print(f"\nALL {n} GATES PASSED")
