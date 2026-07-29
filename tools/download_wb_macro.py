"""
World Bank macro data for the extension phases (docs/EXT_PLAN.md):

  * SL.UEM.TOTL.ZS   unemployment rate, 2022        -> Phase O (op-risk base U)
  * SL.TLF.TOTL.IN   labour force, 2022             -> weights for aggregates
  * NY.GDP.MKTP.CD   GDP current US$, 2000-2023     -> Phase E (equity beta regressor)

Writes raw country panels to data/macro/ and a labour-force-weighted 2022
unemployment rate per 20R region to data/macro/unemployment_20R.csv.

Usage: py -3 tools/download_wb_macro.py
"""
import json
import os
import urllib.request

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "data", "macro")
D20 = os.path.join(ROOT, "DATA_20R")
API = ("https://api.worldbank.org/v2/country/all/indicator/{ind}"
       "?date={dates}&format=json&per_page=20000&page={page}")


def _get(url, tries=4):
    import time
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except Exception as e:                    # noqa: BLE001 transient API errors
            if k == tries - 1:
                raise
            print(f"  retry {k+1} after {type(e).__name__}")
            time.sleep(15 * (k + 1))


def fetch(ind, dates):
    rows, page = [], 1
    while True:
        payload = _get(API.format(ind=ind, dates=dates, page=page))
        meta, data = payload[0], payload[1] or []
        rows += [{"code": d["countryiso3code"], "year": int(d["date"]),
                  "value": d["value"]} for d in data if d.get("countryiso3code")]
        if page >= meta["pages"]:
            break
        page += 1
    return pd.DataFrame(rows)


def main():
    os.makedirs(DEST, exist_ok=True)

    unemp = fetch("SL.UEM.TOTL.ZS", "2022")
    upanel = fetch("SL.UEM.TOTL.ZS", "2000:2023")
    upanel.to_csv(os.path.join(DEST, "wb_unemployment_2000_2023.csv"), index=False)
    unemp.to_csv(os.path.join(DEST, "wb_unemployment_2022.csv"), index=False)
    lf = fetch("SL.TLF.TOTL.IN", "2022")
    lf.to_csv(os.path.join(DEST, "wb_labour_force_2022.csv"), index=False)
    gdp = fetch("NY.GDP.MKTP.CD", "2000:2023")
    gdp.to_csv(os.path.join(DEST, "wb_gdp_current_usd_2000_2023.csv"), index=False)
    print(f"unemployment rows {len(unemp)}, labour force {len(lf)}, gdp {len(gdp)}")

    # labour-force-weighted unemployment per 20R region
    u = unemp.dropna(subset=["value"]).set_index("code").value
    w = lf.dropna(subset=["value"]).set_index("code").value
    mapping = pd.read_csv(os.path.join(D20, "region_mapping.csv"))
    rows = []
    for region, grp in mapping.groupby("region"):
        ws = cw = 0.0
        for c in grp.country:
            if c in u.index and c in w.index:
                ws += w[c]
                cw += w[c] * u[c]
        rows.append({"region": region,
                     "unemployment_2022": round(cw / ws, 3) if ws else None,
                     "coverage_members": int(sum(c in u.index for c in grp.country)),
                     "members": len(grp)})
    out = pd.DataFrame(rows).set_index("region")
    cm = pd.read_csv(os.path.join(D20, "region_carbon_map.csv"))
    out = out.reindex(cm.region)
    out.to_csv(os.path.join(DEST, "unemployment_20R.csv"))
    print(out.unemployment_2022.to_string())


if __name__ == "__main__":
    main()
