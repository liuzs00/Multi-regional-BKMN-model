# Region selection: deriving the set instead of asserting it

The 20 regions used throughout this project were chosen by argument — FX
coverage, CBAM exposure, physical vulnerability — and defended narratively. This
note replaces that with an algorithm, reports what it selects, and states plainly
where it disagrees with us.

Code: [`tools/select_regions.py`](../tools/select_regions.py). Outputs
`out_region_attributes.csv` (all 81 economies) and `out_region_merge_order.csv`.

---

## 1. What a region actually buys you

The instinct is to rank economies by size and take the top *K*. That is the wrong
objective. Promoting an economy out of an aggregate does not buy you **size** — it
buys you **resolution**. Inside a block, every member shares one carbon price, one
carbon intensity, one vulnerability score, one currency and one scenario zone.
Promoting *c* lets it have its own.

So the criterion is not *"which economies are biggest"* but **"which economies, if
left inside a block, would make that block misrepresent them"** — because
aggregation bias comes from within-group heterogeneity, not from group size. A
block of 60 near-identical economies aggregates almost exactly; a block of three
wildly different ones does not.

That reframing has a useful consequence: it makes ROW-robustness the *same*
objective as the selection criterion, rather than a separate condition to check
afterwards.

## 2. Method

**Linkage — how much the EU depends on an economy.** Solve the EU's final-demand
footprint over the 81-economy 2022 ICIO:

$$\mathbf{x}_{\mathrm{EU}} = (\mathbf{I}-\mathbf{A})^{-1}\mathbf{f}_{\mathrm{EU}}$$

the gross output required *everywhere* to satisfy EU final demand — **\$32.2 tn**
in total. This is directed, which is what "EU as centre" means: an economy counts
for what it supplies the EU, not for its global weight. It also captures indirect
supply chains, which a bilateral trade share misses.

| | definition |
|---|---|
| **Economic linkage** | economy *c*'s share of that \$32.2 tn footprint |
| **Carbon linkage** | the same, weighted by carbon intensity — i.e. emissions embodied in EU final demand (consumption-based accounting) |

**Attributes — what a block would blur.** Standardised log carbon intensity and
ND-GAIN vulnerability: the two things that differ within a block and drive the
model's channels.

**Merge cost — Ward's criterion, weighted by linkage.**

$$\mathrm{cost}(G,H) = \frac{w_G\,w_H}{w_G+w_H}\,\lVert \bar{X}_G - \bar{X}_H \rVert^2$$

Merging two large, dissimilar, EU-relevant groups is expensive; merging two small
similar ones is nearly free. Agglomerative rather than greedy forward selection,
for one reason that matters: **there is no residual bucket.** ROW is not
"everything left over" — it is just another cluster, with its heterogeneity cost
measured on the same scale as every other group's.

**Stopping rule.** Your constraint was that ROW must not be the largest region on
either linkage measure. Under merging that becomes: *every multi-member group
must rank below the largest single-economy region, on both measures.* This has
teeth — it fails while any big player is still buried inside a block. **China
stays fused to Turkey until k = 24**, and that is precisely what forces the split.

No cap on the number of regions.

## 3. The linkage numbers

Top non-EU economies, as a share of the EU's footprint:

| | econ % | carbon % | CI (t/\$m) | | | econ % | carbon % | CI (t/\$m) |
|---|--:|--:|--:|---|---|--:|--:|--:|
| **CHN** | 4.55 | **11.91** | 299 | | BRA | 0.30 | 0.83 | 314 |
| **USA** | 2.72 | 2.81 | — | | SAU | 0.27 | 0.77 | 330 |
| **GBR** | 1.62 | 0.86 | — | | CAN | 0.26 | 0.31 | — |
| **CHE** | 1.01 | 0.18 | 20 | | TWN | 0.26 | 0.56 | 243 |
| **RUS** | 0.99 | **4.02** | 467 | | VNM | 0.26 | 0.71 | 315 |
| **IND** | 0.60 | **3.00** | 574 | | AUS | 0.19 | 0.24 | — |
| **JPN** | 0.60 | 0.63 | — | | ISR | 0.18 | 0.12 | 81 |
| **NOR** | 0.53 | 0.32 | 69 | | MEX | 0.16 | 0.34 | 240 |
| **KOR** | 0.51 | 0.64 | — | | ZAF | 0.14 | 0.72 | **608** |
| **TUR** | 0.51 | 1.18 | — | | KAZ | 0.13 | **1.00** | **884** |
| **SGP** | 0.31 | 0.28 | — | | CHL | **0.05** | 0.08 | — |

