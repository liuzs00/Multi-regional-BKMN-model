"""
Phase O — bank operational-risk losses (paper §2.11).

Okun's law (Phillips β = 0, as the paper assumes for the UK):
    ΔU_r = κ_r · ΔY_r                      κ from data/macro/okun_kappa.csv
Loss-frequency regression (paper Table 10, log Λ = β0 + β1·log U):
    ΔOpRisk_i / OpRisk_i = β1_i · ΔU_r / U_r      i ∈ {Conduct, Execution}

Base unemployment U_r is the 2022 labour-force-weighted regional rate
(data/macro/unemployment_20R.csv, World Bank).  β1 are the paper's UK-calibrated
slopes [PROXY] — region-specific calibration needs licensed ORX loss data.
"""
import os

import pandas as pd

from . import regions
from .paper_tables import OPRISK_BETA

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAPPA_DEFAULT = -0.30      # advanced-economy Okun default, for regions with no row


def kappa():
    """Okun slope per region; regions absent from the table take the default."""
    k = pd.read_csv(os.path.join(ROOT, "data", "macro", "okun_kappa.csv"),
                    index_col=0)["kappa"]
    cm = pd.read_csv(os.path.join(regions.DATA, "region_carbon_map.csv"))
    return pd.Series({r: float(k.get(r, KAPPA_DEFAULT)) for r in cm.region})


def base_unemployment():
    return pd.read_csv(regions.aux("macro", "unemployment"),
                       index_col=0)["unemployment_2022"] / 100.0


def unemployment_change(gdp_shock_by_region, kap=None):
    """ΔU_r = κ_r · ΔY_r  (κ<0, ΔY<0 ⇒ unemployment rises)."""
    kap = kappa() if kap is None else kap
    return {r: kap[r] * s for r, s in gdp_shock_by_region.items()}


def oprisk_shift(gdp_shock_by_region, kap=None, u0=None):
    """{region: {event type: relative change in losses}}."""
    u0 = base_unemployment() if u0 is None else u0
    dU = unemployment_change(gdp_shock_by_region, kap)
    return {r: {k: b1 * (dU[r] / u0[r]) for k, b1 in OPRISK_BETA.items()}
            for r in dU}
