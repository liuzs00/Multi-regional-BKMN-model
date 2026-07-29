"""
Phase E — equity index shifts (paper §2.9), region-headline-index level.

Paper model:  log(S_j) = β0 + β1·log(GVA_j)   ⇒   ΔS/S = β1 · ΔGVA/GVA.

β1 is calibrated per region by regressing the log of the region's headline
equity index on the log of its GDP (annual, ~2000-2023), both from free sources
(Yahoo chart API / World Bank).  Regions without a free index series (CHL, KAZ)
or with an implausible fit fall back to the paper's FTSE-100 slope β = 2.00
[PROXY, Table 9].  Calibration R² is reported — the paper's own Table 9 is
candid that these regressions are weak (FTSE R² = 74%, most CDS sectors < 30%).
"""
import os

import numpy as np
import pandas as pd

from .paper_tables import EQUITY_BETA

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BETA_MIN, BETA_MAX = 0.2, 6.0          # plausibility band; outside -> proxy


def _region_gdp():
    gdp = pd.read_csv(os.path.join(ROOT, "data", "macro",
                                   "wb_gdp_current_usd_2000_2023.csv"))
    mapping = pd.read_csv(os.path.join(ROOT, "DATA_20R", "region_mapping.csv"))
    m = dict(zip(mapping.country, mapping.region))
    gdp = gdp.dropna(subset=["value"]).copy()
    gdp["region"] = gdp.code.map(m)
    return (gdp.dropna(subset=["region"])
               .groupby(["region", "year"]).value.sum().unstack("year"))


def calibrate(verbose=False):
    """Return {region: (beta, r2, source)} — 'fit' or 'proxy'."""
    px = pd.read_csv(os.path.join(ROOT, "data", "equity", "index_history.csv"),
                     parse_dates=["date"])
    px["year"] = px.date.dt.year
    annual = px.groupby(["region", "year"]).close.mean().unstack("year")
    gdp = _region_gdp()

    out = {}
    for r in annual.index:
        if r not in gdp.index:
            continue
        yrs = [y for y in annual.columns
               if y in gdp.columns and np.isfinite(annual.loc[r, y])
               and np.isfinite(gdp.loc[r, y]) and gdp.loc[r, y] > 0]
        if len(yrs) < 8:
            continue
        x = np.log(gdp.loc[r, yrs].to_numpy(float))
        y = np.log(annual.loc[r, yrs].to_numpy(float))
        b1, b0 = np.polyfit(x, y, 1)
        r2 = float(np.corrcoef(x, y)[0, 1] ** 2)
        ok = BETA_MIN <= b1 <= BETA_MAX
        out[r] = (float(b1) if ok else EQUITY_BETA, r2, "fit" if ok else "proxy")
        if verbose:
            print(f"  {r:5s} beta={b1:6.2f}  R2={r2:5.2f}  n={len(yrs):2d}  "
                  f"{'fit' if ok else 'PROXY (out of band)'}")
    return out


def betas():
    """β per region for all 20 regions (proxy where no calibration exists)."""
    cal = calibrate()
    cm = pd.read_csv(os.path.join(ROOT, "DATA_20R", "region_carbon_map.csv"))
    return {r: cal.get(r, (EQUITY_BETA, float("nan"), "proxy"))[0] for r in cm.region}


def equity_shift(gdp_shock_by_region, beta_by_region):
    """ΔS/S = β · ΔGVA/GVA per region (fraction)."""
    return {r: beta_by_region[r] * s for r, s in gdp_shock_by_region.items()}


if __name__ == "__main__":
    print("equity beta calibration (log index ~ log GDP, annual):")
    calibrate(verbose=True)
