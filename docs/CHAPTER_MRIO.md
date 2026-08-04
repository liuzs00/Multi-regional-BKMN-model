# Multi-Regional Input–Output Analysis

## 1. Purpose and role in the model

The BKMN framework of Berrahoui, Kenyon, Macrina and Nathanael (2025) is an
ensemble: climate scenarios enter at one end, financial-market shocks leave at
the other, and the object that connects them is an input–output description of
the economy. Physical and transition stresses are applied to *sectors*; the
input–output core determines how a stress applied to one sector propagates to
every other, and the resulting sector-level changes in Gross Value Added (GVA)
drive the macroeconomic and financial channels downstream.

In the original model that core is a single national table — the UK, twenty
sectors. This chapter sets out its generalisation to an **inter-country
input–output (ICIO) system** of twenty regions and fifty industries, and shows
precisely what the generalisation buys. The short answer is that a single-region
model must assume a carbon price levied in one economy stays in that economy. It
does not. Under the twenty-region system a charge levied on China alone
displaces value added outside China equal to 5 % of the total effect; for
Norway, an open economy, the figure is 68 %. That leakage is invisible to a
one-country model and is the quantity this chapter's machinery is built to
measure.

The exposition follows Miller and Blair (2022) for the input–output foundations
and the paper's §2.3–2.4 for the carbon-charge application, and is organised so
that the single-region case appears first as a special case of the general one.

---

## 2. Single-region foundations

### 2.1 The two accounting identities

An economy of *n* sectors is described by two identities that share the same
production vector **x**. The *horizontal*, or demand-side, identity states that
everything a sector produces is either used by another sector or absorbed by
final demand:

$$x_i \;=\; \sum_{j=1}^{n} Z_{ij} \;+\; y_i, \qquad i = 1,\dots,n$$

where $Z_{ij}$ is the flow of goods from sector *i* to sector *j*, and $y_i$ is
final demand for *i*. The *vertical*, or cost-side, identity states that
everything a sector produces is paid for out of intermediate purchases and
primary inputs:

$$x_j \;=\; \sum_{i=1}^{n} Z_{ij} \;+\; \sum_{k=1}^{m} V_{kj}$$

with $V_{kj}$ the *k*-th primary input (labour, capital, taxes) used by sector
*j*. The two are the same table read along rows and down columns; the value
added of sector *j* is $\mathrm{GVA}_j = \sum_k V_{kj}$.

### 2.2 Technical coefficients and the Leontief inverse

Normalising the flow matrix by the output of the *purchasing* sector gives the
**technical coefficients**

$$\mathbf{A} \;=\; \mathbf{Z}\,\hat{\mathbf{x}}^{-1}, \qquad
A_{ij} \;=\; \frac{Z_{ij}}{x_j}$$

where $\hat{\mathbf{x}}$ denotes the diagonal matrix formed from **x**. The
coefficient $A_{ij}$ is the quantity of input *i* required per unit of output
*j*, and is treated as a fixed technology. Substituting into the horizontal
identity and solving,

$$\mathbf{x} \;=\; \mathbf{A}\mathbf{x} + \mathbf{y}
\qquad\Longrightarrow\qquad
\mathbf{x} \;=\; \underbrace{(\mathbf{I}-\mathbf{A})^{-1}}_{\textstyle \mathcal{L}}\,\mathbf{y}$$

The matrix $\mathcal{L}$ is the **Leontief inverse**. Its entry $\mathcal{L}_{ij}$
is the total output of sector *i* required, directly and indirectly, to deliver
one unit of final demand for *j*.

The inverse exists, and is economically meaningful, when the economy is
*productive*: the spectral radius $\rho(\mathbf{A}) < 1$. Under that condition
the Neumann expansion converges,

$$\mathcal{L} \;=\; \sum_{k=0}^{\infty} \mathbf{A}^{k}
\;=\; \mathbf{I} + \mathbf{A} + \mathbf{A}^{2} + \cdots$$

