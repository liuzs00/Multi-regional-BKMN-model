# Tariffs as a Second Cost Shock

## 1. Purpose

The transition chapter models a carbon price as a tax-like cost on production, levied
per unit of output in proportion to emissions intensity, and propagated through the
multi-regional Leontief dual. A tariff is also a tax-like cost, differing in what
triggers it: not the emissions a sector generates but the imported inputs it purchases.

This chapter shows that a tariff can be expressed in exactly the form the existing
machinery already consumes — a per-unit-of-output cost vector — and therefore requires
no new operator, no second inversion, and no change to the transmission chain
downstream. The carbon charge and the tariff charge become two entries in a single
shock vector.

The approach has one clear boundary, stated at the outset because it determines what
the extension can and cannot answer. Because the technical coefficients and final
demand are both held fixed, the framework captures the **cost-push** consequences of a
tariff exactly and its **substitution** consequences not at all. Section 8 develops
this.

---

## 2. Notation and the tariff schedule

The notation follows the multi-regional input–output chapter. There are $R$ regions
and $n$ industries, giving $N = Rn$ region–industry pairs. The technical coefficient

$$A^{rs}_{ij} \;=\; \frac{Z^{rs}_{ij}}{x^{s}_{j}}$$

is the value of good $i$ purchased from region $r$ per unit value of output of industry
$j$ in region $s$. Diagonal blocks $A^{ss}$ hold domestic input coefficients;
off-diagonal blocks $A^{rs}$, $r\neq s$, hold imported ones.

A **tariff schedule** is a set of ad-valorem rates

$$\tau^{rs}_{i} \;\ge\; 0,$$

interpreted as the duty levied by importing region $s$ on commodity $i$ originating in
exporting region $r$, expressed as a fraction of the import's value. By construction
$\tau^{ss}_{i} = 0$: a region does not tariff its own production. The schedule is
indexed by origin, destination and commodity, but **not** by the using industry — a
duty on imported steel is the same duty whoever buys it, which is a property exploited
in §3.2.

---

## 3. The tariff cost vector

### 3.1 Derivation

Consider industry $j$ in region $s$. Producing one unit of output requires, by
definition of the technical coefficients, $A^{rs}_{ij}$ units of value of good $i$
sourced from region $r$. If that flow crosses a border into a tariff regime, the
importer pays duty $\tau^{rs}_{i}$ on its value, so the duty borne per unit of output
on that single input flow is

$$\tau^{rs}_{i}\,A^{rs}_{ij}.$$

Summing over every imported commodity and every foreign source gives the total tariff
cost the sector bears per unit of its own output:

$$\boxed{\;ct^{\,\mathrm{tariff}}_{(s,j)} \;=\; \sum_{r\neq s}\;\sum_{i=1}^{n} \tau^{rs}_{i}\,A^{rs}_{ij}\;}
\tag{1}$$

This is the object required. It is a scalar per region–industry pair, measured as a
fraction of the value of output, and it is therefore commensurate with the carbon
charge of the transition chapter.

### 3.2 Matrix form

Equation (1) is a weighted column sum of the off-diagonal blocks of $\mathbf{A}$, and
is written compactly by introducing the tariff matrix
$\boldsymbol{\Theta}\in\mathbb{R}^{N\times N}$,

$$\Theta_{(r,i),(s,j)} \;=\; \tau^{rs}_{i}\,\mathbf{1}\{r\neq s\},$$

which is constant along $j$ because the schedule does not discriminate by using
industry, and vanishes on the diagonal blocks. Then

$$\mathbf{ct}^{\,\mathrm{tariff}} \;=\; \big(\boldsymbol{\Theta}\odot\mathbf{A}\big)^{\!\top}\mathbf{1}_{N},
\tag{2}$$

with $\odot$ the elementwise (Hadamard) product. Verifying the $(s,j)$ entry
reproduces (1):

$$\Big[(\boldsymbol{\Theta}\odot\mathbf{A})^{\!\top}\mathbf{1}\Big]_{(s,j)}
=\sum_{(r,i)}\Theta_{(r,i),(s,j)}A_{(r,i),(s,j)}
=\sum_{r\neq s}\sum_{i}\tau^{rs}_{i}A^{rs}_{ij}. \;\checkmark$$

An equivalent formulation is sometimes more convenient computationally. For each
importing region $s$, define the origin–commodity tariff vector
$\boldsymbol{\theta}^{s}\in\mathbb{R}^{N}$ with
$\theta^{s}_{(r,i)}=\tau^{rs}_{i}\mathbf{1}\{r\neq s\}$. Then the cost borne by each of
that region's industries is an inner product against the corresponding column of
$\mathbf{A}$:

