"""
Climate term structures (temperature change and CO2e price) per RCP.

Now driven by REAL data from the MESSAGE-GLOBIOM SSP2 marker scenarios
(IIASA SSP Scenario Database):

  * Temperature : region World, "Diagnostics|MAGICC6|Temperature|Global Mean"
                  (deg C vs pre-industrial), in data/temperature_message_world.csv
  * Carbon price: region R5.2OECD, "Price|Carbon" (US$2005/tCO2),
                  in data/carbon_price_message_oecd.csv

Both are SSP2 (the paper's 90%-weighted SSP), giving an internally consistent
ensemble.  Decadal database values are linearly interpolated to annual; carbon
prices are converted US$2005 -> GBP via cfg.USD2005_TO_GBP.

BKMN drives physical risk off the *incremental* temperature change from the
start year:  delta_T(t) = T(t) - T(start).
"""

import os
import numpy as np
import pandas as pd

from . import assumptions as cfg

# Paper's five RCP states (Section 2.2), matched to SSP2-{19,26,34,45,60}.
RCP_STATES = ["RCP1.9", "RCP2.6", "RCP3.4", "RCP4.5", "RCP6.0"]
SSP_STATES = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5"]

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _load(fname):
    df = pd.read_csv(os.path.join(_DATA_DIR, fname))
    years = df["year"].to_numpy(dtype=float)
    cols = {r: df[r].to_numpy(dtype=float) for r in RCP_STATES}
    return years, cols


_TEMP_YEARS, _TEMP = _load("temperature_message_world.csv")
_XCE_YEARS, _XCE_USD = _load("carbon_price_message_oecd.csv")


def warming_absolute(rcp: str, year: float) -> float:
    """Absolute MAGICC6 global-mean warming vs pre-industrial at `year` (linear interp)."""
    return float(np.interp(year, _TEMP_YEARS, _TEMP[rcp]))


def delta_T(rcp: str, year: float, start_year: int = cfg.START_YEAR) -> float:
    """Incremental temperature change since the simulation start (what BKMN uses)."""
    return warming_absolute(rcp, year) - warming_absolute(rcp, start_year)


def carbon_price(rcp: str, year: float, start_year: int = cfg.START_YEAR,
                 horizon: int = cfg.HORIZON_YEARS) -> float:
    """CO2e price (GBP/t) at `year`: interpolated US$2005 series x USD->GBP factor."""
    usd = float(np.interp(year, _XCE_YEARS, _XCE_USD[rcp]))
    return usd * cfg.USD2005_TO_GBP


def delta_carbon_price(rcp: str, year: float, start_year: int = cfg.START_YEAR,
                       horizon: int = cfg.HORIZON_YEARS) -> float:
    """Change in carbon price since start (drives inflation, Section 2.6)."""
    return carbon_price(rcp, year, start_year) - carbon_price(rcp, start_year, start_year)
