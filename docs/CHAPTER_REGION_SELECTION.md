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
| **LAM** | Argentina, Brazil, Colombia, Costa Rica, Mexico, Peru | Agricultural and mineral supply, broadly similar intensity |
| **ROWL** | Australia, Canada, Chile, Hong Kong, Iceland, Japan, Korea, Malaysia, Norway, New Zealand, Singapore, Chinese Taipei | Residual, lower intensity (137 t/\$m) — **derived**, see §6.1 |
| **ROWH** | Bangladesh, Belarus, Brunei, Indonesia, Kazakhstan, Cambodia, Laos, Myanmar, Pakistan, Philippines, Thailand, Ukraine, Viet Nam, ICIO residual | Residual, higher intensity (539 t/\$m) — **derived**, see §6.1 |

The first four are imposed on policy and geographic grounds. The two residuals
are not chosen at all: they are what the capped merge of §6.1 returns.

EU27 is treated as a single region because the model's own policy variables are
defined at that level — the carbon price is the ETS price, and CBAM is an EU
instrument. Modelling members separately would require a within-EU carbon-price
differential that does not exist.

### 3.3 What aggregation costs

The cost of a block is the heterogeneity it conceals. Measured as the ratio of
the highest to the lowest member carbon intensity:

| Block | *n* | median CI (t/\$m) | min | max | max/min |
|---|--:|--:|--:|--:|--:|
| LAM | 6 | 280 | 134 | 314 | **2.3×** |
| AFR | 11 | 461 | 195 | 723 | 3.7× |
| MEA | 4 | 291 | 81 | 330 | 4.1× |
| ROWL | 12 | 139 | 69 | 318 | 4.6× |
| ROWH | 14 | 589 | 227 | 1,268 | 5.6× |
| EU27 | 27 | 102 | 26 | 307 | **11.8×** |

The imposed aggregates are tight — LAM in particular is nearly homogeneous, so
collapsing it costs little. EU27's 11.8× spread is the widest in the set and is
tolerated for the policy reason above, not because it is small.

**The two residuals are tighter than the base region.** This is not the usual
outcome — a residual normally absorbs whatever is left and is correspondingly
heterogeneous — and it is a direct consequence of deriving the partition under a
constraint (§6.1) rather than assigning it geographically. An earlier
two-attribute version of the same procedure produced a block spanning 18.3×, from
Norway (69 t/\$m) to Cambodia (1,268 t/\$m); adding the carbon-price attribute
separates the advanced economies from the developing ones and no block now spans
more than 5.6×.

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

**Attributes.** Each economy carries three standardised quantities — the things a
block would blur and that drive the model's channels:

| attribute | what it protects |
|---|---|
| log carbon intensity | the transition charge $ct = \mathrm{CI}\times\mathrm{XCE}$ |
| ND-GAIN vulnerability | the physical damage allocation |
| carbon-price zone score | the carbon price the members would face |

The third deserves comment, because the obvious encoding is wrong. Scenario
carbon prices are published at NGFS R5 resolution, so a group spanning zones must
take a blended price. Treating the zone as a *categorical* label would penalise
every cross-zone merge equally — but under Net Zero the OECD and Asia paths differ
by 4 %, while under Fragmented World one zone prices carbon at \$0 and another at
\$44. What matters is not whether two economies share a label but whether they
face a similar price, so the attribute is the **price itself**: each zone's
carbon price is z-scored *within* each scenario (so that scenarios with large
absolute prices do not dominate) and averaged across the seven narratives.

All three are standardised to unit variance and enter with equal weight, which is
the neutral choice and not a tuned one; `ZONE_WEIGHT` exposes it for sensitivity.

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
| 8 | LAM | 0.64 | 1.49 | | 19 | VNM | 0.25 | 0.66 |
| 9 | MEA | 0.64 | 1.27 | | 20 | AUS | 0.19 | 0.23 |
| 10 | IND | 0.59 | 2.80 | | 21 | IDN | 0.14 | 0.46 |
| — | *cut* | | | | 22 | KAZ | 0.13 | 0.93 |
| 11 | JPN | 0.59 | 0.59 | | 23 | CHL | 0.05 | 0.07 |

Kazakhstan at 0.93 % carbon is the closest miss, and is the region most sensitive
to where the threshold is placed: a 0.9 % rule would admit it.

### 6.1 The residual must be split, and the split is derived

Applying the rule alone produces twelve regions but **breaks the requirement that
the residual must not dominate**. Absorbing eleven demoted economies leaves a
residual at **5.34 % economic and 14.09 % carbon linkage** — larger than China on
*both* measures. Results attributed to such a region would not be interpretable.

