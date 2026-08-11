# Main Results

This section reports what the model produces when the machinery of the previous
chapter is applied to the thirteen-region calibration built from the OECD ICIO
tables. It follows the shock through the economy in the order the model computes
it: first the real-economy effects on value added, then the price and policy
response, and finally the three financial markets the exercise is aimed at —
exchange rates, interest rates and credit. Trade measures are held out entirely
and treated separately in the next section, so everything below is driven by
carbon pricing and warming alone.

Results are reported at 2040 under the NGFS Net Zero 2050 narrative unless stated
otherwise, with cost pass-through set at φ = 0.5. Both choices are conventions
rather than findings, and the sensitivity of the results to each is examined in
§2 and §7 respectively. All figures are reproducible from the committed result
tables.

## 1. The calibration in brief

The model resolves the world into thirteen regions covering 81 economies and 650
region-industry pairs, with a world gross output of \$199.7 trillion and value
added of \$93.8 trillion. Three region-level characteristics do most of the work
in what follows, and it is worth setting them out before the results because
almost every ordering below can be traced back to one of them.

| | most exposed | least exposed |
|---|---|---|
| Carbon intensity (t CO₂e / \$m) | India 574, Russia 467, Africa 456 | Switzerland 20, UK 61, EU27 87 |
| Carbon-pricing coverage | EU27 0.645, China 0.467, Switzerland 0.425 | India, Türkiye, Russia, Middle East all 0.000 |
| Physical vulnerability (ND-GAIN, world = 1) | India 1.34, Africa 1.34, Middle East 1.22 | UK 0.79, Switzerland 0.83, US 0.89 |

These three are close to independent of one another, which is why no single
ranking of "climate exposure" emerges from the results. India is extreme on two
of the three; Switzerland is mild on all three; the EU is unusual in being the
most heavily *priced* economy while being among the least intensive.

### 1.1 The reporting convention, and how it differs from the original study

Reporting at 2040 under Net Zero 2050 is a presentational choice and needs
defending, because it is not the choice the single-region study makes.

That study reports a **mixture** rather than a single path: a Dirichlet prior
placing 0.90 on SSP2 and 0.90 on RCP4.5, evaluated at risk horizons running from
one day to twenty years out of a fixed valuation date. SSP2 with RCP4.5 is the
middle-of-the-road pairing, corresponding to roughly 2.7 °C of end-century
warming. Among the NGFS narratives used here, the nearest counterpart is not Net
Zero but **Current Policies**, at 2.75 °C.

The two conventions give very different headline numbers, and the difference is
concentrated in exactly one place:

| At 2040 | Net Zero 2050 | Current Policies | ratio |
|---|--:|--:|--:|
| Mean transition shock | −2.20 % | −0.06 % | **37×** |
| Worst regional transition shock | −4.72 % | −0.13 % | 35× |
| Mean physical damage | −1.01 % | −1.07 % | 0.94× |
| Worst five-year forward | −3.61 % | −1.31 % | 2.8× |
| Median credit widening | 3.95 % | 0.82 % | 4.8× |

Net Zero is therefore best understood as an **upper bound on the transition
channel rather than a central estimate**. It is used as the reporting case for a
practical reason: under Current Policies the carbon price reaches only \$1.53 per
tonne in the OECD zone by 2040, so the transition machinery that this model
exists to study produces almost nothing to look at. Reporting the channel where
it is visible makes the mechanism legible, at the cost of showing it at its
largest.

Two things follow, and both are honoured in what comes below. Physical damage is
essentially unaffected by the choice — 0.94× between the two extremes — so every
statement made about that channel is robust to it. And the mixture results of
§7.1 are the closer analogue of the original study's headline, with the
"consensus" prior in particular playing the same role as its SSP2/RCP4.5 anchor,
since both are constructed around published estimates of where current policies
actually lead. The gap between the two framings is large enough to change signs:
the dollar's five-year forward is −1.91 per cent under Net Zero and +0.10 per
cent under the consensus mixture.

The horizon is a milder choice. 2040 sits far enough out for the carbon price to
have risen substantially above its 2025 value of zero, and near enough to avoid
the endpoint of the 2045 reporting window; results at every horizon from 2025 to
2045 are reported throughout, so nothing rests on the single year.

