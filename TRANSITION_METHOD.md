# Transition-risk core: how `L`, `Δp`, and the GVA shock

- `A` — technical coefficients (global MRIO)
- `L` — the Leontief inverse
- `Δp` — the carbon-tax price change, per sector
- `ΔV/V` — the relative GVA (value-added) shock, per sector → the paper's Table 4

Everything follows *Simple climate stress testing: an ensemble framework*
(Berrahoui, Kenyon, Macrina, Nathanael, 2025), §2.3–2.4, Eqs. 2, 6, 8, 10.

---

## 1. Inputs

| Symbol | Meaning | Source |
|---|---|---|
| `Z` | inter-industry flow matrix (650×650) | `DATA_13R/ICIO2025_13R_2022.csv`, region-industry block |
| `x` | gross output per sector (650) | ICIO `OUT` row |
| `GVA` | value added per sector (650) | ICIO `VA` row |
| `CI` | direct carbon intensity, tCO₂e per USD-million output | `DATA_13R/CARBON_INTENSITY_13R_2022.csv` |
| `XCE` | carbon price, USD/tCO₂e | parameter = **70** (paper's Table 4 value) |
| `φ` | cost pass-through fraction | parameter, swept **0 → 1** in 10% steps |

The index is 13 regions × 50 ISIC industries = **650 region-sectors** (labels like
`GBR_C24A`). ROW is the accounting closure region and is kept in the matrix so the
global IO system balances, but carries no financial interpretation.

**Units.** ICIO is in current USD millions; `CI` is tCO₂e per USD-million of
output. With `XCE` in USD/t, the per-output carbon charge is a **dimensionless
fraction of output value**:

$$ct_j = CI_j \times XCE \times 10^{-6}.$$

The $10^{-6}$ reconciles the units: the charge $CT_j = CI_j x_j \times XCE$ comes
out in plain USD, while output $x_j$ is in USD *millions*, so dividing the two
requires the factor of a million.

---

## 2. Step 1 — technical coefficients `A` and Leontief inverse `L`

Column-normalise the flow matrix by gross output (Eq. 2), then invert:

$$A = Z\,\hat{x}^{-1}, \qquad A_{ij} = \frac{Z_{ij}}{x_j}, \qquad
L = (I - A)^{-1}.$$

Zero-output columns are guarded before the division.

`L` is the **demand-side** Leontief inverse; its column sums are sector output
multipliers. Because ICIO is a true multi-regional table, `A` is the full global
block matrix, so `L` embeds cross-border linkages automatically (a shock in one
region propagates to all others via the off-diagonal trade blocks).

The price side uses the **transpose (dual)** form $\tilde{L} = (I - A^{\top})^{-1}$
(Eq. 4).

A validity check: the spectral radius of `A` must be < 1 (productive economy).
For this data it is ≈ **0.586**, so `(I − A)` is invertible.

---

## 3. Step 2 — carbon charge vector `ct_direct`

Multiply each sector's carbon intensity by the carbon price (Eq. 6), aligning the
carbon-intensity table (industries × regions) to the ICIO region-sector ordering:

$$\mathbf{ct}_{\text{direct}} = \mathbf{CI}\times XCE \times 10^{-6}.$$

This is the fraction of each sector's output value taken by the carbon tax on its
**Scope-1** emissions. (Scope 2/3 are captured up/downstream through the IO
linkages, so only direct emissions enter here.)

---

## 4. Step 3 — price change `Δp` (modified Leontief dual, Eq. 8)

Only a fraction `φ` of the charge is passed into prices. With
$\hat{\phi} = \operatorname{diag}(\phi)$, the **modified Leontief dual** and the
resulting price change are:

$$\tilde{L}(\phi) = \big(I - A^{\top}\hat{\phi}\big)^{-1}\hat{\phi},
\qquad
\Delta p = \tilde{L}(\phi)\,\mathbf{ct}_{\text{direct}}.$$

`Δp_j` is the relative increase in sector *j*'s output price. It is **0 at φ=0**
(nothing passed on) and rises monotonically to full pass-through at φ=1.

---

## 5. Step 4 — GVA shock `ΔV/V` (Eq. 10)

The carbon charge splits into a *price* part (`Δp`) and a *retained-in-GVA* part.
Differencing the sector cost identity before/after the tax (Eqs. 3, 5, 9) under
inelastic demand (final demand `y` fixed) gives the per-unit-output value-added
change:

$$\Delta v = \Big[(I - A^{\top})\,\tilde{L}(\phi) - I + \hat{\phi}\Big]\,\mathbf{ct}_{\text{direct}}.$$

Scale to absolute and then to a **relative** shock:

$$\Delta V_j = x_j\,\Delta v_j, \qquad
\boxed{\ \frac{\Delta V_j}{V_j} = \frac{x_j\,\Delta v_j}{\text{GVA}_j}\ }.$$

**Sign convention.** Negative = value added lost. `Δp` and the GVA shock are
complementary: cost not passed into prices shows up as a GVA loss.

### Sanity anchors (the paper's two special cases)

| φ | `Δp` | GVA shock `ΔV/V` |
|---|---|---|
| **0** (absorb all) | 0 | $-CT_j/\text{GVA}_j$ (most negative) |
| **1** (pass all on) | max | $+CT_j/\text{GVA}_j$ (mirror image) |

The script verifies the region-level version: UK shock is **−0.851%** at φ=0 and
**+0.851%** at φ=1, matching $\mp\,CT_{\text{UK}}/\text{GDP}_{\text{UK}}$.

---

## 6. Step 5 — aggregating per-sector → per-nation

A region's GDP is the sum of its sectors' GVA, so the national relative shock is
the total ΔGVA over total GVA — equivalently a **GDP-share-weighted average** of
the per-sector shocks:

$$\frac{\Delta \text{GDP}_r}{\text{GDP}_r}
= \frac{\sum_{j\in r}\Delta V_j}{\sum_{j\in r}\text{GVA}_j}
= \sum_{j\in r} f_{j,r}\,\frac{\Delta V_j}{V_j},
\qquad f_{j,r} = \frac{\text{GVA}_j}{\sum_{k\in r}\text{GVA}_k}.$$

The weighting scheme differs by quantity: the GVA/GDP shock is weighted by **GVA
share**, whereas `Δp` is rolled up with **output weights**, since a producer-price
index is output-weighted rather than value-added-weighted.

The per-sector `ΔV` already contains cross-border cascading, so a national number
includes the drag from pricier imported inputs; aggregation just sums the region's
own sectors.

---

## 7. Outputs

| File | Content |
|---|---|
| `out_gva_shock_by_region_phi.csv` | national GVA/GDP shock (%), 13 regions × φ |
| `out_price_change_by_region_phi.csv` | national output-weighted `Δp` (%), 13 regions × φ |
| `out_gva_shock_by_sector_phi.csv` | full **650 region-sectors × φ** GVA shock (%) |
| `out_price_change_by_sector_phi.csv` | full **650 region-sectors × φ** `Δp` (%) |


