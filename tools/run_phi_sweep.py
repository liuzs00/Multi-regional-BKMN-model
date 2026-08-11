"""
Pass-through sensitivity: run the chain across phi and record what moves.

phi is the paper's cost pass-through parameter (Section 2.4): the share of the
carbon charge a sector passes downstream in its price rather than absorbing in
its own value added.  The paper sweeps it 0 to 1 as its principal sensitivity,
so the multi-regional results must be reported the same way.

The sweep also settles a structural question.  Under the corrected Taylor
specification the policy rate responds to inflation and physical damage only
(Section 2.7's output gap is -Omega), and neither quantity touches the Leontief
dual.  So phi should have NO effect on rates or exchange rates, and its whole
influence should fall on value added and the market prices built from it.  The
script checks that rather than assuming it.

Outputs (at the reporting horizon, per scenario):
  out_phi_transition.csv   transition GVA shock, region x phi
  out_phi_equity.csv       equity index shift, region x phi
  out_phi_credit.csv       CDS spread shift (median across indices), region x phi
  out_phi_invariance.csv   rate and FX at each phi, to show they do not move

Usage: py -3 tools/run_phi_sweep.py
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from bkmn import (credit, equity, fx, macro, physical,      # noqa: E402
                  regions, transition)
from bkmn.run_fx import BASE, warming, xce_annual           # noqa: E402
from bkmn.scenarios import Scenarios                        # noqa: E402

PHIS = np.round(np.arange(0.0, 1.0001, 0.1), 2)
YEAR = 2040
SCENARIO = "Net Zero 2050"


def main():
    m = regions.load()
    sc = Scenarios(m.carbon_map)
    cm = m.carbon_map.set_index("region")
    vl = physical.vl_vector(m)
    betas = equity.betas()
    R = m.regions_order

    xce = xce_annual(sc, SCENARIO)
    fac = sc.intensity_factor(SCENARIO, YEAR)
    dT = warming(sc, SCENARIO, YEAR)
    ph = physical.region_damage(m, dT, vl)
    ct_phys = physical.tax_addon(m, dT, vl)

    tr_rows, eq_rows, cr_rows, inv_rows = {}, {}, {}, {}
    for phi in PHIS:
        M = transition.gva_operator(m, float(phi))
        tr = transition.region_gdp_shock(m, M, xce.loc[YEAR].to_dict(), fac)
        dY = {r: tr[r] + ph[r] for r in R}
        eq = equity.equity_shift(dY, betas)
        ct_all = transition.ct_direct(m, xce.loc[YEAR].to_dict(), fac) + ct_phys
        cs = credit.credit_shift(m, M, ct_all)
        idx = [c for c in credit.CDS_SECTORS if c != "FTSE"]

        tr_rows[phi] = {r: tr[r] * 100 for r in R}
        eq_rows[phi] = {r: eq[r] * 100 for r in R}
        cr_rows[phi] = {r: float(np.median([cs[r][c] for c in idx])) * 100
                        for r in R}

        # the invariance check: rate and FX must not depend on phi at all
        dpi = {r: macro.inflation_dev(
            float(xce.loc[YEAR, r] - xce.loc[YEAR - 1, r]),
            float(cm.loc[r, "carbon_scope"])) for r in R}
        dr = {r: macro.taylor_rate_shift(dpi[r], ph[r]) for r in R}
        cum = {r: macro.INFL_PER_USD * float(cm.loc[r, "carbon_scope"])
               * float(xce.loc[YEAR, r] - xce.loc[BASE, r]) for r in R}
        fxr = [r for r in R if cm.loc[r, "fx_role"] == "analytical"]
        inv_rows[phi] = {"rate_IND_bp": dr["IND"] * 1e4,
                         "rate_EU27_bp": dr["EU27"] * 1e4,
                         "spot_USD_pct": fx.spot_ppp(cum["USA"], cum["EU27"]) * 100,
                         "fwd5_IND_pct": fx.forward_total(
                             cum["IND"], cum["EU27"], dr["IND"], dr["EU27"], 5) * 100,
                         "n_fx": len(fxr)}

    def frame(rows, name):
        df = pd.DataFrame(rows).T
        df.index.name = "phi"
        df.to_csv(os.path.join(ROOT, name), float_format="%.4f")
        return df

    tr_df = frame(tr_rows, "out_phi_transition.csv")
    frame(eq_rows, "out_phi_equity.csv")
    cr_df = frame(cr_rows, "out_phi_credit.csv")
    inv = frame(inv_rows, "out_phi_invariance.csv")

    print(f"pass-through sweep at {YEAR}, {SCENARIO}\n")
    print("transition GVA shock (%), region x phi:")
    print(tr_df[["EU27", "CHN", "USA", "IND", "CHE"]].round(2).to_string())

    print("\ninvariance check -- these must not move with phi:")
    print(inv.round(4).to_string())
    moved = {c: float(inv[c].max() - inv[c].min()) for c in inv.columns}
    worst = max(abs(v) for k, v in moved.items() if k != "n_fx")
    print(f"\n  max variation across phi: {worst:.2e}  "
          f"{'INVARIANT' if worst < 1e-12 else '*** MOVES ***'}")

    print("\nendpoint identities (phi = 0 and 1 give -/+ CT over GVA):")
    ct = transition.ct_direct(m, xce.loc[YEAR].to_dict(), fac)
    for r in ("EU27", "CHN", "IND"):
        k = m.region_of == r
        ref = (m.x * ct)[k].sum() / m.gva[k].sum() * 100
        print(f"  {r:<5} phi=0 {tr_df.loc[0.0, r]:+8.3f}  phi=1 "
              f"{tr_df.loc[1.0, r]:+8.3f}  +/-CT/GVA {ref:8.3f}")

    print("\nsign change: the phi at which each region's shock crosses zero")
    for r in R:
        v = tr_df[r].to_numpy(float)
        s = np.where(np.diff(np.sign(v)) != 0)[0]
        if len(s):
            i = s[0]
            p0, p1 = PHIS[i], PHIS[i + 1]
            root = p0 + (p1 - p0) * (-v[i]) / (v[i + 1] - v[i])
            print(f"  {r:<6} crosses zero at phi = {root:.3f}")
        else:
            print(f"  {r:<6} no crossing in [0, 1]")

    print("\ncredit (median CDS widening, %) at the endpoints and centre:")
    print(cr_df.loc[[0.0, 0.5, 1.0]].round(2).to_string())
    return tr_df, cr_df, inv


if __name__ == "__main__":
    main()