## 2. The real economy: two shocks of comparable size

The carbon charge enters as an ad-valorem cost wedge on each sector's own
emissions and propagates through the Leontief price dual; warming enters through
the Barrage–Nordhaus damage function, allocated across region-industries by
vulnerability. Table 1 reports both at 2040 under Net Zero.

**Table 1.** GDP shock at 2040, Net Zero 2050, φ = 0.5 (per cent of regional
value added)

| Region | Transition | Physical | Total |
|---|--:|--:|--:|
| China | −4.72 | −1.13 | **−5.86** |
| India | −4.29 | −1.37 | −5.66 |
| Rest of Asia | −2.91 | −1.11 | −4.02 |
| Türkiye | −2.86 | −1.10 | −3.96 |
| Russia | −2.86 | −0.85 | −3.71 |
| Africa | −2.31 | −1.35 | −3.66 |
| Latin America | −2.11 | −1.06 | −3.17 |
| Rest of World | −2.14 | −0.96 | −3.10 |
| Middle East | −1.61 | −1.24 | −2.85 |
| EU27 | −0.96 | −0.83 | −1.79 |
| United States | −0.71 | −0.77 | −1.48 |
| United Kingdom | −0.61 | −0.67 | −1.28 |
| Switzerland | −0.44 | −0.73 | **−1.17** |

![transition versus physical](../figures/fig1_transition_vs_physical.png)

Two features stand out. The transition channel dominates in ten of the thirteen
regions, with a mean of −2.20 per cent against −1.01 per cent for physical
damage, so under an ambitious decarbonisation path the cost of the policy
outweighs the cost of the warming it avoids at this horizon. But the *dispersion*
of the two channels could hardly be more different. Transition costs range over a
factor of eleven across regions, from Switzerland's −0.44 to China's −4.72, while
physical damages span only −0.67 to −1.37. The transition channel is a policy
variable; the physical channel is very nearly a constant.

That contrast becomes sharper when the scenario is changed rather than the
region, and §7 returns to it.

## 3. Cost pass-through

The pass-through parameter φ governs how much of the carbon charge a sector
passes downstream in its price rather than absorbing in its own margin. It has no
empirical counterpart that can be estimated here, and the original single-region
study treats it as its principal sensitivity, sweeping it across the whole unit
interval. The same is done here.

![pass-through](../figures/fig14_pass_through.png)

**Table 2.** Transition GVA shock at 2040, Net Zero 2050, by pass-through (%)

| φ | EU27 | CHN | USA | GBR | CHE | RUS | IND | TUR | RASIA | LAM | MEA | AFR | ROW |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 0.0 | −2.93 | −14.36 | −3.27 | −1.85 | −0.71 | −12.45 | −20.90 | −10.92 | −9.44 | −10.47 | −8.62 | −15.90 | −10.37 |
| 0.2 | −2.23 | −10.96 | −2.34 | −1.40 | −0.62 | −8.95 | −14.83 | −8.07 | −7.12 | −7.41 | −6.04 | −10.82 | −7.36 |
| 0.4 | −1.42 | −7.01 | −1.29 | −0.90 | −0.51 | −5.03 | −8.04 | −4.75 | −4.45 | −3.99 | −3.18 | −5.29 | −4.00 |
| **0.5** | **−0.96** | **−4.72** | **−0.71** | **−0.61** | **−0.44** | **−2.86** | **−4.29** | **−2.86** | **−2.91** | **−2.11** | **−1.61** | **−2.31** | **−2.14** |
| 0.6 | −0.43 | −2.13 | −0.08 | −0.28 | −0.35 | −0.48 | −0.24 | −0.77 | −1.18 | −0.08 | +0.07 | +0.83 | −0.13 |
| 0.8 | +0.90 | +4.44 | +1.39 | +0.54 | −0.03 | +5.09 | +9.10 | +4.24 | +3.13 | +4.59 | +3.89 | +7.76 | +4.50 |
| 1.0 | +2.93 | +14.36 | +3.27 | +1.85 | +0.71 | +12.45 | +20.90 | +10.92 | +9.44 | +10.47 | +8.62 | +15.90 | +10.37 |

