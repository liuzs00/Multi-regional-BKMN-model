"""
Region data layer: loads the DATA_20R tables into model-ready arrays.

Everything downstream (transition, macro, rates, fx) consumes the `Model20R`
bundle returned by ``load()`` — the ICIO blocks aligned to a fixed region-sector
order, plus the carbon/scenario map (currency, fx_role, scenario_zone,
carbon_scope, ppp weight).
"""
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D20 = os.path.join(ROOT, "DATA_20R")
YEAR = 2022


@dataclass
class Model20R:
    regions_order: list          # 20 region codes, canonical order
    sectors: list                # 1000 region-sector labels (ICIO order)
    region_of: np.ndarray        # len-1000 region code per sector row
    industry_of: list            # len-1000 industry code per sector row
    Z: np.ndarray                # 1000x1000 intermediate flows, USD m
    x: np.ndarray                # gross output per sector
    gva: np.ndarray              # value added per sector
    ci: np.ndarray               # carbon intensity, tCO2e / USD m output
    carbon_map: pd.DataFrame     # per-region: currency, fx_role, scenario_zone,
                                 # carbon_price_regime, cbam_role, phys_vuln_tier,
                                 # ppp_gdp_weight, carbon_scope

    def mask(self, region: str) -> np.ndarray:
        return self.region_of == region


def load() -> Model20R:
    ic = pd.read_csv(os.path.join(D20, f"ICIO2025_20R_{YEAR}.csv"), index_col=0)
    ri = [r for r in ic.index if r not in ("TLS", "VA", "OUT")]
    Z = ic.loc[ri, ri].to_numpy(float)
    x = ic.loc["OUT", ri].to_numpy(float)
    gva = ic.loc["VA", ri].to_numpy(float)
    region_of = np.array([l.split("_", 1)[0] for l in ri])
    industry_of = [l.split("_", 1)[1] for l in ri]

    ci_tbl = pd.read_csv(os.path.join(D20, f"CARBON_INTENSITY_20R_{YEAR}.csv"),
                         index_col=0)
    ci = np.array([ci_tbl.loc[j, r] for j, r in zip(industry_of, region_of)],
                  float)

    cm = pd.read_csv(os.path.join(D20, "region_carbon_map.csv"))
    return Model20R(regions_order=list(cm.region), sectors=ri,
                    region_of=region_of, industry_of=industry_of,
                    Z=Z, x=x, gva=gva, ci=ci, carbon_map=cm)
