"""
BKMN orchestrator: run the full ensemble for a horizon grid and produce a
results table analogous to Table 11 of the paper, weighted across the RCP
Bayesian mixture (Eq 20-21).
"""

import numpy as np
import pandas as pd

from . import assumptions as cfg
from . import climate, curves, economy, markets, scenarios
from .climate import RCP_STATES

# Rate instruments reported (label -> maturity tau in years), mirroring Table 11.
RATE_TENORS = {
    "Deposit 1D": 1 / 365,
    "Deposit 6M": 0.5,
    "Swap 1Y": 1.0,
    "Swap 5Y": 5.0,
    "Swap 10Y": 10.0,
    "Swap 20Y": 20.0,
}


def _scenario_outputs(rcp: str, horizon_T: float, phi: float):
    """All raw model outputs for one RCP at horizon `horizon_T` (years)."""
    year = cfg.START_YEAR + horizon_T
    dT = climate.delta_T(rcp, year)
    xce = climate.carbon_price(rcp, year)
    dxce = climate.delta_carbon_price(rcp, year)

    # sector GVA shock: transition (carbon-price level as tax) + physical (dT)
    sector_shock = economy.gva_relative_shock(xce, phi, dT, include_physical=True)
    gdp_shock = economy.gdp_relative_shock(xce, phi, dT, include_physical=True)

    infl = markets.inflation_shift(dxce)
    dr = markets.policy_rate_shock(infl, gdp_shock)

    rates = {lbl: markets.rate_term_shift(dr, tau) for lbl, tau in RATE_TENORS.items()}
    cds = markets.cds_shock(sector_shock)
    eq = markets.equity_shock(sector_shock)
    op = markets.oprisk_shock(infl, gdp_shock)

    return {
        "rates": rates, "inflation": infl, "cds": cds, "equity": eq,
        "oprisk": op, "carbon": xce, "temperature": dT, "dr": dr,
    }


def run(phi: float = cfg.PHI, tenors: dict = None) -> pd.DataFrame:
    """
    Returns a DataFrame: rows = model factors, columns = reporting horizons.
    Each cell is the RCP-mixture expectation at that horizon.
    """
    tenors = tenors or cfg.REPORT_TENORS
    rows = {}

    for col, T in tenors.items():
        # compute per-RCP outputs once, then weight by the mixture at T
        per_rcp = {r: _scenario_outputs(r, T, phi) for r in RCP_STATES}

        def E(selector):
            return scenarios.expected_over_rcp(
                {r: selector(per_rcp[r]) for r in RCP_STATES}, T)

        cells = {}
        # interest-rate shifts (bp)
        for lbl in RATE_TENORS:
            cells[("Rate shift (bp)", lbl)] = E(lambda o, l=lbl: o["rates"][l]) * 1e4
        # inflation (bp)
        cells[("Inflation (bp)", "YoY")] = E(lambda o: o["inflation"]) * 1e4
        # CDS (relative %)
        for sector in markets.data.CDS_SECTORS:
            cells[("CDS (%)", sector)] = E(lambda o, s=sector: o["cds"][s]) * 100
        # equity (relative %)
        cells[("Equity (%)", "FTSE100")] = E(lambda o: o["equity"]) * 100
        # carbon price (GBP) and temperature (C)
        cells[("Carbon (GBP)", "XCE")] = E(lambda o: o["carbon"])
        cells[("Temperature (C)", "dT")] = E(lambda o: o["temperature"])
        # operational risk (relative %)
        for rt in markets.data.OPRISK_REG:
            cells[("OpRisk (%)", rt)] = E(lambda o, r=rt: o["oprisk"][r]) * 100

        for key, val in cells.items():
            rows.setdefault(key, {})[col] = val

    df = pd.DataFrame(rows).T
    df.index = pd.MultiIndex.from_tuples(df.index, names=["Factor", "Detail"])
    return df[list(tenors.keys())]


def stressed_levels_table(phi: float = cfg.PHI, tenors: dict = None,
                          maturities=(1.0, 5.0, 10.0, 20.0)) -> pd.DataFrame:
    """
    Absolute *stressed* levels = observed base curve + climate shift.
      - Nominal spot rate (%) at each maturity, per horizon.
      - Implied inflation (%) at each maturity, per horizon.
    Uses the BoE base curves (bkmn/curves.py).  Demonstrates the curves in use.
    """
    tenors = tenors or cfg.REPORT_TENORS
    rows = {}
    for col, T in tenors.items():
        per_rcp = {r: _scenario_outputs(r, T, phi) for r in RCP_STATES}
        dr = scenarios.expected_over_rcp({r: per_rcp[r]["dr"] for r in RCP_STATES}, T)
        infl_shift = scenarios.expected_over_rcp(
            {r: per_rcp[r]["inflation"] for r in RCP_STATES}, T)
        for mat in maturities:
            base_n = curves.nominal_spot(mat)
            shift = markets.rate_term_shift(dr, mat) * 100  # -> percent
            rows.setdefault(("Nominal spot (%)", f"{int(mat)}Y"), {})[col] = base_n + shift
        for mat in maturities:
            base_i = curves.inflation_spot(mat)
            rows.setdefault(("Inflation (%)", f"{int(mat)}Y"), {})[col] = base_i + infl_shift * 100

    df = pd.DataFrame(rows).T
    df.index = pd.MultiIndex.from_tuples(df.index, names=["Factor", "Maturity"])
    return df[list(tenors.keys())]


def base_curve_snapshot(maturities=(1.0, 5.0, 10.0, 20.0)) -> pd.DataFrame:
    """The observed (pre-stress) base curves at selected maturities."""
    return pd.DataFrame({
        "Nominal spot (%)": [curves.nominal_spot(m) for m in maturities],
        "Implied inflation (%)": [curves.inflation_spot(m) for m in maturities],
    }, index=[f"{int(m)}Y" for m in maturities])


def sector_shock_table(phi: float = cfg.PHI, horizon_T: float = 20.0) -> pd.DataFrame:
    """Per-sector relative GVA shocks (transition / physical / total) at a horizon."""
    year = cfg.START_YEAR + horizon_T
    rows = {}
    for r in RCP_STATES:
        dT = climate.delta_T(r, year)
        xce = climate.carbon_price(r, year)
        trans = economy.gva_relative_shock_transition(xce, phi)
        phys, _ = economy.gva_relative_shock_physical(dT)
        rows[r] = trans + phys
    df = pd.DataFrame(rows, index=economy.data.SECTORS)
    return df * 100
