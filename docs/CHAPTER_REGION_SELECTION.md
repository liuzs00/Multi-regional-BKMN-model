# Region Selection and Data Aggregation

## 1. Introduction

Any multi-regional stress test must decide how finely to resolve the world economy.
The decision is normally made implicitly: a set of economies judged important is
asserted, and everything else is swept into a residual. Yet the choice determines the
results directly, because within an aggregate every member necessarily shares a single
carbon price, a single carbon intensity, a single vulnerability score, a single
currency and a single scenario zone. Promoting an economy out of a block therefore
buys not *size* but *resolution*.

That distinction reframes the objective. The relevant question is not which economies
are largest, but

> which economies, if left inside a block, would cause that block to misrepresent
> them?

Aggregation bias arises from within-group heterogeneity rather than from group size. A
block of sixty near-identical economies aggregates almost exactly; a block of three
dissimilar ones does not. The reframing has a useful corollary: it makes the robustness
of the residual the same criterion as the selection itself, rather than a separate
condition to be verified afterwards.

This chapter treats region selection as a quantity to be derived rather than assumed.
Two linkage measures are constructed from the European Union's final-demand footprint
over the 2022 OECD inter-country input–output table, weighted by production-based
emissions. A greedy agglomerative procedure establishes which economies merit
individual resolution; an explicit threshold rule supplies the cut that the clustering
cannot; and a constraint on the residual determines how many aggregate blocks must be
promoted out of it. The outcome is a set of thirteen regions, of which the final
composition — including the number of promotions — is an output of the procedure rather
than an input to it.

The chapter proceeds as follows. Section 2 describes the three data sources and their
reconciliation; Section 3 sets out the aggregation procedure and quantifies what it
costs; Section 4 defines the linkage measures; Sections 5 and 6 develop the two-stage
selection method; Section 7 presents the resulting region set; Section 8 tests whether
the residual closure is sufficient; and Sections 9 and 10 record the limitations and
conclusions.

Implementation is in `tools/select_regions.py` (stage one) and
`tools/select_regions_threshold.py` (stage two).

---

## 2. Data

Three datasets are required: a global input–output table with which to measure economic
linkage, an emissions inventory with which to weight it, and a vulnerability index with
which to characterise exposure to physical risk.

### 2.1 Inter-country input–output tables

The OECD Inter-Country Input–Output tables, 2025 edition, reference year 2022, in the
small (SML) industry classification.

| | |
|---|--:|
| Economies | 81 (80 named, one unallocated residual) |
| Industries per economy (ISIC Rev. 4) | 50 |
| Economy–industry pairs | 4,050 |
| Final-demand columns (6 categories × 81) | 486 |
| World gross output | \$199.69 tn |
| Intermediate flows $\mathbf{Z}$ | \$103.41 tn |

The tables record, for every ordered pair of economy–industries, the value of goods and
services flowing between them, together with final demand disaggregated by category.
Their distinguishing property is that they capture indirect supply chains. Where a
bilateral trade statistic records only the proximate transaction, the Leontief inverse
attributes output to every economy in the chain: if the European Union imports a German
vehicle containing Chinese steel smelted with Australian coal, all three origins are
represented.

The year 2022 is the most recent available and is also the base year of the wider
model, so that the input–output structure, the emissions inventory and the economic
accounting all describe the same world.

### 2.2 Greenhouse gas footprints

The OECD Greenhouse Gas Footprint database, 2025 edition, reference year 2022,
restricted to Scope 1 — production-based emissions attributed to the producing
industry.

| | |
|---|--:|
| Observations | 20,250 |
| Scopes published | S1, S2, S3D, S3U, total |
| Economies | 81 |
| Global Scope-1 total | 44,231 Mt CO₂e |

The five largest emitters are China (13,501 Mt), the United States (5,352 Mt), the
input–output residual (4,304 Mt), India (3,618 Mt) and Russia (1,913 Mt).

One feature of the source requires care. The unit field is labelled `T_CO2E`, which
reads as tonnes, but the magnitudes are millions of tonnes: China's 13,501 corresponds
to 13.5 Gt CO₂e, consistent with published national inventories. Interpreting the label
literally would understate every emissions figure by a factor of $10^{6}$. Carbon
intensities are therefore computed as

$$\mathrm{CI}_c \;=\; \frac{E_c\ [\text{Mt CO}_2\text{e}]}{x_c\ [\$\text{m}]}\times 10^{6}
\qquad [\text{t CO}_2\text{e}/\$\text{m}],$$

which places the EU27 at 88 t/\$m and India at 574 t/\$m, magnitudes consistent with
independent estimates and confirming the interpretation.

Scope 1 is the appropriate choice because the carbon charge in the transition channel
is levied on a sector's own production. Scope 2 and Scope 3 emissions would
double-count flows that the Leontief inverse already propagates.

### 2.3 Vulnerability index