and admits a direct reading: the identity term is the delivery itself, $\mathbf{A}$
is the inputs needed to make it, $\mathbf{A}^2$ the inputs needed to make *those*,
and so on through successive rounds of production.

### 2.3 The price dual

The cost identity, multiplied through by prices, yields the dual system. Writing
$p_i$ for the price of good *i* and $q_k$ for the price of primary input *k*,

$$p_j x_j \;=\; \sum_{i=1}^{n} Z_{ij}\,p_i \;+\; \sum_{k=1}^{m} V_{kj}\,q_k$$

Dividing by $x_j$ and defining the primary-input cost per unit of output
$\mathbf{v} := \mathbf{V}\hat{\mathbf{x}}^{-1}\mathbf{q}$ gives

$$\mathbf{p} \;=\; \mathbf{A}^{\!\top}\mathbf{p} + \mathbf{v}
\qquad\Longrightarrow\qquad
\mathbf{p} \;=\; \underbrace{(\mathbf{I}-\mathbf{A}^{\!\top})^{-1}}_{\textstyle \widetilde{\mathcal{L}}}\,\mathbf{v}$$

This is the **Leontief dual**, or cost-push model. Where the primal answers *how
much must be produced to satisfy demand*, the dual answers *how far do prices
move when costs change* — which is the relevant question for a carbon charge.
Its transposed structure has a clear reading: costs propagate **downstream**,
from suppliers to their customers, whereas output requirements propagate
**upstream**, from customers to their suppliers.

---

## 3. The multi-regional generalisation

### 3.1 Block structure

Let there be *R* regions and *n* industries. Every quantity acquires a region
index, and the natural object is a **block matrix**. Write $Z^{rs}_{ij}$ for the
flow of good *i* produced in region *r* to industry *j* in region *s*. The
horizontal identity becomes

$$x^{r}_{i} \;=\; \sum_{s=1}^{R}\sum_{j=1}^{n} Z^{rs}_{ij}
\;+\; \sum_{s=1}^{R} y^{rs}_{i}$$

Output of sector *i* in region *r* is absorbed as intermediate input by
industries in *every* region, and by final demand in *every* region. Technical
coefficients are defined exactly as before, normalising by the output of the
purchasing industry:

$$A^{rs}_{ij} \;=\; \frac{Z^{rs}_{ij}}{x^{s}_{j}}$$

Stacking the region–industry pairs into a single index of dimension $N = R\,n$,
the system has the same form as the single-region case,

$$\mathbf{x} = \mathbf{A}\mathbf{x} + \mathbf{y}, \qquad
\mathbf{x} = (\mathbf{I}-\mathbf{A})^{-1}\mathbf{y}$$

but $\mathbf{A}$ is now an $R \times R$ array of $n \times n$ blocks:

$$\mathbf{A} \;=\;
\begin{pmatrix}
\mathbf{A}^{11} & \mathbf{A}^{12} & \cdots & \mathbf{A}^{1R}\\
\mathbf{A}^{21} & \mathbf{A}^{22} & \cdots & \mathbf{A}^{2R}\\
\vdots & & \ddots & \vdots\\
\mathbf{A}^{R1} & \mathbf{A}^{R2} & \cdots & \mathbf{A}^{RR}
\end{pmatrix}$$

The **diagonal blocks** $\mathbf{A}^{rr}$ are domestic technical coefficients —
what a single-region model would contain. The **off-diagonal blocks**
$\mathbf{A}^{rs}$, $r \neq s$, are imported-input coefficients, and they are the
entire content of the generalisation. Setting them to zero recovers *R*
independent single-region models.

### 3.2 What the off-diagonal blocks do

The Leontief inverse is not block diagonal even when trade is modest, because
$\mathcal{L} = \sum_k \mathbf{A}^k$ and powers of a block matrix mix the blocks.
A path from sector *i* in region *r* to sector *j* in region *s* may pass through
any number of intermediate countries. Consequently a shock anywhere is
transmitted everywhere, with an intensity that no single-region model can
represent.

