# Region Selection and Data Aggregation

## 1. Why the region set is a modelling decision

A multi-regional stress test must decide how finely to resolve the world. The
decision is usually made implicitly — a set of "important" economies is asserted
and the rest swept into a residual — but it determines the results directly.
Inside an aggregate, every member necessarily shares one carbon price, one carbon
intensity, one vulnerability score, one currency and one scenario zone. Promoting
an economy out of a block does not buy *size*; it buys **resolution**.

That reframing sets the objective. The question is not *"which economies are
largest"* but

> **which economies, if left inside a block, would make that block misrepresent
> them?**

Aggregation bias arises from within-group heterogeneity, not from group size: a
block of sixty near-identical economies aggregates almost exactly, while a block
of three wildly different ones does not. The objective has a useful corollary —
it makes robustness of the residual the *same* criterion as the selection itself,
rather than a separate condition checked afterwards.

This chapter sets out the data (§2), the aggregation procedure (§3), the linkage
measures (§4), the two-stage selection method (§5–§6), the resulting region set
(§7), and what the exercise does and does not establish (§8–§9).

Implementation: [`tools/select_regions.py`](../tools/select_regions.py) (stage 1)
and [`tools/select_regions_threshold.py`](../tools/select_regions_threshold.py)
(stage 2).

---

## 2. Data

Three datasets are required: a global input–output table to measure economic
linkage, an emissions inventory to measure carbon linkage, and a vulnerability
index to measure exposure to physical risk.

### 2.1 OECD Inter-Country Input–Output tables (ICIO)

The 2025 edition, reference year **2022**, in the Small (SML) industry
classification.

| | |
|---|--:|
| Economies | 81 (80 named + one unallocated residual) |
| Industries per economy (ISIC Rev. 4) | 50 |
| Economy–industry pairs | 4,050 |
| Final-demand columns (6 categories × 81) | 486 |
| World gross output | \$199.69 tn |
| Intermediate flows $\mathbf{Z}$ | \$103.41 tn |

The ICIO records, for every pair of economy–industries, the value of goods and
services flowing from one to the other, plus final demand by category (household,
non-profit, government, fixed capital, inventories, direct purchases abroad). It
is the only dataset that captures **indirect** supply chains: if the EU buys a
German car containing Chinese steel smelted with Australian coal, a bilateral
trade statistic sees only the German transaction, whereas the Leontief inverse
attributes output to all three.

2022 is the latest year available and is also the base year of the wider model,
so the input–output structure, the emissions inventory and the economic
accounting all refer to the same world.

### 2.2 OECD Greenhouse Gas Footprint (GHGFP)

The 2025 edition, reference year 2022, **Scope 1** (production-based, direct
emissions from the producing industry).

| | |
|---|--:|
| Observations | 20,250 |
| Scopes published | S1, S2, S3D, S3U, total |
| Economies | 81 |
| Global Scope-1 total | 44,231 Mt CO₂e |

The five largest emitters are China (13,501 Mt), the United States (5,352 Mt),
the ICIO residual (4,304 Mt), India (3,618 Mt) and Russia (1,913 Mt).

**A units caveat.** The unit field is labelled `T_CO2E`, which reads as tonnes,
but the magnitudes are **millions of tonnes**: China's 13,501 is 13.5 Gt CO₂e,
consistent with published inventories. Taking the label literally would
understate every emissions figure by a factor of 10⁶. Carbon intensities are
therefore computed as

$$\mathrm{CI}_c \;=\; \frac{E_c\ [\text{Mt CO}_2\text{e}]}{x_c\ [\$\text{m}]}\times 10^{6}
\qquad [\text{t CO}_2\text{e}/\$\text{m}],$$

which places the EU27 at 88 t/\$m and India at 574 t/\$m — magnitudes that agree
with independent estimates and confirm the interpretation.

Scope 1 is the correct choice here because the carbon charge in the transition
channel is levied on a sector's own production. Scope 2 and 3 would double-count
emissions that the Leontief inverse already propagates.

### 2.3 ND-GAIN vulnerability index

The Notre Dame Global Adaptation Initiative index supplies the cross-economy
scaling of physical vulnerability: 192 economies, 1995–2024, of which the 2024
vector is used. Values run from 0.263 to 0.655 with a median of 0.450. Higher is
more vulnerable.

### 2.4 Reconciling the three sources