The Notre Dame Global Adaptation Initiative (ND-GAIN) index supplies the cross-economy
scaling of physical vulnerability, covering 192 economies over 1995–2024. The 2022
vector is used, so that the vulnerability scale, the gross domestic product weights
used to aggregate it, the input–output table and the emissions inventory all describe
the same year. Values range from 0.263 to 0.655 with a median of 0.450, higher denoting
greater vulnerability.

Unlike the input–output and emissions data, which record flows and must therefore share
a base year for the accounting to hold, ND-GAIN measures exposure, sensitivity and
adaptive capacity — structural attributes that evolve over decades. The vintage is
consequently of little numerical importance, and the index enters the model as a
relative scale normalised to a world output-weighted mean of one, so that any common
drift in global vulnerability cancels and only the cross-section survives. Substituting
the 2024 vector moves the regional scales by at most 0.92 %, leaves them correlated at
0.9998, and changes the ordering only in that India and Africa exchange the two highest
places across a gap of 0.2 %. Propagated through the full model the effect is smaller
still: no regional physical damage moves by more than 0.007 percentage points and every
cross-sectional ordering is preserved exactly. The base year is nonetheless adopted in
preference to the latest release, because pinning the vintage removes a silent
dependence on which edition of the index happens to be in use.

### 2.4 Reconciling the sources

The three datasets do not share a common economy coding. The input–output tables label
the unallocated residual `ROW`, whereas the emissions database labels the same entity
`WXD`. Joining on code alone therefore leaves the residual with no emissions, whereupon
it inherits a median carbon intensity by fallback. The consequence is material, since
`WXD` is the third largest Scope-1 total in the file: correcting the alias raises the
residual's carbon linkage from 2.6 % to 9.2 % and moves its rank among candidate
regions from sixth to second. Economies present in the input–output tables but absent
from ND-GAIN, chiefly small financial centres, are assigned the median vulnerability;
this affects the clustering attributes of Section 5 but not the linkage measures of
Section 4.

---

## 3. Aggregation

### 3.1 Procedure and validity

A region is a set of economies, and aggregation proceeds by plain summation of flows.
For regions $R$ and $S$ and industries $i$ and $j$,

$$Z_{(R,i),(S,j)} \;=\; \sum_{c \in R}\ \sum_{k \in S} Z_{(c,i),(k,j)},
\qquad
x_{(R,i)} \;=\; \sum_{c \in R} x_{(c,i)} .$$

For current-price input–output tables this operation is exact rather than approximate,
because the entries are values denominated in a common currency and value is additive.
No deflation, weighting or rebalancing is required, and the world total is preserved
identically — a property asserted as a build-time check in
`tools/build_multiregion.py`.

Two consequences merit emphasis. First, intra-regional trade becomes a diagonal block:
once Germany and France are placed inside EU27, Franco-German trade is domestic supply
and is no longer visible as trade. Second, the technical coefficients of an aggregate
are output-weighted averages of those of its members,

$$A_{(R,i),(S,j)} \;=\; \frac{\sum_{c\in R}\sum_{k\in S} Z_{(c,i),(k,j)}}
{\sum_{k \in S} x_{(k,j)}},$$

so that a block's carbon intensity is the output-weighted mean of its members'
intensities. This averaging is precisely the mechanism by which aggregation destroys
information, and controlling it is what the selection criterion is designed to achieve.

### 3.2 The aggregate blocks

| Region | Members | Basis |
|---|---|---|
| EU27 | Austria, Belgium, Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden | Customs union, single currency for twenty of the twenty-seven, one carbon price, one border adjustment. The base region |
| MEA | Saudi Arabia, United Arab Emirates, Israel, Jordan | Hydrocarbon supply; effectively no carbon pricing |
| AFR | South Africa, Egypt, Morocco, Tunisia, Nigeria, Senegal, Côte d'Ivoire, Cameroon, DR Congo, Angola, São Tomé | Resource supply; the most climate-vulnerable partners |
| LAM | Argentina, Brazil, Chile, Colombia, Costa Rica, Mexico, Peru | Agricultural and mineral supply of broadly similar intensity |
| RASIA | Korea, Singapore, Chinese Taipei, Hong Kong, Malaysia, Thailand, Viet Nam, Philippines, Bangladesh, Brunei | The NGFS Asia zone after cleaning; derived in §6.2 |
| ROW | Australia, Belarus, Canada, Iceland, Indonesia, Japan, Kazakhstan, Cambodia, Laos, Myanmar, Norway, New Zealand, Pakistan, Ukraine, input–output residual | Closure: the cleaned-out and unpromoted remainder |

The first four blocks are imposed on policy and geographic grounds. RASIA and ROW are
not chosen at all; they are what the procedure of §6.2 and §6.3 returns.

Chile is retained within LAM. An earlier design carved it out as a separate
"Latin America ex-Chile" block because Chile was modelled individually for currency
coverage, but the threshold rule does not select it — 0.05 % economic and 0.07 % carbon
linkage, last on both measures — so the carve-out would serve no purpose and would
strand a single economy in a scenario zone of its own.

