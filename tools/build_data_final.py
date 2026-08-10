"""
Build DATA_final/ -- the calibration tables at the 13 regions the selection
algorithm chooses.

Same structure as DATA_20R, produced from the same sources, but the region
definition is IMPORTED from `tools/select_regions_threshold.py` and re-derived
at build time rather than transcribed, so the data cannot drift from the method
that justifies it.

Region definition (see docs/CHAPTER_REGION_SELECTION.md):
    threshold rule            -> 11 named regions
    residual split by R5 zone -> ASIA / OECD / REF / World
    zone cleaning at k = 1.5  -> outliers dropped into ROW
    promotion until ROW fits  -> RASIA
                                 = 13 regions

Inputs
  D:\\2016-2022_SML\\2022_SML.csv          OECD ICIO 2025 (81 economies x 50 ind.)
  data/ghgfp/SCOPE/2022.csv.gz            GHGFP 2025 Scope-1
  data/scope/owid_carbon_price_coverage.csv   OWID carbon-price coverage
  DATA_20R/industry_mapping.csv           industry code crosswalk (region-free)
  DATA_20R/region_carbon_map.csv          qualitative columns to carry over
  World Bank API (optional)               PPP GDP 2022 for welfare weights

Outputs (DATA_final/)
  ICIO2025_13R_2022.csv, GHG_S1_13R_2022.csv, CARBON_INTENSITY_13R_2022.csv,
  region_mapping.csv, region_carbon_map.csv, industries.csv,
  industry_mapping.csv, README.md

Usage: py -3 tools/build_data_final.py
"""
import json
import os
import shutil
import sys
import urllib.request

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from tools.select_regions_threshold import (CANDIDATES, group,  # noqa: E402
                                            linkage_by_economy, select,
                                            split_residual)

SRC_DIR = r"D:\2016-2022_SML"
OUT_DIR = os.path.join(ROOT, "DATA_final")
D20 = os.path.join(ROOT, "DATA_20R")
YEAR = 2022
TAG = "13R"

FD_CATS = ["HFCE", "NPISH", "GGFC", "GFCF", "INVNT", "DPABR"]
SPECIAL_ROWS = ["TLS", "VA", "OUT"]

# Presentation order: base region, then single economies by linkage, then the
# structural aggregates, then the closure -- the DATA_20R convention.
ORDER = ["EU27", "CHN", "USA", "GBR", "CHE", "RUS", "IND", "TUR",
         "RASIA", "LAM", "MEA", "AFR", "ROW"]

# Columns of region_carbon_map that are judgements rather than measurements.
# Carried over unchanged from DATA_20R where the region is unchanged; the two
# new regions are stated here.
CARBON_MAP_QUAL = {
    "CHE": dict(currency="CHF", fx_role="analytical", scenario_zone="R5.2OECD",
                carbon_price_regime="CH ETS + CO2 levy (CHF120/t)",
                cbam_role="inside-perimeter", phys_vuln_tier="low",
                applied_price_usd=133),
    "RASIA": dict(currency="mixed", fx_role="structural",
                  scenario_zone="R5.2ASIA",
                  carbon_price_regime="mixed (K-ETS, SG tax, rest ~0)",
                  cbam_role="exposed", phys_vuln_tier="med",
                  applied_price_usd=6),
    "ROW": dict(currency="mixed", fx_role="closure",
                scenario_zone="mixed (OECD+REF+ASIA)",
                carbon_price_regime="mixed", cbam_role="mixed",
                phys_vuln_tier="mixed", applied_price_usd=2),
    "LAM": dict(carbon_price_regime="mixed (low; CHL/MEX/COL taxes)"),
}


# --------------------------------------------------------------------------
# region definition, re-derived from the selection algorithm
# --------------------------------------------------------------------------
def region_members():
    """{region: [economies]} exactly as the selection algorithm returns it."""
    d = linkage_by_economy()
    cand = group(d, CANDIDATES)
    kept, _ = select(cand)
    mem = {n: CANDIDATES[n] for n in kept}
    parts, _, _ = split_residual(d, dict(mem))
    mem.update(parts)
    assigned = {c for ms in mem.values() for c in ms}
    mem["ROW"] = sorted(c for c in d.index if c not in assigned)
    assert set(mem) == set(ORDER), f"order mismatch: {set(mem) ^ set(ORDER)}"
    return {r: sorted(mem[r]) for r in ORDER}, d