This is measurable in the estimated system. In the twenty-region table,
**22.6 %** of the mass of $\mathbf{A}$ sits off the block diagonal — the direct
import share. After inversion, **20.0 %** of the mass of $\mathcal{L}$ is
off-diagonal. The two figures being close is itself informative: indirect
linkages roughly preserve the cross-border share rather than diluting it, because
imported inputs are themselves produced using further imports.

The economically important consequence is **leakage**. Applying a carbon charge
to a single region and measuring where the resulting value-added loss falls:

| Region charged | Share of total GVA effect falling **outside** that region |
|---|--:|
| China | 5.0 % |
| India | 10.3 % |
| United States | 10.5 % |
| EU27 | 14.5 % |
| Norway | **68.2 %** |

Large, relatively closed economies retain most of the incidence of their own
carbon policy; small open economies do not. For Norway, more than two-thirds of
the value-added effect of a Norwegian carbon charge is borne abroad. A
single-region model assigns all of it domestically, and there is no parameter
within such a model that can correct the error.

### 3.3 The dual in the multi-regional system

The dual generalises without modification:

$$\mathbf{p} = \mathbf{A}^{\!\top}\mathbf{p} + \mathbf{v}, \qquad
\mathbf{p} = (\mathbf{I}-\mathbf{A}^{\!\top})^{-1}\mathbf{v}$$

with the transpose now exchanging the roles of the off-diagonal blocks:
$(\mathbf{A}^{\!\top})^{sr} = (\mathbf{A}^{rs})^{\!\top}$. Cost increases in
region *r* are transmitted to industries in region *s* in proportion to how much
*s* buys from *r*. This is the channel through which one region's carbon price
raises another region's production costs, and it is the mechanism underlying both
carbon leakage and the case for a border adjustment.

---

## 4. Construction of the twenty-region system

### 4.1 Source and aggregation

The system is built from the **OECD Inter-Country Input–Output tables, 2025
edition**, reference year 2022, in current US dollars at basic prices. The source
distinguishes 81 economies and 50 ISIC Rev. 4 industries. These are aggregated to
**20 regions × 50 industries = 1000 region–industry pairs**.

Aggregation is by **plain summation** of flows. For a group of economies $G$
forming region *r*,

$$Z^{rs}_{ij} \;=\; \sum_{c \in G_r} \sum_{d \in G_s} Z^{cd}_{ij}$$

For current-price tables this is exact, not approximate: monetary flows are
additive, so no weighting scheme is involved and no information is lost beyond
the deliberate loss of within-group detail. Flows *between* two members of the
same group become intra-regional flows on the diagonal block, exactly as domestic
flows are for a single-country region.

Note that aggregation must be performed on the **flows** $\mathbf{Z}$ and outputs
$\mathbf{x}$, and the coefficients $\mathbf{A}$ recomputed afterwards. Averaging
coefficients directly would be incorrect, since $A$ is a ratio and the correct
aggregate is the ratio of sums, not the sum of ratios.

### 4.2 The closure region

The twenty regions comprise nineteen chosen for analysis and one, denoted ROW,
that aggregates all remaining economies together with the source table's own
rest-of-world residual. ROW is not an analytical object: it exists because the
global system only balances — every export having a matching import — if all
economies outside the chosen set are retained. It is assigned no financial
outputs and no scenario interpretation.

Whether this aggregation biases the analytical regions is testable, and was
tested. Disaggregating ROW's six largest and most carbon-intensive members and
re-running the entire chain changes every analytical region's transition shock by
less than 0.007 percentage points and every output multiplier by less than
0.15 %. Since those six are precisely the members most capable of biasing the
result, any finer partition changes less; the aggregation has converged.

### 4.3 Validation

