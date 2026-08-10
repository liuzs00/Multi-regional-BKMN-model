"""
Robustness test: is the single ROW closure sufficient at the 13-region set?

Question: does lumping the 14 non-analytical economies (plus the ICIO's own
unallocated block) into one ROW bias the results for the 12 analytical regions?
ROW's own outputs are never interpreted, so only the analytical regions matter.

Method (aggregation-invariance / convergence test): rebuild the model from the
81-economy source under two partitions sharing the same 12 analytical regions,
  * COARSE — single ROW (the DATA_final model), and
  * FINE   — ROW split into its largest and most carbon-intensive members
             (JPN, CAN, AUS, IDN, KAZ, NOR, UKR, PAK) + a residual,
then compare the analytical regions' transition GVA shocks and Leontief output
multipliers.  Those eight are the worst case for aggregation bias — they carry
the most linkage and the widest intensity spread inside ROW — so if breaking
them out barely moves the analytical results, any finer split moves less.

The φ=0 / φ=1 endpoints are ROW-invariant by construction (the shock there is
the region's own ±CT/GVA), so the test runs at intermediate pass-through.

Note the irreducible part: the ICIO's unallocated block cannot be split by any
method, so it stays inside ROW under both partitions.

Usage: py -3 tools/test_row_sufficiency_13r.py
"""
import os
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r"D:\Download\2016-2022_SML\2022_SML.csv"
SPECIAL = {"TLS", "VA", "OUT"}
REN = {"C241_2431": "C24A", "C242_2432": "C24B", "C30X301": "C302T309"}
ANALYTIC = ["EU27", "CHN", "USA", "GBR", "CHE", "RUS", "IND", "TUR",
            "RASIA", "LAM", "MEA", "AFR"]
SPLIT = ["JPN", "CAN", "AUS", "IDN", "KAZ", "NOR", "UKR", "PAK"]
PHIS = (0.3, 0.5, 0.7)
XCE = 70.0


def load():
    df = pd.read_csv(SRC, index_col=0)
    cm = pd.read_csv(os.path.join(ROOT, "DATA_final", "region_mapping.csv"))
    coarse = dict(zip(cm.country, cm.region))
    fine = dict(coarse)
    for c in SPLIT:
        fine[c] = c
    gf = pd.read_csv(os.path.join(ROOT, "data", "ghgfp", "SCOPE", "2022.csv.gz"))
    gf = gf[(gf.EMISSIONS_SCOPE == "S1") & (gf.TIME_PERIOD == 2022)].copy()
    gf["t"] = gf.OBS_VALUE * 10.0 ** gf.UNIT_MULT
    gf["ind"] = gf.ACTIVITY.replace(REN)
    return df, coarse, fine, gf.groupby(["EMISSIONS_ORIGIN_AREA", "ind"])["t"].sum()


def build(df, Eec, regmap):
    def rof(cc):
        return regmap.get(cc, "ROW")

    def ml(l):
        if l in SPECIAL or l == "OUT":
            return l
        cc, rest = l.split("_", 1)
        return f"{rof(cc)}_{rest}"

    d = df.copy()
    d.columns = [ml(c) for c in d.columns]
    d = d.T.groupby(level=0).sum().T
    d.index = [ml(r) for r in d.index]
    d = d.groupby(level=0).sum()

    ri = [r for r in d.index if r not in SPECIAL]
    Z = d.loc[ri, ri].to_numpy(float)
    x = d.loc["OUT", ri].to_numpy(float)
    gva = d.loc["VA", ri].to_numpy(float)
    reg = np.array([l.split("_", 1)[0] for l in ri])
    ind = [l.split("_", 1)[1] for l in ri]

    E = {}
    for (e, i), v in Eec.items():
        r = "ROW" if e == "WXD" else rof(e)
        E[(r, i)] = E.get((r, i), 0.0) + v
    ci = np.array([E.get((reg[k], ind[k]), 0.0) / x[k] if x[k] > 0 else 0.0
                   for k in range(len(ri))])
    return Z, x, gva, reg, ci


def region_shock(model, phi):
    Z, x, gva, reg, ci = model
    A = Z / np.where(x == 0, 1.0, x)[None, :]
    n = len(x); I = np.eye(n); AT = A.T
    ct = ci * XCE * 1e-6
    Lt = np.linalg.inv(I - phi * AT) * phi
    dV = x * (((I - AT) @ Lt - I + phi * I) @ ct)
    return {r: dV[reg == r].sum() / gva[reg == r].sum() * 100 for r in set(reg)}


def region_multiplier(model):
    Z, x, _g, reg, _c = model
    A = Z / np.where(x == 0, 1.0, x)[None, :]
    m = np.linalg.inv(np.eye(len(x)) - A).sum(0)
    return {r: np.average(m[reg == r], weights=x[reg == r]) for r in set(reg)}


def main():
    df, coarse, fine, Eec = load()
    C, F = build(df, Eec, coarse), build(df, Eec, fine)
    print(f"coarse sectors={len(C[1])}  fine sectors={len(F[1])}  "
          f"(fine breaks out {SPLIT})\n")

    sc = {p: region_shock(C, p) for p in PHIS}
    sf = {p: region_shock(F, p) for p in PHIS}

    rows, maxd = [], 0.0
    print("Transition GVA shock (%), coarse ROW vs fine ROW")
    print(f"{'reg':6s}" + "".join(f"{'phi=' + str(p):>25s}" for p in PHIS))
    print(f"{'':6s}" + ("   coarse    fine     dpp") * len(PHIS))
    for r in ANALYTIC:
        line = f"{r:6s}"
        for p in PHIS:
            c, f = sc[p][r], sf[p][r]
            d = f - c
            maxd = max(maxd, abs(d))
            line += f"{c:9.3f}{f:8.3f}{d:+8.4f}"
            rows.append({"region": r, "phi": p, "coarse": c, "fine": f, "delta_pp": d})
        print(line)

    mc, mf = region_multiplier(C), region_multiplier(F)
    mm = max(abs(mf[r] - mc[r]) for r in ANALYTIC)
    relm = max(abs(mf[r] - mc[r]) / mc[r] for r in ANALYTIC)

    pd.DataFrame(rows).to_csv(os.path.join(ROOT, "out_row_sufficiency_13r.csv"),
                              index=False, float_format="%.5f")
    print(f"\n>>> MAX |delta| GVA shock ({len(ANALYTIC)} regions x {len(PHIS)} phi) "
          f"= {maxd:.4f} pp")
    print(f">>> MAX |delta| output multiplier = {mm:.4f} ({relm * 100:.3f}% relative)")
    print("saved: out_row_sufficiency_13r.csv")


if __name__ == "__main__":
    main()
