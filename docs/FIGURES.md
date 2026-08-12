# Figure catalogue

One entry per figure: what it shows, and what it says. All figures are generated
by [`tools/make_figures.py`](../tools/make_figures.py) from the committed result
tables — no model re-run needed. Regenerate with `py -3 tools/make_figures.py`.

> **Maintenance.** Add an entry here whenever a figure is added or its message
> changes, and never hardcode a number in a caption — fig12's panel title said
> "9x apart" for one commit after the intensity fix made it 3.9x, and fig11
> carried a stale `$80/t` caption for several commits after the calibration moved
> to `$86/t` while its bars were correct. A figure whose caption states a number
> must read that number from the data.
>
> The same applies to *region lists*: the set is derived
> ([CHAPTER_REGION_SELECTION.md](CHAPTER_REGION_SELECTION.md)) and changes when
> the selection does, so figures select regions through `pick_regions()`, which
> raises rather than silently drawing fewer series — the same discipline `scen()`
> applies to scenario names.
>
> **All entries below are current as of the 13-region rebuild** on
> [`DATA_final/`](../DATA_final/), which followed the three specification
> corrections in [FX_REPORT.md](FX_REPORT.md) §7 (Taylor output gap, warming
> baseline, scenario-consistent intensities). Both moved every number.

**Conventions.** Diverging orange/blue for signed quantities (CVD-safe pair),
teal for single-series magnitudes, a printed value on bars wherever it fits so
colour is never the sole encoding. Unless stated, the reporting year is 2040 and
the scenario is Net Zero 2050.

---

## Core results

### fig1 — `fig1_transition_vs_physical.png`
**What.** Transition (carbon-price) versus physical (warming) GDP shock per
region, at 2040. **Two of the seven scenarios**, chosen as the transition
*extremes* — Net Zero has the largest mean transition cost (−2.20 %), Current
Policies the smallest (−0.06 %). Physical damage is deliberately *not* the
selection criterion, because its mean varies only 0.08 pp across all seven, which
is the point the figure makes. All seven inputs are in fig7.

**Findings.** The channel ranking flips cleanly: under Net Zero transition
dominates in **10/13** regions (China −4.72 %), under Current Policies physical
dominates in **13/13**. Physical damage runs −0.67 % to −1.48 % of GVA across all
seven scenarios and its *mean* varies by only 0.08 pp between them, because
warming to 2040 is largely locked in; the transition cost varies enormously
(−4.72 % to −0.01 %).

That is the trade-off in one picture, and it is what [FX_REPORT.md](FX_REPORT.md)
§4 expresses in currencies: **policy chooses the transition cost, not the
physical one.** The panels keep independent x-scales (3.3× apart) with the
difference stated in the subtitle.

### fig2 — `fig2_fx_forward_ranking.png`
**What.** 5-year forward FX shift against the euro at 2040, one bar per currency.
Bars are the **consensus mixture**; the whisker spans all four priors. MEA appears
as a **USD peg**, inheriting the dollar's row exactly.

**Findings.** INR −1.35 %, CNY −0.74 %, TRY −0.69 %, then USD +0.10 %, CHF
+0.22 % and GBP +0.35 %. The ordering blends **physical vulnerability** with the
absence of carbon pricing — India scores badly on both, Switzerland well on both.

The whiskers are the point. INR, CNY and TRY sit entirely below zero, so their
*sign* survives every prior; USD, CHF and GBP straddle it, flipping between the
ambition prior (−0.75, −0.12, −0.15) and consensus (+0.10, +0.22, +0.35). Read
the figure as: three currencies where the model has a view, and three where it
has only a magnitude. The whisker is *not* the spot component — that comparison
is fig12.

Read the sign carefully: a currency "strengthening" here reflects an output
collapse forcing deep rate cuts, so it is a distress signal, not strength.

### fig12 — `fig12_two_fx_channels.png`
**What.** Two panels: (a) spot against 5-year forward per currency; (b) the
Taylor-rule decomposition into output and inflation terms.

