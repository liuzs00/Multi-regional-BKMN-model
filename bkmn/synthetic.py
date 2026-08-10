"""
Synthetic economies for structural validation.

The result tables cannot tell you whether the multi-regional machinery is
*correct* — only whether it runs.  A wrong sign, a transposed block or a leak
between regions produces plausible-looking numbers.  What catches those is
running the model on economies whose right answer is known in advance by
symmetry, and checking that it returns it.

Three constructions, each isolating one property:

  `symmetric`   every region identical, trade symmetric.  Any cross-region
                difference the model reports is spurious by construction.
  `isolate`     one region's trade links cut.  Nothing may propagate into or
                out of it.
  `autarky`     every region's trade links cut.  The model must decompose into
                R independent single-region models.

These build a `Model20R` with the same fields the real loader produces, so every
downstream module runs on them unchanged — which is the point: the test exercises
the production code path, not a reimplementation of it.
"""
import numpy as np
import pandas as pd

from .regions import Model20R


def symmetric(n_regions=4, n_sectors=3, *, intensity=None, gva_share=0.4,
              trade_share=0.3, seed=0):
    """
    An economy of `n_regions` identical regions.

    Every region has the same technology, the same carbon intensity and the same
    size; each ships the same fraction of its inputs to every other region.  The
    only thing that can distinguish regions downstream is an input we vary
    deliberately, so any other asymmetry in the output is a bug.

    `intensity` sets carbon intensity per region (default: identical).  Passing
    a per-region vector breaks symmetry in exactly one place, which is what the
    third validation check needs.
    """
    rng = np.random.default_rng(seed)
    R, S = n_regions, n_sectors
    n = R * S

    # one sector-level technology block, shared by every region
    base = rng.uniform(0.05, 0.15, size=(S, S))

    # domestic share on the diagonal block, the rest split evenly across partners
    dom = 1.0 - trade_share
    off = trade_share / (R - 1) if R > 1 else 0.0

    A = np.zeros((n, n))
    for r in range(R):
        for s in range(R):
            w = dom if r == s else off
            A[r * S:(r + 1) * S, s * S:(s + 1) * S] = base * w

    x = np.full(n, 1000.0)
    Z = A * x[None, :]                      # so that A = Z / x exactly
    gva = x * gva_share

    regions_order = [f"R{i}" for i in range(R)]
    region_of = np.array([f"R{i}" for i in range(R) for _ in range(S)])
    industry_of = [f"S{j}" for _ in range(R) for j in range(S)]

    if intensity is None:
        ci = np.full(n, 200.0)
    else:
        ci = np.array([intensity[r] for r in region_of], float)

    # final demand: each region absorbs an equal share of every sector's output
    fd = np.full((n, R), (x.sum() - Z.sum()) / (n * R))

    cm = pd.DataFrame({
        "region": regions_order,
        "currency": [f"C{i}" for i in range(R)],
        "fx_role": ["base"] + ["analytical"] * (R - 1),
        "scenario_zone": ["R5.2OECD"] * R,
        "carbon_price_regime": ["synthetic"] * R,
        "cbam_role": ["none"] * R,
        "phys_vuln_tier": ["med"] * R,
        "ppp_gdp_weight": [1.0 / R] * R,
        "carbon_scope": [0.5] * R,
        "applied_price_usd": [0] * R,
    })

    return Model20R(regions_order=regions_order,
                    sectors=[f"{r}_{i}" for r, i in zip(region_of, industry_of)],
                    region_of=region_of, industry_of=industry_of,
                    Z=Z, x=x, gva=gva, ci=ci, fd=fd, carbon_map=cm)


def _rebuild_Z(m, A):
    """Return a copy of `m` whose Z implies the given technical matrix."""
    return Model20R(regions_order=m.regions_order, sectors=m.sectors,
                    region_of=m.region_of, industry_of=m.industry_of,
                    Z=A * m.x[None, :], x=m.x, gva=m.gva, ci=m.ci, fd=m.fd,
                    carbon_map=m.carbon_map)


def isolate(m, region):
    """
    Cut `region`'s trade links: it neither buys from nor sells to anyone else.

    Only the off-diagonal blocks are zeroed; the region's own internal structure
    and every other region's structure are untouched, so the comparison against
    the unmodified model is clean.

    Note this deliberately breaks the material balance x = Ax + f.  It does not
    matter: the transition channel is a PRICE calculation and consumes only A,
    x, gva and ct.  The test is about propagation through the dual, not about
    reproducing a consistent economy.
    """
    A = (m.Z / np.where(m.x == 0, 1.0, m.x)[None, :]).copy()
    k = m.region_of == region
    A[np.ix_(k, ~k)] = 0.0          # region sells to no one else
    A[np.ix_(~k, k)] = 0.0          # region buys from no one else
    return _rebuild_Z(m, A)


def autarky(m):
    """Cut every region's trade links: R independent single-region economies."""
    A = (m.Z / np.where(m.x == 0, 1.0, m.x)[None, :]).copy()
    for r in m.regions_order:
        k = m.region_of == r
        A[np.ix_(k, ~k)] = 0.0
    return _rebuild_Z(m, A)


def single_region(m, region):
    """
    Extract `region` as a standalone one-region model.

    Used to check that an isolated region inside the multi-regional model gives
    exactly what a genuinely single-region model of it would give -- i.e. that
    the generalisation reduces to the paper's case.
    """
    k = m.region_of == region
    cm = m.carbon_map[m.carbon_map.region == region].copy()
    cm["fx_role"] = "base"
    A = (m.Z / np.where(m.x == 0, 1.0, m.x)[None, :])[np.ix_(k, k)]
    x = m.x[k]
    return Model20R(regions_order=[region],
                    sectors=[s for s, kk in zip(m.sectors, k) if kk],
                    region_of=m.region_of[k],
                    industry_of=[i for i, kk in zip(m.industry_of, k) if kk],
                    Z=A * x[None, :], x=x, gva=m.gva[k], ci=m.ci[k],
                    fd=m.fd[np.ix_(k, [list(m.regions_order).index(region)])],
                    carbon_map=cm)