def build_icio(members, country_to_region):
    src = os.path.join(SRC_DIR, f"{YEAR}_SML.csv")
    print(f"reading {src} ...")
    df = pd.read_csv(src, index_col=0)
    before = df.drop(index="OUT").drop(columns="OUT").to_numpy().sum()

    def relabel(label):
        if label in SPECIAL_ROWS or label == "OUT":
            return label
        c, rest = label.split("_", 1)
        return f"{country_to_region.get(c, 'ROW')}_{rest}"

    df.columns = [relabel(c) for c in df.columns]
    df = df.T.groupby(level=0).sum().T
    df.index = [relabel(r) for r in df.index]
    df = df.groupby(level=0).sum()

    inds = sorted({c.split("_", 1)[1] for c in df.columns
                   if "_" in c and c.split("_", 1)[1] not in FD_CATS})
    ind_rows = [f"{r}_{i}" for r in ORDER for i in inds]
    fd_cols = [f"{r}_{f}" for r in ORDER for f in FD_CATS]
    df = df.loc[ind_rows + SPECIAL_ROWS, ind_rows + fd_cols + ["OUT"]]

    after = df.drop(index="OUT").drop(columns="OUT").to_numpy().sum()
    rel = abs(after - before) / before
    assert rel < 1e-9, f"aggregation did not preserve the total: {rel}"

    z_fd = df.loc[ind_rows, ind_rows + fd_cols].sum(axis=1)
    out_col = df.loc[ind_rows, "OUT"]
    rel_dev = ((z_fd - out_col).abs() / out_col.clip(lower=1.0)).max()
    assert rel_dev < 0.02, f"OUT identity violated: {rel_dev}"

    dest = os.path.join(OUT_DIR, f"ICIO2025_{TAG}_{YEAR}.csv")
    df.to_csv(dest, float_format="%.3f")
    print(f"  wrote {os.path.basename(dest)}  shape={df.shape}  "
          f"total preserved ({after/1e6:,.1f} T$, OUT dev {rel_dev:.2e})")
    return df, inds


def build_ghg(icio, inds, country_to_region):
    src = os.path.join(ROOT, "data", "ghgfp", "SCOPE", f"{YEAR}.csv.gz")
    g = pd.read_csv(src)
    g = g[(g.EMISSIONS_SCOPE == "S1") & (g.TIME_PERIOD == YEAR)]
    c2r = dict(country_to_region)
    c2r["WXD"] = c2r.get("ROW", "ROW")      # GHGFP names the ICIO residual WXD
    unknown = set(g.EMISSIONS_ORIGIN_AREA) - set(c2r)
    assert not unknown, f"areas not mapped: {unknown}"

    g = g.assign(region=g.EMISSIONS_ORIGIN_AREA.map(c2r),
                 tonnes=g.OBS_VALUE * 10.0 ** g.UNIT_MULT)
    e = g.pivot_table(index="ACTIVITY", columns="region", values="tonnes",
                      aggfunc="sum")
    e = e.rename(index={"C241_2431": "C24A", "C242_2432": "C24B",
                        "C30X301": "C302T309"})[ORDER]

    out_row = icio.loc["OUT"]
    rows = {}
    for col, val in out_row.items():
        if col == "OUT" or "_" not in col:
            continue
        r, ind = col.split("_", 1)
        if ind in FD_CATS:
            continue
        rows.setdefault(ind, {})[r] = val
    x = pd.DataFrame(rows).T[ORDER]

    assert set(e.index) == set(x.index), f"industry mismatch: {set(e.index) ^ set(x.index)}"
    e = e.loc[sorted(e.index)]
    x = x.loc[e.index]
    ci = (e / x.replace(0.0, np.nan)).fillna(0.0)

    (e / 1e6).to_csv(os.path.join(OUT_DIR, f"GHG_S1_{TAG}_{YEAR}.csv"),
                     float_format="%.4f")
    ci.to_csv(os.path.join(OUT_DIR, f"CARBON_INTENSITY_{TAG}_{YEAR}.csv"),
              float_format="%.4f")
    print(f"  wrote GHG_S1_{TAG}_{YEAR}.csv and CARBON_INTENSITY_{TAG}_{YEAR}.csv"
          f"  ({len(e)} industries, world {e.to_numpy().sum()/1e9:.1f} Gt)")
    return e, x


