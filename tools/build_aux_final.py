"""
Build the per-region auxiliary inputs that live outside DATA_final/.

DATA_final holds the IO core (flows, output, emissions, intensity) plus the
carbon/scenario map.  Three other per-region series live under data/ because
they come from different sources and are used by single channels:

    data/physical/vl_scale_13R.csv    ND-GAIN vulnerability  -> physical damage
    data/macro/unemployment_13R.csv   World Bank             -> operational risk
    data/macro/okun_kappa.csv         (shared; extended in place for new regions)

Each is rebuilt from the same economy-level source the 20-region version used,
re-aggregated through DATA_final/region_mapping.csv, so the only thing that
changes is the partition.

Usage: py -3 tools/build_aux_final.py
"""
import io
import os
import sys
import zipfile

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

DF = os.path.join(ROOT, "DATA_final")
PHYS = os.path.join(ROOT, "data", "physical")
MACRO = os.path.join(ROOT, "data", "macro")
TAG = "13R"


def mapping():
    return pd.read_csv(os.path.join(DF, "region_mapping.csv"))


def order():
    return list(pd.read_csv(os.path.join(DF, "region_carbon_map.csv")).region)


def build_vl():
    """scale(r) = GDP-weighted mean ND-GAIN, normalised to world mean 1."""
    z = zipfile.ZipFile(os.path.join(PHYS, "ndgain_resources.zip"))
    v = pd.read_csv(io.BytesIO(z.read("resources/vulnerability/vulnerability.csv")))
    year = max(c for c in v.columns if c.isdigit())
    nd = v.set_index("ISO3")[year].dropna()

    gdp = pd.read_csv(os.path.join(MACRO, "wb_gdp_current_usd_2000_2023.csv"))
    gdp = gdp[gdp.year == 2022].dropna(subset=["value"]).set_index("code").value

    mp = mapping()
    rows = []
    for region, grp in mp.groupby("region"):
        ws = cw = 0.0
        n = 0
        for c in grp.country:
            if c in nd.index and c in gdp.index:
                ws += gdp[c]
                cw += gdp[c] * nd[c]
                n += 1
        rows.append({"region": region, "ndgain": cw / ws if ws else None,
                     "coverage_members": n, "members": len(grp),
                     "ndgain_year": int(year)})
    df = pd.DataFrame(rows).set_index("region")

    wgdp = {r: sum(gdp.get(c, 0.0) for c in g.country)
            for r, g in mp.groupby("region")}
    world = (sum(df.loc[r, "ndgain"] * wgdp[r] for r in df.index)
             / sum(wgdp.values()))
    df["scale"] = (df.ndgain / world).round(4)
    df = df.reindex(order())
    dest = os.path.join(PHYS, f"vl_scale_{TAG}.csv")
    df.to_csv(dest, float_format="%.4f")
    print(f"ND-GAIN {year}, world GDP-weighted mean {world:.4f} -> "
          f"{os.path.basename(dest)}")
    print(df[["ndgain", "scale", "coverage_members", "members"]].to_string())
    return df


def build_unemployment():
    """Labour-force-weighted 2022 unemployment rate per region."""
    u = pd.read_csv(os.path.join(MACRO, "wb_unemployment_2022.csv"))
    u = u.dropna(subset=["value"]).set_index("code").value
    lf = pd.read_csv(os.path.join(MACRO, "wb_labour_force_2022.csv"))
    lf = lf.dropna(subset=["value"]).set_index("code").value

    mp = mapping()
    rows = []
    for region, grp in mp.groupby("region"):
        w = uw = 0.0
        n = 0
        for c in grp.country:
            if c in u.index and c in lf.index:
                w += lf[c]
                uw += lf[c] * u[c]
                n += 1
        rows.append({"region": region,
                     "unemployment_2022": round(uw / w, 3) if w else None,
                     "coverage_members": n, "members": len(grp)})
    df = pd.DataFrame(rows).set_index("region").reindex(order())
    assert df.unemployment_2022.notna().all(), "a region has no unemployment data"
    dest = os.path.join(MACRO, f"unemployment_{TAG}.csv")
    df.to_csv(dest, float_format="%.3f")
    print(f"\n-> {os.path.basename(dest)}")
    print(df.to_string())
    return df


def extend_kappa():
    """Add Okun slopes for regions the 20-region table did not have."""
    path = os.path.join(MACRO, "okun_kappa.csv")
    k = pd.read_csv(path)
    have = set(k.region)
    add = {
        "CHE": (-0.30, "ESTIMATE advanced-economy default (Okun literature "
                       "range -0.25..-0.45)"),
        "RASIA": (-0.20, "ESTIMATE mixed advanced/emerging Asia; between the "
                         "advanced (-0.30) and emerging (-0.15) defaults"),
    }
    new = [{"region": r, "kappa": v, "provenance": p}
           for r, (v, p) in add.items() if r not in have]
    if new:
        k = pd.concat([k, pd.DataFrame(new)], ignore_index=True)
        k.to_csv(path, index=False)
        print(f"\n-> okun_kappa.csv extended with {[n['region'] for n in new]}")
    else:
        print("\n-> okun_kappa.csv already covers every region")
    missing = [r for r in order() if r not in set(k.region)]
    print(f"   regions falling back to the default: {missing or 'none'}")
    return k


def main():
    build_vl()
    build_unemployment()
    extend_kappa()


if __name__ == "__main__":
    main()
