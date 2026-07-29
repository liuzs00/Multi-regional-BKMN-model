"""
Phase 2 — long-rate shift from the short-rate shift (Hull-White 1F, Prop 2).

Given a short-rate shift Δr(t), the zero-coupon rate shift at relative maturity
τ = T − t is
    ΔR(t,T) = B(τ)/τ · Δr(t),   B(τ) = (1 − e^{−aτ}) / a
depending only on mean reversion a (σ-independent). a = 0.04 default (Table 17).
"""
import numpy as np

A_MEANREV = 0.04


def hw_B(tau, a=A_MEANREV):
    tau = np.asarray(tau, float)
    return np.where(a == 0, tau, (1.0 - np.exp(-a * tau)) / a)


def zero_rate_shift(dr, tau, a=A_MEANREV):
    """Zero-coupon rate shift at tenor τ (same units as dr). τ→0 gives dr."""
    tau = np.asarray(tau, float)
    return np.where(tau <= 0, dr, hw_B(tau, a) / np.where(tau <= 0, 1.0, tau) * dr)
