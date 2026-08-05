# FX results: the carbon channel

Results report for the multi-regional BKMN model, **carbon pricing only** — no
tariffs. 20 regions, 14 analytical currencies against the euro, NGFS Phase 5
scenarios, horizons 2025–2045.

Method detail is in [FX_RESULTS.md](FX_RESULTS.md); this note is the results
narrative. Tariff shocks are separate, in [TARIFF_METHOD.md](TARIFF_METHOD.md).
Everything below is reproduced by `py -3 -m bkmn.run_fx` and
`py -3 tools/make_figures.py`; gates in `tests/test_fx.py` (9) and
`tests/test_extensions.py` (66).

---

## 1. The result in one figure

![two FX channels](../figures/fig12_two_fx_channels.png)

The paper takes FX from *"the difference in the changes of yield curves"*
(§4.3). In a multi-regional setting that splits into two channels which turn out
to be **an order of magnitude apart and only weakly related** — correlation
**0.40**, and they disagree in *sign* for 3 of 14 currencies.

| | mechanism | size at 2045 (Net Zero) |
|---|---|--:|
| **Spot** | relative PPP — cumulative inflation differential | ±2.6 pp |
| **5y forward** | spot + CIP rate differential | ±24 pp |

Reporting one without the other would misstate the result, so both are carried
throughout.

## 2. Why they diverge: the two channels measure different things

This is the report's analytical core. Correlating each channel against the two
things a region can be — a carbon *taxer* or a carbon *emitter*:

| | vs carbon-pricing **scope** | vs carbon **intensity** | vs GVA shock |
|---|--:|--:|--:|
| **Spot** | **+1.000** | −0.262 | — |
| **5y forward** | +0.386 | **−0.710** | **+0.993** |

**Spot tracks who *taxes* carbon.** It runs through the Moessner relation
(ΔΠ = 8e-5 · ΔXCE · scope), so a region's spot move is a near-exact function of
its carbon-pricing coverage. A country that prices carbon imports inflation and
its currency weakens under PPP.

**The forward tracks who *emits* carbon.** It is dominated by the rate
differential, which the Taylor rule takes almost entirely from the output term.

The sign flips follow directly. **Korea** prices carbon (spot: KRW weakens
+0.64 %) *and* is emissions-intensive (forward: KRW strengthens −7.56 %). The UK
and Japan flip for the mirror reasons. A region's currency can move in opposite
directions on the two channels because policy coverage and emissions exposure are
different attributes.

**The inflation channel is quantitatively negligible.** Panel (b) shows why: the
Taylor rule's inflation term is a **median 0.6 %** of each region's rate move
(maximum 6.5 %, Norway). ΔΠ reaches single-digit basis points while ΔY reaches
hundreds. This is worth stating plainly because the Moessner relation is
introduced in the paper as a substantive channel — in a multi-regional
calibration it is a rounding error on rates, and matters only because it is the
*sole* driver of spot.

## 3. The cross-section: who moves

![FX ranking](../figures/fig2_fx_forward_ranking.png)

Under Net Zero 2050 at 2045, the 5-year forward against the euro:

| strengthens most | | weakens | |
|---|--:|---|--:|
| CNY | −24.2 % | NOK | +4.8 % |
| INR | −23.4 % | GBP | +1.7 % |
| KZT | −15.3 % | | |
| TRY | −13.3 % | | |
| IDR | −12.5 % | | |

The ordering is the carbon-intensity ordering: China, India, Kazakhstan and
Indonesia carry the largest GVA shocks (−13.4 %, −12.2 %, −9.6 %, −7.7 %), take
the deepest rate cuts, and therefore trade at the largest forward premium against
the euro. Norway and the UK — low-intensity, service-weighted economies — sit at
the other end.

The direction deserves care. A currency "strengthening" here is not a good-news
result: it reflects a collapse in domestic output forcing large rate cuts, which
under covered interest parity produces a forward premium. It is a distress
signal, not a strength signal.

## 4. Scenario choice dominates every other assumption

The 5-year forward range across regions, at 2045:

| scenario | range |
|---|--:|
| **Net Zero 2050** | −24.2 % … +4.8 % |
| Low demand | −13.2 % … +2.5 % |
| Delayed transition | −5.8 % … +1.1 % |
| Below 2°C | −5.7 % … +1.2 % |
| NDCs | −3.7 % … +0.8 % |
| Fragmented World | −1.6 % … +0.2 % |
| **Current Policies** | −0.3 % … +0.0 % |

Roughly **96× between the extremes** (29.1 pp against 0.3 pp). No other choice in the model — φ, the
incidence parameter, the damage coefficient, the base year — comes close. Any FX
number quoted from this framework is first and foremost a statement about which
scenario was assumed.

