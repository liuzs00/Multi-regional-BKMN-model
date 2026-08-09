"""
Region selection by EU-centric agglomerative merging.

Derives the region set instead of asserting it.  The question a selection
algorithm has to answer is not "which economies are biggest" but "which
economies, if left inside an aggregate, would make that aggregate misrepresent
them".  Promoting an economy out of a block buys RESOLUTION: inside a block
everything shares one carbon price, one carbon intensity, one vulnerability and
one currency.  So the cost of merging two groups is the heterogeneity the merge
introduces, weighted by how much the EU depends on them.

Method (Miller & Blair ch. 12 in spirit, Ward's criterion in form):

  linkage      x_EU = (I - A)^-1 f_EU  -- output in every economy-sector needed
               to satisfy EU final demand.  Economic linkage of economy c is its
               share of that; carbon linkage weights it by carbon intensity, i.e.
               emissions embodied in EU final demand (consumption-based).

  attributes   log carbon intensity, ND-GAIN vulnerability -- the things that
               actually differ inside a block and drive the model.  Standardised.

  merge cost   Ward, weighted by linkage:
                   cost(G,H) = w_G w_H / (w_G + w_H) * ||centroid_G - centroid_H||^2
               so merging two large, dissimilar, EU-relevant groups is expensive
               and merging two small similar ones is nearly free.

Nothing caps the number of regions.  The run reports the whole merge order plus
the two structural stopping rules: the largest group must not dominate either
linkage measure.

Usage: py -3 tools/select_regions.py
"""
import os
import sys
import zipfile

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

SRC = r"D:\2016-2022_SML\2022_SML.csv"
GHG = os.path.join(ROOT, "data", "ghgfp", "SCOPE", "2022.csv.gz")
NDGAIN = os.path.join(ROOT, "data", "physical", "ndgain_resources.zip")
YEAR = 2022
FD_CATS = ["HFCE", "NPISH", "GGFC", "GFCF", "INVNT", "DPABR"]
EU27 = ("AUT BEL BGR CYP CZE DEU DNK ESP EST FIN FRA GRC HRV HUN IRL ITA LTU "
        "LUX LVA MLT NLD POL PRT ROU SVK SVN SWE").split()

# Economies whose currency the FX deliverable needs as its own region.  Used
# only for the "feasible" variant; the headline run protects nothing, so the
# algorithm's own choices can be compared against ours.
CURRENCIES = "USA CHN GBR JPN IND CAN NOR IDN CHL AUS SGP TUR KOR KAZ".split()


def load_table():
    df = pd.read_csv(SRC, index_col=0)
    cols = list(df.columns)
    sect = [c for c in cols if "_" in c and c.split("_", 1)[1] not in FD_CATS
            and c != "OUT"]
    fd = [c for c in cols if "_" in c and c.split("_", 1)[1] in FD_CATS]
    Z = df.loc[sect, sect].to_numpy(float)
    F = df.loc[sect, fd]
    x = df.loc[sect, "OUT"].to_numpy(float)
    econ = np.array([s.split("_", 1)[0] for s in sect])
    return Z, F, x, econ, sect


def eu_footprint(Z, F, x, econ):
    """Output in every sector required to satisfy EU27 final demand."""
    xs = np.where(x == 0, 1.0, x)
    A = Z / xs                                     # column-normalised
    eu_fd = [c for c in F.columns if c.split("_", 1)[0] in EU27]
    f = F[eu_fd].to_numpy(float).sum(axis=1)
    return np.linalg.solve(np.eye(len(x)) - A, f)  # one solve, no inversion


# The two sources name the ICIO's own unallocated residual differently: the
# input-output table calls it ROW, the GHG footprint calls it WXD.  Without this
# alias the residual gets no emissions at all and falls back to a median carbon
# intensity, which understates it -- WXD is 4,304 Mt CO2e in 2022, the third
# largest Scope-1 total in the file.
GHG_ALIAS = {"ROW": "WXD"}


