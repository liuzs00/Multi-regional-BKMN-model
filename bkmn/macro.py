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


# Price (US$2022/t) at which carbon pricing is taken to cover essentially all of
# a region's emissions.  The one asserted parameter of the dynamic-scope
# sensitivity; swept in run_extensions.
XCE_FULL_COVERAGE = 100.0


def scope_at(scope_2025, xce, xce_full=XCE_FULL_COVERAGE):
    """
    Coverage Ω_XCE(t), expanding with the scenario's own carbon price.

        Ω(t) = Ω₂₀₂₅ + (1 − Ω₂₀₂₅) · min(1, XCE(t) / XCE_full)

    §2.6 writes the inflation driver as Δ**Ω**_XCE — a *change* in scope — and
    notes "increases in scope of carbon pricing may have similar effects".
    Holding Ω at its 2025 value instead makes a region that pays $338/t under Net
    Zero contribute zero carbon inflation if it prices nothing today (India,
    Turkey), which is inconsistent with the scenario it is being run through.

    Tying expansion to the scenario's own price is the least assumption-heavy
    link available: the carbon price *is* the scenario's policy-stringency
    signal.  Current Policies (~$3/t) leaves coverage essentially unchanged; Net
    Zero (>$300/t) takes it to full.  Monotone, bounded in [Ω₂₀₂₅, 1].
    """
    return scope_2025 + (1.0 - scope_2025) * min(1.0, max(0.0, xce) / xce_full)


def inflation_dev(dxce_usd, scope):
    """Headline-inflation deviation (fraction) from a carbon-price change (USD/t)."""
    return INFL_PER_USD * dxce_usd * scope


def taylor_rate_shift(dPi, dY, phi_pi=PHI_PI, phi_y=PHI_Y):
    """Policy short-rate shift (fraction) from inflation- and output-gap deviations."""
    return phi_pi * dPi + phi_y * dY