Three things emerge, and the first two are structural rather than empirical.

**The endpoints are exact.** At φ = 0 the shock equals minus the region's carbon
bill over its value added; at φ = 1 it equals plus the same quantity. India's
±20.90 per cent is exactly its carbon charge as a share of value added, and the
symmetry holds to machine precision for every region. This is a property of the
Leontief dual rather than a numerical coincidence, and it makes the two endpoints
useful analytic anchors: at neither extreme does the input–output structure matter
at all, and everything interesting happens in between.

**Every region's shock changes sign, and near the same place.** The crossings
cluster between φ = 0.574 for Africa and φ = 0.676 for the United Kingdom, with
Switzerland the sole outlier at 0.812. The clustering is not obvious in advance:
it says that although regions differ enormously in *how much* the charge costs
them, they agree closely on *how much pass-through it takes* before the charge
stops being a cost at all. Note that the crossing is above one-half, so at the
reported φ = 0.5 every region is still a net loser — the dual is not linear in φ,
and the midpoint is not the neutral point.

**Pass-through leaves the rate and exchange-rate channels completely untouched.**
This is the most consequential finding of the sweep. Across the whole range from
φ = 0 to φ = 1, India's policy rate shift is −68.515 basis points and its
five-year forward −3.6101 per cent, at every single value, with a range of
exactly zero. The reason is structural: under the specification adopted here the
Taylor rule responds to inflation and physical damage, and neither quantity
passes through the Leontief dual, so φ cannot reach them. What φ does reach is
value added, and through value added the equity and credit channels — India's
median credit spread swings from +42.0 per cent at φ = 0 to −42.0 at φ = 1.

The practical implication is that the widest single uncertainty in the model is
confined to two of the four financial channels. Results for exchange rates and
interest rates below can be read without any pass-through caveat at all; results
for credit and equity cannot.

## 4. Inflation and interest rates

Carbon pricing raises consumer prices in proportion to the fraction of a region's
emissions actually subject to a price, and central banks are assumed to respond
through a Taylor rule whose output-gap term is the damage function. Table 3
reports the resulting policy-rate shift.

**Table 3.** Policy-rate shift, Net Zero 2050 (basis points)

| Region | 2025 | 2030 | 2035 | 2040 | 2045 |
|---|--:|--:|--:|--:|--:|
| India | −47.5 | −56.5 | −64.0 | **−68.5** | −69.9 |
| Africa | −46.9 | −46.4 | −63.1 | −66.9 | −67.0 |
| Middle East | −42.9 | −51.0 | −57.8 | −61.9 | −63.1 |
| Türkiye | −38.1 | −45.3 | −51.3 | −54.9 | −56.1 |
| Rest of Asia | −38.5 | −40.2 | −51.5 | −54.4 | −55.4 |
| China | −39.3 | −34.3 | −52.1 | −54.2 | −55.0 |
| Latin America | −36.7 | −35.2 | −49.9 | −50.8 | −52.1 |
| Rest of World | −33.2 | −33.9 | −44.3 | −47.0 | −47.7 |
| Russia | −29.6 | −35.1 | −39.8 | −42.6 | −43.5 |
| EU27 | −28.8 | −16.7 | −35.9 | −39.0 | −38.9 |
| United States | −26.7 | −29.3 | −35.6 | −38.1 | −38.8 |
| Switzerland | −25.3 | −18.6 | −32.2 | −34.9 | −35.0 |
| United Kingdom | −23.4 | −19.0 | −30.1 | −32.4 | **−32.7** |

Every region cuts rates, in every scenario, at every horizon: across the full set
of ninety-one region-scenario pairs there is not one positive rate shift. This is
less a statement about central-bank behaviour than about relative magnitudes.
Carbon-driven inflation deviations are a few basis points, while damages are of
order one per cent of output, so the output-gap term outweighs the inflation term
by roughly two orders of magnitude and the net effect of climate stress in this
model is unambiguously disinflationary. The deepest cut anywhere in the results is
−81.6 basis points, for India under Fragmented World at 2045.