**Findings.** The two channels are **1.6× apart** and correlate **0.89** at 2040,
and under this region set they **agree in sign for all 6 currencies**. They still
price different risks: spot is transition (carbon-pricing scope, corr +0.9994),
the forward adds physical damage through the rate differential (corr +0.79 at
2045, against +0.44 for spot). An earlier 20-region build showed two sign flips —
Japan and Australia, which priced carbon more than the EU but were damaged less —
and neither is now a region; the mechanism survives, no current currency sits far
enough along both axes to cross zero. See [FX_REPORT.md](FX_REPORT.md) §2.

---

## Scenario and uncertainty

### fig7 — `fig7_scenario_inputs.png`
**What.** The two NGFS Phase 5 driver paths — OECD carbon price and global mean
warming, 2022–2050 — for **all seven** narratives.

**Findings.** The drivers diverge on completely different scales. Carbon prices
span **~\$3 to ~\$625/tCO₂e** by 2050; warming spans only **1.70 K to 1.93 K**.
That asymmetry is why FX responds to the carbon *price* rather than temperature,
and it is the evidence behind the 2-D (ΔT₂₁₀₀, XCE₂₀₅₀) distance metric for the
scenario transition matrix. The tight warming fan is also the visual form of
[FX_REPORT.md](FX_REPORT.md) §4's floor: policy moves the price panel, not the
temperature panel.

**Low demand** is the reason this figure now shows all seven. It carries the
second-highest carbon price and hence the second-largest FX dispersion, but was
absent from the figure — and *Below 2 °C* was silently dropped by a label
mismatch (`Below 2?C` from the IIASA API against a degree sign in the code), so
the figure plotted four of the five series its code listed. Both fixed; a gate
now asserts every scenario label resolves.

### fig8 — `fig8_fx_term_structure.png`
**What.** 5-year forward FX by horizon year, 2025–2045, Net Zero against NDCs,
for six currencies.

**Findings.** Paths rise steeply to 2030 and are then broadly flat. Two effects
nearly cancel: the transition component peaks and fades as decarbonisation
outruns the carbon price, while the physical component grows with cumulative
warming.

### fig3 — `fig3_mixture_expected_fx.png`
**What.** Expected 5-year forward FX under the Dirichlet scenario mixture, four
priors, at 2040.

**Findings.** A **1.4× range on CNY** from the choice of prior alone — ambition
-1.03 % against consensus -0.74 %. The consensus prior, anchored on
published ~2.7 °C current-policy warming, puts most weight on mild scenarios. The
sensitivity is far smaller than earlier drafts reported, for the reason in
[FX_REPORT.md](FX_REPORT.md) §4: with physical risk providing a
scenario-independent floor, reweighting the scenarios moves the answer less.

### fig9 — `fig9_scenario_drift_sensitivity.png`
**What.** The same mixture with the Eq-1 transition matrix applied — scenario
weights drifting annually — at slow (λ=5) and fast (λ=0.5) drift. Dotted = static
mixture, solid = drifted.

**Findings.** **This is the counterweight to fig3.** Under fast drift the three
priors converge: by 2045 they are nearly indistinguishable, and the 1.4× prior
sensitivity that fig3 reports largely washes out. So the prior matters a great
deal *if* scenario beliefs are static, and much less if they migrate. Read fig3
and fig9 as a pair — neither is the whole answer.

### fig4 — `fig4_fx_at_risk_band.png`
**What.** Central path against 95th-percentile inputs (1.64σ on temperature from
the MAGICC fan and on carbon price from the cross-model spread), at 2040.

**Findings.** CNY moves −1.39 % → −2.20 % and INR −3.60 % → −4.08 %. The tail is
**not uniformly adverse** — NOK and KRW move *further positive* under stress. The stress widens dispersion rather than shifting
a level, which is the correct behaviour for a relative-price channel.

---

## Channels and mechanism