$$ct^{\,\mathrm{tariff}}_{(s,j)} \;=\; \big\langle \boldsymbol{\theta}^{s},\; \mathbf{A}_{\bullet,(s,j)}\big\rangle .$$

### 3.3 Dimensional consistency

The two shocks must live in the same space for their sum to be meaningful. The
carbon charge is

$$ct^{\,\mathrm{carbon}}_{(s,j)} \;=\; \mathrm{CI}^{s}_{j}\cdot \mathrm{XCE}^{s}\cdot 10^{-6},$$

with $\mathrm{CI}$ in tonnes CO₂e per million USD of output and $\mathrm{XCE}$ in USD
per tonne, so the product is dimensionless — a fraction of the value of output. In (1),
$\tau$ is a pure rate and $A$ is a value-per-value ratio, so the product is likewise
dimensionless and on the same base. The two may be added directly:

$$\mathbf{ct} \;=\; \mathbf{ct}^{\,\mathrm{carbon}} + \mathbf{ct}^{\,\mathrm{tariff}} .$$

No rescaling is required, and this is the entire content of the "one common
machinery" claim.

---

## 4. Insertion into the cost-push system

With the combined shock vector in hand, the price response follows from the Leontief
dual unchanged. In the full pass-through case,

$$\Delta\mathbf{p} \;=\; \big(\mathbf{I}-\mathbf{A}^{\!\top}\big)^{-1}\big(\mathbf{ct}^{\,\mathrm{carbon}}+\mathbf{ct}^{\,\mathrm{tariff}}\big),
\tag{3}$$

and under incomplete pass-through $\phi$, using the modified dual
$\widetilde{\mathcal{L}}(\phi)=(\mathbf{I}-\mathbf{A}^{\!\top}\hat{\boldsymbol\phi})^{-1}\hat{\boldsymbol\phi}$,

$$\Delta\mathbf{p} \;=\; \widetilde{\mathcal{L}}(\phi)\,\big(\mathbf{ct}^{\,\mathrm{carbon}}+\mathbf{ct}^{\,\mathrm{tariff}}\big).$$

The value-added shock follows through the same operator as before,

$$\mathbf{M}(\phi) \;=\; \big(\mathbf{I}-\mathbf{A}^{\!\top}\big)\widetilde{\mathcal{L}}(\phi)-\mathbf{I}+\hat{\boldsymbol\phi},
\qquad
\Delta\mathbf{V} \;=\; \mathbf{x}\odot\Big(\mathbf{M}(\phi)\,\mathbf{ct}\Big),
\tag{4}$$

and the relative shock $\Delta V_j / V_j$, the regional aggregation, and every
downstream channel — inflation, the Taylor rule, the term structure, equity, exchange
rates — are unaltered. The extension terminates at equation (2); everything after it is
existing machinery.

A note on the pass-through parameter. Applying the same $\phi$ to both shocks assumes
firms pass on tariff costs and carbon costs at the same rate. This is a modelling
choice rather than a necessity: because $\hat{\boldsymbol\phi}$ enters
$\mathbf{M}(\phi)$ and not $\mathbf{ct}$, distinguishing the two would require running
(4) twice with different $\phi$ and summing, which the additivity of §5.1 licenses.

---

## 5. Structural properties

### 5.1 Exact additivity

Because $\mathbf{M}(\phi)$ is a fixed linear operator for a given $\phi$, the response
to the combined shock decomposes exactly:

$$\Delta\mathbf{V} \;=\; \mathbf{x}\odot\big(\mathbf{M}\mathbf{ct}^{\,\mathrm{carbon}}\big) \;+\; \mathbf{x}\odot\big(\mathbf{M}\mathbf{ct}^{\,\mathrm{tariff}}\big)
\;=\; \Delta\mathbf{V}^{\mathrm{carbon}} + \Delta\mathbf{V}^{\mathrm{tariff}} .$$

There is **no interaction term**. The carbon and tariff contributions may be computed
separately, reported separately, and summed, and the decomposition is exact rather than
approximate. This is analytically convenient — it permits clean attribution of any
result to one policy or the other — but it should be recognised as a consequence of
linearising the system, not a claim about the world. Real carbon and trade policies
interact, most obviously because a tariff alters the composition of imports and hence
the emissions embodied in them.

### 5.2 Uniform tariffs and import intensity

Setting $\tau^{rs}_{i}=\tau$ for all $r\neq s$ and all $i$ reduces (1) to