Three checks are applied at construction.

**Preservation of totals.** Aggregation must leave the global sum of every cell
unchanged to floating-point precision; the assertion is enforced at a relative
tolerance of $10^{-9}$. That checksum totals $300.5$ trillion USD, but it is an
accounting invariant rather than an economic magnitude — it sums intermediate
flows, final demand, taxes and value added together and therefore double-counts.
The economically meaningful totals of the assembled system are **world gross
output of $199.7$ trillion USD** and **world value added of $93.8$ trillion USD**,
the latter being the input–output system's measure of world GDP and consistent
with independent estimates for 2022. That gross output is roughly twice value
added is the expected signature of an economy in which a little over half of all
transactions are inter-industry rather than final.

**The output identity.** Row sums of intermediate flows plus final demand should
equal published gross output. The OECD source carries small imbalances of its own
— of order $10^{-3}$ relative — and linear aggregation passes them through
unchanged. The published output vector is retained as canonical and a loose bound
is asserted to catch genuine construction errors rather than to mask source noise.

**Productiveness.** The estimated system has

$$\rho(\mathbf{A}) \;=\; 0.5865 \;<\; 1$$

so $(\mathbf{I}-\mathbf{A})$ is invertible and the Neumann expansion converges.
Convergence is rapid: successive rounds of production contribute

| Round *k* | Share of $\mathcal{L}$ | Cumulative |
|---|--:|--:|
| 0 (the delivery itself) | 46.9 % | 46.9 % |
| 1 (direct inputs) | 24.1 % | 71.0 % |
| 2 | 13.1 % | 84.1 % |
| 3 | 7.1 % | 91.2 % |
| 4 | 3.9 % | 95.1 % |
| 5–7 | 4.0 % | 99.1 % |

so that essentially the whole multiplier is accounted for within seven rounds.
Output multipliers, the column sums of $\mathcal{L}$, average **2.133** across the
1000 region–industry pairs, ranging from 1.000 for sectors with no purchased
inputs to 3.744 for the most deeply embedded.

---

## 5. The carbon charge in the multi-regional dual

### 5.1 The charge

Following §2.4 of the paper, transition risk enters as a tax-like cost on direct
emissions. For each region–industry pair the charge per unit of output is

$$ct^{r}_{i} \;=\; \mathrm{CI}^{r}_{i} \times \mathrm{XCE}^{r} \times 10^{-6}$$

where $\mathrm{CI}$ is Scope-1 emissions intensity in tonnes of CO₂-equivalent per
million USD of output, and $\mathrm{XCE}$ is the carbon price in USD per tonne.
The factor $10^{-6}$ reconciles the units: the charge $\mathrm{CI}\cdot x \cdot
\mathrm{XCE}$ is denominated in dollars while output is in millions, so the ratio
requires the conversion. The result is dimensionless — a fraction of the value of
output — which is the form required for it to enter a system written in shares.

Scope 2 and Scope 3 emissions are deliberately excluded from the charge, because
they are already captured: emissions embodied in purchased inputs appear as the
Scope-1 emissions of the supplying industry, and are transmitted by the
input–output structure itself. Charging them directly would double-count.

The multi-regional generalisation makes $\mathrm{XCE}^{r}$ **region-specific**,
where the single-region model necessarily has a scalar. This is the point at
which differentiated climate policy — a carbon price in one bloc and none in
another — becomes representable.

### 5.2 Incomplete pass-through

A charge on a sector is not necessarily borne by that sector. Let $\phi_j \in
[0,1]$ be the fraction that industry *j* passes on to its customers in the form of
higher prices, with $1-\phi_j$ absorbed in its own margin. Writing
$\hat{\boldsymbol\phi}$ for the diagonal matrix of pass-through rates, the price
response to the introduction of the charge is