def economy_attributes(econ, sect, x, x_eu):
    """Per-economy linkage weights and the attributes a block must not blur."""
    ghg = pd.read_csv(GHG)
    ghg = ghg[(ghg.TIME_PERIOD == YEAR) & (ghg.EMISSIONS_SCOPE.astype(str).str.upper()
                                           .str.contains("1"))]
    e = ghg.groupby("EMISSIONS_ORIGIN_AREA").OBS_VALUE.sum()
    for icio_code, ghg_code in GHG_ALIAS.items():
        if ghg_code in e.index:
            e[icio_code] = e[ghg_code]

    with zipfile.ZipFile(NDGAIN) as z:
        v = pd.read_csv(z.open("resources/vulnerability/vulnerability.csv"))
    vcol = sorted(c for c in v.columns if c.strip().isdigit())
    vuln = v.set_index("ISO3")[vcol[-1]]

    rows = {}
    for c in sorted(set(econ)):
        m = econ == c
        rows[c] = {
            "gross_output": x[m].sum(),
            "link_econ": x_eu[m].sum(),
            "emissions": float(e.get(c, np.nan)),
            "vuln": float(vuln.get(c, np.nan)),
        }
    d = pd.DataFrame(rows).T
    d["ci"] = d.emissions / d.gross_output.replace(0, np.nan)
    d["link_carbon"] = d.link_econ * d.ci
    return d


def ward_merge(d, protect=()):
    """
    Agglomerative merge; returns the merge order and the group at every step.

    Groups start as singletons.  EU27 is pre-merged (it is the base region) and
    never merges again; anything in `protect` never merges either.
    """
    attrs = ["log_ci", "vuln_z"]
    X = d[attrs].to_numpy(float)
    w = d["link_econ"].to_numpy(float)
    names = list(d.index)

    groups = {}
    eu_idx = [i for i, n in enumerate(names) if n in EU27]
    if eu_idx:
        groups["EU27"] = eu_idx
    for i, n in enumerate(names):
        if n not in EU27:
            groups[n] = [i]
    frozen = {"EU27", *protect}

    def centroid(g):
        ww = w[g]
        return (X[g] * ww[:, None]).sum(0) / ww.sum() if ww.sum() > 0 else X[g].mean(0)

    order = []
    while True:
        keys = [k for k in groups if k not in frozen]
        if len(keys) < 2:
            break
        best, bc = None, np.inf
        cen = {k: centroid(groups[k]) for k in keys}
        wt = {k: w[groups[k]].sum() for k in keys}
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = keys[i], keys[j]
                wa, wb = wt[a], wt[b]
                if wa + wb == 0:
                    c = 0.0
                else:
                    c = wa * wb / (wa + wb) * float(((cen[a] - cen[b]) ** 2).sum())
                if c < bc:
                    best, bc = (a, b), c
        a, b = best
        merged = f"{a}+{b}"
        groups[merged] = groups.pop(a) + groups.pop(b)
        order.append({"step": len(order) + 1, "a": a, "b": b, "cost": bc,
                      "n_groups": len(groups)})
    return pd.DataFrame(order), groups


def groups_at(order, d, k):
    """Rebuild the grouping after enough merges to leave k non-EU groups."""
    g = {n: [n] for n in d.index if n not in EU27}
    g["EU27"] = [n for n in d.index if n in EU27]
    for _, r in order.iterrows():
        if len(g) - 1 <= k:
            break
        g[f"{r.a}+{r.b}"] = g.pop(r.a) + g.pop(r.b)
    return g


