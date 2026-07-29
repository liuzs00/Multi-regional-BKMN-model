"""
Download NGFS Phase 5 scenario data via the IIASA API (anonymous, no login).

Pulls, for model MESSAGEix-GLOBIOM 2.0-M-R12-NGFS, all scenarios:
  * Price|Carbon at the five R5 zones + World      -> data/ngfs/price_carbon_r5.csv
  * Global surface temperature (GSAT, MAGICCv7.5.3)
    50th percentile                                -> data/ngfs/temperature_gsat_p50.csv
    10th & 90th percentiles (volatility ext. 3.3)  -> data/ngfs/temperature_gsat_p10.csv / _p90.csv

Units: carbon price US$2010/tCO2 (converted downstream, see bkmn/scenarios.py);
temperature K anomaly (GSAT). 5-yearly steps 2020-2100; interpolation happens
in the loader, not here — these files are verbatim API output (IAMC long format).

Requires: pip install pyam-iamc.   Usage: py -3 tools/download_ngfs.py
"""
import os

import pyam

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "data", "ngfs")
DB = "ngfs_phase_5"
MODEL = "MESSAGEix-GLOBIOM 2.0-M-R12-NGFS"
R5 = ["Asia (R5)", "Latin America (R5)", "Middle East & Africa (R5)",
      "OECD & EU (R5)", "Reforming Economies (R5)"]
TVAR = "AR6 climate diagnostics|Surface Temperature (GSAT)|MAGICCv7.5.3|{p}th Percentile"


def pull(variable, region, dest):
    df = pyam.read_iiasa(DB, model=MODEL, variable=variable, region=region)
    df.data.to_csv(dest, index=False)
    print(f"  {os.path.basename(dest):32s} {len(df.data):5d} rows  "
          f"scenarios={len(df.scenario)}  unit={df.unit}")


def main():
    os.makedirs(DEST, exist_ok=True)
    print(f"pulling from {DB} / {MODEL} (anonymous IIASA API) ...")
    pull("Price|Carbon", R5 + ["World"],
         os.path.join(DEST, "price_carbon_r5.csv"))
    for p in ("50.0", "10.0", "90.0"):
        pull(TVAR.format(p=p), "World",
             os.path.join(DEST, f"temperature_gsat_p{p.split('.')[0]}.csv"))
    print("done.")


if __name__ == "__main__":
    main()