### fig10 — `fig10_rate_term_structure.png`
**What.** The §2.8 zero-rate shift by tenor (1D to 20Y) under Prop 2, Net Zero
against NDCs.

**Findings.** The shift decays with maturity at a rate fixed entirely by the
Hull-White mean reversion: **20Y/1D = 0.688 = B(20)/20** exactly, verified as a
gate. Because the shape is σ-independent and every region shares one *a*, the
term structure only *rescales* the short-rate shift — all cross-region variation
comes from Δr, none from the curve. This is a validation figure as much as a
result.

### fig6 — `fig6_equity_oprisk.png`
**What.** Two downstream channels at 2040, **consensus mixture, currency regions
only**, to match [CHAPTER_RESULTS.md](CHAPTER_RESULTS.md) Table 11: equity index
shift (β·ΔGVA/GVA) and operational-risk conduct losses (Okun → unemployment →
loss frequency).

**Findings.** The two orderings **differ**, and instructively. Equity losses are
led by MEA −2.86 %, TUR −2.59 %, IND −2.31 %; op-risk conduct losses by
USA +8.77 %, CHE +7.37 %, IND +5.91 %. **Türkiye is 2nd-worst on equity and last
on op-risk** (+2.2 %), because the two channels run on different inputs: equity
on the total GVA shock through a beta, op-risk on physical damage alone through
Okun's law and the *base unemployment rate*. Türkiye's base rate is 10.46 %, so a
given rise in unemployment is a small relative change; RASIA's is 2.83 %, so the
same rise is a large one. A region's financial-market exposure and its
employment-channel exposure are not the same ranking, and the reason is the
denominator.

The two channels also take **different shocks by design**: equity the total
(a tax wedge still reduces the value added accruing to firms), op-risk the
physical only (a wedge destroys no output, so it drives no unemployment). See
[PAPER_AUDIT.md](PAPER_AUDIT.md) §20c — the op-risk panel previously used the
total shock and reached +37 %, above the ceiling the single-region reference's
saturating form can produce at all.

Note that 3 of the 9 currency regions take the **proxy** equity beta of 2.0 (CHE,
RUS, MEA — no index series exists for them), so the equity ordering is partly an
artefact of which regions have market data. Restricting to currency regions
improves this from 7-of-13 but does not remove it. China is the opposite case: an
*estimated* beta of 0.26, the lowest in the set, which is why it is last here and
first on credit (fig13).

### fig5 — `fig5_damage_vs_vulnerability.png`
**What.** Physical GDP damage at 2040 against the ND-GAIN vulnerability scale,
Current Policies, with a fitted line.

**Findings.** Damage tracks vulnerability almost exactly — correlation **−0.99**,
worst IND −1.37 % (scale 1.340), least GBR −0.67 % (scale 0.785), under the
pre-industrial warming convention (§7b of FX_REPORT). **Treat this as a
consistency check, not a discovery:** Proposition 1 allocates damage through the
VL vector, which is built from ND-GAIN, so the relationship is mechanical by
construction. What the figure usefully confirms is that the allocation behaves
monotonically and that the post-correction magnitudes are whole percent of GDP,
not basis points.

### fig11 — `fig11_cbam.png`
**What.** CBAM as a carbon tariff: ad-valorem rate by origin and sector, and the
GVA effect under both incidence assumptions.

**Findings.** Sector rates are high but no longer extreme — **Indian electricity
at 78 %**, African 50 %, Middle Eastern 49 %. Nothing now exceeds 100 %: the
20-region build's headline case was **Kazakh electricity at 160 %**, and
Kazakhstan is inside ROW under the derived selection, so its 884 t/\$m intensity
is averaged away. That is a concrete, quantified cost of aggregating it — the
single clearest illustration in the project of what a region buys.

The macro effect remains **−0.011 % of EU GVA**: coverage, not the rate, is the
binding constraint. The right panel shows incidence flipping the burden entirely:
at θ=1 the EU bears it, at θ=0 Türkiye, Russia and India do.