EU27 is treated as one region because the model's policy variables are themselves
defined at that level: the carbon price is the EU Emissions Trading System price and
the border adjustment is a Union instrument. Modelling members separately would require
an intra-Union carbon-price differential that does not exist.

### 3.3 The cost of aggregation

The cost of a block is the heterogeneity it conceals. Measured as the ratio of the
highest to the lowest member carbon intensity:

| Block | $n$ | median CI (t/\$m) | min | max | max/min |
|---|--:|--:|--:|--:|--:|
| LAM | 7 | 279 | 134 | 314 | 2.3× |
| AFR | 11 | 461 | 195 | 723 | 3.7× |
| RASIA | 10 | 242 | 85 | 341 | 4.0× |
| MEA | 4 | 291 | 81 | 330 | 4.1× |
| EU27 | 27 | 102 | 26 | 307 | 11.8× |
| ROW | 15 | 587 | 69 | 1,268 | 18.3× |

Every block whose results are interpreted is comparatively tight. LAM is nearly
homogeneous, so collapsing it costs almost nothing; RASIA reaches 4.0× only because it
has been cleaned, against 15.0× for the raw NGFS Asia zone. The EU27 figure of 11.8× is
tolerated for the policy reason given above rather than because it is small.

ROW is the deliberate exception. At 18.3× it pairs Norway (69 t/\$m) with Cambodia
(1,268 t/\$m), and this is the price of the design: cleaning improves the blocks whose
results are reported by displacing their outliers into the block whose results are not.
Because ROW's outputs are never interpreted, the heterogeneity is placed where it does
least damage. It is nonetheless real, and it means ROW should be read as a closure term
rather than as a region. Section 8 tests whether that placement is defensible.

---

## 4. Measuring linkage

The model is centred on the European Union, so an economy matters in proportion to what
it supplies to the Union rather than to its global weight. Solving the Leontief system
with EU final demand alone,

$$\mathbf{x}_{\mathrm{EU}} \;=\; (\mathbf{I}-\mathbf{A})^{-1}\,\mathbf{f}_{\mathrm{EU}},$$

yields the gross output required throughout the world to satisfy it. EU final demand of
\$15.38 tn generates a footprint of \$32.16 tn of global gross output, of which 81.00 %
lies within the Union itself. In implementation the system is solved rather than
inverted, since the inverse is never required in its own right.

Two measures follow. Economic linkage $\ell^{\text{econ}}_c$ is economy $c$'s share of
that footprint; carbon linkage $\ell^{\text{carb}}_c$ is the same quantity weighted by
carbon intensity, and therefore measures emissions embodied in EU final demand in the
consumption-based sense:

$$\ell^{\text{econ}}_c = \frac{\sum_{i} x_{\mathrm{EU},(c,i)}}{\sum_{k,i} x_{\mathrm{EU},(k,i)}},
\qquad
\ell^{\text{carb}}_c = \frac{\mathrm{CI}_c \sum_{i} x_{\mathrm{EU},(c,i)}}
{\sum_{k} \mathrm{CI}_k \sum_{i} x_{\mathrm{EU},(k,i)}}.$$

Both measures are carried throughout, and neither is collapsed into a weighted scalar,
because they disagree in an informative way. Switzerland ranks fourth among non-EU
economies on economic linkage and near last on carbon, its intensity being 20 t/\$m;
Kazakhstan ranks twentieth on economic linkage and sixth on carbon, at 884 t/\$m; India
is sixth economically and third on carbon. A single-objective selection would
systematically discard one of these groups.

---

## 5. Stage one: agglomerative clustering

The first stage addresses which economies merit individual resolution, without
reference to a prior list, by merging the 81 economies from the bottom up and recording
the order in which they combine.

Each economy carries two standardised attributes, chosen because they are the
quantities a block would blur and that drive the model's two channels: the logarithm of
carbon intensity, which governs the transition charge $ct = \mathrm{CI}\times
\mathrm{XCE}$, and the ND-GAIN score, which governs the allocation of physical damage.
Both are standardised to unit variance so that neither dominates the distance. The third
quantity a region must share, the carbon price itself, is deliberately excluded here and
handled structurally instead: §6.2 partitions the residual along NGFS R5 zones, which is
the resolution at which prices are published, so price coherence is obtained by
construction rather than by introducing a proxy into a distance metric.

Merges are costed by Ward's criterion, weighted by economic linkage:

$$\mathrm{cost}(G,H) \;=\; \frac{w_G\,w_H}{w_G+w_H}\,
\bigl\lVert \bar{X}_G - \bar{X}_H \bigr\rVert^2,
\qquad w_G = \sum_{c\in G}\ell^{\text{econ}}_c .$$

Merging two large, dissimilar and EU-relevant groups is expensive; merging two small
similar ones is nearly free. At each step the cheapest available pair is merged, with
EU27 pre-merged and frozen as the base region.

The choice of an agglomerative scheme in preference to forward greedy selection matters
for one reason: it admits no residual bucket. ROW is not defined as whatever remains,
but is another cluster whose heterogeneity is measured on the same scale as every
other, so that the residual is disciplined by the objective rather than by a separate
constraint imposed afterwards.

