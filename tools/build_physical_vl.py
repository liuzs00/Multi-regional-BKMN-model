"""
Build the per-region physical-vulnerability scale for Phase P (docs/EXT_PLAN.md).

scale(r) = GDP-weighted mean of member economies' ND-GAIN vulnerability score
(latest year), normalised so the GDP-weighted world mean = 1.  Multiplies the
paper's Table-6 sector pattern to give VL(r,i) = pattern(i) x scale(r).

Inputs : data/physical/ndgain_resources.zip  (official ND-GAIN release,
         resources/vulnerability/vulnerability.csv, ISO3 x year, score in 0-1)
         data/macro/wb_gdp_current_usd_2000_2023.csv  (weights, 2022)
         DATA_20R/region_mapping.csv
Output : data/physical/vl_scale_20R.csv  (region, ndgain, scale, coverage)

Economies absent from ND-GAIN (e.g. TWN, HKG) or from WB GDP simply drop out of
the weighted mean for their region — documented, conservative.

Usage: py -3 tools/build_physical_vl.py
"""
import io
import os
import zipfile

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D20 = os.path.join(ROOT, "DATA_20R")
PHYS = os.path.join(ROOT, "data", "physical")


def main():
    z = zipfile.ZipFile(os.path.join(PHYS, "ndgain_resources.zip"))
    v = pd.read_csv(io.BytesIO(z.read("resources/vulnerability/vulnerability.csv")))
    year = max(c for c in v.columns if c.isdigit())
    nd = v.set_index("ISO3")[year].dropna()

    gdp = pd.read_csv(os.path.join(ROOT, "data", "macro",
                                   "wb_gdp_current_usd_2000_2023.csv"))
    gdp = gdp[gdp.year == 2022].dropna(subset=["value"]).set_index("code").value

    mapping = pd.read_csv(os.path.join(D20, "region_mapping.csv"))
    rows = []
    for region, grp in mapping.groupby("region"):
        ws = cw = 0.0
        n = 0
        for c in grp.country:
            if c in nd.index and c in gdp.index:
                ws += gdp[c]
                cw += gdp[c] * nd[c]
                n += 1
        rows.append({"region": region,
                     "ndgain": cw / ws if ws else None,
                     "coverage_members": n, "members": len(grp),
                     "ndgain_year": int(year)})
    df = pd.DataFrame(rows).set_index("region")

    # normalise: GDP-weighted world mean of the regional scores = 1
    wgdp = {r: sum(gdp.get(c, 0.0) for c in g.country)
            for r, g in mapping.groupby("region")}
    world = sum(df.loc[r, "ndgain"] * wgdp[r] for r in df.index) / sum(wgdp.values())
    df["scale"] = (df.ndgain / world).round(4)

    cm = pd.read_csv(os.path.join(D20, "region_carbon_map.csv"))
    df = df.reindex(cm.region)
    df.to_csv(os.path.join(PHYS, "vl_scale_20R.csv"), float_format="%.4f")
    print(f"ND-GAIN year {year}; world GDP-weighted mean {world:.4f}")
    print(df[["ndgain", "scale", "coverage_members", "members"]].to_string())


if __name__ == "__main__":
    main()