$$\Delta\mathbf{p} \;=\;
\underbrace{\left(\mathbf{I}-\mathbf{A}^{\!\top}\hat{\boldsymbol\phi}\right)^{-1}\hat{\boldsymbol\phi}}_{\textstyle \widetilde{\mathcal{L}}(\phi)}\;
\mathbf{ct}$$

The operator $\widetilde{\mathcal{L}}(\phi)$ is the **modified Leontief dual**.
Pass-through appears twice, and for different reasons: the leading
$\hat{\boldsymbol\phi}$ determines how much of the direct charge enters prices at
all, while the $\hat{\boldsymbol\phi}$ inside the inverse determines how much of
each *round* of downstream cost increase is passed on in turn. Setting
$\phi = 1$ recovers the unmodified dual $(\mathbf{I}-\mathbf{A}^{\!\top})^{-1}$;
setting $\phi = 0$ gives $\widetilde{\mathcal{L}} = \mathbf{0}$ and no price
response whatsoever.

### 5.3 The value-added shock

Differencing the cost identity before and after the charge, under the assumption
of inelastic final demand (**y** held fixed), and substituting the price response
above, gives the change in primary-input cost per unit of output:

$$\Delta\mathbf{v} \;=\;
\Big[\left(\mathbf{I}-\mathbf{A}^{\!\top}\right)\widetilde{\mathcal{L}}(\phi)
\;-\;\mathbf{I}\;+\;\hat{\boldsymbol\phi}\Big]\,\mathbf{ct}$$

Scaling to absolute terms and then to a relative shock,

$$\Delta V_j \;=\; x_j\,\Delta v_j,
\qquad
\boxed{\;\frac{\Delta V_j}{V_j} \;=\; \frac{x_j\,\Delta v_j}{\mathrm{GVA}_j}\;}$$

Two limiting cases verify the construction and both hold exactly in the
implementation. With $\phi = \mathbf{0}$ the bracket reduces to $-\mathbf{I}$, so
$\Delta\mathbf{v} = -\mathbf{ct}$ and the sector absorbs the entire charge. With
$\phi = \mathbf{1}$ the first term becomes the identity and the bracket reduces to
$+\mathbf{I}$, so $\Delta\mathbf{v} = +\mathbf{ct}$: under inelastic demand a
sector that passes on all of its costs increases its nominal value added by the
full amount of the charge. The second case is a nominal accounting result rather
than a welfare gain, and should be read as such.

Between the extremes the response is not monotone for every sector. A sector with
little direct emission but carbon-intensive suppliers reaches its worst outcome at
intermediate pass-through, where it is already paying higher input prices but
cannot yet recover them — an effect that requires the full matrix machinery to
detect, and which no sector-by-sector calculation would reveal.

### 5.4 Linearity and computational form

For fixed $\phi$, the map from charge to value-added change is linear. Defining

$$\mathbf{M}(\phi) \;=\; \left(\mathbf{I}-\mathbf{A}^{\!\top}\right)\widetilde{\mathcal{L}}(\phi) - \mathbf{I} + \hat{\boldsymbol\phi}$$

the entire chain reduces to $\Delta\mathbf{V} = \mathbf{x}\odot(\mathbf{M}(\phi)\,\mathbf{ct})$.
The single $1000 \times 1000$ inversion required to form $\mathbf{M}$ is performed
once; every scenario, horizon and carbon-price path is then a matrix–vector
product. Since $\mathbf{ct}$ is itself linear in the carbon price, so is the
value-added shock — a property that is convenient computationally but is also a
substantive modelling limitation, discussed in §7.

---

## 6. From sectors to regions

The macroeconomic and financial channels require a regional aggregate. Because
gross domestic product is the sum of value added over sectors, the aggregation is
an identity rather than a modelling choice:

$$\frac{\Delta \mathrm{GDP}_r}{\mathrm{GDP}_r}
\;=\; \frac{\sum_{j \in r} \Delta V_j}{\sum_{j \in r} \mathrm{GVA}_j}
\;=\; \sum_{j \in r} f_{j,r}\,\frac{\Delta V_j}{V_j},
\qquad
f_{j,r} = \frac{\mathrm{GVA}_j}{\sum_{k \in r}\mathrm{GVA}_k}$$

