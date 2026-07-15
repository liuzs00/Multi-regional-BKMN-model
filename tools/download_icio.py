"""
Download OECD Inter-Country Input-Output (ICIO) tables, 2023 release.

Source: https://oe.cd/icio  (files hosted at stats.oecd.org/wbos/fileview2.aspx)
Coverage: 76 economies + Rest of World, 45 ISIC Rev.4 industries, 1995-2020.
Format:  one ZIP per 5-year block, each containing YYYY_SML.csv matrices
         (SML = small format, China/Mexico not split; values in current USD m).

File IDs verified 2026-07 (from the OECD download page / okrebs-iotr package).

2025 EDITION: the newer 2025 edition (1995-2022, 80 economies + RoW, 50
industries: A01_02->A01+A02, B05_06->B05+B06, B07_08->B07+B08, C24->C24A+C24B,
C30->C301+C302T309 vs the 45-industry 2023 release) was downloaded manually
from the OECD site in a browser and stored as
    data/icio/ICIO2025_2016-2022_SML.zip   (2016_SML.csv .. 2022_SML.csv)
Its bulk-file GUIDs are not publicly indexed, so it is not scripted here.
Prefer the 2025 file for recent years; the 2023-release blocks below remain
useful for pre-2016 history (note: 45 industries, so harmonisation is needed
when mixing editions).

Usage:
    py -3 tools/download_icio.py               # downloads default blocks
    py -3 tools/download_icio.py --all         # downloads all five blocks
"""

import os
import sys
import urllib.request

BASE = "https://stats.oecd.org/wbos/fileview2.aspx?IDFile="

BLOCKS = {  # year-block: GUID  (ICIO 2023 release)
    "1995-2000": "d26ad811-5b58-4f0c-a4e3-06a1469e475c",
    "2001-2005": "7cb93dae-e491-4cfd-ac67-889eb7016a4a",
    "2006-2010": "ea165bfb-3a85-4e0a-afee-6ba8e6c16052",
    "2011-2015": "1f791bc6-befb-45c5-8b34-668d08a1702a",
    "2016-2020": "d1ab2315-298c-4e93-9a81-c6f2273139fe",
}
DEFAULT = ["2011-2015", "2016-2020"]

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "data", "icio")


def download(block: str) -> str:
    os.makedirs(DEST, exist_ok=True)
    out = os.path.join(DEST, f"ICIO2023_{block}_SML.zip")
    if os.path.exists(out) and os.path.getsize(out) > 1_000_000:
        print(f"already have {out}")
        return out
    url = BASE + BLOCKS[block]
    print(f"downloading {block} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=600) as r, open(out, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    print(f"  -> {out}  ({os.path.getsize(out):,} bytes)")
    return out


if __name__ == "__main__":
    which = list(BLOCKS) if "--all" in sys.argv else DEFAULT
    for b in which:
        download(b)
