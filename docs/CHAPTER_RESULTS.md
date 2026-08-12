# Main Results

This section reports what the model produces when the machinery of the previous
chapter is applied to the thirteen-region calibration built from the OECD ICIO
tables. It follows the shock through the economy in the order the model computes
it: first the real-economy effects on value added, then the price and policy
response, and finally the three financial markets the exercise is aimed at —
exchange rates, interest rates and credit. Trade measures are held out entirely
and treated separately in the next section, so everything below is driven by
carbon pricing and warming alone.

## 1. Setup and reporting convention

### 1.1 The calibration in brief

The model resolves the world into thirteen regions covering 81 economies and 650
region-industry pairs, with a world gross output of \$199.7 trillion and value
added of \$93.8 trillion. Three region-level characteristics do most of the work
in what follows, and it is worth setting them out first, because almost every
ordering below can be traced to one of them.

| | most exposed | least exposed |
|---|---|---|
| Carbon intensity (t CO₂e / \$m) | India 574, Russia 467, Africa 456 | Switzerland 20, UK 61, EU27 87 |
| Carbon-pricing coverage | EU27 0.645, China 0.467, Switzerland 0.425 | India, Türkiye, Russia, Middle East all 0.000 |
| Physical vulnerability (ND-GAIN, world = 1) | India 1.34, Africa 1.34, Middle East 1.22 | UK 0.79, Switzerland 0.83, US 0.89 |

These three are close to independent of one another, which is why no single
ranking of "climate exposure" emerges from the results. India is extreme on two
of them; Switzerland is mild on all three; the EU is unusual in being the most
heavily *priced* economy while being among the least intensive.

### 1.2 Results are reported as a scenario mixture

The seven NGFS narratives are not competing forecasts to be chosen between. The
framework treats them as components of a Dirichlet-categorical mixture, so the
reported quantity is an expectation against a distribution over narratives rather
than the value under any one of them. That is the construction the single-region
study uses, and it is used here for the same reason: a scenario is a conditional
statement, and reporting one as though it were the answer silently assigns it
probability one.

Four priors are carried side by side, because NGFS deliberately publishes no
scenario probabilities and any single choice would be the modeller's rather than
the data's.

**Table 1.** Prior weights over the seven narratives (per cent)

| Narrative | End-century warming | Uniform | Policy-sceptic | Ambition | Consensus |
|---|--:|--:|--:|--:|--:|
| Net Zero 2050 | 1.45 °C | 14.3 | 6.2 | 23.5 | 0.0 |
| Low demand | 1.47 | 14.3 | 6.2 | 17.6 | 0.0 |
| Below 2 °C | 1.69 | 14.3 | 6.2 | 23.5 | 0.3 |
| Delayed transition | 1.75 | 14.3 | 12.5 | 11.8 | 0.5 |
| NDCs | 2.03 | 14.3 | 25.0 | 11.8 | 6.7 |
| Fragmented World | 2.11 | 14.3 | 18.8 | 5.9 | 11.8 |
| Current Policies | 2.75 | 14.3 | 25.0 | 5.9 | **80.7** |

*Uniform* is the conventional uninformative choice. *Policy-sceptic* and
*ambition* are asserted bookends whose directions are narrative logic and whose
magnitudes are arbitrary. *Consensus* is the only one anchored on a citable
source: each narrative is weighted by a Gaussian in its own end-century warming
around the 2.7 °C that the UNEP Emissions Gap Report and Climate Action Tracker
independently place current policy on. It concentrates 80.7 per cent on Current
Policies, which is the same role — and almost the same concentration — as the
single-region study's 90 per cent on SSP2 paired with RCP4.5.

Two properties of the construction should be stated, because the mixture does
less work here than in the original.

Only the **mean** of the Dirichlet is used: reported weights are α_s / Σα and the
expectation is their inner product with the per-scenario results. The
distribution is never sampled, which makes the concentration parameter inert for
every number below — rescaling Σα from 14 to 140 leaves every weight identical,
since it cancels in the mean. It governs only the stiffness of the conjugate
update, where it does bite: three observations attributed to Current Policies
would raise that weight from 14.3 to 29.4 per cent at Σα = 14 but only to 16.1
per cent at Σα = 140.