Priced at the published CBAM certificate price (\$86/t), and the caption now reads
both price and revenue from the data — see the maintenance note above.

### fig13 — `fig13_credit_spreads.png`
**What.** The credit channel (§2.9, CDS half) at 2040, **consensus mixture,
currency regions only**, to match [CHAPTER_RESULTS.md](CHAPTER_RESULTS.md)
Table 9: (a) CDS spread change by sector, one line per region; (b) each index's
paper Table 9 regression slope β against its median widening.

**Findings.** Widening is mostly a **sector** story — a variance decomposition
puts **72 %** between sectors and only **14 %** between regions, so which
industries a book holds matters five times more than which country it sits in.
Health Care is widest (median +3.87 %, and +11.0 % for India, the largest cell in
the model), then Utilities +2.97 % and Basic Materials +2.52 %.

Panel (b) separates what β does from what it does not. It fixes the **sign
exactly** — all ten negative-β indices widen and both positive-β indices narrow,
across all 13 regions without exception — but only sets about half the size
(corr −0.70), the rest coming from which sectors each index is built from.

**Read the two negative bars carefully.** Financials (β = +2.08) and UK Real
Estate (β = +7.21) narrow because the paper's own Table 9 gives them positive
slopes, a property of the UK estimation sample inherited wholesale here. It is
not a finding that climate stress improves bank or property credit. See
[CHAPTER_RESULTS.md](CHAPTER_RESULTS.md) §4.1.

Both panel titles compute their numbers from the data, per the maintenance note.

### fig14 — `fig14_pass_through.png`
**What.** The cost pass-through sensitivity at 2040 under Net Zero: (a) each
region's transition GVA shock as φ runs from 0 to 1, with a marker where it
changes sign; (b) four channels for India, expressed as a percentage change from
their value at the reporting φ = 0.5.

**Findings.** The endpoints are exact — at φ = 0 the shock is minus the region's
carbon bill over value added, at φ = 1 plus the same, holding to machine
precision. Every region's shock changes sign, and the crossings cluster tightly
between **0.574** (Africa) and **0.676** (UK), with Switzerland alone at 0.812.
All of them lie **above** one-half, so at the reported φ = 0.5 every region is
still a net loser; the dual is not linear in φ and the midpoint is not neutral.

Panel (b) is the structural point. **Pass-through does not touch the policy rate
or the exchange rate at all** — both sit exactly on zero across the whole range,
a range of 0e+00 basis points — because the Taylor rule responds to inflation and
physical damage, neither of which passes through the Leontief dual. What φ does
reach is value added and, through it, credit: India's transition shock swings
from −385 % to +590 % of its φ = 0.5 value, and its credit spread from +200 % to
−410 %. The model's widest single uncertainty is therefore confined to two of the
four financial channels. See [CHAPTER_RESULTS.md](CHAPTER_RESULTS.md) §3.

### fig15 — `fig15_prior_sensitivity.png`
**What.** For each channel, the ratio of its largest to its smallest 2040
headline across the four scenario priors, on a log scale, coloured by which
underlying shock the channel carries. A bar at 1× means the prior is irrelevant.

**Findings.** The spread is three orders of magnitude wide and splits cleanly by
driver. Carbon-charge channels inherit the narratives' full disagreement about
policy — spot FX **22.7×**, transition GVA **8.6×**, credit **4.1×**. Physical
channels barely notice it — policy rate **1.04×**, operational risk **1.03×**,
physical damage **1.03×** — because warming to 2040 is largely locked in whatever
policy does. Channels carrying both land between, at about 1.7–1.8×.

This is the honest summary of what the mixture buys. NGFS publishes no scenario
probabilities, so every expectation here rests on an assumed distribution; this
figure says which results survive that assumption and which do not. Read with
fig1, which makes the same point one scenario pair at a time. See
[CHAPTER_RESULTS.md](CHAPTER_RESULTS.md) §7.1.

