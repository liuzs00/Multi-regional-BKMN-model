"""
Region selection, stage 2: the linkage-threshold rule.

`select_regions.py` answers "which economies deserve their own region" by
agglomerative merging over the whole 81-economy ICIO.  That produces a ranking
and a candidate set, but no defensible cut point -- the merge-cost curve has no
knee between 15 and 25 groups, so the algorithm cannot choose a K for us.

This module applies the cut that was chosen instead, as an explicit rule:

    KEEP a candidate region if
        (a) it is among the TOP_N by economic linkage, OR
        (b) its economic linkage > THRESHOLD %, OR
        (c) its carbon  linkage > THRESHOLD %.
    Everything else falls into ROW.

(b) is redundant while TOP_N = 10 (the 10th region already sits above 1 %) but
is kept because it makes the rule symmetric in the two measures and keeps the
selection stable if TOP_N is changed.

Rule (c) is what stops the cut from being a pure size ranking: it re-admits
economies that are small suppliers but carbon-heavy ones, which is precisely the
population a climate stress test must not bury in a residual.

Shares are of the EU27 final-demand footprint x_EU = (I-A)^-1 f_EU, exactly as
in `select_regions.py`; see that module for the linkage definitions.

Usage: py -3 tools/select_regions_threshold.py
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from tools.select_regions import (EU27, economy_attributes,  # noqa: E402
                                  eu_footprint, load_table)

TOP_N = 10          # keep the ten largest by economic linkage
THRESHOLD = 1.0     # ... plus anything above 1 % on EITHER measure

# The rule above leaves a residual that outranks China on BOTH measures, which
# breaks the requirement that the residual must not dominate.  Splitting it in
# two repairs that at the cost of one extra region.
#
# The split is geographic, and deliberately NOT the Ward criterion used in stage
# 1.  Clustering on (log carbon intensity, vulnerability) groups the high-carbon
# economies together and so concentrates carbon: it yields a 16-member block at
# 11.68 % carbon linkage, which exceeds China's 11.11 % and fails the constraint
# outright.  Minimising within-group heterogeneity and keeping each residual
# non-dominant are different objectives, and here they genuinely conflict.
SPLIT_RESIDUAL = True
RAS_MEMBERS = ["JPN", "KOR", "SGP", "TWN", "VNM", "IDN", "MYS", "THA", "PHL",
               "HKG", "BGD", "BRN", "KHM", "LAO", "MMR", "PAK"]

# Candidate regions: the single economies the stage-1 run promotes, plus the
# three structural aggregates.  ROW is not a candidate -- it is the residual,
# and is formed from whatever this rule does not keep.
CANDIDATES = {
    "EU27": list(EU27),
    "MEA": ["SAU", "ARE", "ISR", "JOR"],
    "AFR": ["ZAF", "EGY", "MAR", "TUN", "NGA", "SEN", "CIV", "CMR",
            "COD", "AGO", "STP"],
    "LAM": ["ARG", "BRA", "COL", "CRI", "MEX", "PER"],
}
for _c in ("USA", "CHN", "GBR", "JPN", "IND", "CAN", "NOR", "IDN", "RUS",
           "CHL", "AUS", "SGP", "TUR", "KOR", "KAZ", "CHE", "TWN", "VNM"):
    CANDIDATES[_c] = [_c]

FULL_NAME = {
    "EU27": "European Union (27 members)", "CHN": "China",
    "USA": "United States", "GBR": "United Kingdom", "CHE": "Switzerland",
    "RUS": "Russian Federation", "IND": "India", "JPN": "Japan",
    "NOR": "Norway", "KOR": "Korea", "TUR": "Turkiye", "SGP": "Singapore",
    "CAN": "Canada", "TWN": "Chinese Taipei", "VNM": "Viet Nam",
    "AUS": "Australia", "IDN": "Indonesia", "KAZ": "Kazakhstan",
    "CHL": "Chile", "MEA": "Middle East", "AFR": "Africa",
    "LAM": "Latin America ex-Chile", "ROW": "Rest of World",
    "RAS": "Rest of Asia-Pacific",
}


def linkage_by_economy():
    """Per-economy economic and carbon linkage, as % of the EU footprint."""
    Z, F, x, econ, sect = load_table()
    x_eu = eu_footprint(Z, F, x, econ)
    d = economy_attributes(econ, sect, x, x_eu)
    d["ci"] = d["ci"].fillna(d["ci"].median())      # ICIO residual has no GHG row
    d["link_carbon"] = d.link_econ * d.ci
    d["econ_pct"] = d.link_econ / d.link_econ.sum() * 100
    d["carb_pct"] = d.link_carbon / d.link_carbon.sum() * 100
    return d


def group(d, members):
    """Collapse economies into named regions; ROW takes the remainder."""
    assigned = {c for ms in members.values() for c in ms}
    rows = {}
    for name, ms in members.items():
        sub = d.loc[[c for c in ms if c in d.index]]
        rows[name] = {"n": len(sub), "econ_pct": sub.econ_pct.sum(),
                      "carb_pct": sub.carb_pct.sum(),
                      "members": sorted(sub.index)}
    rest = d.loc[[c for c in d.index if c not in assigned]]
    rows["ROW"] = {"n": len(rest), "econ_pct": rest.econ_pct.sum(),
                   "carb_pct": rest.carb_pct.sum(),
                   "members": sorted(rest.index)}
    return pd.DataFrame(rows).T.sort_values("econ_pct", ascending=False)


def select(cand, top_n=TOP_N, thr=THRESHOLD, count_row_in_top=True):
    """
    Apply the rule.  Returns (kept names, reason per name).

    `count_row_in_top` decides whether the residual occupies one of the TOP_N
    slots.  It does in the table the rule was read off, so it is the default;
    the alternative is reported alongside because the two differ by one region.
    """
    order = cand.sort_values("econ_pct", ascending=False)
    names = [n for n in order.index if count_row_in_top or n != "ROW"]
    top = [n for n in names[:top_n] if n != "ROW"]

    kept, why = list(top), {n: f"top {top_n} by economic linkage" for n in top}
    for n in names[top_n:]:
        if n == "ROW":
            continue
        e, c = order.loc[n, "econ_pct"], order.loc[n, "carb_pct"]
        if e > thr or c > thr:
            kept.append(n)
            hits = ([f"econ {e:.2f} % > {thr:g}"] if e > thr else []) + \
                   ([f"carbon {c:.2f} % > {thr:g}"] if c > thr else [])
            why[n] = " and ".join(hits)
    return kept, why


def main():
    d = linkage_by_economy()
    cand = group(d, CANDIDATES)

    print("candidate regions, ranked by economic linkage")
    print(f"{'':>4} {'region':<6}{'n':>4}{'econ %':>9}{'carb %':>9}")
    for i, (n, r) in enumerate(cand.iterrows(), 1):
        print(f"{i:>4} {n:<6}{int(r.n):>4}{r.econ_pct:>9.2f}{r.carb_pct:>9.2f}")

    for count_row in (True, False):
        kept, why = select(cand, count_row_in_top=count_row)
        lab = "counting ROW in the top 10" if count_row else "excluding ROW"
        print(f"\n--- rule applied, {lab}: {len(kept) + 1} regions ---")
        for n in kept:
            print(f"   {n:<6} {why[n]}")
        dropped = [n for n in cand.index if n not in kept and n != "ROW"]
        print(f"   ROW    <- {', '.join(dropped)}")

    kept, why = select(cand)
    members = {n: CANDIDATES[n] for n in kept}
    resid = [c for c in d.index
             if c not in {m for ms in members.values() for m in ms}]
    if SPLIT_RESIDUAL:
        members["RAS"] = [c for c in resid if c in RAS_MEMBERS]
    final = group(d, members)
    final.to_csv(f"{ROOT}/out_region_selection_final.csv")

    residuals = ["ROW", "RAS"] if SPLIT_RESIDUAL else ["ROW"]
    n_named = len(final) - len(residuals) - 1
    print(f"\nFINAL SET -- {len(final)} regions "
          f"(EU27 + {n_named} named + {len(residuals)} residual)")
    print(f"{'#':>3}  {'region':<6}{'n':>4}{'econ %':>9}{'carb %':>9}   name")
    for i, (n, r) in enumerate(final.iterrows(), 1):
        print(f"{i:>3}  {n:<6}{int(r.n):>4}{r.econ_pct:>9.2f}{r.carb_pct:>9.2f}"
              f"   {FULL_NAME.get(n, n)}")

    named = final.drop(index=["EU27"] + residuals)
    ok = True
    print()
    for k in residuals:
        e, c = final.loc[k, "econ_pct"], final.loc[k, "carb_pct"]
        de, dc = e < named.econ_pct.max(), c < named.carb_pct.max()
        ok &= de and dc
        print(f"  {k:<4} {e:5.2f} % econ ({'ok' if de else 'DOMINATES'}), "
              f"{c:5.2f} % carbon ({'ok' if dc else 'DOMINATES'})")
    print(f"  largest named region: {named.econ_pct.max():.2f} % econ, "
          f"{named.carb_pct.max():.2f} % carbon")
    print(f"  constraint 'no residual is largest on either measure': "
          f"{'SATISFIED' if ok else '*** VIOLATED ***'}")

    tot_e = sum(final.loc[k, "econ_pct"] for k in residuals)
    tot_c = sum(final.loc[k, "carb_pct"] for k in residuals)
    print(f"\ncoverage: named regions carry {100 - tot_e:.1f} % of economic and "
          f"{100 - tot_c:.1f} % of carbon linkage")
    for k in residuals:
        print(f"  {k}: " + ", ".join(final.loc[k, "members"]))
    return d, cand, final


if __name__ == "__main__":
    main()
