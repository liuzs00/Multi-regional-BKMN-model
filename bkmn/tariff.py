"""
Tariffs as a tax — the general machinery behind the CBAM special case.

The project brief's stretch goal is "alternative shocks to CO2 prices, e.g.
tariffs, or changes in trade flows between regions".  A tariff is structurally
the same object as the model's carbon charge: an ad-valorem cost wedge that
propagates through the Leontief dual.  The difference is only where it sits —
the carbon charge is levied on a sector's *own production*, a tariff on its
*imported inputs*, i.e. on the off-diagonal blocks of A.

A tariff schedule is represented by a matrix

    TAU[k, d] = ad-valorem rate on good k (a region-industry pair) entering
                destination region d,  as a fraction of the good's value

which is dimensionless and therefore in the same units as `ct`, so the resulting
charges add to `ct` and go through `transition.gva_operator` unchanged.

Incidence.  Statutorily the importer pays, raising costs in the destination in
proportion to the tariffed inputs it uses.  Under elastic demand some would
instead be absorbed by the exporter as a lower price received.  `theta` splits
the two (1 = importer, 0 = exporter).  Since the model holds final demand fixed
there is **no trade diversion**: the schedule changes costs, never quantities or
sourcing.  That is the principal limitation of any tariff result here.

Note also that a tariff levied on goods going to *final demand* raises consumer
prices rather than producer costs, so it generates revenue without entering the
GVA chain; `final_demand_charge` reports it separately.
"""
import numpy as np

NO_TARIFF = None


def empty(m):
    """A zero schedule, shape (n_sectors, n_regions)."""
    return np.zeros((len(m.x), len(m.regions_order)))


def add_rule(m, tau, rate, origin=None, destination=None, industries=None,
             exclude_intra=True):
    """
    Add a flat ad-valorem `rate` to the schedule, in place.

    `origin` / `destination` are region codes or lists (None = all); `industries`
    an iterable of ICIO industry codes (None = all).  Intra-regional flows are
    excluded by default: a tariff applies to imports, not to domestic supply.
    """
    reg = np.asarray(m.regions_order)
    src = np.ones(len(m.x), bool) if origin is None else \
        np.isin(m.region_of, np.atleast_1d(origin))
    if industries is not None:
        src &= np.isin(np.asarray(m.industry_of), np.atleast_1d(industries))
    dst = np.ones(len(reg), bool) if destination is None else \
        np.isin(reg, np.atleast_1d(destination))

    block = np.outer(src.astype(float), dst.astype(float)) * rate
    if exclude_intra:                       # zero where origin region == destination
        same = (m.region_of[:, None] == reg[None, :])
        block = np.where(same, 0.0, block)
    tau += block
    return tau


def charges(m, A, tau, theta=1.0):
    """
    Per-unit-output tariff charge, ready to add to `ct`.

    Returns (total, importer_part, exporter_part).
    """
    reg = np.asarray(m.regions_order)
    n = len(m.x)
    imp = np.zeros(n)
    exp_num = np.zeros(n)                   # tariffed export value, per origin-sector

    for d, dreg in enumerate(reg):
        is_d = m.region_of == dreg
        if not is_d.any():
            continue
        t = tau[:, d]
        if not t.any():
            continue
        # importer side: destination industries' extra cost per unit of output
        imp[is_d] += theta * (t @ A[:, is_d])
        # exporter side: value of that region's tariffed sales into d
        exp_num += t * (A[:, is_d] * m.x[is_d]).sum(1)

    x_safe = np.where(m.x == 0, 1.0, m.x)
    exp = (1.0 - theta) * exp_num / x_safe
    return imp + exp, imp, exp


def revenue(m, A, tau, include_final_demand=True):
    """
    Tariff revenue (USD millions).

    Intermediate imports are charged through A; imports going straight to final
    demand are charged too — real tariffs do not care what the good is used for —
    but they do not enter the production-cost chain (see `final_demand_charge`).
    """
    reg = np.asarray(m.regions_order)
    total = 0.0
    for d, dreg in enumerate(reg):
        is_d = m.region_of == dreg
        t = tau[:, d]
        if not t.any():
            continue
        total += float(t @ (A[:, is_d] * m.x[is_d]).sum(1))
        if include_final_demand:
            total += float(t @ m.fd[:, d])
    return total


def final_demand_charge(m, tau):
    """
    Tariff on imports going to final demand, as a fraction of each destination's
    total final demand — i.e. the direct consumer-price impact.  Reported
    separately because it raises prices to households rather than producer costs,
    so it does not propagate through the input-output chain.
    """
    out = {}
    for d, dreg in enumerate(m.regions_order):
        base = m.fd[:, d].sum()
        out[dreg] = float(tau[:, d] @ m.fd[:, d] / base) if base else 0.0
    return out
