"""
Phase V — within-scenario volatility (paper §3.3): turns each scenario's point
path into a band, giving climate FX-at-risk / PFE-style quantiles.

Two uncertainty sources, both from data already downloaded:

  temperature σ(t)  from the MAGICC percentile fan:
        σ ≈ (p90 − p10) / (2 · 1.2816)          (Gaussian ΔT, per §3.3)
  carbon-price σ(t) from the NGFS **cross-model spread** (MESSAGEix, REMIND,
        GCAM run the same scenario), per scenario × zone × year.  The paper
        instead tabulates RCP-level σ (Table 15); the cross-model spread is the
        NGFS-native analogue.

Method (the paper's own §4.3 simplification): stress the *inputs* by z_q·σ and
re-run the chain.  This is exact for a monotone chain — Eq 10 is linear in XCE
and Ω is monotone in ΔT — so quantile-of-output = output-of-quantile-input.
"""
import os

import numpy as np
import pandas as pd

from .scenarios import USD2010_TO_USD2022, ZONE_OF_R5, _annualise

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGFS = os.path.join(ROOT, "data", "ngfs")
Z1289 = 1.2815515655446004      # Φ⁻¹(0.90)


def temperature_sigma():
    """σ of GSAT (K) per scenario × year, from the p10/p90 fan."""
    lo = _annualise(pd.read_csv(f"{NGFS}/temperature_gsat_p10.csv")
                    .assign(column=lambda d: d.scenario))
    hi = _annualise(pd.read_csv(f"{NGFS}/temperature_gsat_p90.csv")
                    .assign(column=lambda d: d.scenario))
    return (hi - lo) / (2 * Z1289)


def carbon_price_sigma():
    """σ of the carbon price (US$2022/t) per scenario × zone × year, across IAMs."""
    frames = []
    for tag in ("", "_remind", "_gcam"):
        d = pd.read_csv(f"{NGFS}/price_carbon_r5{tag}.csv")
        d["column"] = list(zip(d.scenario, d.region.map(ZONE_OF_R5)))
        w = _annualise(d) * USD2010_TO_USD2022
        w.columns = pd.MultiIndex.from_tuples(w.columns, names=["scenario", "zone"])
        frames.append(w)
    common = frames[0].columns
    for f in frames[1:]:
        common = common.intersection(f.columns)
    stack = np.stack([f[common].to_numpy(float) for f in frames])
    return pd.DataFrame(stack.std(axis=0, ddof=1), index=frames[0].index,
                        columns=common)


def stress(central, sigma, z):
    """Shift a path by z standard deviations (clipped at zero for prices)."""
    return np.maximum(central + z * sigma, 0.0)