Run without a stopping rule, the procedure first satisfies the selection criteria at
twenty-four non-EU groups. It confirms seven regions of the existing manual selection
unprompted — China, the United Kingdom, Russia, Japan, Norway, Türkiye and Kazakhstan —
and promotes three that the manual selection had buried: Switzerland, Chinese Taipei and
Viet Nam, each of which outranks regions already modelled individually. This recovery is
the principal validation of the exercise, indicating that the manual set was not
arbitrary but was incomplete.

What the clustering cannot supply is a cut point. The merge-cost curve rises smoothly
across the entire relevant range:

| Groups remaining | 15 | 12 | 10 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Merge cost (000s) | 14 | 23 | 55 | 90 | 150 | 394 | 473 | 949 | 1,089 | 6,155 |

The sharp increases occur only at the top of the tree, for $k \le 7$, where the
algorithm is forced to fuse the advanced low-carbon bloc with the developing
high-carbon one. Between twelve and twenty-five regions there is no discernible knee.
The data do not single out a number in that range, and manufacturing a threshold would
misrepresent them. The cut is a judgement about modelling effort and data availability,
and is therefore made explicitly in stage two.

---

## 6. Stage two: the linkage-threshold rule

The cut is applied as a rule stated directly in the two linkage measures:

> Retain a candidate region if it lies among the ten largest by economic linkage, or if
> its economic linkage exceeds 1 %, or if its carbon linkage exceeds 1 %. All remaining
> economies fall into the residual.

The clauses perform different functions. The first captures the Union's principal
trading partners. The carbon clause readmits economies that are small suppliers but
carbon-heavy — precisely the population that a climate stress test must not bury, and
precisely the population that a size ranking discards. Applied to the candidate set it
readmits Africa, at 2.06 % carbon on 0.54 % economic linkage, and Türkiye, at 1.10 % on
0.50 %.

The ranked candidates, with the cut indicated:

| Rank | Region | Econ % | Carb % | | Rank | Region | Econ % | Carb % |
|--:|---|--:|--:|---|--:|---|--:|--:|
| 1 | EU27 | 81.00 | 58.73 | | 12 | AFR | 0.54 | 2.06 ✓ |
| 2 | CHN | 4.49 | 11.11 | | 13 | NOR | 0.52 | 0.30 |
| 3 | USA | 2.68 | 2.62 | | 14 | KOR | 0.50 | 0.60 |
| 4 | *residual* | 2.13 | 9.19 | | 15 | TUR | 0.50 | 1.10 ✓ |
| 5 | GBR | 1.60 | 0.80 | | 16 | SGP | 0.31 | 0.26 |
| 6 | CHE | 1.00 | 0.16 | | 17 | CAN | 0.26 | 0.29 |
| 7 | RUS | 0.97 | 3.75 | | 18 | TWN | 0.26 | 0.52 |
| 8 | LAM | 0.69 | 1.57 | | 19 | VNM | 0.25 | 0.66 |
| 9 | MEA | 0.64 | 1.27 | | 20 | AUS | 0.19 | 0.23 |
| 10 | IND | 0.59 | 2.80 | | 21 | IDN | 0.14 | 0.46 |
| — | *cut* | | | | 22 | KAZ | 0.13 | 0.93 |
| 11 | JPN | 0.59 | 0.59 | | | | | |

Kazakhstan, at 0.93 % carbon linkage, is the closest exclusion and the region most
sensitive to the placement of the threshold; a 0.9 % rule would admit it. Note also that
the residual occupies fourth place in this ranking, so the top-ten clause yields nine
named regions and the carbon clause adds two, giving eleven.

### 6.1 The residual constraint

Applying the rule alone produces twelve regions but violates the requirement that the
residual must not dominate. Absorbing the demoted economies leaves a residual at 5.29 %
economic and 14.02 % carbon linkage, larger than China on both measures
simultaneously. Results attributed to such a region would not be interpretable.

The bound the residual must respect is not a tuning parameter but the linkage of the
largest single-economy region, which the data identify as China on both measures at
once, with $\bar{\ell}^{\text{econ}} = 4.49\,\%$ and
$\bar{\ell}^{\text{carb}} = 11.11\,\%$.

Restoring individual economies is an unsatisfactory remedy. Taking them in descending
order of economic linkage, the constraint is not satisfied until nineteen regions are
retained — Japan, Norway, Korea, Singapore, Canada, Chinese Taipei and Viet Nam must all
return — by which point the cut has been undone. The reason is that the carbon measure
binds more tightly than the economic one, and that the input–output tables' own
unallocated block carries 6.73 % of carbon linkage in isolation and can never be
promoted, since it is not an economy.

### 6.2 Partition by carbon-price zone, and cleaning

What is removed from the residual should be a block rather than a sequence of
individual economies, and the natural blocks are already present in the data. Scenario
carbon prices are published at NGFS R5 resolution, so the residual is partitioned by R5
zone:

| Zone | $n$ | Econ % | Carb % | CI (t/\$m) | Internal spread |
|---|--:|--:|--:|--:|--:|
| ASIA | 15 | 2.03 | 4.16 | 248 | 15.0× |
| OECD | 6 | 1.61 | 1.45 | 109 | 2.1× |
| World *(unallocated)* | 1 | 1.38 | 6.73 | 592 | — |
| REF | 3 | 0.28 | 1.68 | 726 | 1.5× |

This partition is not of our construction. It is the resolution at which the scenario
data are published, which carries a practical consequence: each group takes exactly one
carbon-price path, with no blending and no fallback to a world aggregate.

One zone is unfit as it stands. ASIA spans 15× in carbon intensity, holding Korea
(85 t/\$m) and Cambodia (1,268 t/\$m) within a single block — precisely the
misrepresentation against which §1 defines the exercise. Each zone is therefore cleaned
by removing any member whose carbon intensity exceeds $k$ times its own zone's
linkage-weighted average:

$$\text{drop } c \in Z \iff \mathrm{CI}_c > k\,\overline{\mathrm{CI}}_Z,
\qquad k = 1.5 .$$

Two properties of this rule are worth noting. It is relative rather than absolute: the
REF zone (Belarus, Kazakhstan, Ukraine) is uniformly carbon-heavy at 726 t/\$m with a
spread of only 1.5×, and is therefore perfectly coherent, so it retains every member. An
absolute intensity threshold could not distinguish "heavy" from "heterogeneous", and
would empty REF for no reason while leaving ASIA's internal range untouched. And
economies removed by cleaning fall into ROW rather than forming a group of their own.
The purpose of cleaning is to render the geographic blocks worth selecting, not to
manufacture a rival that would then take the first promotion; an earlier version pooled
the removed economies into a high-intensity group, which competed with ASIA for
promotion on a margin of 0.04 pp and so made the outcome turn on noise.

At $k = 1.5$ five economies are removed — Indonesia, Cambodia, Laos, Myanmar and
Pakistan, together 0.21 % of economic and 0.95 % of carbon linkage — and ASIA's internal
spread falls from 15.0× to 4.0× while its linkage is barely affected.

### 6.3 Promotion

The cleaned zones are then promoted out of the residual, largest first by economic
linkage, until the residual satisfies the constraint:

| | ROW econ % | ROW carb % | |
|---|--:|--:|---|
| All zones inside ROW | 5.29 | 14.02 | ✗ carbon exceeds 11.11 |
| Promote ASIA (1.82 % econ) | 3.47 | 10.80 | ✓ satisfied |

A single promotion suffices, giving thirteen regions. The number of promotions is thus
an output of the constraint rather than a chosen quantity.

The result is stable in the cleaning threshold:

| $k$ | Dropped | Promoted | Regions |
|--:|--:|---|--:|
| 1.25 | 11 | ROECD, RWorld | 14 |
| 1.50 | 5 | RASIA | 13 |
| 1.75 | 4 | RASIA | 13 |
| 2.00 | 4 | RASIA | 13 |
| 2.50 | 4 | RASIA | 13 |
| 3.00 | 4 | RASIA | 13 |

Every value from 1.5 upwards returns the same answer; only $k \le 1.4$ alters it, by
over-cleaning ASIA until OECD overtakes it. The result is therefore insensitive to $k$
across its plausible range, which is the most that can be asked of a threshold that is
asserted rather than estimated.

---

## 7. The selected region set

The procedure returns thirteen regions: EU27 as base, eleven named regions and one
closure. Shares are of the Union's \$32.16 tn final-demand footprint.

| # | Region | Full name | Econ % | Carb % | CI (t/\$m) | Basis for inclusion |
|--:|---|---|--:|--:|--:|---|
| 1 | EU27 | European Union (27) | 81.00 | 58.73 | 88 | Base region and numéraire; EU demand is met overwhelmingly from within the single market |
| 2 | CHN | China | 4.49 | 11.11 | 299 | Largest external supplier on both measures; carbon linkage 2.5× its economic weight. Sets the dominance bound |
| 3 | ROW | Rest of World (15) | 3.47 | 10.80 | 376 | Closure: cleaned-out and unpromoted remainder, including the unallocated block |
| 4 | USA | United States | 2.68 | 2.62 | 118 | Second-largest external supplier; tariff counterparty; reserve currency |
| 5 | RASIA | Rest of Asia (10) | 1.82 | 3.22 | 214 | Derived in §6.2: the NGFS Asia zone, cleaned; exporting Asia on a single carbon-price path |
| 6 | GBR | United Kingdom | 1.60 | 0.80 | 61 | Largest single-country services supplier; most closely integrated non-member |
| 7 | CHE | Switzerland | 1.00 | 0.16 | 20 | Fourth-largest non-EU economic linkage; pharmaceuticals and precision goods |
| 8 | RUS | Russian Federation | 0.97 | 3.75 | 467 | Carbon linkage nearly four times its economic weight |
| 9 | LAM | Latin America (7) | 0.69 | 1.57 | 274 | Agricultural and mineral supply; the most homogeneous block |
| 10 | MEA | Middle East (4) | 0.64 | 1.27 | 240 | Hydrocarbon channel; effectively no carbon pricing |
| 11 | IND | India | 0.59 | 2.80 | 574 | Third on carbon linkage with zero carbon-pricing coverage |
| 12 | AFR | Africa (11) | 0.54 | 2.06 | 462 | Admitted on carbon. Resource supply; the most climate-vulnerable partners |
| 13 | TUR | Türkiye | 0.50 | 1.10 | 264 | Admitted on carbon. Manufacturing satellite under customs union; unpriced; substantial border-adjustment exposure |