### fig16 — `fig16_peg.png`
**What.** Two panels on the Middle East's dollar peg: (a) every currency region's
own Taylor-implied policy shift at 2040 under the consensus mixture, with MEA and
the USA highlighted; (b) the gap between MEA's own shift and the dollar shift it
must import, under each of the four priors.

**Findings.** MEA's own conditions call for **−65.7 bp**, the second-deepest cut
of any currency region, because it is among the most physically exposed in the
model. The dollar delivers **−40.9 bp**. The **~25 bp** shortfall is the climate
component of the peg's cost, and it is almost invariant to the prior — −24.6,
−24.8, −24.4, −24.8 — because *both* legs are driven by physical damage, the part
of the problem the narratives agree about.

This figure exists only because MEA is in the currency set. A pegged region has
no exchange-rate channel of its own (its row in fig2 *is* the dollar's, by
construction), but it still has a rate channel that responds to its own damage,
and the wedge between the two is invisible if the region is dropped as "not a
currency". See [CHAPTER_RESULTS.md](CHAPTER_RESULTS.md) §5.3. The result assumes
the peg holds, which a large enough wedge would eventually call into question.

---

## Coverage

| figure | in | reporting year |
|---|---|---|
| fig1, fig5 | physical / transition channels | 2040 |
| fig2, fig8, fig12 | [FX_REPORT.md](FX_REPORT.md) | 2040, 2045 |
| fig3, fig4, fig9, fig15 | scenario uncertainty | 2040 |
| fig6, fig10 | downstream channels | 2040 |
| fig13 | [CHAPTER_RESULTS.md](CHAPTER_RESULTS.md) §6 (credit) | 2040 |
| fig14 | [CHAPTER_RESULTS.md](CHAPTER_RESULTS.md) §3 (pass-through) | 2040, φ ∈ [0,1] |
| fig15 | [CHAPTER_RESULTS.md](CHAPTER_RESULTS.md) §7.1 (prior sensitivity) | 2040 |
| fig16 | [CHAPTER_RESULTS.md](CHAPTER_RESULTS.md) §5.3 (the peg) | 2040 |
| fig11 | [TARIFF_CALIBRATION.md](TARIFF_CALIBRATION.md) | 2040 |

## Scenario basis

[CHAPTER_RESULTS.md](CHAPTER_RESULTS.md) reports every headline as an expectation
over the seven NGFS narratives, so a figure sitting beside one of its tables must
be the same quantity. Not every figure is a headline, though, and three good
reasons remain to hold one narrative fixed: to *contrast* narratives, to show the
*inputs*, or to make a mechanism legible that the expectation averages away.
This table records which is which, and why.

| basis | figures | why |
|---|---|---|
| **consensus mixture** | fig2, fig4, fig6, fig12, fig13, fig16 | the chapter's headline prior; sits beside a consensus-weighted table |
| **mixture**, priors compared | fig3, fig10, fig15 | the prior *is* the subject |
| all seven narratives | fig7 | model inputs, not results |
| two narratives contrasted | fig1, fig8 | the spread between them is the point |
| Net Zero 2050 only | fig14 | the φ sweep needs a large carbon charge to be legible, and the text labels it a component |
| Current Policies only | fig5 | physical channel, which is near-invariant to the narrative anyway (1.03×) |
| n/a | fig9, fig11 | drift sensitivity and CBAM, neither a climate-scenario result |

**Region coverage.** fig2, fig3, fig4 and fig16 show currencies; fig6, fig10 and
fig13 show the nine **currency regions** (`currency != "mixed"` in the region
map), matching §§4–6 of the chapter. fig1, fig5, fig7 and fig14 keep all thirteen,
because value added and the scenario inputs are not currency quantities.

The rule of thumb: **if a figure carries a headline number, it is the mixture; if
it carries a mechanism, one narrative is allowed, and the caption says so.**

**Not yet drawn:** the tariff illustration of [TARIFF_METHOD.md](TARIFF_METHOD.md)
§5 has no figure, and neither does the China-share sweep. Both are candidates if
the tariff work is presented.