def evaluate(g, d):
    """
    Linkage of every group, and whether any AGGREGATE outranks every named
    (single-economy) region.

    This is the operational form of "ROW must not be the largest".  Under
    agglomerative merging there is no residual bucket, so the constraint becomes:
    every multi-member group must be smaller, on both linkage measures, than the
    largest single-economy region.  While a big player is still buried inside an
    aggregate the rule fails, which is exactly the behaviour wanted.
    """
    rows = {}
    for name, mem in g.items():
        sub = d.loc[mem]
        rows[name] = {"n": len(mem),
                      "econ_pct": sub.link_econ.sum() / d.link_econ.sum() * 100,
                      "carb_pct": sub.link_carbon.sum() / d.link_carbon.sum() * 100}
    t = pd.DataFrame(rows).T.sort_values("econ_pct", ascending=False)
    nb = t.drop(index="EU27", errors="ignore")
    agg, sing = nb[nb.n > 1], nb[nb.n == 1]
    if agg.empty:
        return t, None, (False, False)
    big = agg.econ_pct.idxmax()
    hi_e = sing.econ_pct.max() if not sing.empty else 0.0
    hi_c = sing.carb_pct.max() if not sing.empty else 0.0
    return t, big, (agg.econ_pct.max() > hi_e, agg.carb_pct.max() > hi_c)


def main():
    print("loading the 81-economy 2022 ICIO ...")
    Z, F, x, econ, sect = load_table()
    print(f"  {len(sect)} economy-sectors, {len(set(econ))} economies")
    x_eu = eu_footprint(Z, F, x, econ)
    print(f"  EU final demand pulls ${x_eu.sum()/1e6:,.2f} tn of gross output worldwide")

    d = economy_attributes(econ, sect, x, x_eu)
    d = d[~d.index.isin(["ROW"])]                     # the source's own residual
    d["log_ci"] = np.log(d.ci.replace(0, np.nan))
    for c in ("log_ci", "vuln"):
        d[c] = d[c].fillna(d[c].median())
    d["log_ci"] = (d.log_ci - d.log_ci.mean()) / d.log_ci.std()
    d["vuln_z"] = (d.vuln - d.vuln.mean()) / d.vuln.std()
    d.to_csv(f"{ROOT}/out_region_attributes.csv")

    print("\ntop EU linkages (share of EU-final-demand footprint):")
    tot_e, tot_c = d.link_econ.sum(), d.link_carbon.sum()
    top = d.assign(pe=d.link_econ / tot_e * 100,
                   pc=d.link_carbon / tot_c * 100).sort_values("pe", ascending=False)
    print(top[["pe", "pc"]].head(12).round(2).to_string())

    order, groups = ward_merge(d)
    order.to_csv(f"{ROOT}/out_region_merge_order.csv", index=False)
    print(f"\nmerge order written ({len(order)} merges).")

    print("\nstopping rules -- does the biggest group dominate either linkage?")
    print(f"{'k':>4}  {'biggest group':<22}{'n':>4}{'econ%':>8}{'carb%':>8}"
          f"{'dom_econ':>10}{'dom_carb':>10}")
    first_ok = None
    for k in range(2, 56):
        g = groups_at(order, d, k)
        t, big, (de, dc) = evaluate(g, d)
        if k <= 40 and (k <= 24 or k % 4 == 0):
            print(f"{k:>4}  {big[:20]:<22}{int(t.loc[big,'n']):>4}"
                  f"{t.loc[big,'econ_pct']:>8.2f}{t.loc[big,'carb_pct']:>8.2f}"
                  f"{str(de):>10}{str(dc):>10}")
        if first_ok is None and not de and not dc:
            first_ok = k
    print(f"\n  -> both rules first satisfied at k = {first_ok} non-EU groups "
          f"({first_ok + 1} regions including EU27)")

    if first_ok:
        g = groups_at(order, d, first_ok)
        print(f"\nthe {first_ok + 1}-region set the algorithm chooses:\n")
        t, _, _ = evaluate(g, d)
        for name in t.index:
            mem = g[name]
            lab = mem[0] if len(mem) == 1 else f"[{len(mem)}] " + "+".join(sorted(mem))
            print(f"   {t.loc[name,'econ_pct']:6.2f}% econ {t.loc[name,'carb_pct']:6.2f}%"
                  f" carb   {lab[:110]}")
    return d, order, groups


if __name__ == "__main__":
    main()