The original study *samples* its Dirichlet, and its extreme quantile comes from
that sampling: because SSP and RCP weights are drawn independently while only
certain pairings are admissible, a draw can place its mass on a combination that
does not exist and collapse towards zero. That mechanism cannot arise here. The
NGFS narratives form a single exhaustive dimension with no feasibility
restrictions, so weights always sum to one and no mass can be lost. The tail in
§7.3 therefore comes from stressing the model's inputs, which is a different
object and is labelled as one.

Where a single narrative is shown below it is **Net Zero 2050**, and it is shown
as a *component* — the case in which the transition channel is most visible, and
therefore an upper bound on it rather than a central estimate. Pass-through is
set at φ = 0.5 except in §3, where it is swept.

## 2. The real economy

The carbon charge enters as an ad-valorem cost wedge on each sector's own
emissions and propagates through the Leontief price dual; warming enters through
the Barrage–Nordhaus damage function, allocated across region-industries by
vulnerability.

**Table 2.** Total GDP shock at 2040, mixture-weighted (per cent of regional
value added)

| Region | Uniform | Policy-sceptic | Ambition | Consensus | *Net Zero component* |
|---|--:|--:|--:|--:|--:|
| India | **−3.00** | −2.47 | −3.47 | −1.67 | *−5.66* |
| China | −2.90 | −2.30 | −3.42 | −1.44 | *−5.86* |
| Africa | −2.43 | −2.21 | −2.65 | −1.60 | *−3.66* |
| Türkiye | −2.38 | −2.09 | −2.66 | −1.37 | *−3.96* |
| Rest of Asia | −2.22 | −1.87 | −2.54 | −1.33 | *−4.02* |
| Middle East | −1.99 | −1.84 | −2.14 | −1.43 | *−2.85* |
| Russia | −1.93 | −1.58 | −2.22 | −1.08 | *−3.71* |
| Latin America | −1.84 | −1.60 | −2.06 | −1.27 | *−3.17* |
| Rest of World | −1.80 | −1.56 | −2.03 | −1.13 | *−3.10* |
| EU27 | −1.23 | −1.12 | −1.33 | −0.92 | *−1.79* |
| United States | −1.07 | −0.99 | −1.14 | −0.84 | *−1.48* |
| Switzerland | −0.93 | −0.88 | −0.97 | −0.79 | *−1.17* |
| United Kingdom | **−0.93** | −0.87 | −0.99 | −0.74 | *−1.28* |

The decomposition into the two channels is what makes the prior matter at all.

**Table 3.** The two channels separately, at 2040, mean across regions (%)

| | Uniform | Policy-sceptic | Ambition | Consensus | Range |
|---|--:|--:|--:|--:|--:|
| Transition | −0.84 | −0.57 | −1.08 | −0.13 | **8.6×** |
| Physical | −1.06 | −1.07 | −1.05 | −1.08 | **1.03×** |

![transition versus physical](../figures/fig1_transition_vs_physical.png)

Physical damage is, to three per cent, the same number under every prior. This is
not a modelling assumption but a consequence of the scenario set: warming to 2040
is largely determined by emissions already committed, so the narratives that
disagree violently about carbon prices agree closely about temperature. The
transition channel, by contrast, moves by a factor of nearly nine depending on
what one believes about policy.

The practical reading is that **the physical results below can be quoted without
reference to the prior, and the transition results cannot.** Under the consensus
prior the transition channel nearly vanishes — a mean of −0.13 per cent — and
almost all of the remaining GDP shock is physical.

## 3. Cost pass-through

The pass-through parameter φ governs how much of the carbon charge a sector
passes downstream in price rather than absorbing in its own margin. It has no
empirical counterpart that can be estimated here, and the single-region study
treats it as its principal sensitivity, sweeping the whole unit interval. The
same is done here, on the Net Zero component so that the charge is large enough
for the sweep to be legible.

![pass-through](../figures/fig14_pass_through.png)

**Table 4.** Transition GVA shock at 2040, Net Zero 2050, by pass-through (%)

