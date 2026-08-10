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

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from tools.select_regions import (EU27, economy_attributes,  # noqa: E402
                                  eu_footprint, load_table)

TOP_N = 10          # keep the ten largest by economic linkage
THRESHOLD = 1.0     # ... plus anything above 1 % on EITHER measure

# The rule above leaves a residual that outranks China on BOTH measures, which
# breaks the requirement that the residual must not dominate.  Something has to
# come out of it, and the point of the machinery below is to decide WHAT.
#
#   1. split the residual by NGFS R5 zone -- not our partition, but the
#      resolution at which scenario carbon prices are published, so each group
#      takes exactly one price path with no blending;
#   2. CLEAN each zone: drop members whose carbon intensity exceeds CLEAN_K
#      times their own zone's average.  The rule is relative, not absolute,
#      because a zone that is uniformly carbon-heavy (REF: Belarus, Kazakhstan,
#      Ukraine at 1.5x spread) is already coherent and should keep everyone,
#      while one hiding a Korea beside a Cambodia (ASIA, 15x) is the one that
#      needs it.  An absolute threshold cannot tell those apart.
#      Dropped economies fall into ROW like any other unselected economy -- they
#      do NOT form a rival group, because the purpose of cleaning is to make the
#      geographic groups worth selecting, not to manufacture a competitor;
#   3. promote the most important cleaned zone, test the rest as a new ROW, and
#      repeat until ROW no longer dominates.
#
# The cap is not a tuning parameter: it is the largest single-economy region,
# which the data says is China on both measures.  The number of promotions is
# therefore an output, not an input.
SPLIT_RESIDUAL = True

# Drop a zone member whose carbon intensity exceeds this multiple of its own
# zone's linkage-weighted average.  The selection is stable for every value in
# [1.5, 3.0] (all give 13 regions and promote ASIA first); below ~1.4 the rule
# over-cleans ASIA until OECD overtakes it.  Swept in main().
CLEAN_K = 1.5

# Candidate regions: the single economies the stage-1 run promotes, plus the
# three structural aggregates.  ROW is not a candidate -- it is the residual,
# and is formed from whatever this rule does not keep.
#
# LAM carries Chile.  An earlier design excluded it ("Latin America ex-Chile")
# because Chile was modelled separately; it is not selected by this rule (0.05 %
# economic, 0.07 % carbon -- last on both), so the carve-out has no purpose and
# would strand a single economy in its own zone group.
CANDIDATES = {
    "EU27": list(EU27),
    "MEA": ["SAU", "ARE", "ISR", "JOR"],
    "AFR": ["ZAF", "EGY", "MAR", "TUN", "NGA", "SEN", "CIV", "CMR",
            "COD", "AGO", "STP"],
    "LAM": ["ARG", "BRA", "CHL", "COL", "CRI", "MEX", "PER"],
}
for _c in ("USA", "CHN", "GBR", "JPN", "IND", "CAN", "NOR", "IDN", "RUS",
           "AUS", "SGP", "TUR", "KOR", "KAZ", "CHE", "TWN", "VNM"):
    CANDIDATES[_c] = [_c]

# NGFS R5 zone per ICIO economy.  Scenario carbon prices are published at this
# resolution, so a region spanning zones must take a blended price.  Assignment
# follows the model's own map (bkmn/regions.py `scenario_zone`) where it has one
# and the IPCC R5 definitions elsewhere.
R5 = {}
for _c in ("AUS", "AUT", "BEL", "BGR", "CAN", "CHE", "CYP", "CZE", "DEU", "DNK",
           "ESP", "EST", "FIN", "FRA", "GBR", "GRC", "HRV", "HUN", "IRL", "ISL",
           "ITA", "JPN", "LTU", "LUX", "LVA", "MLT", "NLD", "NOR", "NZL", "POL",
           "PRT", "ROU", "SVK", "SVN", "SWE", "USA"):
    R5[_c] = "R5.2OECD"
for _c in ("BGD", "BRN", "CHN", "HKG", "IDN", "IND", "KHM", "KOR", "LAO", "MMR",
           "MYS", "PAK", "PHL", "SGP", "THA", "TWN", "VNM"):
    R5[_c] = "R5.2ASIA"
for _c in ("AGO", "ARE", "CIV", "CMR", "COD", "EGY", "ISR", "JOR", "MAR", "NGA",
           "SAU", "SEN", "STP", "TUN", "TUR", "ZAF"):
    R5[_c] = "R5.2MAF"
for _c in ("ARG", "BRA", "CHL", "COL", "CRI", "MEX", "PER"):
    R5[_c] = "R5.2LAM"
for _c in ("BLR", "KAZ", "RUS", "UKR"):
    R5[_c] = "R5.2REF"
R5["ROW"] = "World"                     # the ICIO's own residual: blended path

