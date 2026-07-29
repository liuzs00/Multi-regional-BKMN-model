"""
Phase P — physical risk (paper §2.5), generalised to the multi-region grid.

Damage function (Eq 11, Barrage & Nordhaus):  Ω(ΔT) = 0.003467 · ΔT²
  = fraction of *world* GDP lost at incremental warming ΔT (vs the base year).

Proposition 1, applied at world level across all 1000 region-sectors:

    VL(r,i) = pattern(i) × scale(r)      pattern = paper Table 6 (health = 1)
                                         scale   = ND-GAIN region vulnerability
    α(t)    = Ω(ΔT(t)) / Σ_i VL_i · f_i  ,  f_i = GVA_i / world GDP
    direct    : ΔGVA_i / GVA_i = − VL_i · α(t)
    cascading : ct_i += VL_i · α(t)      (fed through the same Leontief operator)

Per-region damage then *emerges* from aggregation: vulnerable regions lose more
for the same global ΔT.  The allocation identity Σ_i f_i·VL_i·α = Ω(ΔT) holds by
construction (tested to machine precision).

Design note (flagged in docs/EXT_PLAN.md): the paper is single-region, so
applying Prop 1 world-wide is our generalisation choice — Ω is a *world* GDP
damage and vulnerability is relative across the whole grid, not within a region.
"""
import os

import numpy as np
import pandas as pd

from .paper_tables import PATTERN_ICIO

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Eq 11 is written as 1.6768/(2.2 x 2.2) x dT^2, where 1.6768 is the GDP damage
# at 2.2 C **in per cent**; the paper's own Eq 13/14 spell the fraction form out
# as 0.003467.  Dropping the 1/100 makes Omega(2.2 C) = 168% of GDP.
DAMAGE_COEF = 1.6768e-2 / (2.2 ** 2)   # 0.003467 — Barrage & Nordhaus (Eq 11)
DAMAGE_COEF_SR = 8.5e-2 / (2.2 ** 2)   # 0.017562 — SwissRe variant (Eq 12)


def omega(delta_T, coef=DAMAGE_COEF):
    """Fraction of world GDP lost at incremental warming ΔT (°C)."""
    return coef * delta_T ** 2


def vl_vector(m):
    """VL per region-sector = Table-6 sector pattern × ND-GAIN region scale."""
    scale = pd.read_csv(os.path.join(ROOT, "data", "physical", "vl_scale_20R.csv"),
                        index_col=0)["scale"]
    return np.array([PATTERN_ICIO[i] * scale[r]
                     for i, r in zip(m.industry_of, m.region_of)], float)


def alpha(m, delta_T, vl=None, coef=DAMAGE_COEF):
    """Prop-1 scale factor α(t) = Ω(ΔT) / Σ_i VL_i·f_i (world GDP weights)."""
    vl = vl_vector(m) if vl is None else vl
    f = m.gva / m.gva.sum()
    return omega(delta_T, coef) / float(np.dot(vl, f))


def direct_shock(m, delta_T, vl=None, coef=DAMAGE_COEF):
    """Per-sector relative GVA damage (negative): −VL_i · α(t)."""
    vl = vl_vector(m) if vl is None else vl
    return -vl * alpha(m, delta_T, vl, coef)


def tax_addon(m, delta_T, vl=None, coef=DAMAGE_COEF):
    """Cascading form: the VL_i·α(t) term added to the per-output tax rate."""
    vl = vl_vector(m) if vl is None else vl
    return vl * alpha(m, delta_T, vl, coef)


def region_damage(m, delta_T, vl=None, coef=DAMAGE_COEF):
    """GVA-weighted relative damage per region (fraction, negative)."""
    d = direct_shock(m, delta_T, vl, coef)
    return {r: float((d * m.gva)[m.region_of == r].sum() / m.gva[m.region_of == r].sum())
            for r in m.regions_order}