The regional shock is thus a **value-added-weighted average** of the sector
shocks. Sectors with large value added dominate, which is why regional figures are
an order of magnitude smaller than the worst-affected sectors within them.

Prices require different treatment. There is no aggregate "price" to sum to, so a
regional price change is necessarily an *index*, and the natural weight is the
value of the output being priced:

$$\Delta p_r \;=\; \frac{\sum_{j\in r} x_j\,\Delta p_j}{\sum_{j\in r} x_j}$$

The distinction matters and is easy to conflate: value added aggregates by an
additive identity, prices only by a chosen index. A consequence is that sectors
with zero output drop out of the price index automatically, whereas the relative
value-added shock is undefined for a sector with zero value added and must be
reported as missing rather than as zero.

---

## 7. Assumptions and limitations

The framework's tractability rests on assumptions that should be stated
explicitly.

**Fixed technical coefficients.** $\mathbf{A}$ is held constant, so there is no
substitution away from inputs that become expensive. Under a carbon charge this
is conservative in one direction — real economies would substitute toward cleaner
inputs, reducing the cost — and the assumption becomes less defensible the larger
the price shock.

**Inelastic final demand.** Holding **y** fixed isolates the cost-push channel and
is what makes the dual solvable in closed form, but it also means that quantity
responses, including trade diversion, are absent by construction. This is the
binding limitation for any extension to tariffs, where diversion is often the
principal effect.

**Linearity in the carbon price.** Since $\Delta V$ is linear in $\mathbf{ct}$ and
$\mathbf{ct}$ is linear in $\mathrm{XCE}$, a carbon price five times larger
produces a shock five times larger, without limit. At the carbon prices implied by
ambitious scenarios this extrapolates a locally-estimated relationship far beyond
its calibration range, and the resulting magnitudes should be read as an ordering
and an upper bound rather than as forecasts.

**A static table.** The 2022 structure is applied to horizons out to 2045, so
structural change — the decarbonisation of electricity, the reconfiguration of
supply chains — is excluded. The paper notes the same limitation for the single
region case, where it is arguably milder, since a national table changes more
slowly than the global trade structure.

**Uniform pass-through.** A single $\phi$ is applied to all sectors and regions,
for want of estimates that differ across them. The machinery admits a full vector
$\hat{\boldsymbol\phi}$, so this is a calibration gap rather than a structural
one.

---

## 8. Summary

The multi-regional generalisation preserves the mathematical form of the
single-region model exactly: the same technical coefficients, the same Leontief
inverse, the same cost-push dual, the same modified dual under incomplete
pass-through. What changes is that $\mathbf{A}$ becomes a block matrix whose
off-diagonal entries carry imported inputs, and $\mathrm{XCE}$ becomes a vector
rather than a scalar.

Those two changes are sufficient to represent what a single-region model
structurally cannot: that carbon policy differs across jurisdictions, that the
cost of a charge levied in one place is partly borne in another, and that the
magnitude of that leakage depends on an economy's position in the global
production network — 5 % for China, 68 % for Norway. Quantifying that
displacement is the purpose of the apparatus developed here, and it is the
foundation on which the exchange-rate results of the following chapters are
built.

---

### References

Berrahoui, M., C. Kenyon, A. Macrina and G. Nathanael (2025). *Simple climate
stress testing: an ensemble framework.* Working paper.

Leontief, W. (1986). *Input–Output Economics*, 2nd edn. Oxford University Press.

Miller, R. E. and P. D. Blair (2022). *Input–Output Analysis: Foundations and
Extensions*, 3rd edn. Cambridge University Press.

OECD (2025). *Inter-Country Input–Output Tables, 2025 edition.*
