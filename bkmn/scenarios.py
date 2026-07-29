"""
Climate-scenario data layer: NGFS Phase 5 carbon prices and temperature.

Reads the verbatim API pulls in data/ngfs/ (see tools/download_ngfs.py) and
prepares them for the model:
  * annual linear interpolation (paper Table 17: linear),
  * carbon price converted US$2010 -> US$2022 (to match the ICIO's current-USD),
  * R5 zone -> 20-region expansion via region_carbon_map.scenario_zone,
  * temperature as GSAT anomaly (K vs 1850-1900) -> incremental dT from a base year.

Scenario names (NGFS Phase 5, MESSAGEix-GLOBIOM 2.0-M-R12-NGFS):
  Net Zero 2050, Below 2C, Delayed transition, Low demand,
  Nationally Determined Contributions (NDCs), Fragmented World, Current Policies.
"""
import os

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGFS = os.path.join(ROOT, "data", "ngfs")

# [DATA] US CPI-U annual average: 2010 = 218.056, 2022 = 292.655 (BLS) -> x1.342.
# Converts the NGFS US$2010/t carbon prices to the ICIO's current-2022-USD world.
USD2010_TO_USD2022 = 1.342

# NGFS R5 label -> region_carbon_map.scenario_zone label
ZONE_OF_R5 = {
    "OECD & EU (R5)": "R5.2OECD",
    "Asia (R5)": "R5.2ASIA",
    "Middle East & Africa (R5)": "R5.2MAF",
    "Reforming Economies (R5)": "R5.2REF",
    "Latin America (R5)": "R5.2LAM",
    "World": "World",
}


def _annualise(df: pd.DataFrame, y0: int = 2020, y1: int = 2100) -> pd.DataFrame:
    """Long IAMC rows -> wide (year x column) with annual linear interpolation."""
    years = np.arange(y0, y1 + 1)
    out = {}
    for col, grp in df.groupby("column"):
        g = grp.sort_values("year")
        out[col] = np.interp(years, g.year, g.value)
    return pd.DataFrame(out, index=pd.Index(years, name="year"))


def load_carbon_prices(to_usd2022: bool = True) -> pd.DataFrame:
    """Annual carbon price paths: index=year, columns=(scenario, zone)."""
    d = pd.read_csv(os.path.join(NGFS, "price_carbon_r5.csv"))
    d["column"] = list(zip(d.scenario, d.region.map(ZONE_OF_R5)))
    wide = _annualise(d)
    wide.columns = pd.MultiIndex.from_tuples(wide.columns,
                                             names=["scenario", "zone"])
    if to_usd2022:
        wide = wide * USD2010_TO_USD2022
    return wide


def load_temperature(pct: int = 50) -> pd.DataFrame:
    """Annual GSAT anomaly (K vs 1850-1900): index=year, columns=scenario."""
    d = pd.read_csv(os.path.join(NGFS, f"temperature_gsat_p{pct}.csv"))
    d["column"] = d.scenario
    return _annualise(d)


class Scenarios:
    """Convenience wrapper joining the NGFS paths to the 20-region layout."""

    def __init__(self, carbon_map: pd.DataFrame):
        self.cm = carbon_map.set_index("region")
        self.px = load_carbon_prices()
        self.temp = load_temperature()
        self.names = sorted(self.px.columns.get_level_values("scenario").unique())

    def _zone(self, region: str) -> str:
        z = self.cm.loc[region, "scenario_zone"]
        return z if z in set(self.px.columns.get_level_values("zone")) else "World"

    def xce_by_region(self, scenario: str, year: int) -> pd.Series:
        """Carbon price (US$2022/t) per region at `year` (zone path; ROW->World)."""
        return pd.Series(
            {r: self.px.loc[year, (scenario, self._zone(r))] for r in self.cm.index},
            name=f"XCE {scenario} {year}")

    def coords(self, year_T: int = 2100, year_X: int = 2050,
               zone: str = "R5.2OECD") -> pd.DataFrame:
        """
        Numeric characteristics of each scenario, for the Eq-1 distance metric.

        The paper measures distance between RCP states as |j−k| on their
        *concentration labels* — a physical number the scenario set supplies.
        NGFS narratives have no such label, so we use the equivalent numbers the
        scenarios themselves report: end-of-century warming (physical outcome)
        and the carbon price (transition-policy stringency).  See
        docs/PAPER_AUDIT.md and mixture.transition_matrix.
        """
        return pd.DataFrame(
            {"T": {s: float(self.temp.loc[year_T, s]) for s in self.names},
             "XCE": {s: float(self.px[s][zone].loc[year_X]) for s in self.names}})

    def delta_T(self, scenario: str, year: int, base_year: int = 2022) -> float:
        """Incremental warming since `base_year` (what BKMN's damage uses)."""
        return float(self.temp.loc[year, scenario] - self.temp.loc[base_year, scenario])


if __name__ == "__main__":
    # smoke test
    import sys
    sys.path.insert(0, ROOT)
    from bkmn.regions import load

    m = load()
    sc = Scenarios(m.carbon_map)
    print("scenarios:", sc.names, "\n")
    for s in ["Net Zero 2050", "Delayed transition", "Current Policies"]:
        x = sc.xce_by_region(s, 2030)
        print(f"XCE 2030 US$2022/t  [{s}]")
        print("  " + "  ".join(f"{r}:{x[r]:.0f}" for r in
                               ["EU27", "USA", "CHN", "IND", "RUS", "TUR", "KAZ", "ROW"]))
        print(f"  dT 2030 vs 2022: {sc.delta_T(s, 2030):+.3f} K   "
              f"GSAT 2022: {sc.temp.loc[2022, s]:.2f} K vs 1850-1900")
    scope = m.carbon_map.set_index("region").carbon_scope
    print("\ncarbon_scope:", "  ".join(f"{r}:{scope[r]:.2f}" for r in
                                       ["EU27", "USA", "CHN", "KOR", "IND"]))