The one horizon at which the inflation term genuinely competes is 2030, where it
contributes +17.4 basis points against −34.2 of damage for the EU27 — slightly
more than the whole net move. This is an artefact of the scenario data rather
than of the model: NGFS publishes carbon prices on a five-year grid with a zero
in 2025, so linear interpolation produces a constant \$67.56 per tonne annual
increment through 2026–2030 against \$9.53 in the late 2030s. Because the
inflation channel responds to the annual *increment* rather than the level, it
spikes in that first segment and subsides thereafter, contributing only 6 per
cent of the EU's rate move by 2040. Every path in this section carries a
corresponding kink at 2030, and it should be read as a property of the
publication grid.

### 4.1 The term structure

The Hull–White expansion converts the short-rate shift into a shift at each
maturity. Because the mean-reversion parameter is shared across regions, the
curve rescales the short-rate shift without reordering anything.

**Table 4.** Zero-rate shift by tenor at 2040, Net Zero 2050 (basis points)

| Region | 1D | 6M | 1Y | 5Y | 10Y | 20Y |
|---|--:|--:|--:|--:|--:|--:|
| India | −68.5 | −67.8 | −67.2 | −62.1 | −56.5 | −47.2 |
| Africa | −66.9 | −66.3 | −65.6 | −60.7 | −55.2 | −46.1 |
| China | −54.2 | −53.6 | −53.1 | −49.1 | −44.7 | −37.3 |
| EU27 | −39.0 | −38.6 | −38.2 | −35.3 | −32.1 | −26.8 |
| United Kingdom | −32.4 | −32.1 | −31.8 | −29.4 | −26.7 | −22.3 |

The twenty-year shift is 0.6884 of the one-day shift for every region without
exception, matching the analytic ratio B(20)/20 = 0.6883 implied by a = 0.04.
This is a useful check that the expansion is behaving, but it is also a
limitation worth stating: a single mean-reversion parameter cannot express the
possibility that some economies' curves would steepen under climate stress while
others flatten. All cross-region variation in this model lives in the short rate.

## 5. Exchange rates

Exchange rates follow the original study's route of taking the difference between
regions' yield-curve changes, which separates naturally into a spot component
driven by relative purchasing-power parity and a forward component driven by
covered interest parity. Rates are quoted as units of the local currency per
euro, so a negative figure indicates appreciation against the euro.

**Table 5.** FX shift against the euro, Net Zero 2050 (per cent)

| | Spot 2040 | Spot 2045 | 5y forward 2040 | 5y forward 2045 |
|---|--:|--:|--:|--:|
| Indian rupee | −2.27 | −2.61 | −3.61 | **−4.01** |
| Turkish lira | −2.27 | −2.61 | −3.00 | −3.38 |
| US dollar | −1.95 | −2.24 | −1.91 | −2.23 |
| Chinese yuan | −0.70 | −0.76 | −1.39 | −1.49 |
| Pound sterling | −1.12 | −1.29 | −0.83 | −1.01 |
| Swiss franc | −0.78 | −0.89 | −0.59 | **−0.71** |

![FX ranking](../figures/fig2_fx_forward_ranking.png)

The first thing to say about this table is that a strengthening currency is not
good news. Appreciation here reflects damage forcing deep rate cuts, which under
covered interest parity produce a forward premium; the ordering is closer to an
ordering of harm than of resilience. India and Türkiye lead it because they score
badly on both relevant attributes at once — negligible carbon pricing, so no
offsetting inflation, and high exposure, so deep cuts.

Two properties of this cross-section are structural rather than empirical.

Every currency appreciates against the euro on the spot leg, and this is forced
rather than observed. The EU27 holds the highest carbon-pricing coverage in the
set at 0.645, against 0.467 for the next-highest, so every other region imports
less carbon inflation than the base region and relative parity requires its
currency to strengthen. The result would reverse for any economy that came to
price carbon more heavily than the EU, and nothing in the mechanism prevents that.

The spot leg also carries very little independent information. Its correlation
with carbon-pricing coverage is +0.9999, which is close to mechanical: the six
currencies map onto only three distinct NGFS carbon-price paths, so the price
varies by less than one per cent across the cross-section and the spot vector is
very nearly a rescaling of the coverage vector. India and Türkiye, which both
price nothing, are identical on spot to every reported digit. The forward leg is
the more informative of the two, correlating +0.79 with physical damage and −0.83
with carbon intensity against +0.45 and −0.53 for spot.