FULL_NAME = {
    "EU27": "European Union (27 members)", "CHN": "China",
    "USA": "United States", "GBR": "United Kingdom", "CHE": "Switzerland",
    "RUS": "Russian Federation", "IND": "India", "JPN": "Japan",
    "NOR": "Norway", "KOR": "Korea", "TUR": "Turkiye", "SGP": "Singapore",
    "CAN": "Canada", "TWN": "Chinese Taipei", "VNM": "Viet Nam",
    "AUS": "Australia", "IDN": "Indonesia", "KAZ": "Kazakhstan",
    "CHL": "Chile", "MEA": "Middle East", "AFR": "Africa",
    "LAM": "Latin America", "ROW": "Rest of World",
    "RASIA": "Rest of Asia", "ROECD": "Rest of OECD",
    "RREF": "Reforming economies", "RLAM": "Rest of Latin America",
    "RWorld": "Unallocated",
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


def agg_ci(d, ms):
    """Linkage-weighted carbon intensity of a set of economies, t CO2e per $m."""
    return d.loc[ms].link_carbon.sum() / d.loc[ms].link_econ.sum() * 1e6


def dominance_cap(d, members):
    """The cap a residual must stay under: the largest SINGLE-economy region."""
    named = group(d, members).drop(index="ROW", errors="ignore")
    singles = named[named.n == 1]
    return singles.econ_pct.max(), singles.carb_pct.max()


def clean_zones(d, pool, k=CLEAN_K):
    """
    Split `pool` by R5 zone, then drop the members that spoil each zone.

    A member is dropped if its carbon intensity exceeds `k` times its own
    zone's linkage-weighted average.  Relative rather than absolute: a zone
    whose members are uniformly carbon-heavy is coherent and keeps everyone.

    Returns (cores, dropped) -- dropped economies belong to ROW.
    """
    zones = {}
    for c in pool:
        zones.setdefault(R5.get(c, "World").replace("R5.2", ""), []).append(c)

    cores, dropped = {}, []
    for z, ms in zones.items():
        if len(ms) == 1:
            cores[z] = ms
            continue
        limit = k * agg_ci(d, ms)
        core = [c for c in ms if d.loc[c, "ci"] * 1e6 <= limit]
        dropped += [c for c in ms if d.loc[c, "ci"] * 1e6 > limit]
        if core:
            cores[z] = core
    return cores, dropped


def promote_zones(d, cores, dropped, cap_e, cap_c):
    """
    Promote cleaned zones out of ROW until ROW no longer dominates.

    Ranked by economic linkage: the aim is to lift out the largest coherent
    geographic block, not to chase the constraint with whichever group happens
    to be carbon-heavy.  Returns (promoted labels, groups left inside ROW).
    """
    left, promoted = dict(cores), []
    while True:
        rest = [c for ms in left.values() for c in ms] + dropped
        e, c = d.loc[rest].econ_pct.sum(), d.loc[rest].carb_pct.sum()
        if (e <= cap_e and c <= cap_c) or len(left) <= 1:
            return promoted, left
        pick = max(left, key=lambda z: d.loc[left[z]].econ_pct.sum())
        promoted.append(pick)
        del left[pick]


def split_residual(d, members, k=CLEAN_K):
    """Everything the threshold rule did not keep: clean, then promote."""
    cap_e, cap_c = dominance_cap(d, members)
    assigned = {m for ms in members.values() for m in ms}
    pool = [c for c in d.index if c not in assigned]
    cores, dropped = clean_zones(d, pool, k)
    promoted, _ = promote_zones(d, cores, dropped, cap_e, cap_c)
    return ({"R" + z: cores[z] for z in promoted}, (cap_e, cap_c),
            (cores, dropped))


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

    print(f"\ncleaning threshold k -- sensitivity")
    print(f"{'k':>6}{'dropped':>9}{'promoted':>22}{'regions':>9}")
    for k_ in (1.25, 1.5, 1.75, 2.0, 2.5, 3.0):
        p_, _, (_, dr_) = split_residual(d, dict(members), k=k_)
        print(f"{k_:>6.2f}{len(dr_):>9}{', '.join(p_) or '-':>22}"
              f"{len(kept) + len(p_) + 1:>9}")

    if SPLIT_RESIDUAL:
        parts, (cap_e, cap_c), (cores, dropped) = split_residual(d, members)
        print(f"\nresidual: split by NGFS R5 zone, then cleaned at k = {CLEAN_K}"
              f"  (cap {cap_e:.2f} % econ / {cap_c:.2f} % carbon)")
        for z, ms in sorted(cores.items(),
                            key=lambda kv: -d.loc[kv[1]].econ_pct.sum()):
            e = d.loc[ms].econ_pct.sum()
            c = d.loc[ms].carb_pct.sum()
            print(f"   {z:<6} n={len(ms):>2}  {e:5.2f} % econ  {c:5.2f} % carbon"
                  f"  CI {agg_ci(d, ms):5.0f}"
                  f"{'   -> PROMOTED' if 'R' + z in parts else ''}")
        if dropped:
            print(f"   dropped to ROW ({len(dropped)}): {', '.join(sorted(dropped))}"
                  f"   {d.loc[dropped].econ_pct.sum():.2f} % econ, "
                  f"{d.loc[dropped].carb_pct.sum():.2f} % carbon, "
                  f"CI {agg_ci(d, dropped):.0f}")
        members.update(parts)
    residuals = ["ROW"]
    final = group(d, members)
    final = final[final.n > 0]
    final.to_csv(f"{ROOT}/out_region_selection_final.csv")
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