| φ | EU27 | CHN | USA | GBR | CHE | RUS | IND | TUR | RASIA | LAM | MEA | AFR | ROW |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 0.0 | −2.93 | −14.36 | −3.27 | −1.85 | −0.71 | −12.45 | −20.90 | −10.92 | −9.44 | −10.47 | −8.62 | −15.90 | −10.37 |
| 0.2 | −2.23 | −10.96 | −2.34 | −1.40 | −0.62 | −8.95 | −14.83 | −8.07 | −7.12 | −7.41 | −6.04 | −10.82 | −7.36 |
| 0.4 | −1.42 | −7.01 | −1.29 | −0.90 | −0.51 | −5.03 | −8.04 | −4.75 | −4.45 | −3.99 | −3.18 | −5.29 | −4.00 |
| **0.5** | **−0.96** | **−4.72** | **−0.71** | **−0.61** | **−0.44** | **−2.86** | **−4.29** | **−2.86** | **−2.91** | **−2.11** | **−1.61** | **−2.31** | **−2.14** |
| 0.6 | −0.43 | −2.13 | −0.08 | −0.28 | −0.35 | −0.48 | −0.24 | −0.77 | −1.18 | −0.08 | +0.07 | +0.83 | −0.13 |
| 0.8 | +0.90 | +4.44 | +1.39 | +0.54 | −0.03 | +5.09 | +9.10 | +4.24 | +3.13 | +4.59 | +3.89 | +7.76 | +4.50 |
| 1.0 | +2.93 | +14.36 | +3.27 | +1.85 | +0.71 | +12.45 | +20.90 | +10.92 | +9.44 | +10.47 | +8.62 | +15.90 | +10.37 |

Three things emerge, the first two structural rather than empirical.

**The endpoints are exact.** At φ = 0 the shock equals minus the region's carbon
bill over its value added, and at φ = 1 plus the same quantity; India's ±20.90
per cent is exactly that ratio, and the symmetry holds to machine precision for
every region. At neither extreme does the input–output structure matter at all,
which makes both useful analytic anchors.

**Every region's shock changes sign, and near the same place.** The crossings lie
between φ = 0.574 for Africa and φ = 0.676 for the United Kingdom, with
Switzerland the sole outlier at 0.812. Regions differ by a factor of eleven in
how much the charge costs them but agree closely on how much pass-through it
takes before it stops being a cost. All the crossings lie above one-half, so at
the reported φ = 0.5 every region is still a net loser: the dual is not linear in
φ, and the midpoint is not the neutral point.

**Pass-through leaves the rate and exchange-rate channels untouched.** Across the
whole range India's policy-rate shift is −68.515 basis points and its five-year
forward −3.6101 per cent, at every value, with a range of exactly zero. The
reason is structural: the Taylor rule responds to inflation and physical damage,
and neither passes through the Leontief dual, so φ cannot reach them. What φ does
reach is value added and, through it, credit and equity — India's median credit
spread swings from +42.0 per cent at φ = 0 to −42.0 at φ = 1.

The model's widest single parameter uncertainty is therefore confined to two of
the four financial channels. Interest-rate and exchange-rate results can be read
without any pass-through caveat; credit and equity cannot.

## 4. Interest rates

Carbon pricing raises consumer prices in proportion to the fraction of a region's
emissions actually subject to a price, and central banks are assumed to respond
through a Taylor rule whose output-gap term is the damage function.

**Table 5.** Policy-rate shift at 2040, mixture-weighted (basis points)

| Region | Uniform | Policy-sceptic | Ambition | Consensus | *Net Zero component* |
|---|--:|--:|--:|--:|--:|
| India | **−71.7** | −72.4 | −70.9 | −72.7 | *−68.5* |
| Africa | −70.2 | −71.1 | −69.4 | −71.7 | *−66.9* |
| Middle East | −64.7 | −65.4 | −64.0 | −65.7 | *−61.9* |
| Rest of Asia | −57.7 | −58.4 | −56.9 | −58.9 | *−54.4* |
| Türkiye | −57.5 | −58.1 | −56.9 | −58.3 | *−54.9* |
| China | −58.3 | −59.3 | −57.3 | −60.1 | *−54.2* |
| Latin America | −54.7 | −55.6 | −53.9 | −56.2 | *−50.8* |
| Rest of World | −49.7 | −50.4 | −49.0 | −50.8 | *−47.0* |
| Russia | −44.6 | −45.1 | −44.1 | −45.3 | *−42.6* |
| EU27 | −42.1 | −43.1 | −41.3 | −44.0 | *−39.0* |
| United States | −40.1 | −40.6 | −39.6 | −40.9 | *−38.1* |
| Switzerland | −37.3 | −38.1 | −36.7 | −38.7 | *−34.9* |
| United Kingdom | **−34.6** | −35.2 | −34.1 | −35.7 | *−32.4* |