![two channels](../figures/fig12_two_fx_channels.png)

## 6. Credit, equity and operational risk

The credit channel blends sector-level value-added shocks into synthetic indices
using the original study's published index weights, then transmits them through
its estimated regression slopes.

![credit](../figures/fig13_credit_spreads.png)

**Table 6.** CDS spread change at 2040, Net Zero 2050, median across regions (%)

| Health Care | Utilities | Basic Materials | Consumer Goods | Industrials | Oil & Gas | Consumer Svs | Government | Telecoms | Technology | Financials | Real Estate |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 25.2 | 17.5 | 14.5 | 13.2 | 11.4 | 10.0 | 2.9 | 2.5 | 0.7 | 0.4 | −1.1 | −3.4 |

Credit is the most sector-specific of the channels: decomposing the variance
across the thirteen-by-twelve grid attributes 61 per cent of it to the sector and
only 19 per cent to the region. The widest single cell is Indian health care at
+71.3 per cent; by region the medians run from India at +14.2 down to
Switzerland at +1.5.

The regression slope fixes the sign of each index exactly — all ten
negative-slope indices widen and both positive-slope indices narrow, across all
thirteen regions without exception — but accounts for only about half the
variation in size, correlating −0.65 with the median widening. The remainder
comes from which sectors each index is built from.

Financials and UK real estate narrow rather than widen, and this deserves to be
read carefully. The original study's own estimates give both a positive slope, so
that a fall in value added compresses their spreads. That is a property of the
sample those regressions were estimated on, and it is inherited unchanged here.
It should not be read as a finding that climate stress improves bank or property
credit.

**Table 7.** Equity and operational risk at 2040, Net Zero 2050 (%)

| Region | Equity | β | Conduct losses | Base unemployment |
|---|--:|--:|--:|--:|
| Rest of Asia | −8.04 | 2.00* | +10.2 | 2.83 |
| India | −7.82 | 1.38 | +5.6 | 4.82 |
| Türkiye | −7.50 | 1.89 | +2.1 | 10.46 |
| Russia | −7.42 | 2.00* | +4.3 | 3.87 |
| Africa | −7.33 | 2.00* | +3.3 | 8.03 |
| United States | −2.36 | 1.59 | +8.3 | 3.65 |
| Switzerland | −2.35 | 2.00* | +6.9 | 4.12 |
| China | −1.54 | 0.26 | +4.5 | 4.98 |
| EU27 | −1.43 | 0.80 | +5.3 | 6.16 |
| United Kingdom | −0.70 | 0.55 | +4.3 | 3.77 |

\* proxy value, applied where no index history is available.

![equity and operational risk](../figures/fig6_equity_oprisk.png)

The equity and operational-risk orderings differ sharply, and the reason is
instructive. Equity runs on the total value-added shock through a market beta;
operational risk runs on physical damage alone through Okun's law and the *base
unemployment rate*. Türkiye is third-worst on equity and last on operational risk
because its base unemployment of 10.5 per cent makes a given rise a small
relative change, while Rest of Asia's 2.8 per cent makes the same rise a large
one. The denominator, not the shock, drives that ranking.

The equity column should be read with the asterisks in mind: seven of thirteen
regions share the proxy beta of 2.00 for want of an index history, so part of
what looks like a cross-section of exposure is a cross-section of data
availability.

## 7. Scenario dependence and uncertainty

Repeating the exercise across all seven NGFS narratives separates what policy
chooses from what it does not.

**Table 8.** Channel responses at 2040 (2045 for FX range), by scenario

| Scenario | Transition mean (%) | Physical mean (%) | FX forward range (pp) | Credit median (%) |
|---|--:|--:|--:|--:|
| Net Zero 2050 | −2.20 | −1.01 | 3.30 | 3.95 |
| Low demand | −1.19 | −1.02 | 2.43 | 2.46 |
| Delayed transition | −0.88 | −1.09 | 2.12 | 2.14 |
| Below 2 °C | −0.68 | −1.05 | 2.08 | 1.89 |
| NDCs | −0.58 | −1.07 | 2.02 | 1.79 |
| Fragmented World | −0.27 | −1.09 | 1.91 | 1.12 |
| Current Policies | −0.06 | −1.07 | 1.88 | 0.82 |