$$ct^{\,\mathrm{tariff}}_{(s,j)} \;=\; \tau\sum_{r\neq s}\sum_{i}A^{rs}_{ij} \;=\; \tau\,\mu_{(s,j)},
\qquad
\mu_{(s,j)} := \sum_{r\neq s}\sum_{i}A^{rs}_{ij},$$

where $\mu_{(s,j)}$ is the sector's **imported-input intensity** — the column sum of
the off-diagonal blocks, i.e. the share of a unit of output accounted for by foreign
inputs. Under a uniform tariff the shock is therefore proportional to a purely
structural statistic of the input–output table, with the tariff rate as the constant of
proportionality.

This yields the sharpest contrast with the carbon channel. Carbon exposure is
proportional to $\mathrm{CI}^{s}_{j}$, an *emissions* characteristic of the sector
itself; tariff exposure is proportional to $\mu_{(s,j)}$, a *trade* characteristic of
its supply chain. The two orderings of sectors are distinct, so the two policies fall
on different parts of the economy even when calibrated to equal aggregate cost.

### 5.3 Incidence: the importer pays

Although $\boldsymbol{\Theta}$ is supported entirely on the off-diagonal blocks, the
resulting cost vector (1) is indexed by the **importing** region $s$. The duty is borne
in the first instance by the purchasing sector, and the exporting region $r$ appears
only as the origin of the input.

This is the mirror image of the carbon-leakage result of the multi-regional chapter. A
carbon charge levied in region $r$ falls directly on $r$'s sectors and leaks abroad
through the dual as $r$'s customers pay higher prices. A tariff levied by region $s$
falls directly on $s$'s sectors and propagates to *their* customers. Under fixed
coefficients and fixed final demand, the exporter suffers no direct loss at all: it
still sells the same volume at the same pre-tariff price.

That conclusion is an artefact of the framework rather than a finding, and it is the
clearest statement of what §8 gives up. The channel by which a tariff actually harms an
exporter — lost market share — is a quantity response, and quantities do not move here.

### 5.4 Indirect exposure through the cascade

A sector with no imported inputs, $\mu_{(s,j)}=0$, still bears tariff cost, because the
dual propagates the shock from its suppliers. Expanding (3) by the Neumann series of
the appendix,

$$\Delta\mathbf{p} \;=\; \sum_{k=0}^{\infty}\big(\mathbf{A}^{\!\top}\big)^{k}\mathbf{ct}^{\,\mathrm{tariff}},$$

each round has a direct reading: $k=0$ is the duty the sector pays itself, $k=1$ the
duty embedded in the prices charged by its domestic suppliers, $k=2$ the duty embedded
in *their* suppliers' prices, and so on. Total tariff exposure is therefore always at
least as large as direct import intensity, and the gap between the two is a measure of
how deeply foreign inputs are embedded in an economy's domestic supply chains — a
quantity invisible to direct trade statistics and available here only because the
system is inter-country.

---

## 6. Parameterising the schedule

The construction in §3 accommodates any schedule $\tau^{rs}_{i}$. Four cases are worth
distinguishing because they correspond to different policy questions and impose
different structure on $\boldsymbol{\Theta}$.

**Uniform.** $\tau^{rs}_{i}=\tau$: a single across-the-board rate, reducing to the
import-intensity result of §5.2. One parameter.

**Sectoral.** $\tau^{rs}_{i}=\tau_{i}$: protection targeted at particular commodities,
independent of origin. $\boldsymbol{\Theta}$ becomes constant along its row blocks.

**Bilateral.** $\tau^{rs}_{i}$ with full generality: the configuration needed to
represent a trade dispute between named regions, or a preferential agreement, in which
a subset of origin–destination pairs carries elevated or zero rates. Retaliation is
representable as a static configuration — region $s$ tariffs $r$ and $r$ tariffs $s$ —
though the dynamics by which retaliation escalates are not.

**Carbon border adjustment.** The case of most interest here, because it makes the
tariff endogenous to variables the model already carries. A border adjustment seeks to
equalise the carbon cost borne by domestic and imported goods, which sets the rate to
the product of the carbon-price gap and the carbon content of the import:

$$\tau^{rs}_{i} \;=\; \big(\mathrm{XCE}^{s}-\mathrm{XCE}^{r}\big)_{+}\cdot e^{r}_{i}\cdot 10^{-6},$$

with $(\cdot)_{+}=\max(\cdot,0)$ ensuring the adjustment applies only where the
importer's carbon price exceeds the exporter's, and $e^{r}_{i}$ the carbon content per
unit output of the exporting sector. Two readings of $e$ are available and the choice
is substantive:

