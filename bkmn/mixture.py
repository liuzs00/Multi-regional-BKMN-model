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

PRIORS = {
    "uniform":        {NZ: 1, B2: 1, DT: 1, LD: 1, ND: 1, FW: 1, CP: 1},
    "policy-sceptic": {NZ: 1, B2: 1, DT: 2, LD: 1, ND: 4, FW: 3, CP: 4},
    "ambition":       {NZ: 4, B2: 4, DT: 2, LD: 3, ND: 2, FW: 1, CP: 1},
}


def weights(prior="uniform", counts=None, scenarios=None):
    """Posterior categorical probabilities p_s (Dirichlet conjugate update)."""
    a = dict(PRIORS[prior] if isinstance(prior, str) else prior)
    if counts:
        for s, c in counts.items():
            a[s] = a.get(s, 0) + c
    if scenarios is not None:
        a = {s: a.get(s, 0) for s in scenarios}
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
