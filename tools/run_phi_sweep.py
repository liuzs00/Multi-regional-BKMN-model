"""
Pass-through sensitivity: run the chain across phi and record what moves.

phi is the paper's cost pass-through parameter (Section 2.4): the share of the
carbon charge a sector passes downstream in its price rather than absorbing in
its own value added.  The paper sweeps it 0 to 1 as its principal sensitivity,
so the multi-regional results must be reported the same way.

The sweep is run for EVERY narrative and then mixture-weighted, like every other
channel in the chapter.  An earlier version ran Net Zero 2050 alone, on the
argument that a large carbon charge makes the sweep legible.  That is true of
the *levels* and false of everything else, and it left one table in the results
chapter quoting a single narrative while its neighbours quoted an expectation.
Separating the two is the point of this script:

  scenario-scaled  the level at any phi is proportional to the carbon price, so
                   it is ~37x larger under Net Zero than under Current Policies
  structural       the endpoint identity, the mirror symmetry about phi = 0.5,
                   and the invariance of rates and FX hold exactly in every
                   narrative
  in between       the zero crossing moves a little with the carbon-price
                   *pattern* across regions, since a scenario that prices the
                   OECD and not the rest changes which charges a sector imports

Outputs (at the reporting horizon):
  out_phi_transition.csv        transition GVA shock, region x phi, consensus
  out_phi_transition_scen.csv   the same, scenario x phi x region
  out_phi_transition_norm.csv   shock(phi) / |shock(0)|, the dimensionless shape
  out_phi_equity.csv            equity index shift, region x phi, consensus
  out_phi_credit.csv            CDS spread shift (median), region x phi, consensus
  out_phi_credit_scen.csv       the same, scenario x phi x region
  out_phi_invariance.csv        rate and FX at each phi, to show they do not move
  out_phi_crossings.csv         zero crossing per region x scenario

Usage: py -3 tools/run_phi_sweep.py
"""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")
os.makedirs(RESULTS, exist_ok=True)
sys.path.insert(0, ROOT)

from bkmn import (credit, equity, fx, macro, mixture,       # noqa: E402
                  physical, regions, transition)
from bkmn.run_fx import BASE, warming, xce_annual           # noqa: E402
from bkmn.scenarios import Scenarios                        # noqa: E402

PHIS = np.round(np.arange(0.0, 1.0001, 0.1), 2)
YEAR = 2040
HEAD = "consensus"                       # the chapter's headline prior
REF = "Net Zero 2050"                    # kept only to quote the level ratio


def crossing(phis, v):
    """Interpolated phi at which a curve first changes sign, or nan."""
    v = np.asarray(v, float)
    s = np.where(np.diff(np.sign(v)) != 0)[0]
    if not len(s) or abs(v[0]) < 1e-12:
        return float("nan")
    i = s[0]
    return float(phis[i] + (phis[i+1] - phis[i]) * (-v[i]) / (v[i+1] - v[i]))


