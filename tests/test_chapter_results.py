"""
Gate every number quoted in docs/CHAPTER_RESULTS.md against the result tables.

That chapter is a dissertation deliverable and has been restructured more than
once -- Net-Zero-led, then mixture-led, now consensus-led and restricted to the
regions with a legal currency -- so its tables are transcribed numbers that can
silently fall out of step with the pipeline when the region set, a data vintage
or the reporting convention changes.  Every figure printed in the chapter, plus
the orderings and the qualitative claims that depend on them ("China is first on
credit and last on equity"), is asserted here, so a stale sentence fails a run
rather than reaching a reader.

The captions in docs/FIGURES.md get the same treatment in section 10, since they
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
    print(f"  [{'OK ' if good else 'BAD'}] {l:<44} got {g:>10}  doc {w}")


def flag(l, c, d=""):
    ok.append(bool(c))
    print(f"  [{'OK ' if c else 'BAD'}] {l:<44} {d}")


m = regions.load()
cm = m.carbon_map.set_index("region")
CCY = [r for r in m.regions_order if cm.loc[r, "currency"] not in ("mixed", "-", "—")]
FX = [r for r in m.regions_order if cm.loc[r, "fx_role"] == "analytical"]
P = ["uniform", "policy-sceptic", "ambition", "consensus"]
HEAD = "consensus"
sc = Scenarios(m.carbon_map)


def M(ch, p=HEAD, idx=0):
    return pd.read_csv(os.path.join(ROOT, f"out_mix_{ch}_{p}.csv"),
                       index_col=0 if idx == 0 else list(range(idx + 1)))


def S(n, i=(0, 1)):
    return pd.read_csv(os.path.join(ROOT, f"{n}.csv"), index_col=list(i))


def credit(p=HEAD, regs=None):
    c = M("credit", p, 1)["2040"].unstack().drop(columns=["FTSE"])
    return c.loc[regs] if regs is not None else c


print("1.1 setup")
chk("regions", len(m.regions_order), 13, 0)
chk("sectors", len(m.sectors), 650, 0)
chk("world output $tn", round(m.x.sum() / 1e6, 1), 199.7)
chk("world VA $tn", round(m.gva.sum() / 1e6, 1), 93.8)

print("1.2 prior weights")
w = pd.read_csv(os.path.join(ROOT, "out_mix_weights.csv"), index_col=0) * 100
NZ, CP = "Net Zero 2050", [s for s in w.index if s.startswith("Current")][0]
B2 = [s for s in w.index if s.startswith("Below")][0]
NDC = [s for s in w.index if s.startswith("Nationally")][0]
for s, u, ps, a, c, t in [(NZ, 14.3, 6.2, 23.5, 0.0, 1.45),
                          ("Low demand", 14.3, 6.2, 17.6, 0.0, 1.47),
                          (B2, 14.3, 6.2, 23.5, 0.3, 1.69),
                          ("Delayed transition", 14.3, 12.5, 11.8, 0.5, 1.75),
                          (NDC, 14.3, 25.0, 11.8, 6.7, 2.03),
                          ("Fragmented World", 14.3, 18.8, 5.9, 11.8, 2.11),
                          (CP, 14.3, 25.0, 5.9, 80.7, 2.75)]:
    for p, v in zip(P, (u, ps, a, c)):
        chk(f"  {s[:16]} {p[:9]}", round(float(w.loc[s, p]), 1), v, 0.05)
    chk(f"  dT2100 {s[:16]}", round(float(sc.temp.loc[2100, s]), 2), t)
chk("  consensus anchor", mx.CONSENSUS_T, 2.7)
chk("  CP after 3 events, a=14", round(mx.weights("uniform", {"Current Policies": 3})[mx.CP] * 100, 1), 29.4)
chk("  CP base weight", round(mx.weights("uniform")[mx.CP] * 100, 1), 14.3)

print("1.3-1.4 conventions")
flag("consensus concentrates on Current Policies", w["consensus"].idxmax() == CP)
flag("nine currency regions", len(CCY) == 9, str(CCY))
flag("dropped four are the mixed-currency ones",
     sorted(set(m.regions_order) - set(CCY)) == ["AFR", "LAM", "RASIA", "ROW"])
flag("MEA is the USD peg", cm.loc["MEA", "currency"] == "USD-peg")
flag("EU27 is the FX base", cm.loc["EU27", "fx_role"] == "base")
flag("six analytical currencies", len(FX) == 6, str(FX))

print("2. real economy")
tot = M("gdp_total")
for r, y25, y30, y40, y45 in [("IND", -0.95, -1.21, -1.67, -1.86), ("AFR", -0.94, -1.18, -1.60, -1.79),
                              ("CHN", -0.79, -1.04, -1.44, -1.60), ("MEA", -0.86, -1.06, -1.43, -1.59),
                              ("TUR", -0.76, -1.00, -1.37, -1.53), ("RASIA", -0.77, -0.97, -1.33, -1.48),
                              ("LAM", -0.73, -1.03, -1.27, -1.39), ("ROW", -0.66, -0.84, -1.13, -1.25),
                              ("RUS", -0.59, -0.76, -1.08, -1.21), ("EU27", -0.57, -0.68, -0.92, -1.02),
                              ("USA", -0.53, -0.63, -0.84, -0.94), ("CHE", -0.51, -0.59, -0.79, -0.89),
                              ("GBR", -0.47, -0.55, -0.74, -0.83)]:
    for y, v in zip(("2025", "2030", "2040", "2045"), (y25, y30, y40, y45)):
        chk(f"  total {r} {y}", round(float(tot.loc[r, y]), 2), v)
flag("worst/best spread just over 2x",
     2.0 < float(tot["2040"].min() / tot["2040"].max()) < 2.4,
     f"{float(tot['2040'].min()/tot['2040'].max()):.2f}x")
for ch, cons, u, ps, a in [("gdp_transition", -0.13, -0.84, -0.57, -1.08),
                           ("gdp_physical", -1.08, -1.06, -1.07, -1.05)]:
    for p, v in zip(("consensus", "uniform", "policy-sceptic", "ambition"), (cons, u, ps, a)):
        chk(f"  {ch[4:]} {p[:9]}", round(float(M(ch, p)["2040"].mean()), 2), v)
tv = [float(M("gdp_transition", p)["2040"].mean()) for p in P]
pv = [float(M("gdp_physical", p)["2040"].mean()) for p in P]
chk("  transition prior range", round(min(tv) / max(tv), 1), 8.6, 0.05)
chk("  physical prior range", round(min(pv) / max(pv), 2), 1.03, 5e-3)
chk("  transition/physical ratio, consensus",
    round(float(M("gdp_physical")["2040"].mean() / M("gdp_transition")["2040"].mean()), 1), 8.6, 0.05)
chk("  Net Zero transition mean", round(float(S("out_ext_gdp_transition").xs(NZ, level=0)["2040"].mean()), 2), -2.20)

print("3. pass-through")
# the sweep is consensus-weighted like every other channel; the chapter splits
# its content into scenario-scaled levels, scenario-free structure, and the
# crossing, which sits between the two.  Each of the three is gated separately.
pt = S("out_phi_transition", (0,))
pts = S("out_phi_transition_scen")
# Table 4 in full: 13 regions x 11 phi, transposed so phi runs across the top
TABLE4 = {
    "EU27":  [-0.100, -0.090, -0.079, -0.067, -0.054, -0.040, -0.022, -0.002, 0.023, 0.056, 0.100],
    "CHN":   [-0.707, -0.627, -0.541, -0.449, -0.348, -0.235, -0.108, 0.040, 0.216, 0.432, 0.707],
    "USA":   [-0.112, -0.097, -0.081, -0.065, -0.047, -0.027, -0.006, 0.018, 0.044, 0.075, 0.112],
    "GBR":   [-0.063, -0.057, -0.050, -0.042, -0.034, -0.025, -0.015, -0.002, 0.013, 0.034, 0.063],
    "CHE":   [-0.024, -0.024, -0.023, -0.022, -0.021, -0.019, -0.017, -0.013, -0.006, 0.005, 0.024],
    "RUS":   [-0.752, -0.649, -0.540, -0.425, -0.303, -0.171, -0.028, 0.131, 0.309, 0.513, 0.752],
    "IND":   [-1.030, -0.885, -0.733, -0.571, -0.400, -0.216, -0.016, 0.202, 0.445, 0.717, 1.030],
    "TUR":   [-0.835, -0.726, -0.610, -0.485, -0.349, -0.202, -0.040, 0.139, 0.341, 0.570, 0.835],
    "RASIA": [-0.465, -0.410, -0.352, -0.290, -0.221, -0.146, -0.061, 0.036, 0.151, 0.291, 0.465],
    "LAM":   [-0.790, -0.676, -0.556, -0.429, -0.294, -0.151, 0.004, 0.172, 0.355, 0.559, 0.790],
    "MEA":   [-0.659, -0.561, -0.458, -0.350, -0.236, -0.115, 0.015, 0.154, 0.306, 0.473, 0.659],
    "AFR":   [-1.216, -1.024, -0.824, -0.616, -0.398, -0.170, 0.072, 0.328, 0.601, 0.896, 1.216],
    "ROW":   [-0.533, -0.458, -0.379, -0.295, -0.206, -0.111, -0.007, 0.106, 0.231, 0.372, 0.533],
}
_phis = [round(0.1 * i, 1) for i in range(11)]
flag("Table 4 covers every region", sorted(TABLE4) == sorted(m.regions_order))
flag("Table 4 covers phi 0 to 1 in steps of 0.1",
     [round(float(x), 1) for x in pt.index] == _phis)
for r, row in TABLE4.items():
    bad = [(p, round(float(pt.loc[p, r]), 3), v) for p, v in zip(_phis, row)
           if abs(round(float(pt.loc[p, r]), 3) - v) > 5e-4]
    flag(f"  Table 4 row {r}", not bad, "11 cells" + (f", off: {bad[:2]}" if bad else ""))

# -- structural: exact, in every narrative -----------------------------------
_mir = max(float((pts.xs(s, level=0)["1.0"] + pts.xs(s, level=0)["0.0"]).abs().max())
           for s in pts.index.get_level_values(0).unique())
flag("phi=1 mirrors phi=0 in every narrative", _mir < 1e-12, f"max|sum| = {_mir:.1e}")
inv = S("out_phi_invariance", (0,))
chk("  rate invariance", float(inv.rate_IND_bp.max() - inv.rate_IND_bp.min()), 0.0, 0.0)
chk("  FX invariance", float(inv.fwd5_IND_pct.max() - inv.fwd5_IND_pct.min()), 0.0, 0.0)
chk("  invariance rate level matches Table 5", round(float(inv.rate_IND_bp.iloc[0]), 1), -72.7, 0.05)
chk("  invariance FX level matches Table 7", round(float(inv.fwd5_IND_pct.iloc[0]), 2), -1.35)

# -- scenario-scaled: only the level -----------------------------------------
_nz0 = pts.xs(NZ, level=0)["0.0"].abs().sum()
_cp0 = pts.xs(CP, level=0)["0.0"].abs().sum()
chk("  phi=0 charge, NZ vs CP", round(float(_nz0 / _cp0)), 37, 0.5)
chk("  IND phi=0, Net Zero component", round(float(pts.loc[(NZ, "IND"), "0.0"]), 2), -20.90)
chk("  IND phi=0, consensus", round(float(pt.loc[0.0, "IND"]), 2), -1.03)

# -- in between: the crossing ------------------------------------------------
cx = S("out_phi_crossings", (0,))
zs = cx[HEAD].sort_values()
chk("  consensus crossing min", round(float(zs.iloc[0]), 3), 0.570)
chk("  consensus crossing max", round(float(zs.iloc[-1]), 3), 0.854)
chk("  GBR crossing", round(float(cx.loc["GBR", HEAD]), 3), 0.715)
chk("  IND crossing", round(float(cx.loc["IND", HEAD]), 3), 0.607)
flag("min crossing is AFR", zs.index[0] == "AFR")
flag("max crossing is CHE", zs.index[-1] == "CHE")
_scen_cols = [c for c in cx.columns if c != HEAD]
_band = cx[_scen_cols].to_numpy(float)
chk("  band low, all regions x narratives", round(float(np.nanmin(_band)), 3), 0.568)
chk("  band high, all regions x narratives", round(float(np.nanmax(_band)), 3), 0.917)
flag("every crossing above one half, every narrative", float(np.nanmin(_band)) > 0.5)
_rng = cx[_scen_cols].max(axis=1) - cx[_scen_cols].min(axis=1)
chk("  crossing spread, median", round(float(_rng.median()), 3), 0.024)
chk("  crossing spread, max", round(float(_rng.max()), 3), 0.139)
flag("widest crossing spread is GBR", _rng.idxmax() == "GBR")

mid = float(pt.loc[0.5, "IND"])
chk("  IND transition swing low", round((float(pt.loc[0.0, "IND"]) - mid) / abs(mid) * 100), -378, 3)
chk("  IND transition swing high", round((float(pt.loc[1.0, "IND"]) - mid) / abs(mid) * 100), 578, 3)
pc = S("out_phi_credit", (0,))
cmid = float(pc.loc[0.5, "IND"])
chk("  IND credit swing low", round((float(pc.loc[0.0, "IND"]) - cmid) / abs(cmid) * 100), 464, 3)
chk("  IND credit swing high", round((float(pc.loc[1.0, "IND"]) - cmid) / abs(cmid) * 100), -664, 3)

print("4. rates")
rt = M("rate")
for r, y25, y30, y40, y45 in [("IND", -47.5, -54.2, -72.7, -81.2), ("MEA", -42.9, -49.0, -65.7, -73.3),
                              ("CHN", -39.3, -44.6, -60.1, -67.0), ("TUR", -38.1, -43.5, -58.3, -65.1),
                              ("RUS", -29.6, -33.8, -45.3, -50.5), ("EU27", -28.7, -32.6, -44.0, -49.1),
                              ("USA", -26.7, -30.4, -40.9, -45.6), ("CHE", -25.3, -28.7, -38.7, -43.2),
                              ("GBR", -23.4, -26.5, -35.7, -39.9)]:
    for y, v in zip(("2025", "2030", "2040", "2045"), (y25, y30, y40, y45)):
        chk(f"  rate {r} {y}", round(float(rt.loc[r, y]), 1), v, 0.05)
allr = S("out_ext_rate_shift")
flag("no positive rate anywhere", int((allr[["2025", "2030", "2035", "2040", "2045"]] > 0).sum().sum()) == 0)
pi, gy = M("inflation")["2040"], M("gdp_physical")["2040"] * 100
chk("  max inflation term (bp)", round(float((0.5 * pi).loc[CCY].max()), 2), 0.07, 5e-3)
flag("inflation term exactly zero for the unpriced four",
     all(abs(float((0.5 * pi)[r])) < 1e-12 for r in ("IND", "TUR", "RUS", "MEA")))
flag("Taylor decomposition reconciles",
     float((0.5 * pi + 0.5 * gy - rt["2040"]).abs().max()) < 1e-6)
_dmg = (0.5 * gy).loc[CCY].abs()
flag("damage contributions span 35-73 bp",
     35 <= float(_dmg.min()) and float(_dmg.max()) <= 73,
     f"{float(_dmg.min()):.0f}..{float(_dmg.max()):.0f} bp")
rm = [float(M("rate", p)["2040"].loc[CCY].mean()) for p in P]
chk("  rate mean prior range", round(min(rm) / max(rm), 2), 1.04, 5e-3)

print("4.1 term structure")
ts = M("rate_term_structure", idx=1)["2040"].unstack()
for r, row in [("IND", [-72.7, -72.0, -71.3, -65.9, -60.0, -50.1]),
               ("MEA", [-65.7, -65.0, -64.4, -59.5, -54.1, -45.2]),
               ("CHN", [-60.1, -59.5, -58.9, -54.4, -49.5, -41.4]),
               ("TUR", [-58.3, -57.8, -57.2, -52.9, -48.1, -40.2]),
               ("RUS", [-45.3, -44.8, -44.4, -41.0, -37.3, -31.2]),
               ("EU27", [-43.9, -43.5, -43.1, -39.8, -36.2, -30.3]),
               ("USA", [-40.9, -40.5, -40.1, -37.0, -33.7, -28.1]),
               ("CHE", [-38.7, -38.3, -37.9, -35.1, -31.9, -26.6]),
               ("GBR", [-35.7, -35.4, -35.0, -32.4, -29.5, -24.6])]:
    for t_, v in zip(["1D", "6M", "1Y", "5Y", "10Y", "20Y"], row):
        chk(f"  {r} {t_}", round(float(ts.loc[r, t_]), 1), v, 0.05)
ratio = (ts["20Y"] / ts["1D"]).round(4)
flag("20Y/1D identical for every region", ratio.nunique() == 1)
chk("  ratio", round(float(ratio.iloc[0]), 4), 0.6884, 5e-5)
an = (hw_B(20.0) / 20.0) / (hw_B(1 / 365) * 365)
chk("  ratio is analytic", round(float(an), 4), 0.6884, 5e-5)
chk("  B(20)/20 alone", round(float(hw_B(20.0) / 20.0), 4), 0.6883, 5e-5)
# fig10 lost its ambition panel, so the prior-insensitivity it used to show has
# to be carried by this number instead
_amb = M("rate_term_structure", "ambition", idx=1)["2040"].unstack()
_gap = max(abs(float(_amb.loc[r, t] - ts.loc[r, t]))
           for r in CCY for t in ["1D", "6M", "1Y", "5Y", "10Y", "20Y"])
chk("  max |ambition - consensus| over the table", round(_gap, 2), 2.75, 5e-3)

print("5. FX")
fw = M("fx_forward")
fw.loc["MEA"] = fw.loc["USA"]
for r, y25, y30, y40, y45 in [("IND", -0.85, -1.01, -1.35, -1.51), ("CHN", -0.48, -0.55, -0.74, -0.82),
                              ("TUR", -0.42, -0.52, -0.69, -0.78), ("USA", 0.09, 0.08, 0.10, 0.11),
                              ("MEA", 0.09, 0.08, 0.10, 0.11), ("CHE", 0.16, 0.17, 0.22, 0.25),
                              ("GBR", 0.24, 0.26, 0.35, 0.39)]:
    for y, v in zip(("2025", "2030", "2040", "2045"), (y25, y30, y40, y45)):
        chk(f"  fwd {r} {y}", round(float(fw.loc[r, y]), 2), v)
flag("MEA inherits USD exactly under every prior",
     all(float(M("fx_forward", p).loc["USA", "2040"]) == float(M("fx_forward", p).loc["USA", "2040"])
         for p in P))
for r, lo, hi in [("IND", -2.31, -1.35), ("CHN", -1.03, -0.74), ("TUR", -1.67, -0.69),
                  ("USA", -0.75, 0.10), ("CHE", -0.12, 0.22), ("GBR", -0.15, 0.35)]:
    v = [float(M("fx_forward", p).loc[r, "2040"]) for p in P]
    chk(f"  range lo {r}", round(min(v), 2), lo)
    chk(f"  range hi {r}", round(max(v), 2), hi)
flag("INR, CNY, TRY negative under every prior",
     all(float(M("fx_forward", p).loc[r, "2040"]) < 0 for p in P for r in ("IND", "CHN", "TUR")))
flag("USD, CHF, GBP flip between ambition and consensus",
     all(np.sign(M("fx_forward", "ambition").loc[r, "2040"])
         != np.sign(M("fx_forward", "consensus").loc[r, "2040"])
         for r in ("USA", "CHE", "GBR")))
sp = M("fx_spot")
sp.loc["MEA"] = sp.loc["USA"]
for r, v in [("IND", -0.043), ("TUR", -0.043), ("USA", -0.037), ("GBR", -0.021),
             ("CHE", -0.015), ("CHN", -0.007)]:
    chk(f"  spot {r}", round(float(sp.loc[r, "2040"]), 3), v, 5e-4)
flag("every spot negative under every prior",
     all(float(M("fx_spot", p).loc[r, "2040"]) < 0 for p in P for r in FX))
sc_ = cm.carbon_scope.astype(float)
flag("EU27 has the highest scope", all(sc_[r] < sc_["EU27"] for r in FX))
chk("  next scope", round(max(sc_[r] for r in FX), 3), 0.467)
chk("  corr(spot, scope) Net Zero 2045",
    round(float(np.corrcoef(S("out_ext_fx_spot").xs(NZ, level=0).loc[FX, "2045"],
                            [sc_[r] for r in FX])[0, 1]), 4), 0.9999, 5e-4)
flag("IND and TUR identical on spot",
     round(float(sp.loc["IND", "2040"]), 6) == round(float(sp.loc["TUR", "2040"]), 6))
def legs(p):
    """How far apart the two FX legs are, on the same definition fig12 uses."""
    return float(M("fx_forward", p)["2040"].abs().max()
                 / M("fx_spot", p)["2040"].abs().max())


chk("  legs apart, consensus", round(legs(HEAD), 1), 31.7, 0.05)
sv = [float(M("fx_spot", p).loc["IND", "2040"]) for p in P]
fv = [float(M("fx_forward", p).loc["IND", "2040"]) for p in P]
chk("  spot prior range", round(min(sv) / max(sv), 1), 22.7, 0.05)
chk("  fwd prior range", round(min(fv) / max(fv), 1), 1.7, 0.05)
chk("  legs apart, ambition", round(legs("ambition"), 1), 2.4, 0.05)
flag("consensus separates the legs an order of magnitude more than ambition",
     legs(HEAD) / legs("ambition") > 10, f"{legs(HEAD)/legs('ambition'):.0f}x")

print("5.3 the peg")
chk("  MEA own rate", round(float(rt.loc["MEA", "2040"]), 1), -65.7, 0.05)
chk("  USD rate", round(float(rt.loc["USA", "2040"]), 1), -40.9, 0.05)
flag("MEA is second-deepest cut among currency regions",
     list(rt.loc[CCY, "2040"].sort_values().index).index("MEA") == 1)
for p, v in zip(P, (-24.6, -24.8, -24.4, -24.8)):
    g = float(M("rate", p).loc["MEA", "2040"] - M("rate", p).loc["USA", "2040"])
    chk(f"  peg gap {p[:9]}", round(g, 1), v, 0.05)

print("6. credit")
# the section opener describes the blend, so gate the numbers it quotes
from bkmn import credit as _cr                            # noqa: E402
from bkmn.paper_tables import CDS_SECTORS, CDS_WEIGHTS    # noqa: E402
_idx = [c for c in CDS_SECTORS if c != "FTSE"]
chk("  indices excluding FTSE", len(_idx), 12, 0)
_hc = list(CDS_SECTORS).index("Health Care")
chk("  Health Care weight on SIC C", round(float(CDS_WEIGHTS["C"][_hc]), 3), 0.553, 5e-4)
chk("  Health Care weight on SIC Q", round(float(CDS_WEIGHTS["Q"][_hc]), 3), 0.447, 5e-4)
_sic = np.array([_cr.ICIO_TO_SIC[i] for i in m.industry_of])
_k = m.region_of == "IND"
chk("  India output ratio C:Q",
    round(float(m.x[_k & (_sic == "C")].sum() / m.x[_k & (_sic == "Q")].sum())), 32, 0.5)
flag("exactly two indices carry a positive slope",
     [c for c in _idx if CDS_BETA[c] > 0] == ["Financials", "UK Real Estate"])
for r, y25, y30, y40, y45, u in [("CHN", 0.89, 1.38, 1.93, 2.15, 4.37), ("IND", 0.73, 1.24, 1.78, 1.98, 5.90),
                                 ("TUR", 0.74, 1.21, 1.67, 1.87, 4.20), ("RUS", 0.55, 0.89, 1.33, 1.51, 3.59),
                                 ("EU27", 0.58, 0.77, 1.04, 1.15, 2.04), ("MEA", 0.32, 0.64, 0.90, 1.00, 2.06),
                                 ("GBR", 0.49, 0.62, 0.84, 0.93, 1.46), ("CHE", 0.48, 0.58, 0.78, 0.87, 1.05),
                                 ("USA", 0.27, 0.36, 0.49, 0.54, 1.16)]:
    for y, v in zip(("2025", "2030", "2040", "2045"), (y25, y30, y40, y45)):
        cc = M("credit", HEAD, 1)[y].unstack().drop(columns=["FTSE"]).loc[CCY]
        chk(f"  credit {r} {y}", round(float(cc.median(axis=1)[r]), 2), v)
    chk(f"  credit {r} uniform", round(float(credit("uniform", CCY).median(axis=1)[r]), 2), u)
cvals = [float(credit(p, CCY).median(axis=1)["IND"]) for p in P]
chk("  credit prior range", round(max(cvals) / min(cvals), 1), 4.1, 0.05)
flag("China leads on consensus, India on uniform",
     credit(HEAD, CCY).median(axis=1).idxmax() == "CHN"
     and credit("uniform", CCY).median(axis=1).idxmax() == "IND")
cc = credit(HEAD, CCY)
med = cc.median()
for s, v, b in [("Health Care", 3.87, -3.417), ("Utilities", 2.97, -1.510),
                ("Basic Materials", 2.52, -1.971), ("Consumer Goods", 2.34, -2.328),
                ("Industrials", 1.83, -1.751), ("Oil & Gas", 1.70, -1.325),
                ("Consumer Services", 0.48, -0.590), ("Government", 0.47, -3.112),
                ("Telecommunications", 0.20, -0.713), ("Technology", 0.11, -0.382),
                ("Financials", -0.38, 2.078), ("UK Real Estate", -0.82, 7.206)]:
    chk(f"  sector {s[:18]}", round(float(med[s]), 2), v)
    chk(f"  beta {s[:18]}", round(float(CDS_BETA[s]), 3), b, 5e-4)
st = cc.stack().rename("v").reset_index()
st.columns = ["region", "index", "v"]
chk("  sector variance %", round(st.groupby("index").v.mean().var() / st.v.var() * 100), 72, 1)
chk("  region variance %", round(st.groupby("region").v.mean().var() / st.v.var() * 100), 14, 1)
flag("sector explains ~5x the region",
     4.5 < (st.groupby("index").v.mean().var() / st.groupby("region").v.mean().var()) < 5.5,
     f"{st.groupby('index').v.mean().var()/st.groupby('region').v.mean().var():.1f}x")
chk("  corr(beta, median)",
    round(float(np.corrcoef([CDS_BETA[c_] for c_ in med.index], med.values)[0, 1]), 2), -0.70)
flag("beta fixes the sign for every index",
     all((CDS_BETA[c_] < 0) == (med[c_] > 0) for c_ in cc.columns))
flag("largest cell is Indian health care", cc.stack().idxmax() == ("IND", "Health Care"))
chk("  largest cell", round(float(cc.stack().max()), 1), 11.0, 0.05)

print("6.1 equity and op-risk")
eq, op = M("equity")["2040"], M("oprisk_conduct")["2040"]
b = pd.Series(equity.betas())
u0 = oprisk.base_unemployment() * 100
for r, e_, be, o, uu in [("MEA", -2.86, 2.00, 4.31, 5.97), ("TUR", -2.59, 1.89, 2.18, 10.46),
                         ("IND", -2.31, 1.38, 5.91, 4.82), ("RUS", -2.15, 2.00, 4.59, 3.87),
                         ("CHE", -1.59, 2.00, 7.37, 4.12), ("USA", -1.34, 1.59, 8.77, 3.65),
                         ("EU27", -0.74, 0.80, 5.60, 6.16), ("GBR", -0.41, 0.55, 4.51, 3.77),
                         ("CHN", -0.38, 0.26, 4.73, 4.98)]:
    chk(f"  equity {r}", round(float(eq[r]), 2), e_)
    chk(f"  beta {r}", round(float(b[r]), 2), be)
    chk(f"  conduct {r}", round(float(op[r]), 2), o)
    chk(f"  U0 {r}", round(float(u0[r]), 2), uu)
flag("TUR 2nd worst on equity, last on op-risk",
     list(eq.loc[CCY].sort_values().index).index("TUR") == 1
     and list(op.loc[CCY].sort_values(ascending=False).index).index("TUR") == 8)
flag("USA leads op-risk", op.loc[CCY].idxmax() == "USA")
flag("CHN first on credit, last on equity",
     credit(HEAD, CCY).median(axis=1).idxmax() == "CHN" and eq.loc[CCY].idxmax() == "CHN")
flag("CHN has the lowest beta", b.loc[CCY].idxmin() == "CHN")
cal = equity.calibrate()
proxy = [r for r in CCY if r not in cal or cal[r][2] == "proxy"]
flag("three of nine carry the proxy beta", sorted(proxy) == ["CHE", "MEA", "RUS"], str(proxy))
chk("  proxy over all 13", len([r for r in m.regions_order
                                if r not in cal or cal[r][2] == "proxy"]), 7, 0)
ov = [float(M("oprisk_conduct", p).loc["TUR", "2040"]) for p in P]
chk("  oprisk prior range", round(max(ov) / min(ov), 2), 1.03, 5e-3)
ev = [float(M("equity", p)["2040"].loc[CCY].mean()) for p in P]
chk("  equity prior range", round(min(ev) / max(ev), 1), 1.7, 0.05)
gv = [float(M("gdp_total", p)["2040"].mean()) for p in P]
chk("  total GDP prior range", round(min(gv) / max(gv), 1), 1.8, 0.05)

print("7.2 scenario components")
for s, a, bb, c, d in [(NZ, -2.20, -1.01, 3.30, 3.78), ("Low demand", -1.19, -1.02, 2.43, 2.44),
                       ("Delayed transition", -0.88, -1.09, 2.12, 2.01), (B2, -0.68, -1.05, 2.07, 1.78),
                       (NDC, -0.58, -1.07, 2.02, 1.70), ("Fragmented World", -0.27, -1.09, 1.91, 1.12),
                       (CP, -0.06, -1.07, 1.88, 0.82)]:
    chk(f"  {s[:14]} trans", round(float(S("out_ext_gdp_transition").xs(s, level=0)["2040"].mean()), 2), a)
    chk(f"  {s[:14]} phys", round(float(S("out_ext_gdp_physical").xs(s, level=0)["2040"].mean()), 2), bb)
    f_ = S("out_ext_fx_forward_5y").xs(s, level=0).loc[FX, "2045"]
    chk(f"  {s[:14]} fx range", round(float(f_.max() - f_.min()), 2), c)
    cs = S("out_ext_credit_spread", (0, 1, 2)).xs(s, level=0)["2040"].unstack().drop(columns=["FTSE"]).loc[CCY]
    chk(f"  {s[:14]} credit", round(float(cs.stack().median()), 2), d)
tms = [float(S("out_ext_gdp_transition").xs(s, level=0)["2040"].mean())
       for s in S("out_ext_gdp_transition").index.get_level_values(0).unique()]
chk("  scenario transition factor", round(min(tms) / max(tms)), 37, 1)

print("7.3 the tail")
q = M("fx_forward_q95")
q.loc["MEA"] = q.loc["USA"]
for r, cen_, hi_ in [("IND", -1.35, -1.75), ("CHN", -0.74, -0.98), ("TUR", -0.69, -0.96),
                     ("USA", 0.10, 0.03), ("MEA", 0.10, 0.03), ("CHE", 0.22, 0.23), ("GBR", 0.35, 0.37)]:
    chk(f"  central {r}", round(float(fw.loc[r, "2040"]), 2), cen_)
    chk(f"  stressed {r}", round(float(q.loc[r, "2040"]), 2), hi_)
cen_r = float(M("fx_forward")["2040"].max() - M("fx_forward")["2040"].min())
hi_r = float(M("fx_forward_q95")["2040"].max() - M("fx_forward_q95")["2040"].min())
chk("  central range", round(cen_r, 2), 1.70)
chk("  stressed range", round(hi_r, 2), 2.12)
amb_c = float(M("fx_forward", "ambition")["2040"].max() - M("fx_forward", "ambition")["2040"].min())
amb_h = float(M("fx_forward_q95", "ambition")["2040"].max() - M("fx_forward_q95", "ambition")["2040"].min())
flag("ambition stress is ~3x the consensus stress",
     2.5 < (amb_h - amb_c) / (hi_r - cen_r) < 3.5,
     f"{(amb_h-amb_c)/(hi_r-cen_r):.1f}x")

print("8. orderings, consensus prior")
cu = credit(HEAD, CCY).median(axis=1)
flag("FX order", list(M("fx_forward")["2040"].loc[FX].sort_values().index)
     == ["IND", "CHN", "TUR", "USA", "CHE", "GBR"],
     str(list(M("fx_forward")["2040"].loc[FX].sort_values().index)))
flag("rate top5", list(rt.loc[CCY, "2040"].sort_values().index[:5])
     == ["IND", "MEA", "CHN", "TUR", "RUS"])
flag("credit top5", list(cu.sort_values(ascending=False).index[:5])
     == ["CHN", "IND", "TUR", "RUS", "EU27"])
flag("equity top5", list(eq.loc[CCY].sort_values().index[:5])
     == ["MEA", "TUR", "IND", "RUS", "CHE"])
flag("USA last on credit", cu.idxmin() == "USA")
flag("USA 4th on FX", list(M("fx_forward")["2040"].loc[FX].sort_values().index).index("USA") == 3)
flag("IND in the first three of every channel",
     all(list(x).index("IND") < 3 for x in
         (M("fx_forward")["2040"].loc[FX].sort_values().index,
          rt.loc[CCY, "2040"].sort_values().index,
          cu.sort_values(ascending=False).index,
          eq.loc[CCY].sort_values().index)))
flag("MEA has no FX row of its own", "MEA" not in FX)

print("10. FIGURES.md captions")
for f_ in ("fig2_fx_forward_ranking", "fig3_mixture_expected_fx", "fig4_fx_at_risk_band",
           "fig6_equity_oprisk", "fig10_rate_term_structure", "fig12_two_fx_channels",
           "fig13_credit_spreads", "fig15_prior_sensitivity", "fig16_peg"):
    flag(f"  {f_} exists", os.path.exists(os.path.join(ROOT, "figures", f_ + ".png")))
for r, v in [("Health Care", 3.87), ("Utilities", 2.97), ("Basic Materials", 2.52)]:
    chk(f"  fig13 median {r[:14]}", round(float(med[r]), 2), v)
# fig12's caption quotes 2045 values, not 2040 like the rest of the chapter
_sp45, _fw45 = M("fx_spot")["2045"], M("fx_forward")["2045"]
chk("  fig12 legs apart at 2045",
    round(float(_fw45.abs().max() / _sp45.abs().max()), 1), 30.4, 0.05)
chk("  fig12 corr at 2045", round(float(np.corrcoef(_sp45, _fw45)[0, 1]), 2), 0.37)
chk("  fig12 sign disagreements",
    int((np.sign(_sp45) != np.sign(_fw45)).sum()), 3, 0)
_pi45 = M("inflation")["2045"].loc[CCY]
_gy45 = M("gdp_physical")["2045"].loc[CCY] * 100
chk("  fig12 inflation share of the rate move",
    round(float((0.5 * _pi45.abs() / (0.5 * _pi45.abs() + 0.5 * _gy45.abs()) * 100).median()), 2),
    0.02, 5e-3)

print("11. CHAPTER_DISCUSSION.md")
# the discussion chapter re-states results from elsewhere; gate only the claims
# it makes in its own words, plus the constants it prints
from bkmn import macro as _mac                             # noqa: E402
from bkmn import physical as _phy                          # noqa: E402
from bkmn.rates import A_MEANREV                           # noqa: E402
from bkmn.run_fx import PHI, TAYLOR_OUTPUT_GAP             # noqa: E402
chk("  Moessner coefficient", _mac.INFL_PER_USD, 8e-5, 1e-9)
chk("  Hull-White mean reversion", A_MEANREV, 0.04, 1e-12)
chk("  reporting pass-through", PHI, 0.5, 1e-12)
chk("  damage coefficient", round(float(_phy.omega(1.0)), 5), 0.00346, 5e-6)
chk("  ... is 1.6768e-2 / 2.2^2", round(float(_phy.omega(1.0)), 8),
    round(1.6768e-2 / 2.2 ** 2, 8), 1e-9)
chk("  Omega at 2.2 C is the DICE loss (%)", round(float(_phy.omega(2.2)) * 100, 4), 1.6768, 5e-5)
flag("Taylor output gap is the physical shock", TAYLOR_OUTPUT_GAP == "physical")
_phn = [float(S("out_ext_gdp_physical").xs(s, level=0)["2040"].mean())
        for s in S("out_ext_gdp_physical").index.get_level_values(0).unique()]
chk("  physical mean varies across narratives (%)",
    round((max(_phn, key=abs) / min(_phn, key=abs) - 1) * 100), 8, 0.5)
flag("six floating currencies plus one peg",
     len(FX) == 6 and cm.loc["MEA", "currency"] == "USD-peg")
chk("  peg wedge, consensus (bp)",
    round(float(rt.loc["MEA", "2040"] - rt.loc["USA", "2040"])), -25, 0.5)

print()
bad = sum(1 for v in ok if not v)
print(f"{'ALL ' + str(len(ok)) + ' CHECKS PASSED' if not bad else str(bad) + ' FAILED of ' + str(len(ok))}")
sys.exit(0 if not bad else 1)