$$e^{r}_{i}=\mathrm{CI}^{r}_{i} \quad\text{(direct, Scope 1 only)},
\qquad
e^{r}_{i}=\big(\mathcal{L}^{\!\top}\mathbf{CI}\big)^{r}_{i} \quad\text{(embodied, all upstream rounds)} .$$

The second uses the Leontief inverse to accumulate emissions over the entire upstream
supply chain and is the economically correct notion of the carbon content of a traded
good; it is also, notably, already computable from objects the model possesses. The
first corresponds to the narrower scope of border adjustments as actually legislated.

Substituting either into (1) gives the border-adjustment cost vector

$$ct^{\,\mathrm{CBAM}}_{(s,j)} \;=\; 10^{-6}\sum_{r\neq s}\sum_{i}\big(\mathrm{XCE}^{s}-\mathrm{XCE}^{r}\big)_{+} e^{r}_{i}\,A^{rs}_{ij},$$

which is scenario-dependent through the carbon prices and requires no data the model
does not already hold. The construction also inherits the correct comparative statics:
under a scenario with a globally uniform carbon price the gap vanishes and the border
adjustment switches itself off, while under a fragmented scenario it grows with the
degree of policy divergence.

---

## 7. Computational form

The extension adds no inversion. $\mathbf{M}(\phi)$ is formed once, as before, and the
additional work is the elementwise product and column sum of (2) followed by a
matrix–vector product — $O(N^{2})$ against the $O(N^{3})$ of the inversion already
performed. For a schedule that varies by scenario or horizon, as a border adjustment
does, only $\mathbf{ct}^{\,\mathrm{tariff}}$ need be rebuilt; $\mathbf{M}(\phi)$ is
reused unchanged.

---

## 8. Assumptions and limitations

**No substitution, and therefore no trade diversion.** This is the binding limitation
and it follows directly from holding $\mathbf{A}$ fixed. A tariff in this framework
raises the cost of imported inputs but does not change *which* inputs are purchased or
from whom. In reality the principal effect of a tariff is precisely that reallocation —
buyers switch to untaxed origins or domestic substitutes — so the model captures the
cost-push consequence exactly and the reallocation consequence not at all. Two
corollaries follow: the computed cost is an **upper bound**, since real buyers would
mitigate by switching; and the exporter's loss, which operates through lost volume, is
**identically zero** rather than merely small.

**No demand response.** Final demand $\mathbf{y}$ is fixed, so higher prices do not
reduce quantities. The framework computes what the tariff costs at unchanged volumes,
not what volumes result.

**Tariff revenue is not recycled.** The duty is a cost to the purchasing sector and
disappears from the system, whereas in reality it accrues to the importing government
and is spent or rebated. Modelling that return flow requires a fiscal closure the
input–output system does not currently have, and its absence overstates the net
domestic burden of a tariff.

**Ad valorem only.** Specific duties, levied per physical unit rather than per unit of
value, would require a quantity normalisation the value table does not supply. Tariff
rate quotas and other non-linear schedules are likewise outside the linear form.

**Valuation base mismatch.** The coefficients $A^{rs}_{ij}$ are derived from flows
recorded at basic prices, whereas customs duties are assessed on transaction value
inclusive of freight and insurance. Applying $\tau$ to $A$ therefore understates the
duty base by the trade and transport margin.

**Non-tariff measures are not represented.** Quotas, standards and licensing operate
principally on quantities and admit no ad-valorem equivalent within this framework
without an auxiliary estimate.

---

## 9. Summary

A tariff enters the model as a per-unit-of-output cost vector formed by weighting the
off-diagonal blocks of the technical coefficient matrix by the tariff schedule,

$$ct^{\,\mathrm{tariff}}_{(s,j)} = \sum_{r\neq s}\sum_{i}\tau^{rs}_{i}A^{rs}_{ij},
\qquad
\Delta\mathbf{p} = \big(\mathbf{I}-\mathbf{A}^{\!\top}\big)^{-1}\big(\mathbf{ct}^{\,\mathrm{carbon}}+\mathbf{ct}^{\,\mathrm{tariff}}\big),$$

after which every existing stage of the model applies unchanged. The two shocks are
dimensionally commensurate, exactly additive, and structurally distinct: carbon
exposure scales with emissions intensity and tariff exposure with imported-input
intensity, so the same aggregate cost falls on different sectors. A carbon border
adjustment is the special case in which the schedule is generated endogenously from the
carbon-price differential and the embodied carbon content of trade, both of which the
model already computes.

What the formulation delivers is the exact cost-push incidence of a given tariff
configuration, including the indirect exposure of sectors that import nothing directly.
What it cannot deliver is any reallocation of trade, which is the effect a tariff is
usually imposed to achieve.