def main():
    m = regions.load()
    sc = Scenarios(m.carbon_map)
    cm = m.carbon_map.set_index("region")
    vl = physical.vl_vector(m)
    betas = equity.betas()
    R = m.regions_order
    idx = [c for c in credit.CDS_SECTORS if c != "FTSE"]

    tr_all, eq_all, cr_all, inv_all, ct_ref = {}, {}, {}, {}, {}
    for s in sc.names:
        xce = xce_annual(sc, s)
        fac = sc.intensity_factor(s, YEAR)
        dT = warming(sc, s, YEAR)
        ph = physical.region_damage(m, dT, vl)
        ct_phys = physical.tax_addon(m, dT, vl)
        ct_ref[s] = transition.ct_direct(m, xce.loc[YEAR].to_dict(), fac)

        for phi in PHIS:
            M = transition.gva_operator(m, float(phi))
            tr = transition.region_gdp_shock(m, M, xce.loc[YEAR].to_dict(), fac)
            dY = {r: tr[r] + ph[r] for r in R}
            eq = equity.equity_shift(dY, betas)
            cs = credit.credit_shift(m, M, ct_ref[s] + ct_phys)
            for r in R:
                tr_all[(s, r)] = {**tr_all.get((s, r), {}), phi: tr[r] * 100}
                eq_all[(s, r)] = {**eq_all.get((s, r), {}), phi: eq[r] * 100}
                cr_all[(s, r)] = {**cr_all.get((s, r), {}),
                                  phi: float(np.median([cs[r][c] for c in idx])) * 100}

            # the invariance check: rate and FX must not depend on phi at all
            dpi = {r: macro.inflation_dev(
                float(xce.loc[YEAR, r] - xce.loc[YEAR - 1, r]),
                float(cm.loc[r, "carbon_scope"])) for r in R}
            dr = {r: macro.taylor_rate_shift(dpi[r], ph[r]) for r in R}
            cum = {r: macro.INFL_PER_USD * float(cm.loc[r, "carbon_scope"])
                   * float(xce.loc[YEAR, r] - xce.loc[BASE, r]) for r in R}
            inv_all[(s, phi)] = {
                "rate_IND_bp": dr["IND"] * 1e4,
                "rate_EU27_bp": dr["EU27"] * 1e4,
                "spot_USD_pct": fx.spot_ppp(cum["USA"], cum["EU27"]) * 100,
                "fwd5_IND_pct": fx.forward_total(
                    cum["IND"], cum["EU27"], dr["IND"], dr["EU27"], 5) * 100}

    def panel(d):
        f = pd.DataFrame(d).T
        f.index = pd.MultiIndex.from_tuples(f.index, names=["scenario", "region"])
        f = f[PHIS]
        # short, stable column labels: the raw floats round-trip as "0.100000",
        # which anything reading the CSV then has to guess at
        f.columns = [f"{p:.1f}" for p in PHIS]
        return f

    tr_s, eq_s, cr_s = panel(tr_all), panel(eq_all), panel(cr_all)
    tr_s.to_csv(f"{RESULTS}/out_phi_transition_scen.csv", float_format="%.6f")
    cr_s.to_csv(f"{RESULTS}/out_phi_credit_scen.csv", float_format="%.6f")

    # mixture-weight to the headline prior, then transpose back to phi x region
    # so the committed filenames keep the shape the figures and gates expect
    # `consensus` is not a static shape -- it is built from the scenarios' own
    # end-century warming against the UNEP/CAT anchor, exactly as run_extensions
    # does, so the two orchestrators cannot drift apart
    shapes = dict(mixture.PRIORS)
    shapes["consensus"] = mixture.consensus_shape(sc.coords())

    def mixed(p_scen, prior=HEAD):
        e = mixture.expected(p_scen, shapes[prior])  # region x phi
        out = e.T
        out.index = [float(c) for c in out.index]
        out.index.name = "phi"
        return out.sort_index()

    tr_df = mixed(tr_s)
    tr_df.to_csv(f"{RESULTS}/out_phi_transition.csv", float_format="%.4f")
    mixed(eq_s).to_csv(f"{RESULTS}/out_phi_equity.csv", float_format="%.4f")
    cr_df = mixed(cr_s)
    cr_df.to_csv(f"{RESULTS}/out_phi_credit.csv", float_format="%.4f")

    # the dimensionless shape: divide out the level, which is the only part the
    # carbon price sets.  phi = 0 is minus the region's whole carbon bill, so
    # this runs from -1 to +1 by construction.
    norm = tr_df.divide(tr_df.loc[0.0].abs(), axis=1)
    norm.to_csv(f"{RESULTS}/out_phi_transition_norm.csv", float_format="%.6f")

    # crossings, region x scenario, plus the mixture column
    cx = pd.DataFrame({s: {r: crossing(PHIS, tr_s.loc[(s, r)].to_numpy(float))
                           for r in R} for s in sc.names})
    cx[HEAD] = {r: crossing(PHIS, tr_df[r].to_numpy(float)) for r in R}
    cx.to_csv(f"{RESULTS}/out_phi_crossings.csv", float_format="%.4f")

    inv = pd.DataFrame(inv_all).T
    inv.index = pd.MultiIndex.from_tuples(inv.index, names=["scenario", "phi"])
    # invariance is exact in every narrative (asserted below), so the mixture of
    # flat curves is flat too; weight it anyway so the figure's quoted levels
    # match the consensus rate and FX numbers in the rest of the chapter
    wt = mixture.weights(shapes[HEAD], scenarios=list(sc.names))
    inv_h = sum(inv.xs(s, level=0) * wt[s] for s in sc.names)
    inv_h.index.name = "phi"
    inv_h.to_csv(f"{RESULTS}/out_phi_invariance.csv", float_format="%.6f")

    print(f"pass-through sweep at {YEAR}: {len(sc.names)} scenarios x "
          f"{len(PHIS)} phi, headline prior = {HEAD}\n")
    print("transition GVA shock (%), consensus mixture, region x phi:")
    print(tr_df[["EU27", "CHN", "USA", "IND", "CHE"]].round(3).to_string())

    print("\n-- structural: holds in EVERY narrative --")
    worst = 0.0
    for s in sc.names:
        b = inv.xs(s, level=0)
        worst = max(worst, float((b.max() - b.min()).abs().max()))
    print(f"  rates and FX invariant to phi: max variation {worst:.2e} "
          f"{'INVARIANT' if worst < 1e-12 else '*** MOVES ***'}")
    mir = max(float((tr_s.loc[s]["1.0"] + tr_s.loc[s]["0.0"]).abs().max())
              for s in sc.names)
    print(f"  mirror  shock(1) = -shock(0): max|sum| {mir:.2e}")
    ident = 0.0
    for s in sc.names:
        for r in R:
            k = m.region_of == r
            ref = (m.x * ct_ref[s])[k].sum() / m.gva[k].sum() * 100
            ident = max(ident, abs(float(tr_s.loc[(s, r), "1.0"]) - ref))
    print(f"  endpoints = +/- carbon bill over GVA: max|diff| {ident:.2e}")
    lo, hi = np.nanmin(cx.values), np.nanmax(cx.values)
    print(f"  every crossing above one half: [{lo:.3f}, {hi:.3f}]  "
          f"{'YES' if lo > 0.5 else '*** NO ***'}")

    print("\n-- scenario-scaled: only the level --")
    ratio = (tr_s.loc[REF]["0.0"].abs().sum()
             / tr_s.loc["Current Policies"]["0.0"].abs().sum())
    print(f"  phi=0 charge, Net Zero vs Current Policies: {ratio:.0f}x")
    print(f"  consensus mixture phi=0, IND {tr_df.loc[0.0,'IND']:.3f} %  "
          f"vs Net Zero {tr_s.loc[(REF,'IND'),'0.0']:.3f} %")

    print("\n-- in between: the crossing moves with the pricing pattern --")
    rng = (cx[list(sc.names)].max(axis=1) - cx[list(sc.names)].min(axis=1))
    print(f"  spread across narratives: median {rng.median():.3f}, "
          f"max {rng.max():.3f} ({rng.idxmax()})")
    print(cx[[HEAD]].round(3).sort_values(HEAD).to_string())
    return tr_df, cr_df, inv


if __name__ == "__main__":
    main()