Restoring economies does not help: promoting them back in descending order of
economic linkage fails to satisfy the constraint until **nineteen** regions, by
which point the cut has been undone.

The residual must therefore be partitioned. Doing so with stage 1's Ward
criterion applied naively **fails**: clustering on (log CI, vulnerability) groups
the high-carbon economies together and thereby *concentrates* carbon, producing a
sixteen-member block at 11.68 % carbon linkage — above China's 11.11 %.

The failure is instructive rather than fatal. Two things are being asked of the
partition, and they are not the same kind of thing:

| | |
|---|---|
| minimise within-group heterogeneity | an **objective** — what Ward optimises |
| no group may dominate | a **constraint** — what Ward knows nothing about |

Unconstrained optimisation of the first will violate the second whenever the two
point in different directions, which here they do. The remedy is not to abandon
the criterion but to give it the constraint. A merge that would produce a group
exceeding the cap on either measure is simply **not available**:

$$\text{merge}(G,H)\ \text{admissible}\iff
\ell^{\text{econ}}_{G\cup H} \le \bar{\ell}^{\text{econ}}
\ \ \text{and}\ \
\ell^{\text{carb}}_{G\cup H} \le \bar{\ell}^{\text{carb}} .$$

Ward continues to choose *which* feasible pair to merge; the cap decides which
pairs exist. Merging halts when no admissible pair remains, so **the number of
residual groups is an output, not a choice**.

The cap is not a tuning parameter either. It is the linkage of the largest
single-economy region — which the data says is China, on both measures
simultaneously ($\bar{\ell}^{\text{econ}} = 4.49\,\%$,
$\bar{\ell}^{\text{carb}} = 11.11\,\%$). This is the same quantity stage 1's
stopping rule already used, now enforced during merging instead of tested
afterwards.

Applied to the twenty-six demoted economies, the capped run halts at **two
groups**, separated cleanly by carbon intensity — 137 t/\$m against 539 t/\$m —
and so labelled ROWL and ROWH. Merges are blocked by the cap along the way, so
the constraint binds rather than merely being satisfied by luck.

The result is better on the objective as well as feasible:

| partition | within-group heterogeneity | worst member CI spread |
|---|--:|--:|
| Geographic Asia-Pacific / other (imposed) | 7.10 | 15.0× |
| Capped, two attributes | 4.69 | 18.3× |
| **Capped, three attributes** | **3.15** | **5.6×** |

Constraining the criterion beats imposing a partition by hand by more than half,
and adding the price attribute more than halves the worst block's internal
spread. The two-attribute run had paired Norway (69 t/\$m) with Cambodia
(1,268 t/\$m) inside one group; with the price attribute the advanced economies
separate from the developing ones and no block spans more than 5.6×.

**Why the cap cannot replace the threshold rule.** Running the capped merge over
all 81 economies from the start produces only **seven** regions: it fuses the
United States with Canada and Australia, Switzerland with the UK and Norway, and
buries India in a twenty-three-member block. The cap is a *ceiling* — it prevents
domination but expresses no view on which economies deserve resolution. The two
rules do different work and both are needed: §6's threshold decides what is
named, §6.1's cap disciplines what is left.

---

## 7. The selected region set

**Thirteen regions**: EU27 as base, ten named regions, two residuals. Shares are
of the EU's \$32.16 tn final-demand footprint.