The constraint is satisfied. The largest named region is China at 4.49 % economic and
11.11 % carbon linkage, while ROW reaches 3.47 % and 10.80 %, below both — though by
only 0.30 pp on the binding measure. The margin is narrow because 6.73 pp of ROW's
carbon linkage is the unallocated block, which no method can promote or decompose.
Named regions carry 96.5 % of economic and 89.2 % of carbon linkage.

### 7.1 Discussion

The carbon clause changes the composition of the set rather than merely its size.
Ranked on economic linkage alone, Africa and Türkiye would stand twelfth and fifteenth
and would be discarded. Ranked instead on the ratio of carbon to economic linkage, the
ordering is very nearly reversed:

| | IND | RUS | AFR | ROW | CHN | LAM | TUR | MEA | RASIA | USA | EU27 | GBR | CHE |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Carb % ÷ econ % | 4.75 | 3.86 | 3.82 | 3.11 | 2.48 | 2.26 | 2.18 | 1.99 | 1.77 | 0.98 | 0.73 | 0.50 | 0.16 |

India's emissions embodied in EU demand are nearly five times its trade weight;
Switzerland's are one sixth of its. A stress test resolved on trade weight alone would
model the Union's carbon exposure with the wrong regions. This spread, a factor of
thirty from top to bottom, is the substantive justification for carrying two measures
rather than one.

Eleven regions of the earlier twenty-three-region design are demoted: Japan, Norway,
Korea, Singapore, Canada, Chinese Taipei, Viet Nam, Australia, Indonesia, Kazakhstan and
Chile. Each falls below both thresholds, so each demotion is consistent with the stated
rule. Three are worth recording as knowingly accepted losses. Kazakhstan, at 0.93 %
carbon linkage and 884 t/\$m, is the highest-intensity economy in the set and misses by
0.07 pp. Viet Nam, at 0.66 % carbon, is the principal destination of trade diverted from
China and therefore the economy most likely to alter EU sourcing over the horizon, which
bears directly on the tariff analysis. Chinese Taipei, at 0.52 % carbon, is a
semiconductor chokepoint whose supply-chain dependency has no substitute at any price.
None of the three can be defended on linkage grounds; each could be defended on a
different criterion, and if any are restored it should be on that stated basis rather
than by moving the threshold to accommodate them.

Finally, the region set determines the foreign-exchange cross-section, because a
currency exists in the model only where its economy is resolved as a region. The
thirteen-region set supports six analytical currencies — the dollar, renminbi, sterling,
Swiss franc, rupee and lira — against fourteen previously. The yen, Canadian dollar,
krone, rupiah, Chilean peso, Australian dollar, Singapore dollar, won and tenge are
lost, and the franc is gained. This is a direct and substantial narrowing of the primary
deliverable, and it follows from the linkage rule rather than from any judgement about
exchange rates. It is recorded here because the trade-off between parsimony and currency
coverage is a decision that belongs at the design level, and not one the selection
algorithm should be permitted to make silently.

---

## 8. Sufficiency of the residual closure

### 8.1 The question

The preceding sections discipline ROW by linkage: §6.3 promotes blocks out of it until
it falls below the largest named region on both measures, and §7 records that it does so
with 0.30 pp to spare. This establishes that ROW is not large enough to dominate. It
does not establish that collapsing fifteen economies into it leaves the other twelve
regions' results undistorted, and those are the only results the model interprets.

The concern is substantive rather than formal. ROW is not a rounding term: it carries
3.47 % of economic and 10.80 % of carbon linkage, more than every named region except
China, and §3.3 shows it to be the most internally heterogeneous block in the set,
spanning 18.3× in carbon intensity. Since aggregation replaces each member's technical
coefficients with an output-weighted average, an analytical region trading with ROW
members whose intensities depart sharply from that average will have its computed shock
distorted by an amount no downstream calibration can recover.

### 8.2 Test design

Sufficiency in this context means convergence: the analytical results should cease to
move as ROW is resolved more finely. This is directly testable by rebuilding the model
from the 81-economy source under two partitions that share the same twelve analytical
regions and differ only in the treatment of the residual.

| | Treatment of ROW | Sectors |
|---|---|--:|
| Coarse | Single closure, as in the estimated model | 650 |
| Fine | Japan, Canada, Australia, Indonesia, Kazakhstan, Norway, Ukraine and Pakistan resolved individually, plus a residual | 1,050 |

