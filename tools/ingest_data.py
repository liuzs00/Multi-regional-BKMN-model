"""
ETL: read the supplied external Excel sources and write tidy CSVs into data/
so the model is self-contained.

Sources:
  D:\\Download\\Temperature.xlsx                         (MESSAGE-GLOBIOM SSP2 temp, World)
  D:\\Download\\price-carbon.xlsx                        (MESSAGE-GLOBIOM SSP2 Price|Carbon)
  D:\\Download\\latest-yield-curve-data\\GLC Nominal ...  (BoE nominal spot curve)
  D:\\Download\\latest-yield-curve-data\\GLC Inflation... (BoE implied inflation spot curve)

Outputs (data/):
  temperature_message_world.csv     year, RCP1.9..RCP6.0   (deg C vs pre-industrial)
  carbon_price_message_oecd.csv     year, RCP1.9..RCP6.0   (US$2005/tCO2, R5.2OECD)
  gbp_nominal_spot_curve.csv        maturity_years, rate_pct  (latest date)
  gbp_inflation_spot_curve.csv      maturity_years, rate_pct  (latest date)
"""
import sys, os
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import pandas as pd

DL = r"D:\Download"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

SCEN_TO_RCP = {"SSP2-19": "RCP1.9", "SSP2-26": "RCP2.6", "SSP2-34": "RCP3.4",
               "SSP2-45": "RCP4.5", "SSP2-60": "RCP6.0"}
RCP_ORDER = ["RCP1.9", "RCP2.6", "RCP3.4", "RCP4.5", "RCP6.0"]


def _year_cols(df):
    cols = []
    for c in df.columns:
        try:
            y = int(float(c))
            if 1900 <= y <= 2200:
                cols.append((c, y))
        except (ValueError, TypeError):
            pass
    return cols


def ingest_scenario(path, region_filter=None, out_name=None):
    df = pd.read_excel(path, sheet_name="data", header=0)
    df = df[df["Scenario"].isin(SCEN_TO_RCP)]
    if region_filter is not None:
        df = df[df["Region"] == region_filter]
    ycols = _year_cols(df)
    years = [y for _, y in ycols]
    rcp_series = {}
    for _, row in df.iterrows():
        rcp = SCEN_TO_RCP[row["Scenario"]]
        rcp_series[rcp] = [float(row[c]) for c, _ in ycols]
    out = pd.DataFrame({"year": years})
    for rcp in RCP_ORDER:
        out[rcp] = rcp_series[rcp]
    dest = os.path.join(OUT, out_name)
    out.to_csv(dest, index=False)
    print(f"wrote {dest}  ({len(years)} years, region={region_filter})")


def ingest_curve(path, out_name):
    raw = pd.read_excel(path, sheet_name="4. spot curve", header=None)
    # locate the 'years:' header row
    yrow = None
    for i in range(min(8, len(raw))):
        if str(raw.iloc[i, 0]).strip().lower().startswith("years"):
            yrow = i
            break
    maturities = pd.to_numeric(raw.iloc[yrow, 1:], errors="coerce").to_numpy()
    # data rows: col0 parses as a date
    dates = pd.to_datetime(raw.iloc[:, 0], errors="coerce")
    data_idx = np.where(dates.notna().to_numpy())[0]
    last = data_idx[-1]
    rates = pd.to_numeric(raw.iloc[last, 1:], errors="coerce").to_numpy()
    mask = ~np.isnan(maturities) & ~np.isnan(rates)
    out = pd.DataFrame({"maturity_years": maturities[mask], "rate_pct": rates[mask]})
    dest = os.path.join(OUT, out_name)
    out.to_csv(dest, index=False)
    print(f"wrote {dest}  (date={dates.iloc[last].date()}, "
          f"{mask.sum()} nodes {out['maturity_years'].min():.2f}-{out['maturity_years'].max():.1f}y)")


if __name__ == "__main__":
    ingest_scenario(os.path.join(DL, "Temperature.xlsx"),
                    region_filter="World", out_name="temperature_message_world.csv")
    ingest_scenario(os.path.join(DL, "price-carbon.xlsx"),
                    region_filter="R5.2OECD", out_name="carbon_price_message_oecd.csv")
    ingest_curve(os.path.join(DL, r"latest-yield-curve-data\GLC Nominal daily data current month.xlsx"),
                 "gbp_nominal_spot_curve.csv")
    ingest_curve(os.path.join(DL, r"latest-yield-curve-data\GLC Inflation daily data current month.xlsx"),
                 "gbp_inflation_spot_curve.csv")
    print("done.")