Note also that the ordering is not the warming ordering: *Low demand* produces
the second-largest FX dispersion despite being a comparatively mild-warming
scenario, because it carries a high carbon price. This is the finding that drove
the switch to a 2-D (ΔT₂₁₀₀, XCE₂₀₅₀) distance metric for the scenario transition
matrix — FX responds to the carbon *price*, not to the temperature.

## 5. Timing: the move is front-loaded

5-year forward under Net Zero 2050:

| | 2025 | 2030 | 2035 | 2040 | 2045 |
|---|--:|--:|--:|--:|--:|
| CNY | 0.0 | **−16.5** | −17.3 | −20.5 | −24.2 |
| INR | 0.0 | −16.5 | −16.8 | −19.9 | −23.4 |
| USD | 0.0 | −1.0 | −0.5 | −0.5 | −0.6 |
| NOK | 0.0 | +3.4 | +3.8 | +4.2 | +4.8 |

**68 % of China's 2045 move has already happened by 2030.** The carbon price path
front-loads, and the FX response follows it. For a stress-testing application
this matters more than the terminal number: the repricing is a near-term event
under an aggressive scenario, not a 2045 one.

## 6. Scenario uncertainty: the prior matters as much as the scenario

![mixture](../figures/fig3_mixture_expected_fx.png)

Mixing the seven scenarios under a Dirichlet prior (§2.2) gives the expected
5-year forward at 2040:

| prior | CNY | INR | USD | NOK |
|---|--:|--:|--:|--:|
| ambition | −8.75 | −8.53 | −0.24 | +1.79 |
| uniform | −6.34 | −6.20 | −0.17 | +1.31 |
| policy-sceptic | −3.59 | −3.55 | −0.10 | +0.79 |
| **consensus** | **−0.52** | **−0.54** | **+0.01** | **+0.09** |

A **17× range on CNY** purely from the choice of prior. The consensus prior —
anchored on published current-policy warming estimates of ~2.7 °C — puts almost
all weight on the mild scenarios and nearly extinguishes the result. Whether that
is the right anchor is a modelling judgement, not a data question, and it should
be stated as prominently as the scenario choice.

![at-risk band](../figures/fig4_fx_at_risk_band.png)

Stressing the inputs by 1.64σ — temperature from the MAGICC fan, carbon price
from the cross-model spread — widens the tail well beyond the central path. At
2040 the CNY forward goes −20.5 % → **−22.7 %** and KZT −13.8 % → **−18.6 %**; by
2045 the CNY tail reaches **−37.5 %** against a central −24.2 %. The gap widens
with horizon because scenario spread compounds, so the tail risk is a late-horizon
phenomenon even though the central move is front-loaded (§5).

Note the tail is not uniformly adverse: NOK and GBP move *further* positive under
stress. The stress widens dispersion rather than shifting a level, which is the
correct behaviour for a relative-price channel.

## 7. What this does not say

**Two regions are indistinguishable on spot by construction.** India and Turkey
both have zero carbon-pricing scope, so both get zero inflation and identical
spot moves. That is an artefact of static scope, not a finding. The dynamic-scope
sensitivity (`out_sens_fx_spot_dynscope.csv`), which lets coverage expand with the
carbon price, separates them and is the honest version to quote.

**Spot carries exactly one piece of information.** Its +1.000 correlation with
scope means it adds nothing beyond the coverage assumption. Given that coverage
is among the softest inputs in the model, spot is the less trustworthy of the two
channels despite being the more intuitive.

**No tariffs, no trade diversion, no retaliation.** Carbon only, and **A** fixed
at 2022 throughout.

**PPP is an assumption, not a result.** The spot channel holds only under
relative purchasing-power parity, which is a poor short-horizon description of
FX. The forward channel, resting on covered interest parity, is the sounder of
the two — a second reason to lead with it.

**RUS, MEA, AFR, LAM and ROW have no FX result** — they are structural regions
without a single analytical currency.

---

## Reproduction

| output | produced by |
|---|---|
| `out_fx_spot_ppp.csv`, `out_fx_forward_5y.csv` | `py -3 -m bkmn.run_fx` |
| `out_rate_shift.csv`, `out_inflation_shift.csv`, `out_gdp_shock_fx.csv` | `py -3 -m bkmn.run_fx` |
| `out_ext_fx_expected_*.csv`, `out_ext_fx_forward_q95.csv` | `py -3 -m bkmn.run_extensions` |
| `figures/fig2`, `fig3`, `fig4`, `fig12` | `py -3 tools/make_figures.py` |
