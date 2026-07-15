"""
Download the OECD Greenhouse Gas Footprints (GHGFP) 2025 edition - the
successor of the TeCO2 (Trade in embodied CO2) database - in FULL, via the
OECD SDMX REST API.

Aligned with ICIO 2025 (same 80 economies + RoW / industry structure).
Agency OECD.STI.PIE, dataflows (discovered from the SDMX catalog 2026-07):

  MAIN   DSD_ICIO_GHG_MAIN_2025@DF_ICIO_GHG_MAIN_2025    principal indicators
  SCOPE  DSD_ICIO_GHG_SCOPE_2025@DF_ICIO_GHG_SCOPE_2025  emissions in production by scope
  EXPD   DSD_ICIO_GHG_EXPD_2025@DF_ICIO_GHG_EXPD_2025    emissions in final demand
  ORGN   DSD_ICIO_GHG_ORGN_2025@DF_ICIO_GHG_ORGN_2025    origin of FD emissions (~82 MB/yr)
  TRADE  DSD_ICIO_GHG_TRADE_2025@DF_ICIO_GHG_TRADE_2025  bilateral trade (~113 MB/yr)

Values are tonnes CO2e with UNIT_MULT=6 (i.e. million tonnes).

Files land in data/ghgfp/<NAME>/<YEAR>.csv.gz - one file per dataflow-year,
gzip-compressed on the fly, skipped if already present (resumable).

Usage:
    py -3 tools/download_ghgfp.py            # everything, 1995-2022
    py -3 tools/download_ghgfp.py MAIN SCOPE # only selected dataflows
"""

import gzip
import os
import sys
import time
import urllib.error
import urllib.request

BASE = ("https://sdmx.oecd.org/public/rest/data/OECD.STI.PIE,{flow},1.0/all"
        "?format=csvfile&startPeriod={y}&endPeriod={y}")

FLOWS = {
    "MAIN":  "DSD_ICIO_GHG_MAIN_2025@DF_ICIO_GHG_MAIN_2025",
    "SCOPE": "DSD_ICIO_GHG_SCOPE_2025@DF_ICIO_GHG_SCOPE_2025",
    "EXPD":  "DSD_ICIO_GHG_EXPD_2025@DF_ICIO_GHG_EXPD_2025",
    "ORGN":  "DSD_ICIO_GHG_ORGN_2025@DF_ICIO_GHG_ORGN_2025",
    "TRADE": "DSD_ICIO_GHG_TRADE_2025@DF_ICIO_GHG_TRADE_2025",
}

YEARS = range(1995, 2023)
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "data", "ghgfp")


POLITE_DELAY = 3          # seconds between successful requests
MAX_BACKOFF = 900         # cap for 429 backoff
MAX_ATTEMPTS = 40         # per file; with backoff this spans several hours


def fetch(name: str, flow: str, year: int, t0: float) -> str:
    """Download one dataflow-year, retrying through 429 rate limits.

    Returns 'have', 'empty', 'ok', or 'FAILED ...'.  An empty year writes a
    .empty marker so later runs do not re-request it.
    """
    folder = os.path.join(ROOT, name)
    os.makedirs(folder, exist_ok=True)
    dest = os.path.join(folder, f"{year}.csv.gz")
    marker = os.path.join(folder, f"{year}.empty")
    if os.path.exists(dest) and os.path.getsize(dest) > 200:
        return "have"
    if os.path.exists(marker):
        return "have"

    url = BASE.format(flow=flow, y=year)
    tmp = dest + ".part"
    backoff = 60
    for attempt in range(1, MAX_ATTEMPTS + 1):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=1800) as r:
                n = 0
                with gzip.open(tmp, "wb", compresslevel=6) as f:
                    while chunk := r.read(1 << 20):
                        f.write(chunk)
                        n += len(chunk)
            if n < 200:  # header only -> year not available in this dataflow
                os.remove(tmp)
                open(marker, "w").close()
                return "empty"
            os.replace(tmp, dest)
            time.sleep(POLITE_DELAY)
            return f"ok {n/1e6:.1f} MB (try {attempt})"
        except urllib.error.HTTPError as e:
            if os.path.exists(tmp):
                os.remove(tmp)
            if e.code == 429:
                # OECD sometimes sends Retry-After: 0 - never trust a hint
                # shorter than our own backoff, or retries burn out instantly.
                hdr = e.headers.get("Retry-After")
                hinted = int(hdr) if hdr and hdr.isdigit() else 0
                wait = min(max(hinted, backoff), MAX_BACKOFF)
                print(f"[{time.time()-t0:7.0f}s] {name} {year}: 429, waiting {wait}s "
                      f"(try {attempt})", flush=True)
                time.sleep(wait)
                backoff = min(backoff * 2, MAX_BACKOFF)
                continue
            if e.code == 404:
                open(marker, "w").close()
                return "empty (404)"
            print(f"[{time.time()-t0:7.0f}s] {name} {year}: HTTP {e.code}, retry in 60s",
                  flush=True)
            time.sleep(60)
        except Exception as e:  # noqa: BLE001 - transient network errors
            if os.path.exists(tmp):
                os.remove(tmp)
            print(f"[{time.time()-t0:7.0f}s] {name} {year}: {type(e).__name__}, "
                  f"retry in 60s", flush=True)
            time.sleep(60)
    return "FAILED after max attempts"


def main():
    wanted = [a.upper() for a in sys.argv[1:] if a.upper() in FLOWS] or list(FLOWS)
    t0 = time.time()
    failed = []
    for name in wanted:
        flow = FLOWS[name]
        for y in YEARS:
            status = fetch(name, flow, y, t0)
            if status != "have":
                print(f"[{time.time()-t0:7.0f}s] {name} {y}: {status}", flush=True)
            if status.startswith("FAILED"):
                failed.append(f"{name} {y}")
    print(f"done in {time.time()-t0:.0f}s; failures: {failed or 'none'}")


if __name__ == "__main__":
    main()