The transition mean varies by a factor of thirty-seven across the seven
narratives; the physical mean varies by eight per cent. Warming to 2040 is
largely determined by emissions already committed, so scenario choice moves the
cost of the policy but barely touches the cost of the climate.

This asymmetry propagates unevenly. Credit spans a factor of 4.8 across the
scenarios because it is driven almost entirely by the transition channel.
Exchange rates span only 1.8, because the two components move in opposite
directions — ambitious policy means a high carbon price and large spot dispersion
but low warming, while weak policy means the reverse — leaving a floor of roughly
1.9 percentage points of FX dispersion that no scenario removes. The
policy-relevant version of that statement is that transition risk is a choice and
physical risk, at this horizon, is not.

![scenario inputs](../figures/fig7_scenario_inputs.png)

### 7.1 Weighting the scenarios, and the tail

Treating the narratives as a mixture rather than a menu gives an expected shift
under each of four priors. The construction is the Dirichlet-categorical one of
the original study: a prior concentration α over the narratives, a conjugate
update by observed events, and an expectation taken against the resulting
categorical weights. Three of the priors are asserted — a uniform baseline and
two illustrative bookends — while the fourth, *consensus*, is built by weighting
each narrative by a Gaussian in its own end-century warming around the 2.7 °C
that UNEP and Climate Action Tracker put current policy on. That fourth prior is
the analogue of the original study's 90 per cent mass on SSP2 with RCP4.5, and
is constructed for the same reason: to anchor the weights on a published
statement about where policy actually leads rather than on the modeller's taste.

Two differences from the original are worth stating, because the mixture does
less work here than it does there.

The first is that only the **mean** of the Dirichlet is used. The weights
reported below are α_s / Σα, and the expectation is their inner product with the
per-scenario results; the distribution is never sampled. A consequence is that
the concentration parameter, set at Σα = 14, does not affect any number in this
section — rescaling it leaves every weight identical, since it cancels in the
mean. It governs only how much observed evidence would be needed to move the
prior, and would begin to matter if the conjugate update were used in earnest:
three observations attributed to Current Policies raise that narrative's weight
from 14.3 to 29.4 per cent at Σα = 14, but only to 16.1 per cent at Σα = 140.

The second is that the original study *samples* the Dirichlet, and its tail comes
from that sampling. Because it draws SSP and RCP weights independently while only
certain pairings are admissible, a draw can place its mass on a combination that
does not exist, losing most of its weight and collapsing the associated shock
towards zero; the 99.9th percentile is generated by those degenerate draws. That
mechanism cannot arise here. The NGFS narratives form a single exhaustive
dimension with no feasibility restrictions, so weights always sum to one and no
mass can be lost. The tail reported below therefore comes from stressing the
model's *inputs* rather than reweighting its scenarios, which is a different
object and is treated as such.

**Table 9.** Expected five-year forward at 2040, by prior (%)

| Prior | INR | TRY | CNY | USD | GBP | CHF |
|---|--:|--:|--:|--:|--:|--:|
| Ambition | −2.31 | −1.67 | −1.03 | −0.75 | −0.15 | −0.12 |
| Uniform | −2.04 | −1.40 | −0.95 | −0.51 | −0.01 | −0.02 |
| Policy-sceptic | −1.75 | −1.10 | −0.88 | −0.25 | +0.15 | +0.08 |
| Consensus | −1.35 | −0.69 | −0.74 | +0.10 | +0.35 | +0.22 |

![mixture](../figures/fig3_mixture_expected_fx.png)

The prior matters most where the move is largest — a factor of 1.7 on the rupee
between the most and least ambitious weightings. For sterling and the franc it
changes the sign, but on moves of a few tenths of a percentage point, where the
sign is not the quantity of interest.

Stressing the inputs by 1.64 standard deviations, taking temperature from the
MAGICC ensemble and the carbon price from the cross-model spread, widens the tail
and, more interestingly, reorders it.

