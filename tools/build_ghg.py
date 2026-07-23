"""
Build the 12-region Scope-1 emissions and direct carbon-intensity tables for
2022 - the inputs for the transition-risk charge ct_direct in the
multi-regional BKMN model (paper Eq. 6: E_direct = CI x output).

Inputs
  data/ghgfp/SCOPE/2022.csv.gz      GHGFP 2025: emissions by scope (Mt CO2e,
                                    OBS_VALUE x 10^UNIT_MULT tonnes), filtered
                                    to EMISSIONS_SCOPE == "S1"
  DATA_12R/ICIO2025_12R_2022.csv    gross output x (OUT row, current USD m)
  DATA_12R/region_mapping.csv       the 81-economy -> 12-region map

Outputs (DATA_12R/)
  GHG_S1_12R_2022.csv               Scope-1 emissions, Mt CO2e
                                    rows = 50 industries, cols = 12 regions
  CARBON_INTENSITY_12R_2022.csv     CI = tonnes CO2e per million USD of gross
                                    output, same shape (multi-region Table 2)

Unit note for the model: with CI in t/MUSD and a carbon price XCE in USD/t,
the per-output charge rate is ct = CI * XCE * 1e-6 (fraction of output value).
"""

import os
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D12 = os.path.join(ROOT, "DATA_12R")
YEAR = 2022

REGIONS = ["EU27", "USA", "CHN", "GBR", "JPN", "IND", "CAN", "NOR", "IDN",
           "MEA", "AFR", "ROW"]
FD_CATS = {"HFCE", "NPISH", "GGFC", "GFCF", "INVNT", "DPABR"}


def load_s1() -> pd.DataFrame:
    """Scope-1 emissions per region x industry, in tonnes CO2e."""
    src = os.path.join(ROOT, "data", "ghgfp", "SCOPE", f"{YEAR}.csv.gz")
    df = pd.read_csv(src)
    df = df[(df["EMISSIONS_SCOPE"] == "S1") & (df["TIME_PERIOD"] == YEAR)]

    mapping = pd.read_csv(os.path.join(D12, "region_mapping.csv"))
    region_of = dict(zip(mapping["country"], mapping["region"]))
    # GHGFP labels the rest-of-world residual WXD where ICIO uses ROW
    # (verified 2022: 4.3 Gt, sector mix consistent with undisclosed economies)
    region_of["WXD"] = "ROW"
    unknown = set(df["EMISSIONS_ORIGIN_AREA"]) - set(region_of)
    assert not unknown, f"areas not in region mapping: {unknown}"

    df["region"] = df["EMISSIONS_ORIGIN_AREA"].map(region_of)
    df["tonnes"] = df["OBS_VALUE"] * 10.0 ** df["UNIT_MULT"]
    out = df.pivot_table(index="ACTIVITY", columns="region", values="tonnes",
                         aggfunc="sum")
    # GHGFP names the 2025-edition industry splits by ISIC detail where ICIO
    # uses letter suffixes; same content, different codes:
    out = out.rename(index={"C241_2431": "C24A",     # basic iron & steel
                            "C242_2432": "C24B",     # non-ferrous metals
                            "C30X301": "C302T309"})  # transport eq. excl. ships
    return out[REGIONS]


def load_output() -> pd.DataFrame:
    """Gross output x per region x industry (USD millions) from the 12R ICIO."""
    icio = pd.read_csv(os.path.join(D12, f"ICIO2025_12R_{YEAR}.csv"), index_col=0)
    out_row = icio.loc["OUT"]
    rows = {}
    for col, val in out_row.items():
        if col == "OUT" or "_" not in col:
            continue
        region, industry = col.split("_", 1)
        if industry in FD_CATS:
            continue
        rows.setdefault(industry, {})[region] = val
    x = pd.DataFrame(rows).T
    return x[REGIONS]


def main():
    e = load_s1()          # tonnes
    x = load_output()      # USD millions

    # align industries (GHGFP uses the same 50 ICIO industry codes)
    assert set(e.index) == set(x.index), (
        f"industry mismatch: {set(e.index) ^ set(x.index)}")
    e = e.loc[sorted(e.index)]
    x = x.loc[e.index]

    ci = e / x.replace(0.0, np.nan)          # tonnes per USD million
    ci = ci.fillna(0.0)

    (e / 1e6).to_csv(os.path.join(D12, f"GHG_S1_12R_{YEAR}.csv"),
                     float_format="%.4f")
    ci.to_csv(os.path.join(D12, f"CARBON_INTENSITY_12R_{YEAR}.csv"),
              float_format="%.4f")

    print(f"industries: {len(e.index)}, regions: {list(e.columns)}")
    print(f"world S1 total {YEAR}: {e.to_numpy().sum()/1e9:.1f} Gt CO2e")
    print("\nregional S1 totals (Mt):")
    print((e.sum(axis=0) / 1e6).round(0).to_string())
    print("\ntop-10 carbon intensities (t/MUSD):")
    flat = ci.stack().sort_values(ascending=False).head(10)
    print(flat.round(1).to_string())
    print("\nUK sample (t/MUSD): A01 agriculture "
          f"{ci.loc['A01','GBR']:.0f}, D electricity {ci.loc['D','GBR']:.0f}, "
          f"K finance {ci.loc['K','GBR']:.1f}")


if __name__ == "__main__":
    main()
