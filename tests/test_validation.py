"""
Structural validation gates.  Run: py -3 tests/test_validation.py

These do not check that the model reproduces a number.  They check that it has
the STRUCTURE it claims: that regions are coupled only through trade, that the
multi-regional generalisation reduces to the single-region case, and that no
asymmetry appears in the output that was not put into the input.

Every check runs the production code path -- `transition`, `macro`, `fx` -- on an
economy whose right answer is known by symmetry, so a pass is evidence about the
shipped code and not about a reimplementation of it.

Groups:
  A  isolation      a region with no trade links is causally disconnected
  B  symmetry       identical regions must give identical results, FX exactly 0
  C  one shock      breaking symmetry in one place must show up in exactly that
                    place, with the right sign and the right ordering
  D  reduction      autarky decomposes into R independent single-region models
  E  real data      the same properties on the shipped 13-region calibration
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from bkmn import fx, macro, synthetic, transition   # noqa: E402
from bkmn.regions import load                       # noqa: E402

PHI = 0.5
XCE = 100.0
n_pass = 0


def check(name, cond, detail=""):
    global n_pass
    assert cond, f"FAIL: {name}  {detail}"
    n_pass += 1
    print(f"  PASS  {name}  {detail}")


def shock(m, xce_by_region, phi=PHI):
    return transition.region_gdp_shock(m, transition.gva_operator(m, phi),
                                       xce_by_region)


# ===========================================================================
print("A. isolation -- a region with no trade links is causally disconnected")
# ===========================================================================
m = synthetic.symmetric(n_regions=4, n_sectors=3)
iso = synthetic.isolate(m, "R0")
regs = m.regions_order

# A1: shocking the isolated region must not move anyone else
s = shock(iso, {r: (XCE if r == "R0" else 0.0) for r in regs})
leak = max(abs(s[r]) for r in regs if r != "R0")
check("A1 shock to isolated region does not leak out",
      leak < 1e-15, f"max |other| = {leak:.1e}")
check("A1b ... and does move the isolated region itself",
      s["R0"] < -1e-6, f"R0 = {s['R0']*100:.4f} %")

# A2: shocking everyone else must not move the isolated region
s = shock(iso, {r: (0.0 if r == "R0" else XCE) for r in regs})
check("A2 shock to the rest does not leak in",
      abs(s["R0"]) < 1e-15, f"|R0| = {abs(s['R0']):.1e}")
check("A2b ... and does move the rest",
      all(s[r] < -1e-6 for r in regs if r != "R0"))

# A3: the isolated region inside the MR model == a standalone single-region model
one = synthetic.single_region(iso, "R0")
s_mr = shock(iso, {r: (XCE if r == "R0" else 0.0) for r in regs})["R0"]
s_sr = shock(one, {"R0": XCE})["R0"]
check("A3 isolated region == standalone single-region model",
      abs(s_mr - s_sr) < 1e-14, f"|Δ| = {abs(s_mr - s_sr):.1e}")

# A4: connected regions DO leak -- the test above must be able to fail
s = shock(m, {r: (XCE if r == "R0" else 0.0) for r in regs})
spill = max(abs(s[r]) for r in regs if r != "R0")
check("A4 control: connected regions do transmit",
      spill > 1e-6, f"max |other| = {spill*100:.4f} % (isolation test has teeth)")

# ===========================================================================
print("\nB. symmetry -- identical regions, identical answers, zero FX")
# ===========================================================================
m = synthetic.symmetric(n_regions=5, n_sectors=4)
s = shock(m, {r: XCE for r in m.regions_order})
spread = max(s.values()) - min(s.values())
check("B1 identical regions give identical GVA shocks",
      spread < 1e-15, f"spread = {spread:.1e}")
check("B1b ... and the shock is negative", all(v < 0 for v in s.values()),
      f"each = {list(s.values())[0]*100:.4f} %")

# B2: inflation identical -> cumulative identical -> spot FX exactly zero
scope = dict(zip(m.carbon_map.region, m.carbon_map.carbon_scope))
cum = {r: macro.INFL_PER_USD * scope[r] * XCE for r in m.regions_order}
spot = {r: fx.spot_ppp(cum[r], cum["R0"]) for r in m.regions_order}
check("B2 spot FX is exactly zero between identical regions",
      max(abs(v) for v in spot.values()) == 0.0,
      f"max |spot| = {max(abs(v) for v in spot.values()):.1e}")

# B3: identical output gaps -> identical policy rates -> zero forward points.
#
# Note the asymmetry with B2, which is exact.  Spot FX is a difference of
# quantities built by multiplying identical inputs, so the floats are bit-wise
# identical and the difference is exactly 0.  Forward points descend from the
# GVA shock, which passes through a matrix inversion: identical rows are solved
# independently and agree only to machine precision.  So the right claim here is
# "zero to rounding", and the tolerance says so rather than pretending to more.
dr = {r: macro.taylor_rate_shift(0.0, s[r]) for r in m.regions_order}
pts = {r: fx.forward_points(dr[r], dr["R0"], 5) for r in m.regions_order}
worst = max(abs(v) for v in pts.values())
rel = worst / abs(list(dr.values())[0])
check("B3 forward points vanish between identical regions (to rounding)",
      rel < 1e-14, f"max |pts| = {worst:.1e}, relative to Δr = {rel:.1e}")

# B4: symmetry must not be an artefact of the shock being uniform
check("B4 control: the operator is not degenerate",
      abs(list(s.values())[0]) > 1e-6, "a uniform shock does move GVA")

# ===========================================================================
print("\nC. one broken symmetry -- effects appear where they were put")
# ===========================================================================
m = synthetic.symmetric(n_regions=5, n_sectors=4)
regs = m.regions_order
s = shock(m, {r: (XCE if r == "R2" else 0.0) for r in regs})

check("C1 the shocked region is worst hit",
      s["R2"] == min(s.values()), f"R2 = {s['R2']*100:.4f} %")
others = [s[r] for r in regs if r != "R2"]
check("C2 all unshocked regions are affected identically",
      max(others) - min(others) < 1e-15, f"spread = {max(others)-min(others):.1e}")
check("C3 spillover is negative but smaller than the direct hit",
      others[0] < 0 and abs(others[0]) < abs(s["R2"]),
      f"spill {others[0]*100:.4f} % vs direct {s['R2']*100:.4f} %")

# C4: FX -- the shocked region's currency must move against every other, and
# all the others must be identical to each other
dr = {r: macro.taylor_rate_shift(0.0, s[r]) for r in regs}
pts = {r: fx.forward_points(dr[r], dr["R0"], 5) for r in regs}
oth = [pts[r] for r in regs if r not in ("R2", "R0")]
worst = max(abs(v) for v in oth)
check("C4 unshocked currencies do not move against each other",
      worst / abs(pts["R2"]) < 1e-14,
      f"max = {worst:.1e}, {worst/abs(pts['R2']):.1e} of the shocked pair")
# The shocked region takes the deeper rate cut, so under CIP its currency trades
# at a forward PREMIUM: with S in units of r per base, pts < 0 means r
# appreciates forward.  This is the counter-intuitive sign the FX report
# documents -- the harder-hit economy strengthens on the forward leg -- and it is
# asserted here as a mechanism, not an intuition:  sign(pts) == sign(Δr_r − Δr_base).
check("C5 the shocked currency moves, with the sign CIP requires",
      pts["R2"] < 0 and np.sign(pts["R2"]) == np.sign(dr["R2"] - dr["R0"]),
      f"Δr gap {(dr['R2']-dr['R0'])*1e4:+.2f} bp -> pts {pts['R2']*1e4:+.2f} bp "
      f"(forward premium)")
check("C5b ... and the magnitude is B(5)·Δr gap exactly",
      abs(pts["R2"] - float(__import__("bkmn.rates", fromlist=["hw_B"]).hw_B(5))
          * (dr["R2"] - dr["R0"])) < 1e-18)

# C6: intensity asymmetry -- one dirty region, uniform price
ci = {r: (400.0 if r == "R3" else 200.0) for r in regs}
md = synthetic.symmetric(n_regions=5, n_sectors=4, intensity=ci)
sd = shock(md, {r: XCE for r in regs})
check("C6 the carbon-intensive region is worst hit",
      sd["R3"] == min(sd.values()), f"R3 = {sd['R3']*100:.4f} %")
rest = [sd[r] for r in regs if r != "R3"]
check("C7 the rest remain identical to each other",
      max(rest) - min(rest) < 1e-15, f"spread = {max(rest)-min(rest):.1e}")

# C8: linearity -- doubling the price doubles every shock
s1 = shock(m, {r: XCE for r in regs})
s2 = shock(m, {r: 2 * XCE for r in regs})
err = max(abs(2 * s1[r] - s2[r]) for r in regs)
check("C8 the charge channel is exactly linear in the carbon price",
      err < 1e-15, f"max |2·s(p) − s(2p)| = {err:.1e}")

# C9: superposition -- shocking two regions equals the sum of shocking each
sa = shock(m, {r: (XCE if r == "R1" else 0.0) for r in regs})
sb = shock(m, {r: (XCE if r == "R4" else 0.0) for r in regs})
sab = shock(m, {r: (XCE if r in ("R1", "R4") else 0.0) for r in regs})
err = max(abs(sa[r] + sb[r] - sab[r]) for r in regs)
check("C9 shocks superpose exactly (contributions decompose)",
      err < 1e-15, f"max |a+b−ab| = {err:.1e}")

# ===========================================================================
print("\nD. reduction -- autarky decomposes into independent economies")
# ===========================================================================
m = synthetic.symmetric(n_regions=4, n_sectors=3)
au = synthetic.autarky(m)
s_all = shock(au, {r: XCE for r in m.regions_order})
worst = 0.0
for r in m.regions_order:
    s_one = shock(au, {q: (XCE if q == r else 0.0) for q in m.regions_order})
    worst = max(worst, max(abs(s_one[q]) for q in m.regions_order if q != r))
    worst = max(worst, abs(s_one[r] - s_all[r]))
check("D1 under autarky each region depends only on its own price",
      worst < 1e-15, f"max deviation = {worst:.1e}")

for r in m.regions_order:
    one = synthetic.single_region(au, r)
    a = shock(au, {q: XCE for q in m.regions_order})[r]
    b = shock(one, {r: XCE})[r]
    check(f"D2 {r} autarky == standalone single-region",
          abs(a - b) < 1e-14, f"|Δ| = {abs(a - b):.1e}")

# ===========================================================================
print("\nE. the same properties on the shipped calibration")
# ===========================================================================
real = load()
R = real.regions_order
print(f"  (dataset: {len(R)} regions, {len(real.sectors)} sectors)")

# E1: superposition on real data -- the basis of contribution decomposition
sa = shock(real, {r: (XCE if r == "CHN" else 0.0) for r in R})
sb = shock(real, {r: (XCE if r == "USA" else 0.0) for r in R})
sab = shock(real, {r: (XCE if r in ("CHN", "USA") else 0.0) for r in R})
err = max(abs(sa[r] + sb[r] - sab[r]) for r in R)
check("E1 shocks superpose on the real calibration", err < 1e-15,
      f"max |a+b−ab| = {err:.1e}")

# E2: isolating a real region kills its spillovers exactly
iso = synthetic.isolate(real, "CHN")
s = shock(iso, {r: (XCE if r == "CHN" else 0.0) for r in R})
leak = max(abs(s[r]) for r in R if r != "CHN")
check("E2 isolating CHN removes every spillover", leak < 1e-15,
      f"max |other| = {leak:.1e}")

# E3: and the connected model does spill -- so E2 is informative
s = shock(real, {r: (XCE if r == "CHN" else 0.0) for r in R})
spill = {r: s[r] for r in R if r != "CHN"}
big = max(spill, key=lambda r: abs(spill[r]))
check("E3 control: China's carbon price does reach other regions",
      abs(spill[big]) > 1e-7,
      f"largest spillover {big} {spill[big]*100:.4f} % vs CHN {s['CHN']*100:.4f} %")

# E4: own-region effect must dominate its own spillover into anyone else
check("E4 the priced region is the worst hit", s["CHN"] == min(s.values()),
      f"CHN {s['CHN']*100:.4f} %")

# E5: a uniform world price must hit every region (no region is disconnected)
s = shock(real, {r: XCE for r in R})
check("E5 no region is inert under a world carbon price",
      all(v < -1e-9 for v in s.values()),
      f"least affected {max(s, key=lambda r: s[r])} {max(s.values())*100:.4f} %")

# E6: φ=0 endpoint identity, per region (the analytic anchor)
M0 = transition.gva_operator(real, 0.0)
s0 = transition.region_gdp_shock(real, M0, {r: XCE for r in R})
ct = real.ci * XCE * 1e-6
ref = {r: -(real.x * ct)[real.region_of == r].sum()
          / real.gva[real.region_of == r].sum() for r in R}
err = max(abs(s0[r] - ref[r]) for r in R)
check("E6 φ=0 reduces to −CT/GVA exactly", err < 1e-12, f"max |Δ| = {err:.1e}")

# ===========================================================================
print("\nF. sign and composition conventions")
# ===========================================================================
# Groups A-E are all symmetry or magnitude arguments, and symmetry is SIGN-BLIND:
# a global sign flip in the spot channel leaves every zero at zero and every
# magnitude unchanged.  Mutation testing confirmed it -- flipping the sign of
# `fx.spot_ppp` passed all 120 gates, as did composing the forward as
# spot MINUS points.  These gates close both holes by pinning the direction and
# the composition on cases where the right answer is unambiguous.

K = macro.INFL_PER_USD

# F1/F2: relative PPP direction.  A region pricing MORE carbon than the base
# imports more carbon inflation, so its price level rises faster and its currency
# must DEPRECIATE.  With S_r in units of r per base, that means spot > 0.
hi = fx.spot_ppp(K * 0.80 * XCE, K * 0.30 * XCE)      # r prices more than base
lo = fx.spot_ppp(K * 0.10 * XCE, K * 0.30 * XCE)      # r prices less than base
check("F1 higher carbon scope than base => currency depreciates (spot > 0)",
      hi > 0, f"scope 0.80 vs 0.30 -> spot {hi*100:+.4f} %")
check("F2 lower carbon scope than base => currency appreciates (spot < 0)",
      lo < 0, f"scope 0.10 vs 0.30 -> spot {lo*100:+.4f} %")
check("F3 spot is antisymmetric in the pair",
      abs(fx.spot_ppp(1e-3, 4e-3) + fx.spot_ppp(4e-3, 1e-3)) < 1e-18)

# F4-F6: the forward is spot PLUS points, not minus, and each leg is recoverable
c_r, c_b, d_r, d_b, tau = 2.0e-2, 0.5e-2, -40e-4, -10e-4, 5
tot = fx.forward_total(c_r, c_b, d_r, d_b, tau)
sp_ = fx.spot_ppp(c_r, c_b)
pt_ = fx.forward_points(d_r, d_b, tau)
check("F4 forward = spot + points exactly", abs(tot - (sp_ + pt_)) < 1e-18,
      f"{tot*100:+.4f} = {sp_*100:+.4f} {pt_*100:+.4f}")
check("F5 with no rate gap the forward collapses to spot",
      abs(fx.forward_total(c_r, c_b, d_r, d_r, tau) - sp_) < 1e-18)
check("F6 with no inflation gap the forward collapses to points",
      abs(fx.forward_total(c_r, c_r, d_r, d_b, tau) - pt_) < 1e-18)

# F7: the two legs genuinely disagree here, so F4 is not trivially satisfied
check("F7 control: the two legs have opposite signs in this case",
      sp_ > 0 > pt_, f"spot {sp_*100:+.3f} %, points {pt_*100:+.3f} %")

# F8: on the real calibration, EU27 holds the HIGHEST carbon-pricing scope, so
# relative PPP requires every other currency to appreciate against the euro.
# This is why no spot sign reversal appears in the results -- it is mechanical,
# not a coincidence, and it would break if a region ever out-priced the EU.
_cm = real.carbon_map.set_index("region")
_fx = [r for r in real.regions_order if _cm.loc[r, "fx_role"] == "analytical"]
_sc = _cm.carbon_scope.astype(float)
check("F8 EU27 has the highest carbon-pricing scope in the set",
      all(_sc[r] < _sc["EU27"] for r in _fx),
      f"EU27 {_sc['EU27']:.3f} vs max other {max(_sc[r] for r in _fx):.3f}")
_spot = pd.read_csv(f"{ROOT}/out_fx_spot_ppp.csv")
_nz = _spot[_spot.scenario.str.startswith("Net Zero")].set_index("region")
check("F8b ... so every analytical currency appreciates on spot",
      all(float(_nz.loc[r, "2040"]) < 0 for r in _fx),
      f"max {max(float(_nz.loc[r, '2040']) for r in _fx):+.4f} %")

print(f"\nALL {n_pass} VALIDATION GATES PASSED")