The eight economies are chosen as the worst case for aggregation bias rather than as a
random sample: they comprise ROW's largest members by linkage — Japan, Canada and
Australia — together with its intensity extremes, Kazakhstan at 884 t/\$m and Norway at
69 t/\$m. If resolving the members most capable of biasing the aggregate leaves the
analytical regions largely unmoved, any finer partition will move them less.

The comparison is made at intermediate pass-through only. At $\phi = 0$ and $\phi = 1$
the transition shock reduces to the region's own $\mp\,\mathrm{CT}/\mathrm{GVA}$, which
involves no cross-region propagation and is invariant to the partition by construction,
so testing there would establish nothing.

### 8.3 Results

Transition value-added shocks under the two partitions, in percentage points:

| Region | $\phi=0.3$ coarse | fine | $\Delta$ | $\phi=0.5$ coarse | fine | $\Delta$ | $\phi=0.7$ coarse | fine | $\Delta$ |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| EU27 | $-0.840$ | $-0.835$ | $+0.005$ | $-0.426$ | $-0.420$ | $+0.007$ | $+0.099$ | $+0.105$ | $+0.007$ |
| CHN | $-3.614$ | $-3.621$ | $-0.007$ | $-1.883$ | $-1.893$ | $-0.010$ | $+0.343$ | $+0.333$ | $-0.010$ |
| USA | $-0.840$ | $-0.838$ | $+0.002$ | $-0.319$ | $-0.316$ | $+0.003$ | $+0.293$ | $+0.297$ | $+0.004$ |
| GBR | $-0.524$ | $-0.503$ | $+0.021$ | $-0.266$ | $-0.234$ | $+0.032$ | $+0.058$ | $+0.094$ | $+0.036$ |
| CHE | $-0.257$ | $-0.265$ | $-0.008$ | $-0.194$ | $-0.205$ | $-0.011$ | $-0.089$ | $-0.100$ | $-0.011$ |
| RUS | $-3.723$ | $-3.731$ | $-0.008$ | $-1.494$ | $-1.506$ | $-0.012$ | $+1.153$ | $+1.140$ | $-0.013$ |
| IND | $-4.597$ | $-4.602$ | $-0.006$ | $-1.712$ | $-1.721$ | $-0.009$ | $+1.668$ | $+1.658$ | $-0.010$ |
| TUR | $-2.343$ | $-2.354$ | $-0.012$ | $-1.075$ | $-1.093$ | $-0.018$ | $+0.500$ | $+0.479$ | $-0.020$ |
| RASIA | $-2.329$ | $-2.324$ | $+0.006$ | $-1.163$ | $-1.155$ | $+0.008$ | $+0.314$ | $+0.322$ | $+0.008$ |
| LAM | $-2.125$ | $-2.127$ | $-0.002$ | $-0.791$ | $-0.793$ | $-0.002$ | $+0.768$ | $+0.767$ | $-0.002$ |
| MEA | $-1.666$ | $-1.669$ | $-0.003$ | $-0.591$ | $-0.596$ | $-0.005$ | $+0.654$ | $+0.649$ | $-0.005$ |
| AFR | $-2.897$ | $-2.900$ | $-0.003$ | $-0.840$ | $-0.844$ | $-0.005$ | $+1.467$ | $+1.462$ | $-0.005$ |

The largest deviation anywhere in the grid is 0.036 pp and the median is 0.007 pp.
Output multipliers move by at most 0.51 % in relative terms.

Absolute magnitude is an incomplete yardstick, since a fixed error matters more where
the shock is small. Measured against the cross-region spread, the deviations amount to
0.49 %, 1.90 % and 2.03 % of the range at $\phi = 0.3$, $0.5$ and $0.7$ respectively.
The cross-section is essentially unchanged: the Spearman rank correlation between
partitions is 1.0000 at $\phi = 0.5$ and $\phi = 0.7$, and 0.9930 at $\phi = 0.3$, where
the single rank change consists of the EU27 and the United States exchanging ninth and
tenth place across a coarse gap of 0.0003 pp — two regions that are indistinguishable on
this measure under either partition.

The United Kingdom exhibits the largest deviation and merits comment. It trades
disproportionately with precisely the economies the fine partition resolves — Japan,
Canada, Australia and Norway — and is therefore the analytical region most exposed to
how ROW is averaged. Even so its shock moves by 0.032 pp at $\phi = 0.5$ against a shock
of $-0.266$ pp, so the effect is detectable but not material, and it establishes the
scale of the error for the region most vulnerable to it.

### 8.4 Interpretation

The test establishes that the analytical regions' transition shocks and output
multipliers have converged with respect to the granularity of ROW. Resolving the eight
members most capable of biasing the aggregate alters no conclusion, no ordering and no
magnitude by an amount that would change a reading of the results, so a finer partition
is not required for the outputs the model interprets.

