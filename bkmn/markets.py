"""
Financial-market impact modules (Sections 2.6 - 2.11):

  inflation        carbon-price -> inflation shift          (2.6)
  short_rate       Taylor-rule policy-rate shock            (2.7)
  rate_term_shift  Hull-White 1F zero-rate shift, Prop 2    (2.8)
  cds_equity_shock GVA -> CDS spread / equity shifts        (2.9)
  oprisk_shock     GDP/unemployment -> operational losses   (2.11)
"""

import numpy as np

from . import data
from . import assumptions as cfg


# ---------------------------------------------------------------------------
# 2.6 Inflation
# ---------------------------------------------------------------------------
def inflation_shift(delta_xce: float, scope: float = cfg.CARBON_SCOPE) -> float:
    """
    Climate inflation shift (Section 2.6):
        dPi = (0.08% / $10) * dXCE * scope
    `delta_xce` is the change in carbon price; scope is the fraction of
    emissions priced.  Returned as a decimal (e.g. 0.004 = 40bp).
    """
    return cfg.INFLATION_PER_10USD * (delta_xce / 10.0) * scope


# ---------------------------------------------------------------------------
# 2.7 Short rate via Taylor rule
# ---------------------------------------------------------------------------
def policy_rate_shock(delta_inflation: float, delta_gdp: float) -> float:
    """
    Taylor-rule policy-rate shock (Section 2.7):
        dr_policy = phi_Pi * dPi + phi_Y * dY
    dY is the (log) GDP change.  Both arguments are decimals.
    """
    return cfg.PHI_PI * delta_inflation + cfg.PHI_Y * delta_gdp


# ---------------------------------------------------------------------------
# 2.8 Long-term rate shift (Hull-White 1F, Proposition 2)
# ---------------------------------------------------------------------------
def hw_B(tau: float, a: float = cfg.HW_A) -> float:
    """B(t,T) = (1 - e^{-a*tau}) / a, tau = T - t."""
    if a == 0:
        return tau
    return (1.0 - np.exp(-a * tau)) / a


def rate_term_shift(delta_r: float, tau: float, a: float = cfg.HW_A) -> float:
    """
    Zero-coupon rate shift at relative maturity tau (Proposition 2):
        dR(t,T) = B(t,T)/tau * dr(t)
    As tau -> 0 this tends to dr (the short-rate shift). sigma-independent.
    """
    if tau <= 0:
        return delta_r
    return hw_B(tau, a) / tau * delta_r


# ---------------------------------------------------------------------------
# 2.9 Equity & CDS shifts from sector GVA shocks
# ---------------------------------------------------------------------------
def synthetic_gva_relative_change(gva_rel_shock: np.ndarray) -> dict:
    """
    Map the 20-sector relative GVA shock onto CDS sectors + FTSE using the
    Table 8 weights:  dV_j^CDS / V_j^CDS  (Section 3.1.3).

    V_j = sum_i w_ij GVA_i ;  dV_j = sum_i w_ij (GVA_i * shock_i).
    Returns dict {cds_sector or 'FTSE': relative change}.
    """
    W = data.mapping_matrix()                 # 20 x 13 (cols = CDS + FTSE)
    gva = data.vector(data.GVA)
    cols = data.CDS_SECTORS + ["FTSE"]

    V = W.T @ gva                              # synthetic GVA level per column
    dV = W.T @ (gva * gva_rel_shock)          # synthetic GVA change per column
    out = {}
    for k, name in enumerate(cols):
        out[name] = (dV[k] / V[k]) if V[k] != 0 else 0.0
    return out


def cds_shock(gva_rel_shock: np.ndarray) -> dict:
    """
    Relative CDS spread shift per CDS sector (Section 2.9):
        dCDS_j / CDS_j = beta1_j * dV_j^CDS / V_j^CDS
    """
    rel = synthetic_gva_relative_change(gva_rel_shock)
    out = {}
    for sector, (_b0, b1, _r2) in data.CDS_REG.items():
        out[sector] = b1 * rel[sector]
    return out


def equity_shock(gva_rel_shock: np.ndarray) -> float:
    """FTSE100 relative equity shift = beta1_FTSE * dV_FTSE / V_FTSE."""
    rel = synthetic_gva_relative_change(gva_rel_shock)
    _b0, b1, _r2 = data.FTSE_REG
    return b1 * rel["FTSE"]


# ---------------------------------------------------------------------------
# 2.11 Operational risk via macro factors
# ---------------------------------------------------------------------------
def unemployment_change(delta_inflation: float, delta_gdp: float) -> float:
    """
    Combined Phillips + Okun unemployment change (Section 2.11):
        dU = -beta * dPi + kappa * dY
    With UK calibration beta=0, kappa=-0.182.  dY is GDP growth change.
    """
    return -cfg.PHILLIPS_BETA * delta_inflation + cfg.OKUN_KAPPA * delta_gdp


def oprisk_shock(delta_inflation: float, delta_gdp: float,
                 base_unemployment: float = 0.04) -> dict:
    """
    Relative change in operational-risk losses by event type (Section 2.11):
        dOpRisk_i / OpRisk_i = beta1_i * dU / U
    """
    dU = unemployment_change(delta_inflation, delta_gdp)
    rel_U = dU / base_unemployment
    out = {}
    for risk_type, (_b0, b1, _r2) in data.OPRISK_REG.items():
        out[risk_type] = b1 * rel_U
    return out
