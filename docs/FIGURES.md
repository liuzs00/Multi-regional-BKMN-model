# Figure catalogue

One entry per figure: what it shows, and what it says. All figures are generated
by [`tools/make_figures.py`](../tools/make_figures.py) from the committed result
tables — no model re-run needed. Regenerate with `py -3 tools/make_figures.py`.

> **Maintenance.** Add an entry here whenever a figure is added or its message
> changes, and never hardcode a number in a caption — fig12's panel title said
> "9x apart" for one commit after the intensity fix made it 3.9x. All entries below are current as of the three specification
> corrections in [FX_REPORT.md](FX_REPORT.md) §7 (Taylor output gap, warming
> baseline, scenario-consistent intensities), which moved every number. A figure whose caption states a number must read that number from the
> data, never hardcode it — fig11 carried a stale `$80/t` caption for several
> commits after the calibration moved to `$86/t` while its bars were correct.

**Conventions.** Diverging orange/blue for signed quantities (CVD-safe pair),
teal for single-series magnitudes, a printed value on bars wherever it fits so
colour is never the sole encoding. Unless stated, the reporting year is 2040 and
the scenario is Net Zero 2050.

---

## Core results

### fig1 — `fig1_transition_vs_physical.png`
**What.** Transition (carbon-price) versus physical (warming) GDP shock per
region, Net Zero 2050 against Current Policies, at 2040.

**Findings.** The channel ranking flips cleanly: under Net Zero transition
dominates in **17/20** regions (China −4.74 %), under Current Policies physical
dominates in **20/20**. Physical damage now runs −0.67 % to −1.43 % of GVA and
barely varies by scenario, because warming to 2040 is largely locked in; the
transition cost varies enormously (−4.74 % to −0.14 %).

That is the trade-off in one picture, and it is what [FX_REPORT.md](FX_REPORT.md)
§4 expresses in currencies: **policy chooses the transition cost, not the
physical one.** The panels keep independent x-scales (3.3× apart) with the
difference stated in the subtitle.

### fig2 — `fig2_fx_forward_ranking.png`
**What.** 5-year forward FX shift against the euro at 2040, one bar per currency,
with a tick marking the spot-only component.

**Findings.** INR −3.60 %, TRY −2.98 %, IDR −2.67 % at one end; NOK +0.40 % and
KRW +0.32 % at the other. The ordering blends **physical vulnerability** with the
absence of carbon pricing — India, Turkey and Indonesia score badly on both. The
ticks are now a substantial share of each bar, since spot and forward are only
1.5× apart.

Read the sign carefully: a currency "strengthening" here reflects an output
collapse forcing deep rate cuts, so it is a distress signal, not strength.

### fig12 — `fig12_two_fx_channels.png`
**What.** Two panels: (a) spot against 5-year forward per currency; (b) the
Taylor-rule decomposition into output and inflation terms.

**Findings.** The two channels are **1.5× apart** and correlate **0.96**, but
still **disagree in sign for 2 of 14 currencies** (JPY, AUD — starred). They
price different risks: spot is transition (carbon-pricing scope, corr +1.000),
the forward adds physical damage through the rate differential. Japan and
Australia flip because they price carbon more than the EU but are damaged less.
See [FX_REPORT.md](FX_REPORT.md) §2.

---

## Scenario and uncertainty

### fig7 — `fig7_scenario_inputs.png`
**What.** The two NGFS Phase 5 driver paths: OECD carbon price and global mean
warming, 2022–2050, for four scenarios.

**Findings.** The two drivers diverge on completely different scales. Carbon
prices span **~$3 to ~$625/tCO₂e** by 2050; warming spans only **1.70 K to
1.93 K**. That asymmetry is why FX responds to the carbon *price* rather than to
temperature, and it is the evidence behind switching the scenario-transition
distance metric from 1-D warming to 2-D (ΔT₂₁₀₀, XCE₂₀₅₀).

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
**What.** Two downstream channels at 2040 under Net Zero: equity index shift
(β·ΔGVA/GVA) and operational-risk conduct losses (Okun → unemployment → loss
frequency).

**Findings.** The two orderings **differ**, and instructively. Equity is led by
ROW −8.7 %, IND −7.8 %, TUR −7.5 %; op-risk by **KOR +45 %**, JPN +32 %, SGP
+30 %. Korea is mid-table on equity but 1st on op-risk, because op-risk runs
through the Okun coefficient and the base unemployment rate rather than through
an equity beta. A region's financial-market exposure and its
employment-channel exposure are not the same ranking.

### fig5 — `fig5_damage_vs_vulnerability.png`
**What.** Physical GDP damage at 2040 against the ND-GAIN vulnerability scale,
Current Policies, with a fitted line.

**Findings.** Damage tracks vulnerability closely — worst about −1.43 %, least
−0.71 %, under the pre-industrial warming convention (§7b of FX_REPORT). **Treat this as a consistency check, not
a discovery:** Proposition 1 allocates damage through the VL vector, which is
built from ND-GAIN, so the relationship is largely mechanical. What the figure
usefully confirms is that the allocation behaves monotonically and that the
post-correction magnitudes are basis points of GDP, not percent.

### fig11 — `fig11_cbam.png`
**What.** CBAM as a carbon tariff: ad-valorem rate by origin and sector, and the
GVA effect under both incidence assumptions.

**Findings.** Sector rates are extreme — **Kazakh electricity at 160 %**, above
the value of the good itself; Indian electricity 78 %, Indonesian 64 %. Yet the
macro effect is **−0.011 % of EU GVA on \$10.1 bn of revenue**. Coverage, not the
rate, is the binding constraint. The right panel shows incidence flipping the
burden entirely: at θ=1 the EU bears it, at θ=0 Turkey, Russia and Kazakhstan do.

Priced at the published CBAM certificate price (\$86/t), and the caption now reads
both price and revenue from the data — see the maintenance note above.

---

## Coverage

| figure | in | reporting year |
|---|---|---|
| fig1, fig5 | physical / transition channels | 2040 |
| fig2, fig8, fig12 | [FX_REPORT.md](FX_REPORT.md) | 2040, 2045 |
| fig3, fig4, fig9 | scenario uncertainty | 2040 |
| fig6, fig10 | downstream channels | 2040 |
| fig11 | [TARIFF_CALIBRATION.md](TARIFF_CALIBRATION.md) | 2040 |

**Not yet drawn:** the tariff illustration of [TARIFF_METHOD.md](TARIFF_METHOD.md)
§5 has no figure, and neither does the China-share sweep. Both are candidates if
the tariff work is presented.