**The two measures disagree, and that is the point.** Switzerland is 4th on
economic linkage and nowhere on carbon (CI of 20 t/\$m). Kazakhstan is 20th on
economic linkage and **6th on carbon** (884 t/\$m). India is 6th economically and
**3rd on carbon**. A single-objective selection would systematically miss one or
the other, which is why both are carried and neither collapsed into a weighted
scalar.

## 4. What the algorithm selects

**Free run — 25 regions** (rules satisfied at k = 24 non-EU groups).

| outcome | economies |
|---|---|
| **Confirms 7 of our 15** named non-EU regions, unprompted | CHN, GBR, RUS, JPN, NOR, TUR, KAZ |
| **Adds 5 we currently bury** | **CHE**, TWN, SAU, ZAF, ISR |
| **Declines to separate 8 of ours** | USA, IND, KOR, AUS, CAN, SGP, IDN, CHL |

That it recovers seven of our regions without being told to is the main
validation: the existing selection was not arbitrary.

**Currency-protected run — 18 regions.** Protecting the 14 economies whose
currencies the FX deliverable needs gives a smaller set, but a worse one:
protected economies cannot absorb their natural neighbours, so the unprotected
ones clump into two large blocks — one of which buries **Russia** (4.02 % carbon
linkage) with Brazil, Mexico, Taiwan and Ukraine. Reported for completeness, not
recommended.

## 5. Where it disagrees with us, and who is right

### 5.1 Switzerland is an error, not a judgement call

CHE is **4th among all non-EU economies on economic linkage (1.01 %)** — ahead of
India, Japan, Korea and Turkey, all of which we model individually. We have it
inside ROW.