The datasets do not use identical economy codes. The ICIO calls its unallocated
residual `ROW`; the GHG footprint calls the same entity `WXD`. Joining on code
alone silently leaves the residual with no emissions, whereupon it falls back to
a median carbon intensity — a material error, since `WXD` is the **third largest
Scope-1 total in the file**. Correcting the alias raises the residual's carbon
linkage from 2.6 % to 9.2 % and changes its rank among regions from sixth to
second. Economies present in the ICIO but absent from ND-GAIN (chiefly small
financial centres) are assigned the median vulnerability, which affects the
clustering attributes but not the linkage measures.

---

## 3. Aggregation

### 3.1 The procedure and why it is valid

A region is a set of economies. Aggregation is **plain summation of flows**: for
regions $R$ and $S$ and industries $i,j$,

$$Z_{(R,i),(S,j)} \;=\; \sum_{c \in R}\ \sum_{k \in S} Z_{(c,i),(k,j)},
\qquad
x_{(R,i)} \;=\; \sum_{c \in R} x_{(c,i)} .$$

This is exact for current-price input–output tables because the entries are
values in a common currency, and value is additive. No deflation, weighting or
re-balancing is required, and the world total is preserved identically — a
property asserted as a build-time check in
[`tools/build_multiregion.py`](../tools/build_multiregion.py).

Two consequences deserve emphasis. First, intra-regional trade becomes a diagonal
block: once Germany and France are inside EU27, Franco-German trade is domestic
supply and no longer visible as trade. Second, the technical coefficients of the
aggregate are **output-weighted averages** of the members',

$$A_{(R,i),(S,j)} \;=\; \frac{\sum_{c\in R}\sum_{k\in S} Z_{(c,i),(k,j)}}
{\sum_{k \in S} x_{(k,j)}},$$

so a block's carbon intensity is the output-weighted mean of its members'. This
is precisely the mechanism by which aggregation loses information, and it is what
the selection criterion is designed to control.

### 3.2 The aggregates used

| Region | Members | Basis |
|---|---|---|
| **EU27** | Austria, Belgium, Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden | Customs union, single currency for 20 of the 27, one carbon price (EU ETS), one CBAM. The base region. |
| **MEA** | Saudi Arabia, United Arab Emirates, Israel, Jordan | Hydrocarbon supply; essentially no carbon pricing |
| **AFR** | South Africa, Egypt, Morocco, Tunisia, Nigeria, Senegal, Côte d'Ivoire, Cameroon, DR Congo, Angola, São Tomé | Resource supply; the most climate-vulnerable partners |
| **LAM** | Argentina, Brazil, Chile, Colombia, Costa Rica, Mexico, Peru | Agricultural and mineral supply, broadly similar intensity |
| **RASIA** | Korea, Singapore, Chinese Taipei, Hong Kong, Malaysia, Thailand, Viet Nam, Philippines, Bangladesh, Brunei | The NGFS Asia zone after cleaning — **derived**, see §6.2 |
| **ROW** | Australia, Belarus, Canada, Iceland, Indonesia, Japan, Kazakhstan, Cambodia, Laos, Myanmar, Norway, New Zealand, Pakistan, Ukraine, ICIO residual | Closure — the cleaned-out and unpromoted remainder |

The first four are imposed on policy and geographic grounds. RASIA and ROW are
not chosen at all: they are what §6.2–6.3 return.

