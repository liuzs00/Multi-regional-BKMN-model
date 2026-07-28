"""
Build the `ppp_gdp_weight` column of DATA_12R/region_carbon_map.csv from World
Bank PPP GDP (2022).

These are welfare-relevant aggregation weights for the **physical-damage**
channel only (a per-region damage fraction Omega_r is aggregated as
sum_r w_ppp,r * Omega_r).  They must NOT be used inside the ICIO/Leontief, nor
for the FX / financial (transition-cost) channels, which stay market-priced.

Source : World Bank indicator NY.GDP.MKTP.PP.CD  (GDP, PPP, current int'l $),
         World Bank REST API, no key required.
Method : w_r = GDP_ppp(r) / GDP_ppp(World),  region GDP = sum over member
         economies from region_mapping.csv.  ROW is a residual
         (World - sum of all non-ROW economies), so it also absorbs economies
         absent from the World Bank series (e.g. Taiwan) and the ICIO's own RoW.

Usage:  py -3 tools/build_ppp_weights.py
"""

import json
import os
import urllib.request

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D20 = os.path.join(ROOT, "DATA_20R")
CARBON_MAP = os.path.join(D20, "region_carbon_map.csv")
YEAR = 2022
INDICATOR = "NY.GDP.MKTP.PP.CD"
API = (f"https://api.worldbank.org/v2/country/all/indicator/{INDICATOR}"
       f"?date={YEAR}&format=json&per_page=20000")


def fetch_ppp() -> dict:
    """ISO3 code -> PPP GDP (current int'l USD) for `YEAR`, from the WB API."""
    req = urllib.request.Request(API, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        payload = json.load(r)
    meta, rows = payload[0], payload[1]
    assert meta["pages"] == 1, f"response paginated ({meta['pages']} pages)"
    out = {}
    for row in rows:
        code, val = row.get("countryiso3code"), row.get("value")
        if code and val is not None:
            out[code] = float(val)
    return out


def market_gdp_shares() -> dict:
    """Region market-GDP shares from the ICIO VA row (for the printed contrast)."""
    icio = pd.read_csv(os.path.join(D20, f"ICIO2025_20R_{YEAR}.csv"), index_col=0)
    va = icio.loc["VA"]
    fd = {"HFCE", "NPISH", "GGFC", "GFCF", "INVNT", "DPABR"}
    reg = {}
    for col, v in va.items():
        if col == "OUT" or "_" not in col:
            continue
        r, ind = col.split("_", 1)
        if ind in fd:
            continue
        reg[r] = reg.get(r, 0.0) + float(v)
    tot = sum(reg.values())
    return {r: v / tot for r, v in reg.items()}


def main():
    ppp = fetch_ppp()
    world = ppp["WLD"]
    mapping = pd.read_csv(os.path.join(D20, "region_mapping.csv"))

    named = mapping[mapping.region != "ROW"]
    missing = [c for c in named.country if c not in ppp]
    if missing:
        print(f"WARNING: no WB PPP GDP for {missing} -> folded into ROW residual")

    region_ppp = {r: sum(ppp.get(c, 0.0) for c in g.country)
                  for r, g in named.groupby("region")}
    region_ppp["ROW"] = world - sum(region_ppp.values())

    cm = pd.read_csv(CARBON_MAP)
    order = cm.region.tolist()

    # normalize; round to 3dp with ROW absorbing the residual so the column
    # sums to exactly 1.0
    w = {r: round(region_ppp[r] / world, 3) for r in order if r != "ROW"}
    w["ROW"] = round(1.0 - sum(w.values()), 3)

    cm["ppp_gdp_weight"] = cm.region.map(w)
    cm.to_csv(CARBON_MAP, index=False, float_format="%.3f")

    mkt = market_gdp_shares()
    print(f"World PPP GDP {YEAR}: {world/1e12:,.1f} T int'l$   (sum of weights = {sum(w.values()):.3f})\n")
    print(f"{'region':6s} {'PPP GDP $T':>11s} {'ppp_wt':>7s} {'mkt_wt':>7s} {'ppp/mkt':>8s}")
    for r in order:
        gdp_t = region_ppp[r] / 1e12
        ratio = w[r] / mkt[r] if mkt.get(r) else float("nan")
        print(f"{r:6s} {gdp_t:11.2f} {w[r]:7.3f} {mkt.get(r, 0):7.3f} {ratio:8.2f}")
    print(f"\nwrote ppp_gdp_weight into {CARBON_MAP}")


if __name__ == "__main__":
    main()