**The rate channel is nearly invariant to the prior**, moving by only six per
cent across the four for the EU27 and four per cent on the cross-region mean.
This follows directly from §2: the Taylor rule's output-gap term is physical
damage, and physical damage barely responds to the scenario weighting. The rate
results are therefore the most robust in this section — and, notably, the
mixture rates are slightly *deeper* than the Net Zero component, because the
narratives with lower carbon prices have higher warming.

Every region cuts, in every scenario, at every horizon: across ninety-one
region-scenario pairs there is not one positive rate shift. Carbon-driven
inflation deviations are a few basis points while damages are of order one per
cent of output, so the output-gap term outweighs the inflation term by roughly
two orders of magnitude and climate stress in this model is unambiguously
disinflationary. The deepest cut anywhere is −81.6 basis points, for India under
Fragmented World at 2045.

The one horizon at which the inflation term competes is 2030, where it
contributes +17.4 basis points against −34.2 of damage for the EU27. This is an
artefact of the scenario data rather than the model: NGFS publishes carbon prices
on a five-year grid with a zero in 2025, so linear interpolation produces a
constant \$67.56 per tonne annual increment through 2026–2030 against \$9.53 in
the late 2030s. Because the inflation channel responds to the annual *increment*
rather than the level, it spikes in that first segment and subsides to 6 per cent
of the EU's rate move by 2040. Every path in this section carries a corresponding
kink at 2030.

### 4.1 The term structure

The Hull–White expansion converts the short-rate shift into a shift at each
maturity. Because the mean-reversion parameter is shared, the curve rescales the
short-rate shift without reordering anything.

**Table 6.** Zero-rate shift by tenor at 2040, Net Zero component (basis points)

| Region | 1D | 6M | 1Y | 5Y | 10Y | 20Y |
|---|--:|--:|--:|--:|--:|--:|
| India | −68.5 | −67.8 | −67.2 | −62.1 | −56.5 | −47.2 |
| Africa | −66.9 | −66.3 | −65.6 | −60.7 | −55.2 | −46.1 |
| China | −54.2 | −53.6 | −53.1 | −49.1 | −44.7 | −37.3 |
| EU27 | −39.0 | −38.6 | −38.2 | −35.3 | −32.1 | −26.8 |
| United Kingdom | −32.4 | −32.1 | −31.8 | −29.4 | −26.7 | −22.3 |

The twenty-year shift is 0.6884 of the one-day shift for every region without
exception, matching the analytic ratio B(20)/20 = 0.6883 implied by a = 0.04.
That is a useful check that the expansion behaves, and also a limitation: a
single mean-reversion parameter cannot express that some economies' curves would
steepen under climate stress while others flatten. All cross-region variation in
this model lives in the short rate.

## 5. Exchange rates

Exchange rates follow the original study's route of differencing regions'
yield-curve changes, which separates into a spot component driven by relative
purchasing-power parity and a forward component driven by covered interest
parity. Rates are quoted as units of local currency per euro, so a negative
figure is appreciation against the euro.

**Table 7.** Five-year forward against the euro at 2040, mixture-weighted (%)

| | Uniform | Policy-sceptic | Ambition | Consensus | *Net Zero component* |
|---|--:|--:|--:|--:|--:|
| Indian rupee | **−2.04** | −1.75 | −2.31 | −1.35 | *−3.61* |
| Turkish lira | −1.40 | −1.10 | −1.67 | −0.69 | *−3.00* |
| Chinese yuan | −0.95 | −0.88 | −1.03 | −0.74 | *−1.39* |
| US dollar | −0.51 | −0.25 | −0.75 | **+0.10** | *−1.91* |
| Swiss franc | −0.02 | +0.08 | −0.12 | **+0.22** | *−0.59* |
| Pound sterling | −0.01 | +0.15 | −0.15 | **+0.35** | *−0.83* |

![FX ranking](../figures/fig2_fx_forward_ranking.png)

The first thing to say is that a strengthening currency is not good news.
Appreciation here reflects damage forcing deep rate cuts, which under covered
interest parity produce a forward premium; the ordering is closer to an ordering
of harm than of resilience. India and Türkiye lead it because they score badly on
both relevant attributes at once — negligible carbon pricing, so no offsetting
inflation, and high exposure, so deep cuts.