Chile sits inside LAM. An earlier design carved it out ("Latin America
ex-Chile") because Chile was modelled separately for currency coverage; the
threshold rule does not select it — 0.05 % economic and 0.07 % carbon linkage,
last on both measures — so the carve-out serves no purpose and would strand a
single economy in a zone group of its own.

EU27 is treated as a single region because the model's own policy variables are
defined at that level — the carbon price is the ETS price, and CBAM is an EU
instrument. Modelling members separately would require a within-EU carbon-price
differential that does not exist.

### 3.3 What aggregation costs

The cost of a block is the heterogeneity it conceals. Measured as the ratio of
the highest to the lowest member carbon intensity:

| Block | *n* | median CI (t/\$m) | min | max | max/min |
|---|--:|--:|--:|--:|--:|
| LAM | 7 | 279 | 134 | 314 | **2.3×** |
| AFR | 11 | 461 | 195 | 723 | 3.7× |
| RASIA | 10 | 242 | 85 | 341 | 4.0× |
| MEA | 4 | 291 | 81 | 330 | 4.1× |
| EU27 | 27 | 102 | 26 | 307 | 11.8× |
| ROW | 15 | 587 | 69 | 1,268 | **18.3×** |

Every block that carries interpreted results is tight. LAM is nearly homogeneous,
so collapsing it costs almost nothing; RASIA reaches 4.0× only because it has
been cleaned (§6.2), against 15.0× for the raw NGFS Asia zone. EU27's 11.8× is
tolerated for the policy reason above, not because it is small.

**ROW is the exception, deliberately.** At 18.3× it pairs Norway (69 t/\$m) with
Cambodia (1,268 t/\$m), and that is the price of the design: cleaning improves
the blocks that get *reported* by pushing their outliers into the block that does
not. ROW's outputs are never interpreted, so the heterogeneity is placed where it
does least harm — but it is real, and it means ROW should be read as a closure
term rather than as a region.

---

## 4. Measuring linkage: the EU final-demand footprint

The model is EU-centred, so an economy matters in proportion to what it supplies
the EU — not its global weight. Solving the Leontief system with EU final demand
alone,

$$\mathbf{x}_{\mathrm{EU}} \;=\; (\mathbf{I}-\mathbf{A})^{-1}\,\mathbf{f}_{\mathrm{EU}},$$

gives the gross output required *everywhere in the world* to satisfy it. EU final
demand of \$15.38 tn pulls a footprint of **\$32.16 tn** of global gross output,
of which 81.00 % is inside the EU itself.

In implementation this is solved rather than inverted — `np.linalg.solve` on a
4,050 × 4,050 system — since the inverse is never needed in its own right.

Two measures follow:

| | definition |
|---|---|
| **Economic linkage** $\ell^{\text{econ}}_c$ | economy *c*'s share of the \$32.16 tn footprint |
| **Carbon linkage** $\ell^{\text{carb}}_c$ | the same, weighted by carbon intensity — i.e. emissions embodied in EU final demand (consumption-based accounting) |

$$\ell^{\text{econ}}_c = \frac{\sum_{i} x_{\mathrm{EU},(c,i)}}{\sum_{k,i} x_{\mathrm{EU},(k,i)}},
\qquad
\ell^{\text{carb}}_c = \frac{\mathrm{CI}_c \sum_{i} x_{\mathrm{EU},(c,i)}}
{\sum_{k} \mathrm{CI}_k \sum_{i} x_{\mathrm{EU},(k,i)}}.$$

Both are carried throughout and neither is collapsed into a weighted scalar,
because **they disagree, and the disagreement is informative**. Switzerland ranks
fourth among non-EU economies on economic linkage and near-last on carbon
(CI = 20 t/\$m); Kazakhstan ranks twentieth on economic linkage and sixth on
carbon (CI = 884 t/\$m); India is sixth economically and third on carbon. A
single-objective selection would systematically discard one group or the other.

---

## 5. Stage 1: greedy agglomerative merging

The first stage answers *"which economies deserve their own region"* without a
prior list, by merging the 81 economies bottom-up and recording the order.

**Attributes.** Each economy carries two standardised quantities — the things a
block would blur and that drive the model's channels:

| attribute | what it protects |
|---|---|
| log carbon intensity | the transition charge $ct = \mathrm{CI}\times\mathrm{XCE}$ |
| ND-GAIN vulnerability | the physical damage allocation |

Both are standardised to unit variance so neither dominates the distance. The
third quantity a region must share — the carbon *price* — is deliberately absent
here and handled structurally instead: §6.2 partitions the residual along NGFS R5
zones, which is the resolution at which prices are published, so price coherence
is obtained by construction rather than by putting a proxy into a distance
metric.

**Merge cost.** Ward's criterion, weighted by economic linkage:

$$\mathrm{cost}(G,H) \;=\; \frac{w_G\,w_H}{w_G+w_H}\,
\bigl\lVert \bar{X}_G - \bar{X}_H \bigr\rVert^2,
\qquad w_G = \sum_{c\in G}\ell^{\text{econ}}_c .$$

Merging two large, dissimilar, EU-relevant groups is expensive; merging two small
similar ones is nearly free. At each step the algorithm greedily merges the
cheapest available pair, EU27 being pre-merged and frozen as the base region.

The choice of an agglomerative scheme over forward greedy selection matters for
one reason: **there is no residual bucket.** ROW is not "everything left over" —
it is another cluster whose heterogeneity is measured on the same scale as
everyone else's, so the residual is disciplined by the objective rather than by a
separate constraint.

**What stage 1 establishes.** Run freely, the rules are first satisfied at 24
non-EU groups. The result confirms seven regions of the existing manual selection
unprompted (China, UK, Russia, Japan, Norway, Türkiye, Kazakhstan), and promotes
three the manual selection had buried — **Switzerland, Chinese Taipei and
Viet Nam** — each of which outranks regions already modelled individually. That
recovery is the main validation of the exercise: the manual set was not
arbitrary, but it was incomplete.

**What stage 1 cannot establish.** A cut point. The merge-cost curve rises
smoothly through the whole relevant range:

| groups remaining | 15 | 12 | 10 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| merge cost (000s) | 14 | 23 | 55 | 90 | 150 | 394 | 473 | 949 | 1,089 | 6,155 |

The sharp increases are all at the top of the tree ($k \le 7$), where the
algorithm is forced to fuse the advanced low-carbon bloc with the developing
high-carbon one. **Between 12 and 25 regions there is no knee.** The data does
not single out a number in that range, and manufacturing a threshold would be
dishonest. The cut is a judgement about modelling effort and data availability,
and is made explicitly in stage 2.

---

## 6. Stage 2: the linkage-threshold rule

The cut applied is a rule stated in the two linkage measures directly:

> **Keep** a candidate region if it is among the **top 10 by economic linkage**,
> **or** its economic linkage exceeds **1 %**, **or** its carbon linkage exceeds
> **1 %**. All remaining economies fall into the residual.

The two clauses do different work. The top-10 clause captures the EU's principal
trading partners. The 1 % carbon clause re-admits economies that are *small
suppliers but carbon-heavy* — precisely the population a climate stress test must
not bury, and precisely the population a size ranking discards. Applied to the
candidate set, it re-admits **Africa** (2.06 % carbon on 0.54 % economic linkage)
and **Türkiye** (1.10 % on 0.50 %).

Ranked candidates, with the cut shown:

| rank | region | econ % | carb % | | rank | region | econ % | carb % |
|--:|---|--:|--:|---|--:|---|--:|--:|
| 1 | EU27 | 81.00 | 58.73 | | 12 | **AFR** | 0.54 | **2.06** ✓ |
| 2 | CHN | 4.49 | 11.11 | | 13 | NOR | 0.52 | 0.30 |
| 3 | USA | 2.68 | 2.62 | | 14 | KOR | 0.50 | 0.60 |
| 4 | *residual* | 2.13 | 9.19 | | 15 | **TUR** | 0.50 | **1.10** ✓ |
| 5 | GBR | 1.60 | 0.80 | | 16 | SGP | 0.31 | 0.26 |
| 6 | CHE | 1.00 | 0.16 | | 17 | CAN | 0.26 | 0.29 |
| 7 | RUS | 0.97 | 3.75 | | 18 | TWN | 0.26 | 0.52 |
| 8 | LAM | 0.69 | 1.57 | | 19 | VNM | 0.25 | 0.66 |
| 9 | MEA | 0.64 | 1.27 | | 20 | AUS | 0.19 | 0.23 |
| 10 | IND | 0.59 | 2.80 | | 21 | IDN | 0.14 | 0.46 |
| — | *cut* | | | | 22 | KAZ | 0.13 | **0.93** |
| 11 | JPN | 0.59 | 0.59 | | | | | |

Kazakhstan at 0.93 % carbon is the closest miss, and is the region most sensitive
to where the threshold is placed: a 0.9 % rule would admit it.

Note that the residual occupies rank 4 in this ranking, so the top-10 clause
yields nine named regions and the carbon clause adds two, giving eleven.

### 6.1 The residual dominates, so something must come out of it

Applying the rule alone produces twelve regions but **breaks the requirement that
the residual must not dominate**. Absorbing the demoted economies leaves a
residual at **5.29 % economic and 14.02 % carbon linkage** — larger than China on
*both* measures. Results attributed to such a region would not be interpretable.

The cap it must respect is not a tuning parameter: it is the linkage of the
largest single-economy region, which the data says is China on both measures
simultaneously ($\bar{\ell}^{\text{econ}} = 4.49\,\%$,
$\bar{\ell}^{\text{carb}} = 11.11\,\%$).

Promoting individual economies back is a poor way to fix it. Taking them in
descending order of economic linkage, the constraint is not satisfied until
**nineteen** regions — Japan, Norway, Korea, Singapore, Canada, Chinese Taipei
and Viet Nam must all return — by which point the cut has been undone. The reason
is that carbon binds harder than economics, and the ICIO's own unallocated block
carries 6.73 % of carbon linkage on its own and can never be promoted, because it
is not an economy.

### 6.2 Splitting by carbon-price zone, then cleaning

What comes out should be a *block*, not a sequence of individual economies, and
the natural blocks are already in the data. Scenario carbon prices are published
at NGFS R5 resolution, so the residual is split by R5 zone:

| zone | *n* | econ % | carb % | CI (t/\$m) | internal spread |
|---|--:|--:|--:|--:|--:|
| ASIA | 15 | 2.03 | 4.16 | 248 | **15.0×** |
| OECD | 6 | 1.61 | 1.45 | 109 | 2.1× |
| World *(unallocated)* | 1 | 1.38 | 6.73 | 592 | — |
| REF | 3 | 0.28 | 1.68 | 726 | 1.5× |

This partition is not ours. It is the resolution at which the scenario data is
published, which has a practical consequence: each group takes **exactly one
carbon-price path**, with no blending and no fallback to a world aggregate.

One zone is unfit as it stands. ASIA spans **15×** in carbon intensity, holding
Korea (85 t/\$m) and Cambodia (1,268 t/\$m) in the same block — precisely the
misrepresentation §1 defines the exercise against. So each zone is **cleaned**: a
member is dropped if its carbon intensity exceeds $k$ times its own zone's
linkage-weighted average,

$$\text{drop } c \in Z \iff \mathrm{CI}_c > k\,\overline{\mathrm{CI}}_Z,
\qquad k = 1.5 .$$

Two properties of this rule matter.

**It is relative, not absolute.** REF (Belarus, Kazakhstan, Ukraine) is uniformly
carbon-heavy — 726 t/\$m at a 1.5× spread — and is perfectly coherent, so it
keeps every member. An absolute intensity threshold cannot distinguish "heavy"
from "heterogeneous" and would empty REF for no reason while leaving ASIA's
internal range untouched.

**Dropped economies fall into ROW.** They do not form a group of their own. The
purpose of cleaning is to make the geographic blocks *worth selecting*, not to
manufacture a rival that would take the first promotion — an earlier version
pooled them into a high-intensity group which then competed with ASIA for
promotion on a 0.04 pp margin, making the outcome turn on noise.

At $k = 1.5$ five economies are dropped — Indonesia, Cambodia, Laos, Myanmar,
Pakistan, together 0.21 % of economic and 0.95 % of carbon linkage — and ASIA's
internal spread falls from **15.0× to 4.0×** while its linkage barely moves.

### 6.3 Promotion

The cleaned zones are then promoted out of the residual, largest first by
economic linkage, until the residual passes:

| | ROW econ % | ROW carb % | |
|---|--:|--:|---|
| all zones inside ROW | 5.29 | 14.02 | ✗ carbon > 11.11 |
| promote **ASIA** (1.82 % econ) | 3.47 | 10.80 | ✓ **passes** |

One promotion suffices, giving **13 regions**. The number of promotions is an
output of the constraint, not a chosen quantity.

The result is stable in $k$:

| $k$ | dropped | promoted | regions |
|--:|--:|---|--:|
| 1.25 | 11 | ROECD, RWorld | 14 |
| **1.50** | **5** | **RASIA** | **13** |
| 1.75 | 4 | RASIA | 13 |
| 2.00 | 4 | RASIA | 13 |
| 2.50 | 4 | RASIA | 13 |
| 3.00 | 4 | RASIA | 13 |

Every value from 1.5 upward gives the same answer. Only $k \le 1.4$ breaks it, by
over-cleaning ASIA until OECD overtakes it. $k$ is therefore a parameter the
result is insensitive to across its plausible range, which is the most that can
be asked of a threshold that is asserted rather than estimated.

---

## 7. The selected region set

**Thirteen regions**: EU27 as base, eleven named regions, one closure. Shares are
of the EU's \$32.16 tn final-demand footprint.

| # | Region | Full name | econ % | carb % | CI (t/\$m) | Basis for inclusion |
|--:|---|---|--:|--:|--:|---|
| 1 | **EU27** | European Union (27) | 81.00 | 58.73 | 88 | Base region and numéraire; EU demand is met overwhelmingly from inside the single market |
| 2 | **CHN** | China | 4.49 | **11.11** | 299 | Largest external supplier on both measures; carbon linkage 2.5× its economic weight. Sets the dominance cap |
| 3 | **ROW** | Rest of World (15) | 3.47 | 10.80 | 376 | Closure — cleaned-out and unpromoted remainder, incl. the ICIO's unallocated block |
| 4 | **USA** | United States | 2.68 | 2.62 | 118 | Second-largest external supplier; tariff counterparty; reserve currency |
| 5 | **RASIA** | Rest of Asia (10) | 1.82 | 3.22 | 214 | Derived (§6.2) — the NGFS Asia zone, cleaned; exporting Asia on one carbon-price path |
| 6 | **GBR** | United Kingdom | 1.60 | 0.80 | 61 | Largest single-country services supplier; closest integrated non-member |
| 7 | **CHE** | Switzerland | 1.00 | 0.16 | 20 | 4th-largest non-EU economic linkage; pharmaceuticals and precision goods |
| 8 | **RUS** | Russian Federation | 0.97 | **3.75** | 467 | Carbon linkage nearly 4× economic weight |
| 9 | **LAM** | Latin America (7) | 0.69 | 1.57 | 274 | Agricultural and mineral supply; the most homogeneous block |
| 10 | **MEA** | Middle East (4) | 0.64 | 1.27 | 240 | Hydrocarbon channel; essentially no carbon pricing |
| 11 | **IND** | India | 0.59 | **2.80** | 574 | Third on carbon linkage with zero carbon-pricing coverage |
| 12 | **AFR** | Africa (11) | 0.54 | **2.06** | 462 | *Admitted on carbon.* Resource supply; most climate-vulnerable partners |
| 13 | **TUR** | Türkiye | 0.50 | **1.10** | 264 | *Admitted on carbon.* Manufacturing satellite under customs union; unpriced; prime CBAM exposure |

**Constraint check.** The largest named region is China at 4.49 % economic and
11.11 % carbon. ROW reaches 3.47 % / 10.80 %, below both — **satisfied**, and by
0.30 pp on the binding measure. The margin is thin because 6.73 pp of ROW's
carbon linkage is the ICIO's unallocated block, which cannot be promoted or
decomposed by any method.

**Coverage.** Named regions carry 96.5 % of economic and 89.2 % of carbon
linkage.

### 7.1 Discussion

**The carbon clause changes the set, not just its size.** Ranked on economic
linkage alone, Africa and Türkiye would sit 12th and 15th and be discarded.
Ranked on the ratio of carbon to economic linkage, the ordering is almost
reversed:

| | IND | RUS | AFR | ROW | CHN | LAM | TUR | MEA | RASIA | USA | EU27 | GBR | CHE |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| carb % ÷ econ % | **4.75** | 3.86 | 3.82 | 3.11 | 2.48 | 2.26 | 2.18 | 1.99 | 1.77 | 0.98 | 0.73 | 0.50 | **0.16** |

India's embodied emissions in EU demand are nearly five times its trade weight;
Switzerland's are a sixth of its. A stress test resolved only on trade weight
would model the EU's carbon exposure with the wrong regions. This spread —
a factor of thirty from top to bottom — is the substantive justification for
carrying two measures.

**What is lost.** Eleven regions of the earlier 23-region design are demoted:
Japan, Norway, Korea, Singapore, Canada, Chinese Taipei, Viet Nam, Australia,
Indonesia, Kazakhstan and Chile. Each falls below both thresholds, so each
demotion is consistent with the stated rule. Three are worth recording as
knowingly accepted losses:

* **Kazakhstan** (0.93 % carbon, CI 884 t/\$m) is the highest-intensity economy
  in the set and misses by 0.07 pp.
* **Viet Nam** (0.66 % carbon) is the principal destination of trade diverted
  from China, and so the economy most likely to alter EU sourcing over the
  horizon — relevant to the tariff analysis specifically.
* **Chinese Taipei** (0.52 % carbon) is a semiconductor chokepoint whose
  supply-chain dependency has no substitute at any price.

None can be defended on linkage; each could be defended on a different criterion,
and if any are restored it should be on that stated basis rather than by moving
the threshold to accommodate them.

**Consequences for the FX deliverable.** The region set determines the FX
cross-section, because a currency exists in the model only if its economy is a
region. The thirteen-region set supports **six** analytical currencies — USD,
CNY, GBP, CHF, INR, TRY — against fourteen previously. JPY, CAD, NOK, IDR, CLP,
AUD, SGD, KRW and KZT are lost; CHF is gained. This is a direct and substantial
narrowing of the primary deliverable, and it follows from the linkage rule rather
than from any judgement about FX. It is recorded here because the trade-off
between parsimony and FX coverage is a decision that belongs at the design level,
not one the selection algorithm should be allowed to make silently.

---

## 8. Limitations

**Scenario zones are not applied carbon prices.** §6.2 partitions on the price the
*scenario* assigns a region's R5 zone, not the price the economy actually levies
today, because no per-economy applied-price series exists for all 81. The
distinction matters: Switzerland was missed by the manual selection precisely
because it sat in a residual assumed to price carbon at \$2/t while it has levied
CHF 120/t (≈ \$133) since 2022, a roughly 65-fold error. Zone membership would not
have caught that.

**The cleaning threshold is asserted.** $k = 1.5$ is a judgement, not an estimate.
Its defence is insensitivity rather than derivation: every value in [1.5, 3.0]
returns the same thirteen regions and the same promotion, and only $k \le 1.4$
changes the answer. That is weaker than deriving it, and is reported as such.

**Ward's weighting favours absorption.** In stage 1 the harmonic term
$w_Gw_H/(w_G+w_H)$ makes attaching a tiny economy to a large one nearly free,
which is why Iceland lands on the United States and India lands in a block with
Cambodia and Myanmar. Average or complete linkage would behave differently, and
the stability of the stage-1 ranking across linkage rules has not been tested.

**The cap is a hard constraint on a noisy quantity.** The dominance cap is set by
one economy's measured linkage. China's shares come from a single input–output
table, so a revision that moved them could change the number of promotions
discontinuously. The current margin is **0.30 pp** on the binding measure, which
is thin.

**The residual absorbs the heterogeneity.** Cleaning improves the blocks that
carry interpreted results by pushing their outliers into the one that does not.
ROW's 18.3× internal intensity spread is the direct cost of RASIA's 4.0×, and
anything attributed to ROW is correspondingly unreliable. This is a deliberate
placement of error, not its elimination.

**Structural attributes only, deliberately.** Selection never uses model outputs
— no FX moves, no GVA shocks. Choosing regions because they produce large results
and then reporting those results would be selection on the outcome.

**Feasibility is not modelled.** Equity betas, Okun coefficients and unemployment
series do not exist for every economy. A region the algorithm promotes but for
which every downstream parameter is a proxy may be worse than an aggregate.

**One base year.** The 2022 table fixes the trade structure. Linkages that have
moved since — the collapse in Russian pipeline gas, the diversion of Chinese
exports through Viet Nam and Mexico — are absent by construction, which matters
most for the economies sitting closest to the threshold.

---

## 9. Summary

Region selection is treated as a derived result rather than an assertion. Two
linkage measures are computed from the EU's final-demand footprint over the 2022
OECD ICIO, weighted by OECD Scope-1 emissions. A greedy agglomerative scheme
establishes which economies deserve resolution, and confirms seven of the manual
selections while promoting three that had been missed; it cannot supply a cut
point, because the merge-cost curve has no knee in the relevant range. An
explicit threshold rule — top ten by economic linkage, plus anything above 1 % on
either measure — supplies the cut, admitting Africa and Türkiye on carbon grounds
that a size ranking would have missed.

The residual this leaves would dominate both measures, so a block must come out
of it. The blocks are taken from the data rather than invented: the residual is
split along NGFS R5 zones, the resolution at which scenario carbon prices are
published, so each takes exactly one price path. One zone — Asia, spanning 15× in
carbon intensity — is unfit as it stands, and is cleaned by dropping members more
than 1.5× its own average intensity, which cuts its spread to 4.0× at a cost of
0.21 % of economic linkage. Cleaned zones are then promoted until the residual
passes the cap. One promotion suffices.

The result is thirteen regions covering **96.5 %** of the EU's economic and
**89.2 %** of its carbon footprint, with the residual below the largest single
economy on both measures. The number of promotions is an output of the
constraint, and the answer is unchanged for every cleaning threshold in
[1.5, 3.0].