**Table 10.** Central and stressed five-year forward at 2040 (%)

| | Central | Stressed |
|---|--:|--:|
| INR | −3.61 | −4.09 |
| TRY | −3.00 | −4.01 |
| USD | −1.91 | −3.37 |
| CNY | −1.39 | −2.20 |
| GBP | −0.83 | −1.91 |
| CHF | −0.59 | −1.32 |

![at-risk band](../figures/fig4_fx_at_risk_band.png)

Every currency moves further from the euro under stress, and the ordering
changes: the lira overtakes the dollar and the gap between the rupee and the lira
nearly closes. The stress widens the dispersion rather than shifting a level,
which is the correct behaviour for a channel defined by relative prices.

## 8. The channels do not agree

Ranking the worst-affected regions by each channel produces four different
answers.

**Table 11.** Five worst-affected regions, by channel, 2040 Net Zero

| Channel | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| FX forward | India | Türkiye | **United States** | China | UK |
| Policy rate | India | Africa | Middle East | Türkiye | Rest of Asia |
| Credit | India | China | Africa | Russia | Türkiye |
| Equity | **Rest of Asia** | India | Türkiye | Russia | Africa |

India is first or second everywhere, and beyond that the orderings diverge. Each
divergence is traceable to what the channel weights.

The United States is third on exchange rates and twelfth on credit. Exchange
rates are a *relative* price against the euro, and the US pays for pricing almost
none of its emissions while the EU prices most of them; its currency moves on a
differential it did not choose. Credit is an *absolute* shock, and the US economy
is not carbon-intensive, so its spreads barely move.

Rest of Asia is first on equity and sixth on credit, partly because it carries
the proxy beta of 2.00 where China's fitted beta is 0.26.

Africa is second on rates and third on credit but appears in no exchange-rate
result at all, because it is a structural region with no single analytical
currency — a limitation of the region selection rather than a statement about
African exchange rates.

The general conclusion is that "climate exposure" is not one quantity. The
channels weight the same two underlying shocks differently: exchange rates by
*relative* carbon pricing, policy rates by *absolute* damage, credit by *sectoral
composition*, and equity by the availability of a market beta. An institution
with European credit exposure, one with emerging-market currency exposure and one
with a domestic interest-rate position face identical warming and identical
carbon prices, and would rank their worst regions differently.

## 9. Limitations

Several caveats attach to the numbers above and should be carried into any
interpretation of them.

The credit betas are estimated on a single national sample and applied to every
region. The sign anomaly on financials and real estate is direct evidence that
those regressions carry period-specific structure, and there is no reason to
expect the spread-to-value-added elasticity to travel to Indian or African
credit. The same applies, more weakly, to the operational-risk slopes.

Seven of thirteen regions share one equity beta, so the equity cross-section is
partly an artefact of which regions have an accessible index history.

The exchange-rate cross-section rests on six currencies. Correlations computed on
six points are indicative rather than estimates, and none of the coefficients
reported in §5 should be quoted with a standard error.

Results are reported as *shifts* rather than levels, because the market curve
that would anchor them is deliberately omitted in order to isolate the
climate-attributable component. One consequence is that nothing here imposes a
zero lower bound on the implied policy rate.

The spot channel rests on relative purchasing-power parity, which is a poor
description of exchange rates at short horizons; the forward channel, resting on
covered interest parity, is the sounder of the two.

Finally, and most substantially, there is an unresolved ambiguity in the
currency to which the inflation coefficient should be applied. The original study
writes it against a dollar carbon price, but its own published results are
reproduced only when it is applied to a sterling price. This model applies it to
dollars. If the original reading is the correct one, every spot level reported
here is overstated by the sterling–dollar rate, roughly a third. The ratios
between currencies and their ordering are unaffected, since the factor is common
to both legs of every difference; the levels are not.

No external benchmark exists for the exchange-rate or credit numbers themselves.
The GDP shocks do sit inside the range of NGFS's own macroeconomic estimates,
which is some comfort about the scale of the underlying real shock, but a −4 per
cent forward on the rupee has nothing to be compared against.