**The prior changes signs, and it does so for exactly the currencies whose moves
are small.** The dollar, franc and sterling all appreciate against the euro under
the ambition prior and *depreciate* under consensus. The mechanism is clear
enough: these are the three currencies whose net position depends on the balance
between an inflation differential that shrinks as the carbon price falls and a
damage differential that does not. Nothing in the model resolves which sign is
right, because that depends on scenario weights the data does not supply. What
can be said is that the moves in question are a few tenths of a percentage point,
where the sign is not the interesting quantity; the rupee and the lira, whose
moves are an order of magnitude larger, keep their sign under every prior.

Two properties of the cross-section are structural rather than empirical.

Every currency appreciates on the spot leg under every prior, and this is forced.
The EU27 holds the highest carbon-pricing coverage in the set at 0.645 against
0.467 for the next, so every other region imports less carbon inflation than the
base and relative parity requires its currency to strengthen. The result would
reverse for any economy that came to price carbon more heavily than the EU.

The spot leg also carries very little independent information. Its correlation
with carbon-pricing coverage is +0.9999 on the Net Zero component, which is close
to mechanical: the six currencies map onto only three distinct NGFS carbon-price
paths, so the price varies by less than one per cent across the cross-section and
the spot vector is very nearly a rescaling of the coverage vector. India and
Türkiye, which both price nothing, are identical on spot to every reported digit.
The forward leg is the more informative, correlating +0.79 with physical damage
and −0.83 with carbon intensity, against +0.45 and −0.53 for spot.

Spot is also by some distance the most prior-sensitive quantity in the model: the
rupee's spot move ranges over a factor of **22.7** across the four priors,
against 1.7 for its forward. The spot leg is pure transition risk, and transition
risk is what the prior is about.

![two channels](../figures/fig12_two_fx_channels.png)

## 6. Credit, equity and operational risk

The credit channel blends sector-level value-added shocks into synthetic indices
using the original study's published index weights, then transmits them through
its estimated regression slopes.

![credit](../figures/fig13_credit_spreads.png)

**Table 8.** CDS spread change at 2040, median across indices, mixture-weighted (%)

| Region | Uniform | Policy-sceptic | Ambition | Consensus | *Net Zero component* |
|---|--:|--:|--:|--:|--:|
| India | **5.90** | 4.24 | 7.36 | 1.78 | *14.2* |
| China | 4.37 | 3.37 | 5.24 | 1.93 | *9.3* |
| Africa | 4.33 | 3.58 | 5.08 | 1.59 | *8.5* |
| Türkiye | 4.20 | 3.46 | 4.92 | 1.67 | *8.2* |
| Russia | 3.59 | 2.66 | 4.38 | 1.33 | *8.3* |
| Rest of Asia | 3.45 | 2.72 | 4.09 | 1.62 | *7.1* |
| Rest of World | 2.85 | 2.21 | 3.46 | 1.10 | *6.2* |
| Latin America | 2.37 | 1.80 | 2.92 | 1.02 | *5.6* |
| Middle East | 2.06 | 1.73 | 2.39 | 0.90 | *3.9* |
| EU27 | 2.04 | 1.70 | 2.36 | 1.04 | *3.8* |
| United Kingdom | 1.46 | 1.24 | 1.67 | 0.84 | *2.6* |
| United States | 1.16 | 0.92 | 1.40 | 0.49 | *2.4* |
| Switzerland | **1.05** | 0.95 | 1.14 | 0.78 | *1.5* |

Credit is the most sector-specific of the channels: decomposing the variance
across the thirteen-by-twelve grid attributes 68 per cent of it to the sector and
only 16 per cent to the region. Under the consensus prior the sector ordering is
health care +4.9 per cent, basic materials +2.9, consumer goods +2.7 and
utilities +2.2, with financials and real estate negative.

The regression slope fixes the sign of each index exactly — all ten
negative-slope indices widen and both positive-slope indices narrow, across all
thirteen regions without exception — but accounts for only about half the
variation in size, correlating −0.67 with the median widening. The remainder
comes from which sectors each index is built from.

