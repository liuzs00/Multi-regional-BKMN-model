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
# NOTE on provenance: `uniform` is the conventional uninformative prior;
# `policy-sceptic` and `ambition` are **illustrative bookends we assert** — the
# directions are narrative logic, the magnitudes are arbitrary, and NGFS
# deliberately publishes no scenario probabilities. The `consensus` prior built
# by `consensus_shape()` below is the one anchored on a citable source.

# --- citable anchor: published end-century warming under current policies -----
# UNEP Emissions Gap Report 2025: current policies 2.8 C; full NDCs 2.3-2.5 C.
#   https://www.unep.org/resources/emissions-gap-report-2025
# Climate Action Tracker, COP30 global update (2025-11): policies & action and
# pledges & targets both ~2.6 C; optimistic (all net-zero announcements) 1.6 C.
#   https://climateactiontracker.org/publications/warming-projections-global-update-2025/
CONSENSUS_T = 2.7      # midpoint of CAT 2.6 and UNEP 2.8, degC vs pre-industrial
CONSENSUS_SD = 0.3     # spread across the two assessments and their stated ranges


def consensus_shape(coords, mu=CONSENSUS_T, sd=CONSENSUS_SD):
    """
    Prior weights from proximity to the published current-policy warming estimate.

    Mirrors the paper's own construction: §3.1.4 takes an authoritative statement
    about where current policies lead ("a path closer to SSP2 combined with
    RCP4.5 or RCP6.0", IPCC 2023) and puts 90 % of the mass on that pair.  Here
    the authoritative statement is the UNEP/CAT current-policy warming estimate,
    and scenarios are weighted by a Gaussian in their own end-century warming:

        α_s ∝ exp(−½ ((T₂₁₀₀,s − μ) / sd)²)

    Like the paper's 90 %, this is concentrated — which is itself informative: on
    the published trajectory most probability sits on the low-carbon-price end, so
    transition-driven FX risk lives in the tail rather than the expectation.
    """
    t = coords["T"].astype(float)
    w = np.exp(-0.5 * ((t - mu) / sd) ** 2)
    return (w / w.sum() * ALPHA0).to_dict()

#: α per scenario, normalised to Σα = ALPHA0 for every named prior.
PRIORS = {name: {s: v / sum(shape.values()) * ALPHA0 for s, v in shape.items()}
          for name, shape in PRIOR_SHAPES.items()}


def _key(s):
    """
    Normalised scenario key for matching.

    The IIASA API returns "Below 2?C" (an ASCII '?' where the source has a
    degree sign), so an exact-string lookup against a literal "Below 2°C" in
    this module silently failed and that scenario was dropped from the mixture.
    Matching on alphanumerics only makes the join robust to that and to any
    other punctuation drift ('°', '?', '℃', hyphens, case).
    """
    return "".join(ch for ch in str(s).lower() if ch.isalnum())


def alphas(prior="uniform", counts=None):
    """
    Dirichlet parameters after the conjugate update (paper §2.2):
        posterior α_s = prior α_s + c_s
    `counts` are observed events the user attributes to each narrative — e.g.
    {"Current Policies": 3, "Net Zero 2050": 1} for three policy rollbacks and
    one net-zero commitment since the prior date.
    """
    a = dict(PRIORS[prior] if isinstance(prior, str) else prior)
    by_key = {_key(s): s for s in a}
    for s, c in (counts or {}).items():
        s = by_key.get(_key(s), s)              # tolerate punctuation drift
        a[s] = a.get(s, 0.0) + c
    return a


def weights(prior="uniform", counts=None, scenarios=None):
    """
    Posterior categorical probabilities p_s = α_s / Σα (Dirichlet mean).

    `scenarios` restricts/reorders the output to the caller's own labels; they
    are matched to the prior on the normalised key (see `_key`), and an
    unmatched label is an error rather than a silent zero weight.
    """
    a = alphas(prior, counts)
    if scenarios is not None:
        by_key = {_key(s): v for s, v in a.items()}
        missing = [s for s in scenarios if _key(s) not in by_key]
        if missing:
            raise KeyError(f"scenarios absent from the prior: {missing}")
        a = {s: by_key[_key(s)] for s in scenarios}
    tot = float(sum(a.values()))
    return {s: v / tot for s, v in a.items()}


def transition_matrix(coords, lam=2.0, axes=("T", "XCE")):
    """
    Annual scenario-transition matrix, paper Eq 1:

        q(j,k) = exp(−λ·d(j,k)) / Σ_h exp(−λ·d(j,h))

    The paper's d is |j−k| on RCP concentration labels.  NGFS narratives carry no
    such label, so d is the Euclidean distance in **standardised (T₂₁₀₀, XCE)
    space** — the two characteristics that distinguish the scenarios and that
    drive this model.  Standardising (z-score per axis) makes λ dimensionless and
    stops the $/t axis swamping the K axis.

    Eq 1 permits exactly this: the distance "can be generalized to include any
    function of RCP characteristics".  A 1-D coordinate (`axes=("T",)` or
    `("XCE",)`) reproduces the paper's literal form and is kept as a sensitivity
    — note |ΔT| alone correlates only 0.28 with how differently the model
    behaves, against 0.98 for |ΔXCE| (docs/PAPER_AUDIT.md §E).

    `coords` is a DataFrame indexed by scenario (see Scenarios.coords).
    Returns (scenarios, Q) with Q[j, k] = P(j → k) in one year.
    """
    c = coords[list(axes)].to_numpy(float)
    c = (c - c.mean(0)) / c.std(0, ddof=0)                 # standardise each axis
    d = np.linalg.norm(c[:, None, :] - c[None, :, :], axis=-1)
    w = np.exp(-lam * d)
    return list(coords.index), w / w.sum(axis=1, keepdims=True)


def drifted_weights(prior, coords, years, lam=2.0, axes=("T", "XCE"), counts=None):
    """
    Mixture weights after `years` annual applications of Q (paper §3.1.5):
        p_T = p_0 · Q^T
    λ → ∞ gives Q = I and reproduces the static mixture exactly.
    """
    scen, Q = transition_matrix(coords, lam, axes)
    p0 = np.array([weights(prior, counts, scen)[s] for s in scen])
    pT = p0 @ np.linalg.matrix_power(Q, int(years))
    return dict(zip(scen, pT))


def expected_drift(table, coords, prior="uniform", lam=2.0, base_year=2022,
                   axes=("T", "XCE"), counts=None):
    """Expectation with horizon-dependent weights (scenario drift under Eq 1)."""
    out = None
    for col in table.columns:
        yrs = max(0, int(col) - base_year)
        p = drifted_weights(prior, coords, yrs, lam, axes, counts)
        part = sum(table.xs(s, level=0)[col] * p[s] for s in p)
        out = part.to_frame(col) if out is None else out.join(part.to_frame(col))
    return out


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
