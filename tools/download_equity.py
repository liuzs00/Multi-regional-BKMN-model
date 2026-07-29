"""
Equity index histories per FX region (Phase E, docs/EXT_PLAN.md) via the
keyless Yahoo Finance chart API. Quarterly closes, up to 30y.

Symbols verified 2026-07 (probe): headline index per region where freely
available. CHL (^IPSA truncated) and KAZ (no free index) have no series ->
those regions fall back to the paper-proxy beta [PROXY], documented in Phase E.

Output: data/equity/index_history.csv  (region, symbol, date, close)

Usage: py -3 tools/download_equity.py
"""
import json
import os
import time
import urllib.request

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "data", "equity")

SYMBOLS = {  # region -> (yahoo symbol, index name)
    "EU27": ("^STOXX", "STOXX Europe 600"),
    "USA": ("^GSPC", "S&P 500"),
    "CHN": ("000001.SS", "SSE Composite"),
    "GBR": ("^FTSE", "FTSE 100"),
    "JPN": ("^N225", "Nikkei 225"),
    "IND": ("^BSESN", "BSE Sensex"),
    "CAN": ("^GSPTSE", "S&P/TSX Composite"),
    "NOR": ("OSEBX.OL", "Oslo OSEBX"),
    "IDN": ("^JKSE", "IDX Composite"),
    "AUS": ("^AXJO", "S&P/ASX 200"),
    "SGP": ("^STI", "Straits Times"),
    "TUR": ("XU100.IS", "BIST 100"),
    "KOR": ("^KS11", "KOSPI"),
    # CHL, KAZ: no free reliable series -> paper-proxy beta in Phase E
}

URL = ("https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
       "?interval=3mo&range=30y")


def fetch(sym):
    req = urllib.request.Request(URL.format(sym=urllib.request.quote(sym)),
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        j = json.loads(r.read())
    res = j["chart"]["result"][0]
    ts = res["timestamp"]
    close = res["indicators"]["quote"][0]["close"]
    return pd.DataFrame({"date": pd.to_datetime(ts, unit="s").date,
                         "close": close}).dropna()


def main():
    os.makedirs(DEST, exist_ok=True)
    frames = []
    for region, (sym, name) in SYMBOLS.items():
        for attempt in range(3):
            try:
                df = fetch(sym)
                break
            except Exception as e:                # noqa: BLE001 transient
                if attempt == 2:
                    raise
                print(f"  {region}: retry after {type(e).__name__}")
                time.sleep(10)
        df.insert(0, "region", region)
        df.insert(1, "symbol", sym)
        frames.append(df)
        print(f"  {region:5s} {sym:10s} {len(df):3d} quarters  "
              f"{df.date.iloc[0]} .. {df.date.iloc[-1]}   ({name})")
        time.sleep(0.5)
    out = pd.concat(frames, ignore_index=True)
    out.to_csv(os.path.join(DEST, "index_history.csv"), index=False)
    print(f"\nwrote data/equity/index_history.csv  ({len(out)} rows, "
          f"{len(SYMBOLS)} regions; CHL/KAZ -> proxy beta)")


if __name__ == "__main__":
    main()