Financials and UK real estate narrow rather than widen, and this deserves care.
The original study's own estimates give both a positive slope, so a fall in value
added compresses their spreads. That is a property of the sample those
regressions were estimated on, and it is inherited unchanged here. It should not
be read as a finding that climate stress improves bank or property credit.

**Table 9.** Equity and operational risk at 2040, uniform prior (%)

| Region | Equity | β | Conduct losses | Base unemployment |
|---|--:|--:|--:|--:|
| Africa | −4.86 | 2.00* | +3.45 | 8.03 |
| Türkiye | −4.50 | 1.89 | +2.15 | 10.46 |
| Rest of Asia | −4.45 | 2.00* | **+10.71** | 2.83 |
| India | −4.14 | 1.38 | +5.82 | 4.82 |
| Middle East | −3.98 | 2.00* | +4.25 | 5.97 |
| United States | −1.70 | 1.59 | +8.64 | 3.65 |
| Switzerland | −1.86 | 2.00* | +7.26 | 4.12 |
| EU27 | −0.98 | 0.80 | +5.52 | 6.16 |
| China | −0.76 | 0.26 | +4.66 | 4.98 |
| United Kingdom | −0.51 | 0.55 | +4.45 | 3.77 |

\* proxy value, applied where no index history is available.

![equity and operational risk](../figures/fig6_equity_oprisk.png)

The two orderings differ sharply, and the reason is instructive. Equity runs on
the total value-added shock through a market beta; operational risk runs on
physical damage alone through Okun's law and the *base unemployment rate*.
Türkiye is second-worst on equity and last on operational risk because its base
unemployment of 10.5 per cent makes a given rise a small relative change, while
Rest of Asia's 2.8 per cent makes the same rise a large one. The denominator, not
the shock, drives that ranking — and operational risk, being physical-driven, is
as prior-insensitive as the rate channel, at 1.03 across the four.

The equity column should be read with the asterisks in mind: seven of thirteen
regions share the proxy beta of 2.00 for want of an index history, so part of
what looks like a cross-section of exposure is a cross-section of data
availability.

## 7. Where the uncertainty lies

### 7.1 The prior matters for some channels and not others

Collecting the prior sensitivity of every channel gives the section's organising
result.

**Table 10.** Range across the four priors at 2040 (max ÷ min)

| Channel | Range | Driven by |
|---|--:|---|
| Spot FX (rupee) | **22.7×** | carbon price |
| Transition GVA (mean) | 8.6× | carbon price |
| Credit (India median) | 4.1× | carbon price |
| Total GDP (mean) | 1.8× | both |
| Equity (mean) | 1.7× | both |
| Forward FX (rupee) | 1.7× | both |
| **Policy rate (mean)** | **1.04×** | physical damage |
| **Operational risk** | **1.03×** | physical damage |
| **Physical damage (mean)** | **1.03×** | physical damage |

![prior sensitivity](../figures/fig15_prior_sensitivity.png)

The split is clean, and it is the same distinction that ran through §2: channels
carrying the carbon charge inherit the full disagreement between the narratives,
while channels carrying physical damage are nearly indifferent to it. An
institution whose exposure runs through interest rates or employment can take
these results without holding a view on climate policy. One whose exposure runs
through carbon-intensive credit or the spot currency cannot, and should quote a
range rather than a number.

### 7.2 What the mixture is made of

**Table 11.** Per-scenario components at 2040 (2045 for the FX range)

| Scenario | Transition mean (%) | Physical mean (%) | FX forward range (pp) | Credit median (%) |
|---|--:|--:|--:|--:|
| Net Zero 2050 | −2.20 | −1.01 | 3.30 | 3.95 |
| Low demand | −1.19 | −1.02 | 2.43 | 2.46 |
| Delayed transition | −0.88 | −1.09 | 2.12 | 2.14 |
| Below 2 °C | −0.68 | −1.05 | 2.08 | 1.89 |
| NDCs | −0.58 | −1.07 | 2.02 | 1.79 |
| Fragmented World | −0.27 | −1.09 | 1.91 | 1.12 |
| Current Policies | −0.06 | −1.07 | 1.88 | 0.82 |

The transition mean varies by a factor of thirty-seven across the narratives; the
physical mean by eight per cent. Exchange rates span only 1.8 because their two
components move in opposite directions — ambitious policy means a high carbon
price and large spot dispersion but low warming, weak policy the reverse —
leaving a floor of roughly 1.9 percentage points of dispersion that no narrative
removes. Transition risk is a policy choice; physical risk, at this horizon, is
not.