Worse, ROW carries an assumed carbon price of **\$2/t**. Switzerland has levied
**CHF 120/t (≈ \$133) since 2022** ([FOEN](https://www.bafu.admin.ch/en/co2-levy-private-individuals)) —
higher than the EU ETS. That is roughly a **65× error** on an economy with its own
freely traded currency. This is the single clearest finding of the exercise and
should be fixed regardless of what else changes.

### 5.2 The ones it refuses to separate split two ways

**Cosmetic:** the USA pairs with Iceland — the block is 2.74 % against 2.72 % for
the USA alone, so it *is* the USA.

**Not cosmetic:** India carries **3.00 % of the EU's embodied carbon**, third
behind only China and Russia, and the free run leaves it in a six-member block
with Cambodia, Laos and Myanmar. The merge is cheap because Ward's harmonic
weighting lets small economies attach to large ones almost for free — a known
property, and a reason not to read the free run as prescriptive.

**Genuinely small:** Australia (0.19 % / 0.24 %), Indonesia (0.14 % / 0.49 %) and
above all **Chile (0.05 % / 0.08 %)** cannot be justified on EU linkage at all.
They are in our set for **FX coverage and a critical-minerals narrative**, which
is a legitimate reason — but it is a different reason from the one the rest of the
selection rests on, and the write-up should say so rather than imply a uniform
criterion.

### 5.3 Economies we exclude that outrank ones we include

Every economy below beats Chile on both measures, and several beat Australia and
Indonesia too:

| | econ % | carbon % | why it matters |
|---|--:|--:|---|
| **CHE** | 1.01 | 0.18 | \$133/t carbon price modelled at \$2 |
| BRA | 0.30 | 0.83 | largest LAM economy, currently aggregated |
| SAU | 0.27 | 0.77 | oil, no carbon price |
| TWN | 0.26 | 0.56 | semiconductor chokepoint |
| **VNM** | 0.26 | 0.71 | **the trade-diversion destination** (TARIFF_CALIBRATION §5.1) |
| ZAF | 0.14 | **0.72** | CI 608 t/\$m, carbon tax since 2019 |

Vietnam is the pointed one: it absorbed much of China's lost US import share, it
is central to the base-year problem in the tariff work, and it sits invisibly
inside ROW while Chile — a fifth of its economic linkage and a ninth of its
carbon linkage — has its own region.

## 6. Where to cut, and what the data does not say

The merge-cost curve rises smoothly through the range that matters:

| groups remaining | 15 | 12 | 10 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| merge cost (000s) | 14 | 23 | 55 | 90 | 150 | 394 | 473 | 949 | 1,089 | 6,155 |

The sharp jumps are all at the top of the tree (k ≤ 7), where the algorithm is
forced to merge the advanced/low-carbon bloc with the developing/high-carbon one.
**Between 15 and 25 regions there is no knee** — costs rise steadily, so the data
does not single out a number in that range. Any choice there is a judgement about
effort and data availability, not something the algorithm settles. Saying so is
more honest than manufacturing a threshold.

## 7. Final decision: 23 regions

Three economies are promoted out of ROW — **Switzerland, Taiwan and Viet Nam** —
because each outranks named regions we already model, on both linkage measures.
Nothing is demoted: the FX deliverable needs its currencies, and the small ones
are kept for that reason, stated openly in the table.

Shares are of the EU's \$32.2 tn final-demand footprint. **ROW now ranks 4th on
economic and 6th on carbon linkage** — behind China on both — so the constraint
that the residual must not dominate is satisfied.

| # | Region | Full name | econ % | carbon % | Economic rationale (one line) |
|--:|---|---|--:|--:|---|
| 1 | **EU27** | European Union (27 members) | 81.00 | 62.97 | The base region and numéraire: EU demand is met overwhelmingly from inside the single market, so intra-EU supply chains carry most of the footprint. |
| 2 | **CHN** | China | 4.49 | **11.91** | Largest non-EU supplier on both measures, and the only economy whose carbon linkage (11.9 %) is nearly triple its economic linkage — the EU's single biggest embodied-emissions exposure. |
| 3 | **USA** | United States | 2.68 | 2.81 | Second-largest external supplier and the counterparty for the EU–US tariff framework; also the reserve-currency leg of every FX pair. |
| 4 | **ROW** | Rest of World (15 economies) | 2.13 | 2.64 | Residual for economies individually below the promotion threshold; kept small enough that it dominates neither measure. |
| 5 | **GBR** | United Kingdom | 1.60 | 0.86 | Largest single-country services supplier to the EU and the closest integrated non-member; sterling is a core FX leg. |
| 6 | **CHE** | Switzerland | 1.00 | 0.18 | **Newly promoted.** 4th-largest non-EU economic linkage — ahead of India, Japan and Korea — with pharmaceuticals and precision goods deeply embedded in EU chains. |
| 7 | **RUS** | Russian Federation | 0.97 | **4.02** | Second on carbon linkage: modest trade share but 467 t/\$m intensity, so its embodied emissions in EU demand are four times its economic weight. |
| 8 | **LAM** | Latin America ex-Chile (6) | 0.64 | 1.60 | Argentina, Brazil, Colombia, Costa Rica, Mexico, Peru — agricultural and mineral supply with broadly similar intensity, so aggregation costs little. |
| 9 | **MEA** | Middle East (4) | 0.64 | 1.36 | UAE, Israel, Jordan, Saudi Arabia — the EU's hydrocarbon import channel and a bloc with essentially no carbon pricing. |
| 10 | **IND** | India | 0.59 | **3.00** | Third on carbon linkage at 574 t/\$m intensity, with zero carbon-pricing coverage — the largest unpriced embodied-emissions source after China. |
| 11 | **JPN** | Japan | 0.59 | 0.63 | Advanced-manufacturing supplier with its own carbon-pricing regime and a major traded currency. |
| 12 | **AFR** | Africa (11) | 0.54 | 2.21 | Angola, Côte d'Ivoire, Cameroon, DR Congo, Egypt, Morocco, Nigeria, Senegal, São Tomé, Tunisia, South Africa — resource supply and the EU's most climate-vulnerable trading partners. |
| 13 | **NOR** | Norway | 0.52 | 0.32 | The EU's dominant pipeline-gas supplier post-2022, and the only region pricing carbon above the EU. |
| 14 | **KOR** | Korea | 0.51 | 0.64 | Electronics and shipbuilding supplier operating its own ETS — one of the two currencies whose FX channels point opposite ways. |
| 15 | **TUR** | Türkiye | 0.50 | 1.18 | Large EU manufacturing satellite under a customs union, carbon-intensive and unpriced, hence a prime CBAM exposure. |
| 16 | **SGP** | Singapore | 0.31 | 0.28 | Most import-dependent economy in the set (50.8 % of intermediate inputs imported) — the entrepôt through which much Asian trade reaches the EU. |
| 17 | **CAN** | Canada | 0.26 | 0.31 | Resource supplier with a federal carbon price near EU levels; useful as a high-price, low-intensity contrast. |
| 18 | **TWN** | Chinese Taipei | 0.26 | 0.56 | **Newly promoted.** Semiconductor chokepoint: small trade share but a supply-chain dependency with no substitute. |
| 19 | **VNM** | Viet Nam | 0.25 | 0.71 | **Newly promoted.** The principal destination of trade diverted from China, so the economy most likely to alter EU sourcing over the horizon. |
| 20 | **AUS** | Australia | 0.19 | 0.24 | Coal and iron-ore exporter; retained mainly for AUD coverage, its EU linkage being modest. |
| 21 | **IDN** | Indonesia | 0.14 | 0.49 | Coal, nickel and palm oil with 7,614 t/\$m electricity intensity — a large CBAM rate on a small trade share. |
| 22 | **KAZ** | Kazakhstan | 0.13 | **1.00** | The extreme case: 884 t/\$m aggregate intensity gives it a carbon linkage eight times its economic linkage, and a CBAM rate above 100 % on electricity. |
| 23 | **CHL** | Chile | **0.05** | 0.08 | Weakest on both measures. Retained for **CLP coverage and copper/lithium exposure**, not for EU linkage — a different criterion from the rest, and flagged as such. |

**ROW after promotion (15):** Bangladesh, Belarus, Brunei, Hong Kong, Iceland,
Cambodia, Laos, Myanmar, Malaysia, New Zealand, Pakistan, Philippines, Thailand,
Ukraine, plus the OECD table's own unallocated residual.

**Three honest notes on this table.** Chile is kept on a criterion the others are
not judged by. Thailand, Malaysia and Ukraine sit just below the promotion line
and are the first candidates if the set grows again. And Brazil (0.30 / 0.83),
Saudi Arabia (0.27 / 0.77) and South Africa (0.14 / 0.72) each outrank several
named regions but stay inside LAM, MEA and AFR — being inside a *regional* block
of 4–11 similar economies is far less costly than being inside a 15-member global
residual, which is why they were not promoted and Switzerland was.

## 8. Limitations

**Two attributes only.** Carbon intensity and vulnerability. Carbon-*price*
regime is not in the distance metric because we lack a per-economy price series
for all 81 — which is itself why Switzerland was missed by our manual selection.
Adding it would likely promote CHE, and possibly Canada and the UK, more strongly.

**Ward's weighting favours absorption.** The harmonic term makes attaching a tiny
economy to a large one nearly free, which is why Iceland lands on the USA and
India lands with Cambodia. An alternative (average or complete linkage) would
behave differently; we have not tested whether the selection is stable across
linkage rules, and it should be.

**Structural attributes only, deliberately.** Selection never uses model outputs
— no FX moves, no GVA shocks. Choosing regions because they produce large results
and then reporting those results would be selection-on-outcome.

**Feasibility is not modelled.** Equity betas, Okun coefficients and unemployment
series do not exist for all 81 economies. An economy the algorithm promotes but
for which every downstream parameter is a proxy may be worse than leaving it in a
block.

**Not yet acted on.** The 20-region set remains in force throughout the results;
this note is the case for changing it, not the change. See
[FURTHER_WORK.md](FURTHER_WORK.md).
