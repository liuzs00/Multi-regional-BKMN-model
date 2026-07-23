"""
Build the 12-region ICIO tables for the multi-regional BKMN project.

Input : OECD ICIO 2025 edition, YYYY_SML.csv (81 economies x 50 industries,
        current USD millions), extracted at D:\\Download\\2016-2022_SML\\
Output: DATA_12R/ICIO2025_12R_YYYY.csv  - aggregated 12-region tables
        DATA_12R/region_mapping.csv     - country -> region map used
        DATA_12R/industries.csv         - the 50 ISIC Rev.4 industry codes

Regions (2026-07 FX/CBAM/physical-damage redesign): EU27 (base currency), USA,
CHN, GBR, JPN, IND, CAN, NOR, IDN as single-currency FX-analytical regions;
MEA (Middle East) and AFR (Africa) as structural aggregates; and ROW (all
remaining economies + the ICIO's own RoW, summed) to close global accounting.

Aggregation is plain summation of flows (valid for current-price IO tables).
Row/column layout of the output mirrors the ICIO original:
    rows: 12 regions x 50 industries, then TLS, VA, OUT
    cols: 12 regions x 50 industries, then 12 regions x 6 FD categories, OUT
"""

import os
import sys
import numpy as np
import pandas as pd

SRC_DIR = r"D:\2016-2022_SML"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "DATA_12R")
YEARS = range(2016, 2023)

# 12-region selection (2026-07 FX + CBAM + physical-damage redesign):
# single-currency FX-analytical regions, two structural aggregates
# (MEA = Middle East, AFR = Africa), and ROW closure.  EU27 is the FX base.
REGION_MEMBERS = {
    "EU27": ["AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN",
             "FRA", "DEU", "GRC", "HUN", "IRL", "ITA", "LVA", "LTU", "LUX",
             "MLT", "NLD", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"],
    "USA": ["USA"], "CHN": ["CHN"], "GBR": ["GBR"], "JPN": ["JPN"],
    "IND": ["IND"], "CAN": ["CAN"], "NOR": ["NOR"], "IDN": ["IDN"],
    "MEA": ["SAU", "ARE", "ISR", "JOR"],                              # Middle East
    "AFR": ["ZAF", "EGY", "MAR", "TUN", "NGA", "SEN", "CIV", "CMR",   # Africa
            "COD", "AGO", "STP"],
}

# output region order; ROW (all remaining economies + ICIO's own RoW) closes it
REGIONS = ["EU27", "USA", "CHN", "GBR", "JPN", "IND", "CAN", "NOR", "IDN",
           "MEA", "AFR", "ROW"]

FD_CATS = ["HFCE", "NPISH", "GGFC", "GFCF", "INVNT", "DPABR"]
SPECIAL_ROWS = ["TLS", "VA", "OUT"]

_COUNTRY_TO_REGION = {c: r for r, cs in REGION_MEMBERS.items() for c in cs}


def region_of(country: str) -> str:
    return _COUNTRY_TO_REGION.get(country, "ROW")


def map_label(label: str) -> str:
    """Map an ICIO row/col label 'CCC_rest' -> 'REGION_rest'; specials pass through."""
    if label in SPECIAL_ROWS or label == "OUT":
        return label
    country, rest = label.split("_", 1)
    return f"{region_of(country)}_{rest}"


def build_year(year: int) -> None:
    src = os.path.join(SRC_DIR, f"{year}_SML.csv")
    print(f"[{year}] reading {src} ...")
    df = pd.read_csv(src, index_col=0)

    total_before = df.drop(index="OUT").drop(columns="OUT").to_numpy().sum()

    # aggregate columns then rows by mapped label
    df.columns = [map_label(c) for c in df.columns]
    df = df.T.groupby(level=0).sum().T
    df.index = [map_label(r) for r in df.index]
    df = df.groupby(level=0).sum()

    # canonical ordering
    industries = sorted({c.split("_", 1)[1] for c in df.columns
                         if "_" in c and c.split("_", 1)[1] not in FD_CATS})
    ind_rows = [f"{r}_{i}" for r in REGIONS for i in industries]
    ind_cols = ind_rows
    fd_cols = [f"{r}_{f}" for r in REGIONS for f in FD_CATS]
    df = df.loc[ind_rows + SPECIAL_ROWS, ind_cols + fd_cols + ["OUT"]]

    # sanity: aggregation must preserve the global total exactly (mod fp noise)
    total_after = df.drop(index="OUT").drop(columns="OUT").to_numpy().sum()
    rel_err = abs(total_after - total_before) / total_before
    assert rel_err < 1e-9, f"sum not preserved: {rel_err}"

    # sanity: OUT column ~= row sums of Z + FD for industry rows.
    # The OECD source itself carries small imbalances (verified: e.g. USA_L
    # off by 17.5 MUSD in 2016_SML.csv; worst relative case is Malta C24B at
    # ~1.6%), and linear aggregation passes them through unchanged.  We keep
    # OECD's published OUT and only assert a loose bound to catch real bugs.
    z_fd = df.loc[ind_rows, ind_cols + fd_cols].sum(axis=1)
    out_col = df.loc[ind_rows, "OUT"]
    rel_dev = ((z_fd - out_col).abs() / out_col.clip(lower=1.0)).max()
    max_dev = (z_fd - out_col).abs().max()
    assert rel_dev < 0.02, f"OUT identity badly violated: rel {rel_dev}"
    print(f"[{year}] source OUT imbalance passed through: "
          f"max {max_dev:.1f} MUSD, rel {rel_dev:.2e}")

    dest = os.path.join(OUT_DIR, f"ICIO2025_12R_{year}.csv")
    df.to_csv(dest, float_format="%.3f")
    print(f"[{year}] wrote {dest}  shape={df.shape}  "
          f"global total {total_after/1e6:,.1f} T$  (preserved, OUT dev<{max_dev:.3f}M$)")


def write_metadata(sample_year: int = 2022) -> None:
    src = os.path.join(SRC_DIR, f"{sample_year}_SML.csv")
    header = pd.read_csv(src, index_col=0, nrows=0)
    countries = sorted({c.split("_", 1)[0] for c in header.columns if "_" in c})
    mapping = pd.DataFrame({"country": countries,
                            "region": [region_of(c) for c in countries]})
    mapping.to_csv(os.path.join(OUT_DIR, "region_mapping.csv"), index=False)

    industries = sorted({c.split("_", 1)[1] for c in header.columns
                         if "_" in c and c.split("_", 1)[1] not in FD_CATS})
    pd.Series(industries, name="industry").to_csv(
        os.path.join(OUT_DIR, "industries.csv"), index=False)
    print(f"wrote region_mapping.csv ({len(countries)} countries) and "
          f"industries.csv ({len(industries)} industries)")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    write_metadata()
    years = YEARS if "--all" in sys.argv else YEARS
    for y in years:
        build_year(y)
    print("done.")
