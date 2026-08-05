"""
CBAM — the EU Carbon Border Adjustment Mechanism as a carbon tariff.

The project brief's stretch goal is "alternative shocks to CO2 prices, e.g.
tariffs, or changes in trade flows between regions".  CBAM is the one carbon
tariff that actually exists, and it needs no data beyond what the model already
holds: the MRIO supplies bilateral trade by sector, `CARBON_INTENSITY_20R`
supplies embodied carbon by origin, and `region_carbon_map` supplies the carbon
price each origin already pays.

Mechanism.  On imports of covered goods the EU levies the difference between its
own carbon price and the price already paid at origin, applied to the embodied
carbon of the good:

    tau(r, i) = max(0, XCE_EU - XCE_r) * CI(r, i) * 1e-6        [fraction of value]

`tau` is dimensionless — the charge as a share of the imported good's value —
exactly the units of the model's own carbon charge `ct`, so it enters the same
modified Leontief dual with no new machinery.

Incidence.  Statutorily the EU importer pays, so the charge raises EU production
costs in proportion to how much covered import each EU industry uses:

    cbam_eu(j) = theta * sum_{r != EU} sum_{i in covered} A[(r,i),(EU,j)] * tau(r,i)

Under elastic demand some of it would instead be absorbed by the exporter as a
lower price received; `theta` splits the two (1 = full statutory incidence on the
EU importer, 0 = fully absorbed abroad).  The absorbed part is a charge on the
exporting sector, scaled by the share of its output that goes to the EU:

    cbam_exp(r,i) = (1 - theta) * tau(r,i) * (exports of (r,i) to EU) / x(r,i)

Both are per-unit-output charges, so the total is simply added to `ct` and pushed
through `transition.gva_operator` as before.

Coverage.  CBAM Annex I covers cement, iron & steel, aluminium, fertilisers,
electricity and hydrogen, mapped onto ICIO industries as below.  Fertilisers and
hydrogen both sit inside the chemicals industry C20, which therefore overstates
coverage; a coverage fraction is applied to it.
"""
import numpy as np

# ICIO industry -> share of that industry within CBAM scope
COVERED = {
    "C23": 1.0,        # cement (other non-metallic mineral products)
    "C24A": 1.0,       # iron and steel
    "C24B": 1.0,       # aluminium (basic precious and other non-ferrous metals)
    "C20": 0.15,       # fertilisers + hydrogen, a minority of chemicals [ESTIMATE]
    "D": 1.0,          # electricity
}
BASE_REGION = "EU27"


def tariff_rate(m, xce_by_region, base=BASE_REGION):
    """
    tau per region-sector: the CBAM charge as a fraction of the good's value.
    Zero for the base region itself, for uncovered industries, and wherever the
    origin already pays at least the base price (no rebate).
    """
    cov = np.array([COVERED.get(i, 0.0) for i in m.industry_of], float)
    diff = np.array([max(0.0, xce_by_region[base] - xce_by_region[r])
                     for r in m.region_of], float)
    diff = np.where(m.region_of == base, 0.0, diff)
    return cov * diff * m.ci * 1e-6


def charges(m, A, xce_by_region, theta=1.0, base=BASE_REGION):
    """
    Per-unit-output CBAM charge vector, ready to add to `ct`.

    Returns (total, importer_part, exporter_part) so the incidence split can be
    reported separately.
    """
    tau = tariff_rate(m, xce_by_region, base)
    is_base = m.region_of == base

    # importer side: EU industries' extra cost from covered imports they use
    imp = np.zeros(len(m.x))
    imp[is_base] = theta * (tau[~is_base] @ A[np.ix_(~is_base, is_base)])

    # exporter side: absorbed by the origin, scaled by its EU-bound output share
    #   (intermediate exports to the base region, per unit of own output)
    eu_share = np.zeros(len(m.x))
    x_safe = np.where(m.x == 0, 1.0, m.x)
    eu_share[~is_base] = (A[np.ix_(~is_base, is_base)] * m.x[is_base]).sum(1) \
        / x_safe[~is_base]
    exp = (1.0 - theta) * tau * np.clip(eu_share, 0.0, 1.0)

    return imp + exp, imp, exp


def revenue(m, A, xce_by_region, base=BASE_REGION):
    """CBAM revenue (USD m): tau x the value of covered intermediate imports."""
    tau = tariff_rate(m, xce_by_region, base)
    is_base = m.region_of == base
    imports = (A[np.ix_(~is_base, is_base)] * m.x[is_base]).sum(1)
    return float((tau[~is_base] * imports).sum())