| # | Region | Full name | econ % | carb % | CI (t/\$m) | Basis for inclusion |
|--:|---|---|--:|--:|--:|---|
| 1 | **EU27** | European Union (27) | 81.00 | 58.73 | 88 | Base region and numéraire; EU demand is met overwhelmingly from inside the single market |
| 2 | **CHN** | China | 4.49 | **11.11** | 299 | Largest external supplier on both measures; carbon linkage 2.5× its economic weight. Sets the dominance cap |
| 3 | **ROWL** | Rest of World, lower-intensity (12) | 2.92 | 3.31 | 137 | Derived residual (§6.1) — advanced Asia-Pacific, Oceania, Canada, Nordics |
| 4 | **USA** | United States | 2.68 | 2.62 | 118 | Second-largest external supplier; tariff counterparty; reserve currency |
| 5 | **ROWH** | Rest of World, higher-intensity (14) | 2.42 | **10.78** | 539 | Derived residual (§6.1) — developing and transition economies; second on carbon linkage after China |
| 6 | **GBR** | United Kingdom | 1.60 | 0.80 | 61 | Largest single-country services supplier; closest integrated non-member |
| 7 | **CHE** | Switzerland | 1.00 | 0.16 | 20 | 4th-largest non-EU economic linkage; pharmaceuticals and precision goods |
| 8 | **RUS** | Russian Federation | 0.97 | **3.75** | 467 | Carbon linkage nearly 4× economic weight |
| 9 | **LAM** | Latin America ex-Chile (6) | 0.64 | 1.49 | 282 | Agricultural and mineral supply; the most homogeneous block |
| 10 | **MEA** | Middle East (4) | 0.64 | 1.27 | 240 | Hydrocarbon channel; essentially no carbon pricing |
| 11 | **IND** | India | 0.59 | **2.80** | 574 | Third on carbon linkage with zero carbon-pricing coverage |
| 12 | **AFR** | Africa (11) | 0.54 | **2.06** | 462 | *Admitted on carbon.* Resource supply; most climate-vulnerable partners |
| 13 | **TUR** | Türkiye | 0.50 | **1.10** | 264 | *Admitted on carbon.* Manufacturing satellite under customs union; unpriced; prime CBAM exposure |

**Constraint check.** The largest named region is China at 4.49 % economic and
11.11 % carbon. ROWL reaches 2.92 % / 3.31 % and ROWH 2.42 % / 10.78 %: neither
residual is largest on either measure. **Satisfied by construction** — the cap is
enforced during merging (§6.1), so this is a restatement of the feasibility
condition rather than a test that could have failed.

**Coverage.** Named regions carry 94.7 % of economic and 85.9 % of carbon
linkage.

### 7.1 Discussion

**The carbon clause changes the set, not just its size.** Ranked on economic
linkage alone, Africa and Türkiye would sit 12th and 15th and be discarded.
Ranked on the ratio of carbon to economic linkage, the ordering is almost
reversed:

| | IND | ROWH | RUS | AFR | CHN | LAM | TUR | MEA | ROWL | USA | EU27 | GBR | CHE |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| carb % ÷ econ % | **4.75** | 4.46 | 3.86 | 3.82 | 2.48 | 2.33 | 2.18 | 1.99 | 1.13 | 0.98 | 0.73 | 0.50 | **0.16** |

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

**The price attribute is a zone score, not an applied price.** §5's third
attribute is the carbon price the *scenario* assigns a region's R5 zone, not the
price the economy actually levies today, because no per-economy applied-price
series exists for all 81. The distinction matters: Switzerland was missed by the
manual selection precisely because it sat in a residual assumed to price carbon
at \$2/t while it has levied CHF 120/t (≈ \$133) since 2022, a roughly 65-fold
error. A genuine applied-price attribute would likely promote Switzerland, Canada
and the UK more strongly than the zone score does.

**The zone attribute buys tightness, not zone purity.** Adding it at equal weight
cuts within-group heterogeneity by a third and halves the worst block's internal
spread, but leaves the share of group weight sitting outside its own dominant
zone unchanged at 44 %. Zone purity improves only if the attribute is weighted
about three times the others (falling to 32 %), which is not defensible a priori
and costs heterogeneity. The equal-weight choice is reported; the trade-off is
visible by setting `ZONE_WEIGHT`.

**Ward's weighting favours absorption.** The harmonic term $w_Gw_H/(w_G+w_H)$
makes attaching a tiny economy to a large one nearly free, which is why Iceland
lands on the United States and India lands in a block with Cambodia and Myanmar.
Average or complete linkage would behave differently, and the stability of the
selection across linkage rules has not been tested.

**The cap is a hard constraint on a noisy quantity.** The dominance cap is set by
one economy's measured linkage. China's shares are estimated from a single
input–output table, so a revision that moved them would change which merges are
admissible and could alter the residual partition discontinuously. A soft
penalty would degrade more gracefully than a hard feasibility test, at the cost
of no longer guaranteeing the constraint.

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

The residual this leaves would dominate both measures. It is partitioned by the
same Ward criterion, now carrying the dominance requirement as a feasibility
condition rather than a post-hoc test: a merge that would produce a group
outranking the largest single economy is not admissible, and merging halts when
none remains. The number of residual groups is therefore an output. Two result,
separated by carbon intensity at 137 against 539 t/\$m — and both tighter,
internally, than the base region itself.

The result is thirteen regions covering 94.7 % of the EU's economic and 85.9 % of
its carbon footprint, with no residual largest on either measure — a property
that now holds by construction rather than by inspection.
