"""
Phase 2 — macro channels: inflation (§2.6) and the Taylor-rule short-rate shift (§2.7).

Inflation (Moessner):  +$10/tCO2e -> +0.08pp headline inflation, scaled by the
region's carbon-pricing *scope* (fraction of emissions actually priced).
  annual rate deviation :  ΔΠ_r(t) = k · [XCE_r(t) − XCE_r(t−1)] · scope_r
  cumulative price level:  ΣΔΠ_r(t) = k · [XCE_r(t) − XCE_r(base)] · scope_r   (telescopes)
with k = 0.08% / $10 = 8e-5 per $1/t.

Taylor rule (short-rate policy response to the climate-induced gaps at t):
  Δr_r(t) = φΠ · ΔΠ_r(t) + φY · ΔY_r(t)
ΔY_r(t) is the transition GDP shock (level deviation, negative); ΔΠ_r(t) the
annual inflation deviation. Defaults φΠ = φY = 0.5 (paper).
"""
INFL_PER_USD = 0.08e-2 / 10.0     # 8e-5 : fraction of inflation per $1/t priced
PHI_PI = 0.5
PHI_Y = 0.5


def inflation_dev(dxce_usd, scope):
    """Headline-inflation deviation (fraction) from a carbon-price change (USD/t)."""
    return INFL_PER_USD * dxce_usd * scope


def taylor_rate_shift(dPi, dY, phi_pi=PHI_PI, phi_y=PHI_Y):
    """Policy short-rate shift (fraction) from inflation- and output-gap deviations."""
    return phi_pi * dPi + phi_y * dY
