"""
Sensitivity of the calibrated US tariff schedule to China's import share.

The May-2026 calibration (docs/TARIFF_METHOD.md 5.1) pins two published numbers
-- a 7.2% US average effective tariff rate and 23.4% on China -- and solves for
the residual rate on all other origins.  That solution depends on China's share
of US imports, and our 2022 ICIO base year puts it at 14.7% while the current
figure is nearer 10% and falling.  This sweep turns that hidden assumption into
a stated range.

Two shares are in play and must not be confused:

    s_world  what China's share actually is (the swept uncertainty)
    s_table  14.7%, what the 2022 table says, i.e. what the model charges

Sweeping the first and levying on the second would break the constraint the
calibration exists to satisfy.  So we match *charges* rather than rates -- the
charge is what enters `ct`:

    tau_CHN(s) = 23.4% * s / s_table      China's burden matches the real world
    r(s)       = (7.2% - s*23.4%) / (1 - s_table)      total still lands on 7.2%

At s = s_table this collapses to the committed (23.4%, 4.4%).

Writes out_sens_china_share.csv.  Run: py -3 tools/sweep_china_share.py
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")
os.makedirs(RESULTS, exist_ok=True)
sys.path.insert(0, ROOT)

from bkmn import equity, oprisk, physical, tariff, transition          # noqa: E402
from bkmn.regions import load                                          # noqa: E402
from bkmn.run_extensions import PHI, chain, derive                     # noqa: E402
from bkmn.scenarios import Scenarios                                   # noqa: E402

BAR_TAU = 0.072      # published US average effective rate, May 2026  [DATA]
TAU_CHN = 0.234      # published effective rate on China, May 2026    [DATA]
SHARES = [0.07, 0.09, 0.10, 0.12, 0.147, 0.165, 0.185, 0.20]
YEAR = 2040


def solve(s, s_table):
    """(tau_CHN, r) that match China's real burden and still total BAR_TAU."""
    return TAU_CHN * s / s_table, (BAR_TAU - s * TAU_CHN) / (1 - s_table)


def main():
    m = load()
    sc = Scenarios(m.carbon_map)
    cm = m.carbon_map.set_index("region")
    scope, vl = cm.carbon_scope, physical.vl_vector(m)
    fxregs = [r for r in m.regions_order if cm.loc[r, "fx_role"] == "analytical"]
    M = transition.gva_operator(m, PHI)
    Lt = transition.price_operator(m, PHI)
    A = transition.technical_matrix(m)
    betas, kap, u0 = equity.betas(), oprisk.kappa(), oprisk.base_unemployment()

    iu = list(m.regions_order).index("USA")
    isus = m.region_of == "USA"
    impv = (A[:, isus] * m.x[isus]).sum(1) + m.fd[:, iu]
    s_table = impv[m.region_of == "CHN"].sum() / impv[~isus].sum()

    base_c = chain(m, sc, "Current Policies", M, scope, vl)
    base_d = derive(m, base_c, fxregs, betas, kap, u0)

    rows = {}
    for s in SHARES:
        tc, r = solve(s, s_table)
        tau = tariff.add_rule(m, tariff.empty(m), r, destination="USA")
        tau = tariff.add_rule(m, tau, tc - r, origin="CHN", destination="USA")
        eff = float(tau[~isus, iu] @ impv[~isus] / impv[~isus].sum())
        assert abs(eff - BAR_TAU) < 1e-6, (s, eff)      # constraint must hold

        c = chain(m, sc, "Current Policies", M, scope, vl, tau=tau, theta=1.0,
                  Ltilde=Lt, A=A)
        d = derive(m, c, fxregs, betas, kap, u0)
        chn_only = tau.copy()
        chn_only[m.region_of != "CHN"] = 0.0
        rows[round(s * 100, 1)] = {
            "tau_CHN_pct": tc * 100,
            "r_other_pct": r * 100,
            "effective_pct": eff * 100,
            "revenue_bn": tariff.revenue(m, A, tau) / 1e3,
            "CHN_share_of_revenue_pct":
                tariff.revenue(m, A, chn_only) / tariff.revenue(m, A, tau) * 100,
            "USD_spot_vs_EUR_pct":
                (d["spot"]["USA"][YEAR] - base_d["spot"]["USA"][YEAR]) * 100,
            "USD_fwd5y_pct":
                (d["fwd5"]["USA"][YEAR] - base_d["fwd5"]["USA"][YEAR]) * 100,
            "USA_rate_bp":
                (c["dr"]["USA"][YEAR] - base_c["dr"]["USA"][YEAR]) * 1e4,
            "USA_gva_pct": c["tariff"]["USA"][YEAR] * 100,
            "CHN_gva_pct": c["tariff"]["CHN"][YEAR] * 100,
        }
    out = pd.DataFrame(rows).T.rename_axis("china_share_pct")
    out.to_csv(f"{RESULTS}/out_sens_china_share.csv")
    print(f"s_table = {s_table*100:.1f}%   (2022 ICIO, all industries)\n")
    print(out.round(3).to_string())
    rng = out.max() - out.min()
    print("\nrange across the sweep:")
    for k in ["USD_spot_vs_EUR_pct", "USA_gva_pct", "CHN_share_of_revenue_pct"]:
        print(f"   {k:26s} {out[k].min():7.3f} .. {out[k].max():7.3f}"
              f"   (spread {rng[k]:.3f})")


if __name__ == "__main__":
    main()
