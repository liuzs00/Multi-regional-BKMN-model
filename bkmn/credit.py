"""
Phase C — the credit channel (paper §2.9, CDS half; §3.1.3 synthetic indices).

The paper's §2.9 transmits a GVA shock to two market prices through a regression
beta: equity (implemented in `equity.py`) and CDS spreads (here).  The two halves
share a structure and differ in one step -- a CDS index is not the whole economy,
so the sector shocks must first be blended into a synthetic index.

    synthetic index j, region r:
        (ΔV/V)_{j,r} = Σ_i w_ij · size_{i,r} · (ΔV/V)_{i,r}  /  Σ_i w_ij · size_{i,r}

    spread shift:
        Δs_{j,r} = β_j · (ΔV/V)_{j,r}                                    (§2.9)

`w` is Tables 7–8 (published index weights by SIC section) and `β` is Table 9.
Both are UK estimates applied unchanged to every region -- the same [PROXY]
treatment `OPRISK_BETA` already gets, and for the same reason: the coefficients
are published, the histories needed to re-estimate them per region are not.

Two details carried over from the single-region reproduction, both of which it
established against the paper's printed rows rather than its text:

  * `size` is **total output**, not GVA.  The two differ materially only for
    indices whose constituent sectors have very different output-to-GVA ratios
    -- Utilities above all -- and output weighting is what reproduces those
    cells.  `SIZE = "gva"` restores the literal reading.
  * a negative β means the spread WIDENS as GVA falls.  Financials and UK Real
    Estate carry positive slopes in the paper's own estimates and therefore move
    against the rest of the cross-section; that is a property of the UK sample.

Because a CDS index is a weighted blend of the same sector shocks the equity
channel uses, the credit cross-section is NOT independent information about a
region -- it is the sectoral composition of that region's shock, read through
twelve different weightings.  §5 of CHAPTER_RESULTS makes that explicit.
"""
import numpy as np

from .paper_tables import CDS_BETA, CDS_SECTORS, CDS_WEIGHTS, SIC_TO_ICIO

SIZE = "output"          # "output" (reproduces the paper) or "gva" (literal)

#: ICIO industry code -> UK SIC section, the inverse of SIC_TO_ICIO
ICIO_TO_SIC = {ind: sic for sic, inds in SIC_TO_ICIO.items() for ind in inds}


def weight_matrix(m):
    """(n_sectors × n_indices) index weight for every region-sector row."""
    cols = list(CDS_SECTORS)
    W = np.zeros((len(m.sectors), len(cols)))
    for k, ind in enumerate(m.industry_of):
        W[k] = CDS_WEIGHTS[ICIO_TO_SIC[ind]]
    return W, cols


def synthetic_shock(m, rel_dgva, size=SIZE):
    """
    {region: {index: relative GVA shock of that synthetic index}}.

    `rel_dgva` is the per-sector relative GVA shock (len = n_sectors).  The
    blend is taken WITHIN each region, so an index is that region's own version
    of the sector basket rather than a global one.
    """
    W, cols = weight_matrix(m)
    s = m.x if size == "output" else m.gva
    num = W * (s * rel_dgva)[:, None]
    den = W * s[:, None]
    out = {}
    for r in m.regions_order:
        k = m.region_of == r
        d = den[k].sum(axis=0)
        n = num[k].sum(axis=0)
        out[r] = {c: (float(n[j] / d[j]) if d[j] > 0 else 0.0)
                  for j, c in enumerate(cols)}
    return out


def spread_shift(syn, beta=None):
    """{region: {index: Δspread}} = β_j · synthetic shock (§2.9)."""
    beta = CDS_BETA if beta is None else beta
    return {r: {c: beta[c] * v for c, v in d.items()} for r, d in syn.items()}


def rel_dgva_sectors(m, M, ct):
    """Per-sector relative GVA shock ΔV_i/GVA_i from a charge vector."""
    gva = np.where(m.gva == 0, np.nan, m.gva)
    return np.nan_to_num(m.x * (M @ ct) / gva)


def credit_shift(m, M, ct, size=SIZE, beta=None):
    """End to end: charge vector -> per-region CDS spread shifts."""
    return spread_shift(synthetic_shock(m, rel_dgva_sectors(m, M, ct), size),
                        beta)
