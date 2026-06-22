"""
Sector economy: Input-Output core, transition risk (CO2 tax as cost) and
physical risk (GDP damage + sector vulnerability).

Notation follows the paper (Section 2.3-2.5).
  Z      inter-industry flows (M GBP)
  x      total output per sector (M GBP)
  GVA    value added per sector (M GBP)
  A      = Z @ diag(1/x)          technical coefficients (column-normalised)
  ct_j   = CI_j * XCE * 1e-3      carbon charge per unit of output
"""

import numpy as np

from . import data
from . import assumptions as cfg


# ---------------------------------------------------------------------------
# Input-Output primitives
# ---------------------------------------------------------------------------
def technical_matrix():
    """A = Z x^{-1} (Eq 2).  A[i,j] = Z[i,j] / x_j."""
    Z = data.Z_matrix()
    x = data.vector(data.TOTAL_OUTPUT)
    return Z @ np.diag(1.0 / x)


def carbon_charge_per_output(xce: float) -> np.ndarray:
    """
    ct_direct (Eq 6, scaled by output): ct_j = CI_j * XCE * 1e-3.

    The 1e-3 factor reconciles the Table 2 carbon-intensity units with the
    Table 4 results (emissions are effectively kilo-tonnes per M GBP).
    """
    ci = data.vector(data.CARBON_INTENSITY)
    return ci * xce * 1e-3


# ---------------------------------------------------------------------------
# Transition risk  (Section 2.4) -> reproduces Table 4
# ---------------------------------------------------------------------------
def gva_relative_shock_transition(xce: float, phi: float) -> np.ndarray:
    """
    Relative GVA shock per sector from introducing a carbon tax `xce`
    with uniform pass-through `phi`.

    Implements Eq 8 & Eq 10:
        L_tilde(phi) = (I - A^T phi_hat)^{-1} phi_hat        (modified Leontief dual)
        dv           = [ (I - A^T) L_tilde(phi) - I + phi_hat ] ct_direct
        dV_j         = x_j * dv_j
        return        dV_j / GVA_j

    Sanity (paper): phi=0 -> dV = -CT_direct ; phi=1 -> dV = +CT_direct.
    """
    A = technical_matrix()
    x = data.vector(data.TOTAL_OUTPUT)
    gva = data.vector(data.GVA)
    ct = carbon_charge_per_output(xce)

    n = data.N
    I = np.eye(n)
    phi_hat = np.diag(np.full(n, phi))

    L_tilde = np.linalg.inv(I - A.T @ phi_hat) @ phi_hat
    dv = ((I - A.T) @ L_tilde - I + phi_hat) @ ct
    dV = x * dv
    return dV / gva


# ---------------------------------------------------------------------------
# Physical risk  (Section 2.5)
# ---------------------------------------------------------------------------
def gdp_damage_fraction(delta_T: float, coef: float = cfg.DAMAGE_COEF_BN) -> float:
    """Omega(dT) = coef * dT^2  (Eq 11). Fraction of GDP lost."""
    return coef * delta_T ** 2


def gva_relative_shock_physical(delta_T: float, cascading: bool = False):
    """
    Sector GVA shocks from physical (temperature) damage, allocated by
    vulnerability (Proposition 1).

        alpha = Omega(dT) / sum_i (VL_i * f_i),     f_i = GVA_i / GDP
        dGVA_i / GVA_i (direct) = VL_i * alpha

    Returns (relative_shock_vector, alpha).  Direct effects are negative
    (damage reduces GVA).  `cascading` adds VL*alpha into the tax rate, handled
    by the caller; here we return the direct sector shock.
    """
    vl = data.vector(data.VULNERABILITY)
    gva = data.vector(data.GVA)
    gdp = gva.sum()
    f = gva / gdp

    omega = gdp_damage_fraction(delta_T)
    alpha = omega / np.sum(vl * f)
    direct = -vl * alpha            # negative: GVA falls
    return direct, alpha


def physical_tax_addon(delta_T: float) -> np.ndarray:
    """
    Cascading physical effect expressed as an addition to the per-output tax
    rate (Proposition 1): VL_i * alpha, fed back through the Leontief dual so
    it cascades like the carbon tax.
    """
    vl = data.vector(data.VULNERABILITY)
    _, alpha = gva_relative_shock_physical(delta_T)
    return vl * alpha


# ---------------------------------------------------------------------------
# Combined sector GVA shock (transition + physical), used downstream
# ---------------------------------------------------------------------------
def gva_relative_shock(xce: float, phi: float, delta_T: float,
                       include_physical: bool = True) -> np.ndarray:
    """Total relative GVA shock per sector = transition (+ physical)."""
    shock = gva_relative_shock_transition(xce, phi)
    if include_physical:
        direct, _ = gva_relative_shock_physical(delta_T)
        shock = shock + direct
    return shock


def gdp_relative_shock(xce: float, phi: float, delta_T: float,
                       include_physical: bool = True) -> float:
    """GDP-weighted aggregate of the sector GVA shocks."""
    gva = data.vector(data.GVA)
    w = gva / gva.sum()
    return float(np.dot(w, gva_relative_shock(xce, phi, delta_T, include_physical)))
