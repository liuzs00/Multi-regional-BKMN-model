"""
Observed market base curves (Bank of England GLC data, single snapshot).

  * Nominal GBP spot curve   -> data/gbp_nominal_spot_curve.csv
  * Implied inflation curve   -> data/gbp_inflation_spot_curve.csv

Each is (maturity_years, rate_pct) at one observation date.  The model reports
climate *shifts*; these curves let it also report *absolute stressed levels*
(base + shift).  Interpolation is linear in maturity; outside the node range the
nearest endpoint is used (np.interp clamps), which is fine for the short end.
"""

import os
import numpy as np
import pandas as pd

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _load(fname):
    df = pd.read_csv(os.path.join(_DATA_DIR, fname)).sort_values("maturity_years")
    return df["maturity_years"].to_numpy(), df["rate_pct"].to_numpy()


_NOM_M, _NOM_R = _load("gbp_nominal_spot_curve.csv")
_INF_M, _INF_R = _load("gbp_inflation_spot_curve.csv")


def nominal_spot(maturity_years: float) -> float:
    """Observed nominal GBP spot rate (%) at a maturity (linear interp / clamp)."""
    return float(np.interp(maturity_years, _NOM_M, _NOM_R))


def inflation_spot(maturity_years: float) -> float:
    """Observed implied inflation (%) at a maturity (curve starts ~2.5y)."""
    return float(np.interp(maturity_years, _INF_M, _INF_R))
