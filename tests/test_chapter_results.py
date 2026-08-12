"""
Gate every number quoted in docs/CHAPTER_RESULTS.md against the result tables.

That chapter is a dissertation deliverable and has been restructured more than
once -- from a Net-Zero-led narrative to a mixture-led one -- so its tables are
transcribed numbers that can silently fall out of step with the pipeline when
the region set, a data vintage or the reporting convention changes.  Every
figure printed in the chapter, plus the orderings and the qualitative claims
that depend on them ("the dollar is fourth on FX and twelfth on credit"), is
asserted here, so a stale sentence fails a run rather than reaching a reader.

The captions in docs/FIGURES.md get the same treatment in section 9, since they
quote values too.

Usage: py -3 tests/test_chapter_results.py    (exit 1 if any check fails)
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from bkmn import mixture as mx                # noqa: E402
from bkmn import equity, oprisk, regions      # noqa: E402
from bkmn.paper_tables import CDS_BETA        # noqa: E402
from bkmn.rates import hw_B                   # noqa: E402
from bkmn.scenarios import Scenarios          # noqa: E402

ok = []


def chk(l, g, w, t=5e-3):
    good = abs(g - w) <= t
    ok.append(good)
    print(f"  [{'OK ' if good else 'BAD'}] {l:<40} got {g:>10}  doc {w}")


def flag(l, c, d=""):
    ok.append(bool(c))
    print(f"  [{'OK ' if c else 'BAD'}] {l:<40} {d}")


m = regions.load()
cm = m.carbon_map.set_index("region")
FX = [r for r in m.regions_order if cm.loc[r, "fx_role"] == "analytical"]
P = ["uniform", "policy-sceptic", "ambition", "consensus"]
sc = Scenarios(m.carbon_map)


def M(ch, p, idx=0):
    return pd.read_csv(os.path.join(ROOT, f"out_mix_{ch}_{p}.csv"),
                       index_col=0 if idx == 0 else list(range(idx + 1)))


def S(n, i=(0, 1)):
    return pd.read_csv(os.path.join(ROOT, f"{n}.csv"), index_col=list(i))


print("1. setup")
chk("regions", len(m.regions_order), 13, 0)
chk("sectors", len(m.sectors), 650, 0)
chk("world output $tn", round(m.x.sum() / 1e6, 1), 199.7)
chk("world VA $tn", round(m.gva.sum() / 1e6, 1), 93.8)

print("1.2 prior weights")
w = pd.read_csv(os.path.join(ROOT, "out_mix_weights.csv"), index_col=0) * 100
NZ, CP = "Net Zero 2050", [s for s in w.index if s.startswith("Current")][0]
for s, u, ps, a, c in [(NZ, 14.3, 6.2, 23.5, 0.0),
                       ("Low demand", 14.3, 6.2, 17.6, 0.0),
                       ("Delayed transition", 14.3, 12.5, 11.8, 0.5),
                       ("Fragmented World", 14.3, 18.8, 5.9, 11.8),
                       (CP, 14.3, 25.0, 5.9, 80.7)]:
    chk(f"  {s[:18]} uniform", round(float(w.loc[s, "uniform"]), 1), u, 0.05)
    chk(f"  {s[:18]} sceptic", round(float(w.loc[s, "policy-sceptic"]), 1), ps, 0.05)
    chk(f"  {s[:18]} ambition", round(float(w.loc[s, "ambition"]), 1), a, 0.05)
    chk(f"  {s[:18]} consensus", round(float(w.loc[s, "consensus"]), 1), c, 0.05)
for s, t in [(NZ, 1.45), ("Low demand", 1.47), (CP, 2.75),
             ("Fragmented World", 2.11)]:
    chk(f"  dT2100 {s[:18]}", round(float(sc.temp.loc[2100, s]), 2), t)
flag("consensus concentrates on Current Policies",
     w["consensus"].idxmax() == CP, f"{float(w.loc[CP,'consensus']):.1f} %")
chk("  consensus anchor", mx.CONSENSUS_T, 2.7)
w14 = mx.weights("uniform")
u3 = mx.weights("uniform", {"Current Policies": 3})
chk("  CP after 3 events, a=14", round(u3[mx.CP] * 100, 1), 29.4)
chk("  CP base weight", round(w14[mx.CP] * 100, 1), 14.3)

print("2. real economy")
for r, u, ps, a, c, nz in [("IND", -3.00, -2.47, -3.47, -1.67, -5.66),
                           ("CHN", -2.90, -2.30, -3.42, -1.44, -5.86),
                           ("AFR", -2.43, -2.21, -2.65, -1.60, -3.66),
                           ("EU27", -1.23, -1.12, -1.33, -0.92, -1.79),
                           ("USA", -1.07, -0.99, -1.14, -0.84, -1.48),
                           ("GBR", -0.93, -0.87, -0.99, -0.74, -1.28),
                           ("CHE", -0.93, -0.88, -0.97, -0.79, -1.17)]:
    for p, v in zip(P, (u, ps, a, c)):
        chk(f"  total {r} {p[:9]}", round(float(M("gdp_total", p).loc[r, "2040"]), 2), v)
    chk(f"  total {r} NetZero", round(float(S("out_ext_gdp_total").xs(NZ, level=0)["2040"][r]), 2), nz)
for p, v in zip(P, (-0.84, -0.57, -1.08, -0.13)):
    chk(f"  transition mean {p[:9]}", round(float(M("gdp_transition", p)["2040"].mean()), 2), v)
for p, v in zip(P, (-1.06, -1.07, -1.05, -1.08)):
    chk(f"  physical mean {p[:9]}", round(float(M("gdp_physical", p)["2040"].mean()), 2), v)
tv = [float(M("gdp_transition", p)["2040"].mean()) for p in P]
pv = [float(M("gdp_physical", p)["2040"].mean()) for p in P]
chk("  transition prior range", round(min(tv) / max(tv), 1), 8.6, 0.05)
chk("  physical prior range", round(min(pv) / max(pv), 2), 1.03, 5e-3)

print("3. pass-through")
pt = S("out_phi_transition", (0,))
for phi, r, v in [(0.0, "IND", -20.90), (1.0, "IND", 20.90), (0.5, "EU27", -0.96),
                  (0.2, "EU27", -2.23), (0.6, "MEA", 0.07), (0.8, "USA", 1.39)]:
    chk(f"  phi={phi} {r}", round(float(pt.loc[phi, r]), 2), v)
zc = {}
p_ = pt.index.to_numpy(float)
for r in pt.columns:
    v = pt[r].to_numpy(float)
    i = np.where(np.diff(np.sign(v)) != 0)[0][0]
    zc[r] = p_[i] + (p_[i+1]-p_[i]) * (-v[i]) / (v[i+1]-v[i])
chk("  crossing min", round(min(zc.values()), 3), 0.574)
chk("  crossing max", round(max(zc.values()), 3), 0.812)
chk("  GBR crossing", round(zc["GBR"], 3), 0.676)
flag("all crossings > 0.5", all(v > 0.5 for v in zc.values()))
inv = S("out_phi_invariance", (0,))
chk("  rate invariance", float(inv.rate_IND_bp.max() - inv.rate_IND_bp.min()), 0.0, 0.0)
chk("  FX invariance", float(inv.fwd5_IND_pct.max() - inv.fwd5_IND_pct.min()), 0.0, 0.0)
chk("  IND rate", round(float(inv.rate_IND_bp.iloc[0]), 3), -68.515)
chk("  IND fwd", round(float(inv.fwd5_IND_pct.iloc[0]), 4), -3.6101, 5e-4)
pc = S("out_phi_credit", (0,))
chk("  IND credit phi=0", round(float(pc.loc[0.0, "IND"]), 1), 42.0)
chk("  IND credit phi=1", round(float(pc.loc[1.0, "IND"]), 1), -42.0)

print("4. rates")
for r, u, ps, a, c, nz in [("IND", -71.7, -72.4, -70.9, -72.7, -68.5),
                           ("AFR", -70.2, -71.1, -69.4, -71.7, -66.9),
                           ("EU27", -42.1, -43.1, -41.3, -44.0, -39.0),
                           ("GBR", -34.6, -35.2, -34.1, -35.7, -32.4)]:
    for p, v in zip(P, (u, ps, a, c)):
        chk(f"  rate {r} {p[:9]}", round(float(M("rate", p).loc[r, "2040"]), 1), v, 0.05)
    chk(f"  rate {r} NetZero", round(float(S("out_ext_rate_shift").xs(NZ, level=0)["2040"][r]), 1), nz, 0.05)
rv = [float(M("rate", p).loc["EU27", "2040"]) for p in P]
chk("  rate EU27 prior range", round(min(rv) / max(rv), 2), 1.06, 5e-3)
rm = [float(M("rate", p)["2040"].mean()) for p in P]
chk("  rate mean prior range", round(min(rm) / max(rm), 2), 1.04, 5e-3)
flag("mixture rates deeper than Net Zero",
     all(float(M("rate", p).loc["EU27", "2040"])
         < float(S("out_ext_rate_shift").xs(NZ, level=0)["2040"]["EU27"]) for p in P))
allr = S("out_ext_rate_shift")
Y = ["2025", "2030", "2035", "2040", "2045"]
chk("  region-scenario pairs", len(allr), 91, 0)
flag("no positive rate", int((allr[Y] > 0).sum().sum()) == 0)
chk("  deepest cut", round(float(allr[Y].min().min()), 1), -81.6)
inf = S("out_inflation_shift").xs(NZ, level=0)
rrz = S("out_ext_rate_shift").xs(NZ, level=0)
chk("  EU27 inflation half 2030", round(0.5 * float(inf.loc["EU27", "2030"]), 1), 17.4)
chk("  EU27 damage 2030", round(float(rrz.loc["EU27", "2030"]) - 0.5 * float(inf.loc["EU27", "2030"]), 1), -34.2)
ts = S("out_ext_rate_term_structure", (0, 1, 2)).xs(NZ, level=0)["2040"].unstack()
for r, t, v in [("IND", "1D", -68.5), ("IND", "20Y", -47.2), ("EU27", "20Y", -26.8),
                ("GBR", "10Y", -26.7), ("CHN", "5Y", -49.1)]:
    chk(f"  {r} {t}", round(float(ts.loc[r, t]), 1), v, 0.05)
ratio = (ts["20Y"] / ts["1D"]).round(4)
flag("20Y/1D identical", ratio.nunique() == 1)
chk("  ratio", round(float(ratio.iloc[0]), 4), 0.6884, 5e-5)
# the ratio the chapter quotes is not fitted: at a = 0.04 it is the ratio of two
# closed-form B(tau)/tau factors, so assert the table against the formula rather
# than against itself.  The overnight leg is B(1/365)*365, not 1 -- close enough
# that dropping it would move the fourth decimal (0.6883 vs 0.6884), which is
# exactly the digit the chapter prints
an = (hw_B(20.0) / 20.0) / (hw_B(1 / 365) * 365)
chk("  ratio is analytic B(20)/20", round(float(an), 4), 0.6884, 5e-5)

print("5. FX")
for r, u, ps, a, c, nz in [("IND", -2.04, -1.75, -2.31, -1.35, -3.61),
                           ("TUR", -1.40, -1.10, -1.67, -0.69, -3.00),
                           ("CHN", -0.95, -0.88, -1.03, -0.74, -1.39),
                           ("USA", -0.51, -0.25, -0.75, 0.10, -1.91),
                           ("CHE", -0.02, 0.08, -0.12, 0.22, -0.59),
                           ("GBR", -0.01, 0.15, -0.15, 0.35, -0.83)]:
    for p, v in zip(P, (u, ps, a, c)):
        chk(f"  fwd {r} {p[:9]}", round(float(M("fx_forward", p).loc[r, "2040"]), 2), v)
    chk(f"  fwd {r} NetZero", round(float(S("out_ext_fx_forward_5y").xs(NZ, level=0).loc[r, "2040"]), 2), nz)
flips = [r for r in FX
         if np.sign(M("fx_forward", "ambition").loc[r, "2040"])
         != np.sign(M("fx_forward", "consensus").loc[r, "2040"])]
flag("sign flips are USD, GBP, CHF", sorted(flips) == ["CHE", "GBR", "USA"], str(sorted(flips)))
flag("INR and TRY keep their sign",
     all(np.sign(M("fx_forward", p).loc[r, "2040"]) < 0 for p in P for r in ("IND", "TUR")))
sv = [float(M("fx_spot", p).loc["IND", "2040"]) for p in P]
fv = [float(M("fx_forward", p).loc["IND", "2040"]) for p in P]
chk("  spot prior range", round(min(sv) / max(sv), 1), 22.7, 0.05)
chk("  fwd prior range", round(min(fv) / max(fv), 1), 1.7, 0.05)
flag("spot negative under every prior",
     all(float(M("fx_spot", p).loc[r, "2040"]) < 0 for p in P for r in FX))
sc_ = cm.carbon_scope.astype(float)
flag("EU27 highest scope", all(sc_[r] < sc_["EU27"] for r in FX))
chk("  next scope", round(max(sc_[r] for r in FX), 3), 0.467)
spz = S("out_ext_fx_spot").xs(NZ, level=0)
chk("  corr(spot,scope) NZ 2045",
    round(float(np.corrcoef(spz.loc[FX, "2045"], [sc_[r] for r in FX])[0, 1]), 4), 0.9999, 5e-4)

print("6. credit / equity / oprisk")
for r, u, ps, a, c, nz in [("IND", 5.90, 4.24, 7.36, 1.78, 14.2),
                           ("CHN", 4.37, 3.37, 5.24, 1.93, 9.3),
                           ("AFR", 4.33, 3.58, 5.08, 1.59, 8.5),
                           ("EU27", 2.04, 1.70, 2.36, 1.04, 3.8),
                           ("USA", 1.16, 0.92, 1.40, 0.49, 2.4),
                           ("CHE", 1.05, 0.95, 1.14, 0.78, 1.5)]:
    for p, v in zip(P, (u, ps, a, c)):
        cc = M("credit", p, 1)["2040"].unstack().drop(columns=["FTSE"]).median(axis=1)
        chk(f"  credit {r} {p[:9]}", round(float(cc[r]), 2), v)
    nzc = S("out_ext_credit_spread", (0, 1, 2)).xs(NZ, level=0)["2040"].unstack().drop(columns=["FTSE"])
    chk(f"  credit {r} NetZero", round(float(nzc.median(axis=1)[r]), 1), nz)
cvals = [float(M("credit", p, 1)["2040"].unstack().drop(columns=["FTSE"]).median(axis=1)["IND"]) for p in P]
chk("  credit prior range", round(max(cvals) / min(cvals), 1), 4.1, 0.05)
cons_c = M("credit", "consensus", 1)["2040"].unstack().drop(columns=["FTSE"]).median()
for s, v in [("Health Care", 4.86), ("Basic Materials", 2.93),
             ("Consumer Goods", 2.67), ("Utilities", 2.18)]:
    chk(f"  consensus sector {s[:14]}", round(float(cons_c[s]), 2), v)
flag("financials and real estate negative under consensus",
     cons_c["Financials"] < 0 and cons_c["UK Real Estate"] < 0)
nzc = S("out_ext_credit_spread", (0, 1, 2)).xs(NZ, level=0)["2040"].unstack().drop(columns=["FTSE"])
stk = nzc.stack().rename("v").reset_index()
stk.columns = ["region", "index", "v"]
chk("  sector variance %", round(stk.groupby("index").v.mean().var() / stk.v.var() * 100), 61, 1)
chk("  region variance %", round(stk.groupby("region").v.mean().var() / stk.v.var() * 100), 19, 1)
chk("  corr(beta, median)",
    round(float(np.corrcoef([CDS_BETA[c] for c in nzc.median().index], nzc.median().values)[0, 1]), 2), -0.65)
eq = M("equity", "uniform")["2040"]
oc = M("oprisk_conduct", "uniform")["2040"]
b = equity.betas()
u0 = oprisk.base_unemployment() * 100
for r, e_, be, o, uu in [("AFR", -4.86, 2.00, 3.45, 8.03), ("TUR", -4.50, 1.89, 2.15, 10.46),
                         ("RASIA", -4.45, 2.00, 10.71, 2.83), ("IND", -4.14, 1.38, 5.82, 4.82),
                         ("USA", -1.70, 1.59, 8.64, 3.65), ("EU27", -0.98, 0.80, 5.52, 6.16),
                         ("CHN", -0.76, 0.26, 4.66, 4.98), ("GBR", -0.51, 0.55, 4.45, 3.77)]:
    chk(f"  equity {r}", round(float(eq[r]), 2), e_)
    chk(f"  beta {r}", round(float(b[r]), 2), be)
    chk(f"  conduct {r}", round(float(oc[r]), 2), o)
    chk(f"  U0 {r}", round(float(u0[r]), 2), uu)
ov = [float(M("oprisk_conduct", p).loc["RASIA", "2040"]) for p in P]
chk("  oprisk prior range", round(max(ov) / min(ov), 2), 1.03, 5e-3)
ev = [float(M("equity", p)["2040"].mean()) for p in P]
chk("  equity prior range", round(min(ev) / max(ev), 1), 1.7, 0.05)
gv = [float(M("gdp_total", p)["2040"].mean()) for p in P]
chk("  total GDP prior range", round(min(gv) / max(gv), 1), 1.8, 0.05)
cal = equity.calibrate()
chk("  proxy-beta regions", len([r for r in m.regions_order
                                 if r not in cal or cal[r][2] == "proxy"]), 7, 0)

print("7. scenario decomposition and tail")
for s, a, bb, c, d in [(NZ, -2.20, -1.01, 3.30, 3.95),
                       ("Low demand", -1.19, -1.02, 2.43, 2.46),
                       ("Delayed transition", -0.88, -1.09, 2.12, 2.14),
                       (CP, -0.06, -1.07, 1.88, 0.82)]:
    chk(f"  {s[:14]} trans", round(float(S("out_ext_gdp_transition").xs(s, level=0)["2040"].mean()), 2), a)
    chk(f"  {s[:14]} phys", round(float(S("out_ext_gdp_physical").xs(s, level=0)["2040"].mean()), 2), bb)
    f_ = S("out_ext_fx_forward_5y").xs(s, level=0).loc[FX, "2045"]
    chk(f"  {s[:14]} fwd rng", round(float(f_.max() - f_.min()), 2), c)
    cc = S("out_ext_credit_spread", (0, 1, 2)).xs(s, level=0)["2040"].unstack().drop(columns=["FTSE"])
    chk(f"  {s[:14]} credit", round(float(cc.stack().median()), 2), d)
tms = [float(S("out_ext_gdp_transition").xs(s, level=0)["2040"].mean())
       for s in S("out_ext_gdp_transition").index.get_level_values(0).unique()]
chk("  scenario transition factor", round(min(tms) / max(tms)), 37, 1)
q = S("out_ext_fx_forward_q95").xs(NZ, level=0)["2040"]
fwz = S("out_ext_fx_forward_5y").xs(NZ, level=0)["2040"]
for r, cc, qq in [("IND", -3.61, -4.09), ("TUR", -3.00, -4.01), ("USA", -1.91, -3.37),
                  ("CHN", -1.39, -2.20), ("GBR", -0.83, -1.91), ("CHE", -0.59, -1.32)]:
    chk(f"  central {r}", round(float(fwz[r]), 2), cc)
    chk(f"  stressed {r}", round(float(q[r]), 2), qq)

print("8. orderings (uniform prior)")
fu = M("fx_forward", "uniform")["2040"]
ru = M("rate", "uniform")["2040"]
cu = M("credit", "uniform", 1)["2040"].unstack().drop(columns=["FTSE"]).median(axis=1)
equ = M("equity", "uniform")["2040"]
flag("FX order", list(fu.loc[FX].sort_values().index) == ["IND", "TUR", "CHN", "USA", "CHE", "GBR"],
     str(list(fu.loc[FX].sort_values().index[:5])))
flag("rate top5", list(ru.sort_values().index[:5]) == ["IND", "AFR", "MEA", "CHN", "RASIA"],
     str(list(ru.sort_values().index[:5])))
flag("credit top5", list(cu.sort_values(ascending=False).index[:5]) == ["IND", "CHN", "AFR", "TUR", "RUS"],
     str(list(cu.sort_values(ascending=False).index[:5])))
flag("equity top5", list(equ.sort_values().index[:5]) == ["AFR", "TUR", "RASIA", "IND", "MEA"],
     str(list(equ.sort_values().index[:5])))
flag("USA 12th on credit", list(cu.sort_values(ascending=False).index).index("USA") == 11)
flag("AFR/MEA have no FX", "AFR" not in FX and "MEA" not in FX)

print("9. FIGURES.md captions")
nzf = S("out_ext_fx_forward_5y").xs(NZ, level=0)["2040"]
mxf = M("fx_forward", "uniform")["2040"]
for r, v in [("IND", 1.8), ("TUR", 2.1), ("CHN", 1.5), ("USA", 3.7)]:
    chk(f"  fig2 overstatement {r}", round(float(nzf[r] / mxf[r]), 1), v, 0.05)
chk("  fig2 CHE overstatement", round(float(nzf["CHE"] / mxf["CHE"])), 25, 0.5)
chk("  fig2 GBR overstatement", round(float(nzf["GBR"] / mxf["GBR"])), 120, 0.5)
flag("fig2 Net Zero outside every bar", all(nzf[r] < mxf[r] for r in FX))
zs = pd.Series(zc).sort_values()
flag("fig14 min crossing is AFR", zs.index[0] == "AFR")
flag("fig14 max crossing is CHE", zs.index[-1] == "CHE")
flag("fig14 GBR is second-highest", zs.index[-2] == "GBR")
flag("fig15 exists", os.path.exists(os.path.join(ROOT, "figures", "fig15_prior_sensitivity.png")))

print()
bad = sum(1 for v in ok if not v)
print(f"{'ALL ' + str(len(ok)) + ' CHECKS PASSED' if not bad else str(bad) + ' FAILED of ' + str(len(ok))}")
sys.exit(0 if not bad else 1)
