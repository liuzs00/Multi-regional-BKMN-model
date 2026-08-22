"""
Build the per-region carbon-pricing scope for the 20-region BKMN model.

Scope = fraction of a region's emissions subject to a carbon price (tax or ETS).
It scales the Moessner inflation channel (paper 2.6: dPi = 0.08%/10 x dXCE x scope)
and is a first-order driver of cross-region rate/FX differentials.

Source: "Share of CO2 emissions covered by a carbon price" - Our World in Data,
        https://ourworldindata.org/grapher/carbon-tax-trading-coverage
        (republication of the World Carbon Pricing Database, Dolphin et al.;
        license CC BY). Downloaded to data/scope/owid_carbon_price_coverage.csv
        via:  curl -A "Mozilla/5.0" -o data/scope/owid_carbon_price_coverage.csv \
              "https://ourworldindata.org/grapher/carbon-tax-trading-coverage.csv?v=1&csvType=full&useColumnShortNames=true"

Method: for each of the 20 regions, scope = emissions-weighted mean of member
economies' latest coverage share, weights = GHGFP 2022 Scope-1 emissions
(the same emissions data the model's carbon-intensity table is built from).
Economies missing from OWID (e.g. TWN) get coverage 0 — conservative.

Caveats (documented, acceptable at this stage):
  * OWID coverage is share of CO2; the model's emissions are GHG CO2e.
  * Coverage is an *applied-policy* fact as of the latest OWID year; scenario
    narratives may widen scope over time (a Phase-2 modelling choice).

Outputs: data/scope/carbon_scope_20R.csv (region, scope, n_covered, source year)
         and updates the `carbon_scope` column in DATA_final/region_carbon_map.csv.

Usage: py -3 tools/build_carbon_scope.py
"""
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "DATA_final")
OWID = os.path.join(ROOT, "data", "scope", "owid_carbon_price_coverage.csv")
COVER_COL = "co2_with_tax_or_ets_as_share_of_co2"


def main():
    owid = pd.read_csv(OWID)
    year = int(owid.year.max())
    cov = (owid[owid.year == year]
           .dropna(subset=["code"])
           .set_index("code")[COVER_COL] / 100.0)   # percent -> fraction

    mapping = pd.read_csv(os.path.join(DATA, "region_mapping.csv"))

    # per-economy Scope-1 emissions (tonnes) as weights, from GHGFP 2022
    gf = pd.read_csv(os.path.join(ROOT, "data", "ghgfp", "SCOPE", "2022.csv.gz"))
    gf = gf[(gf.EMISSIONS_SCOPE == "S1") & (gf.TIME_PERIOD == 2022)]
    emis = (gf.assign(t=gf.OBS_VALUE * 10.0 ** gf.UNIT_MULT)
              .groupby("EMISSIONS_ORIGIN_AREA")["t"].sum())

    rows = []
    for region, grp in mapping.groupby("region"):
        w_sum, cw_sum, n_cov = 0.0, 0.0, 0
        for c in grp.country:
            w = float(emis.get(c, 0.0))
            cvg = float(cov.get(c, 0.0))          # missing -> 0 (conservative)
            if c == "ROW":                         # ICIO's own RoW residual
                cvg = 0.0
            w_sum += w
            cw_sum += w * cvg
            n_cov += cvg > 0
        rows.append({"region": region,
                     "carbon_scope": round(cw_sum / w_sum, 3) if w_sum else 0.0,
                     "covered_members": n_cov, "members": len(grp),
                     "owid_year": year})

    out = pd.DataFrame(rows).set_index("region")
    cm = pd.read_csv(os.path.join(DATA, "region_carbon_map.csv"))
    out = out.reindex(cm.region)
    out.to_csv(os.path.join(ROOT, "data", "scope", "carbon_scope_20R.csv"))

    cm["carbon_scope"] = cm.region.map(out.carbon_scope)
    cm.to_csv(os.path.join(DATA, "region_carbon_map.csv"), index=False,
              float_format="%.3f")

    print(f"OWID coverage year: {year}")
    print(out.to_string())
    print(f"\nwrote data/scope/carbon_scope_20R.csv and updated "
          f"DATA_final/region_carbon_map.csv (carbon_scope column)")


if __name__ == "__main__":
    main()
