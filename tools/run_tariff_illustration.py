"""
The worked example in docs/TARIFF_METHOD.md 5.

One assumed case, chosen to be simple and EU-centred rather than realistic: EU27
imposes a uniform 10% ad-valorem tariff on all imported goods, from every origin.
Goods industries only -- services are not charged at customs.  Reported at 2040,
phi = 0.5, against the Current Policies carbon baseline, at both ends of the
incidence parameter.

The rate is a round number, not a calibration; the chain is linear in tau, so
every figure scales with it and the illustration is about mechanism rather than
magnitude.  For schedules matched to measures actually in force see
docs/TARIFF_CALIBRATION.md and bkmn/run_extensions.py.

Writes out_illus_eu_tariff_{gva,fx}.csv.
Run: py -3 tools/run_tariff_illustration.py
"""
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from bkmn import equity, oprisk, physical, tariff, transition          # noqa: E402
from bkmn.regions import load                                          # noqa: E402
from bkmn.run_extensions import PHI, chain, derive                     # noqa: E402
from bkmn.scenarios import Scenarios                                   # noqa: E402

RATE = 0.10
LEVIER = "EU27"
YEAR = 2040
# ICIO industries a customs authority could actually charge.  Services are
# excluded: they do not cross a customs border and are not tariffed.
GOODS = ("A B C10T12 C13T15 C16 C17_18 C19 C20 C21 C22 C23 C24A C24B C25 C26 "
         "C27 C28 C29 C301 C302T309 C31T33 D E").split()


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

    tau = tariff.add_rule(m, tariff.empty(m), RATE, destination=LEVIER,
                          industries=GOODS)
    base_c = chain(m, sc, "Current Policies", M, scope, vl)
    base_d = derive(m, base_c, fxregs, betas, kap, u0)

    rev = tariff.revenue(m, A, tau)
    rev_i = tariff.revenue(m, A, tau, include_final_demand=False)
    ct, _, _ = tariff.charges(m, A, tau, 1.0)
    px = tariff.price_effect(m, Lt, ct, tau)[LEVIER]

    runs = {th: chain(m, sc, "Current Policies", M, scope, vl, tau=tau,
                      theta=th, Ltilde=Lt, A=A) for th in (1.0, 0.5, 0.0)}
    d1 = derive(m, runs[1.0], fxregs, betas, kap, u0)

    gva = pd.DataFrame(
        {f"theta={th}": {r: runs[th]["tariff"][r][YEAR] * 100
                         for r in m.regions_order} for th in runs}
    ).rename_axis("region")
    # policy-rate shift for every region, including the base currency, which is
    # absent from the FX table because spot is quoted against it
    gva["rate_bp"] = [(runs[1.0]["dr"][r][YEAR] - base_c["dr"][r][YEAR]) * 1e4
                      for r in gva.index]
    gva.to_csv(f"{ROOT}/out_illus_eu_tariff_gva.csv")

    fx = pd.DataFrame({
        "spot_pct": {r: (d1["spot"][r][YEAR] - base_d["spot"][r][YEAR]) * 100
                     for r in fxregs},
        "fwd5y_pct": {r: (d1["fwd5"][r][YEAR] - base_d["fwd5"][r][YEAR]) * 100
                      for r in fxregs},
        "rate_bp": {r: (runs[1.0]["dr"][r][YEAR] - base_c["dr"][r][YEAR]) * 1e4
                    for r in fxregs},
    }).rename_axis("region")
    fx.to_csv(f"{ROOT}/out_illus_eu_tariff_fx.csv")

    dr_eu = (runs[1.0]["dr"][LEVIER][YEAR] - base_c["dr"][LEVIER][YEAR]) * 1e4
    print(f"{LEVIER} levies {RATE*100:.0f}% on imported goods "
          f"-- at {YEAR}, phi={PHI}, theta=1\n")
    print(f"  revenue                ${rev/1e3:,.0f}bn/yr")
    print(f"    intermediate         ${rev_i/1e3:,.0f}bn   (enters ct)")
    print(f"    final demand         ${(rev-rev_i)/1e3:,.0f}bn   (consumer prices only)")
    print(f"  {LEVIER} consumer price   {px*100:+.3f}%")
    print(f"  {LEVIER} GVA              {gva.loc[LEVIER, 'theta=1.0']:+.4f}%")
    print(f"  {LEVIER} policy rate      {dr_eu:+.2f}bp"
          f"   (a tariff is a tax wedge, not an output gap -- 2.7's gap is -Omega)")
    print(f"\n  {(fx.spot_pct < 0).sum()}/{len(fx)} currencies strengthen vs EUR, "
          f"range {fx.spot_pct.min():+.3f}% .. {fx.spot_pct.max():+.3f}%")
    print("\nincidence (GVA %, at both ends of theta):")
    # the levier plus the four most export-dependent suppliers in the set
    show = ["EU27"] + [r for r in ("TUR", "RASIA", "RUS", "CHE", "ROW")
                       if r in gva.index]
    print(gva.loc[show].round(4).to_string())


if __name__ == "__main__":
    main()
