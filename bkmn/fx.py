"""
Phase 3 — FX shifts vs the base currency (EUR), the project's core deliverable.

The paper's route (§4.3): FX from "the difference in the changes of yield curves".
Two channels, reported separately and combined. Convention: S_r = units of
currency r per 1 EUR, so a POSITIVE Δlog = r depreciates against the euro.

  spot / relative-PPP (needs the PPP anchor):
      Δlog S_r(t) = cumΠ_r(t) − cumΠ_EUR(t)          [cumulative inflation diff.]

  forward points / CIP (assumption-free, from rate differentials):
      Δpts_r(t,τ) = ΔR_r(t,t+τ)·τ − ΔR_EUR(t,t+τ)·τ = B(τ)·[Δr_r(t) − Δr_EUR(t)]

  total forward for delivery at t+τ:
      Δlog F_r(t,τ) = Δlog S_r(t) + Δpts_r(t,τ)

Triangular consistency (A/B = A/EUR − B/EUR) holds by construction because every
pair is a difference of per-region quantities against the same base.
"""
from .rates import hw_B


def spot_ppp(cum_infl_region, cum_infl_base):
    """Relative-PPP spot log-shift vs base."""
    return cum_infl_region - cum_infl_base


def forward_points(dr_region, dr_base, tau, a=0.04):
    """CIP forward-point log-shift at tenor τ: B(τ)·(Δr_r − Δr_base)."""
    return float(hw_B(tau, a)) * (dr_region - dr_base)


def forward_total(cum_infl_region, cum_infl_base, dr_region, dr_base, tau, a=0.04):
    return (spot_ppp(cum_infl_region, cum_infl_base)
            + forward_points(dr_region, dr_base, tau, a))
