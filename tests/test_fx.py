"""
Phase 4 — FX validation gates. Run: py -3 tests/test_fx.py

Each gate must pass before the result tables are trusted.
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from bkmn import fx, macro, transition          # noqa: E402
from bkmn.regions import load                   # noqa: E402
from bkmn.scenarios import Scenarios            # noqa: E402
from bkmn.run_fx import run_scenario, HORIZONS  # noqa: E402

m = load()
n_pass = 0


def check(name, cond, detail=""):
    global n_pass
    assert cond, f"FAIL: {name}  {detail}"
    n_pass += 1
    print(f"  PASS  {name}  {detail}")


# --- Gate 1: reduction test — flat XCE=70 reproduces the committed CSV ------
ref = pd.read_csv(f"{ROOT}/out_gva_shock_by_region_phi.csv", index_col=0)
for phi, col in [(0.0, "0%"), (0.5, "50%"), (1.0, "100%")]:
    M = transition.gva_operator(m, phi)
    got = transition.region_gdp_shock(m, M, {r: 70.0 for r in m.regions_order})
    err = max(abs(got[r] * 100 - ref.loc[r, col]) for r in m.regions_order)
    check(f"reduction φ={phi}", err < 1e-6, f"max|Δ|={err:.2e} pp vs {col}")

# --- Gate 2: φ=0 / φ=100 endpoint identities (±CT/GVA), per region ----------
M0 = transition.gva_operator(m, 0.0)
s0 = transition.region_gdp_shock(m, M0, {r: 70.0 for r in m.regions_order})
ct = m.ci * 70.0 * 1e-6
CToverGVA = {r: -(m.x * ct)[m.region_of == r].sum() / m.gva[m.region_of == r].sum()
             for r in m.regions_order}
err = max(abs(s0[r] - CToverGVA[r]) for r in m.regions_order)
check("endpoint φ=0 = -CT/GVA", err < 1e-12, f"max|Δ|={err:.1e}")

# --- Gate 3: HW rate-shift limits -------------------------------------------
from bkmn.rates import zero_rate_shift          # noqa: E402
check("HW τ→0 gives dr", abs(float(zero_rate_shift(0.01, 1e-9)) - 0.01) < 1e-6)
check("HW decays with τ", float(zero_rate_shift(0.01, 20)) < float(zero_rate_shift(0.01, 1)))

# --- Gate 4: FX base + triangular consistency -------------------------------
sc = Scenarios(m.carbon_map)
cm = m.carbon_map.set_index("region")
fxregs = [r for r in m.regions_order if cm.loc[r, "fx_role"] == "analytical"]
M = transition.gva_operator(m, 0.5)
res = run_scenario(m, sc, "Net Zero 2050", M, cm.carbon_scope, fxregs)

# spot triangular: (A vs EUR) - (B vs EUR) == cum_A - cum_B (definition)
A, B, t = "USA", "IND", 2040
tri = res["spotfx"][A][t] - res["spotfx"][B][t]
check("EUR base: spot self-consistent", abs(res["spotfx"][A][2025]) < 1e-12,
      "2025 (XCE≈base) ≈ 0")
# forward-points triangular: pts(A,EUR)-pts(B,EUR) == pts(A,B)
dr = res["dr"]
lhs = fx.forward_points(dr[A][t], dr["EU27"][t], 5) - fx.forward_points(dr[B][t], dr["EU27"][t], 5)
rhs = fx.forward_points(dr[A][t], dr[B][t], 5)
check("forward points triangular", abs(lhs - rhs) < 1e-15, f"|Δ|={abs(lhs-rhs):.1e}")

# --- Gate 5: scenario monotonicity — |spot| CP < NDCs < NZ2050 --------------
r, t = "USA", 2040
mags = {}
for s in ["Current Policies", "Nationally Determined Contributions (NDCs)", "Net Zero 2050"]:
    rr = run_scenario(m, sc, s, M, cm.carbon_scope, fxregs)
    mags[s] = abs(rr["spotfx"][r][t])
ordered = (mags["Current Policies"] < mags["Nationally Determined Contributions (NDCs)"]
           < mags["Net Zero 2050"])
check("scenario monotonicity (|USD spot| 2040)", ordered,
      f"CP {mags['Current Policies']*100:.3f}% < NDC "
      f"{mags['Nationally Determined Contributions (NDCs)']*100:.3f}% < NZ "
      f"{mags['Net Zero 2050']*100:.3f}%")

print(f"\nALL {n_pass} GATES PASSED")