def carbon_scope(members):
    """Emissions-weighted carbon-pricing coverage per region (OWID x GHGFP)."""
    owid = pd.read_csv(os.path.join(ROOT, "data", "scope",
                                    "owid_carbon_price_coverage.csv"))
    yr = int(owid.year.max())
    cov = (owid[owid.year == yr].dropna(subset=["code"])
           .set_index("code")["co2_with_tax_or_ets_as_share_of_co2"] / 100.0)
    gf = pd.read_csv(os.path.join(ROOT, "data", "ghgfp", "SCOPE", "2022.csv.gz"))
    gf = gf[(gf.EMISSIONS_SCOPE == "S1") & (gf.TIME_PERIOD == 2022)]
    emis = (gf.assign(t=gf.OBS_VALUE * 10.0 ** gf.UNIT_MULT)
              .groupby("EMISSIONS_ORIGIN_AREA")["t"].sum())
    emis["ROW"] = emis.get("WXD", 0.0)

    rows = {}
    for r, ms in members.items():
        w = cw = 0.0
        n = 0
        for c in ms:
            wi = float(emis.get(c, 0.0))
            cv = 0.0 if c == "ROW" else float(cov.get(c, 0.0))
            w += wi
            cw += wi * cv
            n += cv > 0
        rows[r] = {"carbon_scope": round(cw / w, 3) if w else 0.0,
                   "covered_members": n, "members": len(ms), "owid_year": yr}
    return pd.DataFrame(rows).T.loc[ORDER]


def ppp_weights(members):
    """World Bank PPP GDP shares; ROW is the residual. None if the API fails."""
    api = ("https://api.worldbank.org/v2/country/all/indicator/"
           f"NY.GDP.MKTP.PP.CD?date={YEAR}&format=json&per_page=20000")
    try:
        req = urllib.request.Request(api, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            payload = json.load(r)
    except Exception as exc:                       # offline build
        print(f"  *** WARNING: World Bank API unavailable ({exc}). "
              f"ppp_gdp_weight left BLANK for every region -- re-run when "
              f"online; do not copy the DATA_20R column, the groupings differ.")
        return None
    ppp = {row["countryiso3code"]: float(row["value"]) for row in payload[1]
           if row.get("countryiso3code") and row.get("value") is not None}
    world = ppp["WLD"]
    w = {r: round(sum(ppp.get(c, 0.0) for c in ms) / world, 3)
         for r, ms in members.items() if r != "ROW"}
    w["ROW"] = round(1.0 - sum(w.values()), 3)     # residual absorbs the rest
    return w


def build_carbon_map(members, scope, ppp):
    old = pd.read_csv(os.path.join(D20, "region_carbon_map.csv")).set_index("region")
    cols = ["currency", "fx_role", "scenario_zone", "carbon_price_regime",
            "cbam_role", "phys_vuln_tier", "ppp_gdp_weight", "carbon_scope",
            "applied_price_usd"]
    rows = []
    for r in ORDER:
        rec = {"region": r}
        base = old.loc[r].to_dict() if r in old.index else {}
        rec.update({c: base.get(c) for c in cols})
        rec.update(CARBON_MAP_QUAL.get(r, {}))
        rec["carbon_scope"] = scope.loc[r, "carbon_scope"]
        # PPP weights are region-composition dependent, so a DATA_20R value is
        # WRONG here even where the region name is unchanged (LAM gained Chile,
        # ROW lost most of its members).  Blank the whole column rather than
        # carry a plausible-looking wrong number if the API was unreachable.
        rec["ppp_gdp_weight"] = ppp[r] if ppp else ""
        rows.append(rec)
    cm = pd.DataFrame(rows)[["region"] + cols]
    cm.to_csv(os.path.join(OUT_DIR, "region_carbon_map.csv"), index=False)
    return cm


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    members, d = region_members()
    c2r = {c: r for r, ms in members.items() for c in ms}
    print(f"\n{len(members)} regions, {sum(len(v) for v in members.values())} "
          f"economies allocated\n")
    for r in ORDER:
        print(f"  {r:<6} n={len(members[r]):>2}  {', '.join(members[r])}")

    print()
    icio, inds = build_icio(members, c2r)
    build_ghg(icio, inds, c2r)

    pd.DataFrame({"country": sorted(c2r), "region": [c2r[c] for c in sorted(c2r)]}
                 ).to_csv(os.path.join(OUT_DIR, "region_mapping.csv"), index=False)
    pd.Series(inds, name="industry").to_csv(
        os.path.join(OUT_DIR, "industries.csv"), index=False)
    shutil.copy(os.path.join(D20, "industry_mapping.csv"),
                os.path.join(OUT_DIR, "industry_mapping.csv"))
    print(f"  wrote region_mapping.csv ({len(c2r)} economies), "
          f"industries.csv ({len(inds)}), industry_mapping.csv")

    scope = carbon_scope(members)
    ppp = ppp_weights(members)
    cm = build_carbon_map(members, scope, ppp)
    print(f"  wrote region_carbon_map.csv\n")
    print(cm.to_string(index=False))
    return members, icio, cm


if __name__ == "__main__":
    main()
