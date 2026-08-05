"""
Phase 1 — transition core generalised to PER-REGION carbon prices.

Same modified-Leontief-dual maths as compute_transition.py (paper Eq 8/10), but
the carbon charge vector is built from a per-region XCE(t) instead of a flat $70:

    ct_j = CI_j · XCE(region of j) · 1e-6

Because Eq 10 is linear in ct for a fixed φ, we precompute the operator
    M(φ) = (I − Aᵀ)·L̃(φ) − I + φ̂      (one inversion)
and then every scenario/horizon is a cheap matvec  dV = x · (M @ ct).

Reduction guarantee (tests/test_fx.py): with XCE ≡ 70 everywhere this reproduces
out_gva_shock_by_region_phi.csv exactly.
"""
import numpy as np


def technical_matrix(m):
    return m.Z / np.where(m.x == 0, 1.0, m.x)[None, :]


def gva_operator(m, phi):
    """M(φ) such that per-sector ΔV = x · (M @ ct_direct). One inversion."""
    A = technical_matrix(m)
    n = len(m.x)
    I = np.eye(n)
    AT = A.T
    Ltil = np.linalg.inv(I - phi * AT) * phi          # modified Leontief dual
    return (I - AT) @ Ltil - I + phi * I


def price_operator(m, phi):
    """Modified Leontief dual L~(phi) = (I - A^T phi_hat)^-1 phi_hat (Eq 8)."""
    A = technical_matrix(m)
    n = len(m.x)
    return np.linalg.inv(np.eye(n) - phi * A.T) * phi


def ct_direct(m, xce_by_region):
    """Per-sector carbon charge (fraction of output): CI · XCE(region) · 1e-6."""
    xce = np.array([xce_by_region[r] for r in m.region_of], float)
    return m.ci * xce * 1e-6


def sector_dV(m, M, xce_by_region):
    """Absolute per-sector value-added change (USD m)."""
    return m.x * (M @ ct_direct(m, xce_by_region))


def region_shock_from_ct(m, M, ct):
    """GDP-weighted relative GVA shock per region, from any charge vector."""
    dV = m.x * (M @ ct)
    return {r: dV[m.region_of == r].sum() / m.gva[m.region_of == r].sum()
            for r in m.regions_order}


def region_gdp_shock(m, M, xce_by_region):
    """GDP-weighted relative GVA shock per region (fraction)."""
    return region_shock_from_ct(m, M, ct_direct(m, xce_by_region))
