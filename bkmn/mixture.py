"""
Phase M — Bayesian scenario mixture (paper §2.2 + expected output §3.1.5).

Purely additive: every per-scenario table is left untouched and becomes a
*component*; the mixture adds a probability weight per scenario and reports the
expectation and the discrete scenario distribution.

    Dirichlet-categorical:  p_s = (α_s + c_s) / Σ_k (α_k + c_k)
    E[X] = Σ_s p_s · X_s                               (paper Eq 21)

Named priors (narrative weights — a modelling judgment, to be blessed by the
supervisor; report several side by side):
  uniform         equal weight on all NGFS scenarios
  policy-sceptic  mass on Current Policies / NDCs / Fragmented World
  ambition        mass on Net Zero 2050 / Below 2°C / Low demand
"""
import numpy as np
import pandas as pd

NZ = "Net Zero 2050"
B2 = "Below 2°C"
DT = "Delayed transition"
LD = "Low demand"
ND = "Nationally Determined Contributions (NDCs)"
FW = "Fragmented World"
CP = "Current Policies"

# Relative *shape* of each narrative — direction only.  All priors are rescaled
# to the same total concentration ALPHA0 so that switching prior changes the
# direction of belief, never its strength: in a Dirichlet, Σα is how many
# observed events it takes to overturn the prior.  Equal Σα keeps the three
# comparable under the event-count update below.  (Rescaling does not change the
# implied probabilities — they are proportions — only the posterior stiffness.)
ALPHA0 = 14.0

PRIOR_SHAPES = {
    "uniform":        {NZ: 1, B2: 1, DT: 1, LD: 1, ND: 1, FW: 1, CP: 1},
    "policy-sceptic": {NZ: 1, B2: 1, DT: 2, LD: 1, ND: 4, FW: 3, CP: 4},
    "ambition":       {NZ: 4, B2: 4, DT: 2, LD: 3, ND: 2, FW: 1, CP: 1},
}

#: α per scenario, normalised to Σα = ALPHA0 for every named prior.
PRIORS = {name: {s: v / sum(shape.values()) * ALPHA0 for s, v in shape.items()}
          for name, shape in PRIOR_SHAPES.items()}


def alphas(prior="uniform", counts=None):
    """
    Dirichlet parameters after the conjugate update (paper §2.2):
        posterior α_s = prior α_s + c_s
    `counts` are observed events the user attributes to each narrative — e.g.
    {"Current Policies": 3, "Net Zero 2050": 1} for three policy rollbacks and
    one net-zero commitment since the prior date.
    """
    a = dict(PRIORS[prior] if isinstance(prior, str) else prior)
    for s, c in (counts or {}).items():
        a[s] = a.get(s, 0.0) + c
    return a


def weights(prior="uniform", counts=None, scenarios=None):
    """Posterior categorical probabilities p_s = α_s / Σα (Dirichlet mean)."""
    a = alphas(prior, counts)
    if scenarios is not None:
        a = {s: a.get(s, 0.0) for s in scenarios}
    tot = float(sum(a.values()))
    return {s: v / tot for s, v in a.items()}


def expected(table, prior="uniform", counts=None):
    """
    Probability-weighted expectation over scenarios.

    `table`: DataFrame indexed by (scenario, region), columns = horizons.
    Returns a DataFrame indexed by region.
    """
    scen = table.index.get_level_values(0).unique()
    p = weights(prior, counts, scen)
    out = None
    for s in scen:
        part = table.xs(s, level=0) * p[s]
        out = part if out is None else out + part
    return out


def quantile(table, q, prior="uniform", counts=None):
    """
    Weighted quantile across the discrete scenario distribution (per region ×
    horizon): the smallest scenario value whose cumulative weight reaches q.
    """
    scen = list(table.index.get_level_values(0).unique())
    p = weights(prior, counts, scen)
    regions = table.xs(scen[0], level=0).index
    out = pd.DataFrame(index=regions, columns=table.columns, dtype=float)
    for r in regions:
        for c in table.columns:
            vals = sorted(((table.loc[(s, r), c], p[s]) for s in scen))
            cum = 0.0
            for v, w in vals:
                cum += w
                if cum >= q - 1e-12:
                    out.loc[r, c] = v
                    break
    return out


if __name__ == "__main__":
    names = {NZ: "Net Zero 2050", B2: "Below 2C", LD: "Low demand",
             DT: "Delayed transition", ND: "NDCs", FW: "Fragmented World",
             CP: "Current Policies"}
    order = [NZ, B2, LD, DT, ND, FW, CP]
    print(f"concentration Σα = {ALPHA0} for every prior "
          f"(direction differs, strength does not)\n")
    print(f"{'scenario':20s}" + "".join(f"{p:>18s}" for p in PRIORS))
    print(f"{'':20s}" + "".join(f"{'alpha   prob':>18s}" for _ in PRIORS))
    for s in order:
        row = f"{names[s]:20s}"
        for p in PRIORS:
            row += f"{PRIORS[p][s]:11.2f}{weights(p)[s]*100:6.1f}%"
        print(row)
    print(f"{'TOTAL':20s}" + "".join(f"{sum(PRIORS[p].values()):11.2f}"
                                     f"{100.0:6.1f}%" for p in PRIORS))

    ev = {CP: 3, NZ: 1}
    print(f"\nevent-count update, counts={ {names[k]: v for k, v in ev.items()} }:")
    for p in PRIORS:
        w0, w1 = weights(p), weights(p, ev)
        print(f"  {p:15s} CP {w0[CP]*100:5.1f}% -> {w1[CP]*100:5.1f}%   "
              f"NZ {w0[NZ]*100:5.1f}% -> {w1[NZ]*100:5.1f}%")