It establishes nothing about ROW's own outputs, which are for that reason not reported.
Section 3.3 records ROW's 18.3× intensity spread precisely because cleaning improves the
reported blocks by displacing their outliers into the block that is not reported. The
heterogeneity is genuine; the test demonstrates only that it remains contained.

One component is irreducible. The unallocated block carries 6.73 pp of ROW's 10.80 pp of
carbon linkage and cannot be split by any method, since it is not an economy and has no
members to resolve. It therefore sits inside ROW under both partitions, and the test is
silent on it. That fraction of the closure region is a limitation of the source data
rather than of the aggregation, and it is the reason the dominance margin in §7 is
narrow.

The test also inherits its own assumptions, being conducted on the transition channel at
a flat \$70 carbon price. Physical damage is allocated on vulnerability rather than trade
and is considerably less sensitive to the partition, but a scenario pricing ROW members
very differently from one another — which the zone structure of §6.2 in part prevents by
construction — would widen these deviations.

---

## 9. Limitations

**Scenario zones are not applied carbon prices.** The partition in §6.2 is made on the
price the scenario assigns to a region's R5 zone, not on the price the economy actually
levies, because no per-economy applied-price series exists for all 81. The distinction
matters: Switzerland was missed by the manual selection precisely because it sat within
a residual assumed to price carbon at \$2/t, when it has in fact levied CHF 120/t
(approximately \$133) since 2022 — an error of some sixty-five-fold. Zone membership
would not have detected this.

**The cleaning threshold is asserted.** The value $k = 1.5$ is a judgement rather than
an estimate. Its defence is insensitivity rather than derivation: every value in
$[1.5, 3.0]$ returns the same thirteen regions and the same promotion, and only
$k \le 1.4$ changes the answer. This is weaker than deriving it, and is reported as such.

**Ward's weighting favours absorption.** In stage one the harmonic term
$w_Gw_H/(w_G+w_H)$ renders the attachment of a very small economy to a large one nearly
costless, which is why Iceland is absorbed by the United States and India is placed in a
group with Cambodia and Myanmar. Average or complete linkage would behave differently,
and the stability of the stage-one ranking across linkage rules has not been tested.

**The dominance bound is a hard constraint on a noisy quantity.** It is set by a single
economy's measured linkage. China's shares derive from one input–output table, so a
revision that moved them could change the number of promotions discontinuously. The
current margin of 0.30 pp on the binding measure is narrow.

**The residual absorbs the heterogeneity.** Cleaning improves the blocks carrying
interpreted results by displacing their outliers into the block that does not. ROW's
18.3× internal spread is the direct cost of RASIA's 4.0×. Section 8 shows this remains
contained for the analytical regions, but anything attributed to ROW itself is
correspondingly unreliable. The error is deliberately placed rather than eliminated.

**Selection uses structural attributes only.** No model output enters the procedure — no
exchange-rate moves, no value-added shocks. Choosing regions because they produce large
results and then reporting those results would constitute selection on the outcome.

**Feasibility is not modelled.** Equity elasticities, Okun coefficients and unemployment
series do not exist for every economy. A region that the algorithm promotes but for
which every downstream parameter must be a proxy may be less useful than an aggregate.

**A single base year.** The 2022 table fixes the trade structure. Linkages that have
shifted since — the collapse in Russian pipeline gas, the diversion of Chinese exports
through Viet Nam and Mexico — are absent by construction, which matters most for those
economies lying closest to the threshold.

---

## 10. Summary

This chapter has treated region selection as a derived result rather than an assertion.
Two linkage measures are computed from the European Union's final-demand footprint over
the 2022 OECD inter-country input–output table, weighted by production-based emissions.
A greedy agglomerative scheme establishes which economies merit individual resolution,
confirming seven of the manual selections while promoting three that had been overlooked;
it cannot supply a cut point, because the merge-cost curve exhibits no knee across the
relevant range. An explicit threshold rule — the ten largest by economic linkage, plus
anything exceeding 1 % on either measure — supplies that cut, admitting Africa and
Türkiye on carbon grounds that a size ranking would have missed.

The residual this leaves would dominate both measures, so a block must be removed from
it. The blocks are taken from the data rather than invented: the residual is partitioned
along NGFS R5 zones, the resolution at which scenario carbon prices are published, so
that each takes exactly one price path. One zone, Asia, spanning 15× in carbon
intensity, is unfit as it stands and is cleaned by removing members more than 1.5 times
its own average intensity, reducing its spread to 4.0× at a cost of 0.21 % of economic
linkage. Cleaned zones are then promoted until the residual satisfies the bound, and a
single promotion suffices.

The result is thirteen regions covering 96.5 % of the Union's economic and 89.2 % of its
carbon footprint, with the residual below the largest single economy on both measures.
The number of promotions is an output of the constraint, and the answer is unchanged for
every cleaning threshold in $[1.5, 3.0]$. An aggregation-invariance test confirms that
the analytical regions have converged with respect to the granularity of the residual:
resolving the eight members most capable of biasing it moves no regional shock by more
than 0.036 pp and leaves the cross-sectional ordering intact.