![scenario inputs](../figures/fig7_scenario_inputs.png)

### 7.3 The tail

Stressing the inputs by 1.64 standard deviations, taking temperature from the
MAGICC ensemble and the carbon price from the cross-model spread, widens the
distribution and reorders it.

**Table 12.** Central and stressed five-year forward at 2040, Net Zero component (%)

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
nearly closes. The stress widens dispersion rather than shifting a level, which
is the correct behaviour for a channel defined by relative prices.

![mixture](../figures/fig3_mixture_expected_fx.png)

## 8. The channels do not agree

Ranking the worst-affected regions by each channel, under the uniform prior,
produces four different answers.

**Table 13.** Five worst-affected regions by channel, 2040

| Channel | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| FX forward | India | Türkiye | China | **United States** | Switzerland |
| Policy rate | India | Africa | Middle East | China | Rest of Asia |
| Credit | India | China | Africa | Türkiye | Russia |
| Equity | **Africa** | Türkiye | Rest of Asia | India | Middle East |

India is first everywhere, and beyond that the orderings diverge. Each divergence
is traceable to what the channel weights.

The United States is high on exchange rates and twelfth on credit. Exchange rates
are a *relative* price against the euro, and the US pays for pricing almost none
of its emissions while the EU prices most of them; its currency moves on a
differential it did not choose. Credit is an *absolute* shock, and the US economy
is not carbon-intensive, so its spreads barely move.

Africa leads on equity while sitting second on rates, because equity compounds a
large total shock with a proxy beta of 2.00 that the model cannot verify.

Africa and the Middle East appear in no exchange-rate result at all, because they
are structural regions with no single analytical currency — a limitation of the
region selection rather than a statement about their exchange rates.

The general conclusion is that "climate exposure" is not one quantity. The
channels weight the same two underlying shocks differently: exchange rates by
*relative* carbon pricing, policy rates by *absolute* damage, credit by *sectoral
composition*, and equity partly by the availability of a market beta. An
institution with European credit exposure, one with emerging-market currency
exposure and one with a domestic interest-rate position face identical warming
and identical carbon prices, and would rank their worst regions differently.

## 9. Limitations

Several caveats attach to the numbers above and should be carried into any
interpretation of them.

The prior is not data. NGFS publishes no scenario probabilities, and three of the
four priors used here are the modeller's construction; only the consensus prior
is anchored on a citable external estimate. Reporting four side by side is a way
of being honest about that rather than a way of resolving it, and §7.1 identifies
which results survive the choice.

The credit betas are estimated on a single national sample and applied to every
region. The sign anomaly on financials and real estate is direct evidence that
those regressions carry period-specific structure, and there is no reason to
expect the spread-to-value-added elasticity to travel to Indian or African
credit. The same applies, more weakly, to the operational-risk slopes.

Seven of thirteen regions share one equity beta, so that cross-section is partly
an artefact of which regions have an accessible index history.

The exchange-rate cross-section rests on six currencies. Correlations computed on
six points are indicative rather than estimates, and none should be quoted with a
standard error.

Results are reported as *shifts* rather than levels, because the market curve
that would anchor them is deliberately omitted in order to isolate the
climate-attributable component. One consequence is that nothing imposes a zero
lower bound on the implied policy rate.

The spot channel rests on relative purchasing-power parity, a poor description of
exchange rates at short horizons; the forward channel, resting on covered
interest parity, is the sounder of the two.

Finally, there is an unresolved ambiguity in the currency to which the inflation
coefficient should be applied. The original study writes it against a dollar
carbon price, but its own published results are reproduced only when it is
applied to a sterling price. This model applies it to dollars. If the original
reading is correct, every spot level reported here is overstated by the
sterling–dollar rate, roughly a third. Ratios between currencies and their
ordering are unaffected, since the factor is common to both legs of every
difference; the levels are not.

No external benchmark exists for the exchange-rate or credit numbers themselves.
The GDP shocks do sit inside the range of NGFS's own macroeconomic estimates,
which is some comfort about the scale of the underlying real shock, but a −2 per
cent expected forward on the rupee has nothing to be compared against.
