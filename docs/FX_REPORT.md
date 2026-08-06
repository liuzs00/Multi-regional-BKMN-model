# FX results: the carbon channel

Results report for the multi-regional BKMN model, **carbon pricing only** — no
tariffs. 20 regions, 14 analytical currencies against the euro, NGFS Phase 5
scenarios, horizons 2025–2045.

Method detail is in [FX_RESULTS.md](FX_RESULTS.md); this note is the results
narrative. Tariff shocks are separate, in [TARIFF_METHOD.md](TARIFF_METHOD.md).
Everything below is reproduced by `py -3 -m bkmn.run_fx` and
`py -3 tools/make_figures.py`; gates in `tests/test_fx.py` (9) and
`tests/test_extensions.py` (73).

---

## 1. The result in one figure

![two FX channels](../figures/fig12_two_fx_channels.png)

The paper takes FX from *"the difference in the changes of yield curves"*
(§4.3). In a multi-regional setting that splits into two channels which turn out
to be **~4× apart and only loosely related** — correlation **0.62**, and they
disagree in *sign* for 2 of 14 currencies.

| | mechanism | size at 2045 (Net Zero) |
|---|---|--:|
| **Spot** | relative PPP — cumulative inflation differential | ±2.6 pp |
| **5y forward** | spot + CIP rate differential | ±10 pp |

Reporting one without the other would misstate the result, so both are carried
throughout.

## 2. Why they diverge: the two channels measure different things

This is the report's analytical core. Correlating each channel against the two
things a region can be — a carbon *taxer* or a carbon *emitter*:

| | vs carbon-pricing **scope** | vs carbon **intensity** | vs GVA shock |
|---|--:|--:|--:|
| **Spot** | **+1.000** | −0.262 | — |
| **5y forward** | +0.605 | −0.563 | **+0.951** |

**Spot tracks who *taxes* carbon.** It runs through the Moessner relation
(ΔΠ = 8e-5 · ΔXCE · scope), so a region's spot move is a near-exact function of
its carbon-pricing coverage. A country that prices carbon imports inflation and
its currency weakens under PPP.

**The forward tracks who *emits* carbon.** It is dominated by the rate
differential, which the Taylor rule takes almost entirely from the output term.

The sign flips follow directly. **Korea** prices carbon (spot: KRW weakens
+0.64 %) *and* is emissions-intensive (forward: KRW strengthens −2.42 %). Japan
flips for the same reason. A region's currency can move in opposite
directions on the two channels because policy coverage and emissions exposure are
different attributes.

**The inflation channel is small but not negligible.** Panel (b): the Taylor
rule's inflation term is a **median 2.1 %** of each region's rate move, though it
reaches **21 %** for Norway, whose output shock is slight while its carbon-pricing
coverage is high. So the Moessner relation is a minor contributor to rates in
most regions and matters chiefly as the *sole* driver of spot — but it is not the
rounding error it appeared to be before intensities were made
scenario-consistent, which shrank the output term without touching inflation.

## 3. The cross-section: who moves

![FX ranking](../figures/fig2_fx_forward_ranking.png)

The figure is drawn at **2040**; the table below is the same ranking at **2045**,
the final horizon, which is what the rest of this report quotes:

| strengthens most | | weakens | |
|---|--:|---|--:|
| INR | -10.15 % | NOK | +1.57 % |
| CNY | -9.11 % | | |
| TRY | -7.01 % | | |
| IDR | -5.96 % | | |
| KZT | -3.42 % | | |

The ordering is the carbon-intensity ordering: India, China, Turkey and Indonesia
carry the largest GVA shocks (-4.31 %, -4.74 %, -2.87 %,
-2.74 % at 2040), take the deepest rate cuts, and therefore trade at the
largest forward premium against the euro. Norway sits at the other end, and the
UK — low-intensity and service-weighted — is now marginally on the strengthening
side rather than the weakening one.

The direction deserves care. A currency "strengthening" here is not a good-news
result: it reflects a collapse in domestic output forcing large rate cuts, which
under covered interest parity produces a forward premium. It is a distress
signal, not a strength signal.

## 4. Scenario choice dominates every other assumption

The 5-year forward range across regions, at 2045:

| scenario | range |
|---|--:|
| **Net Zero 2050** | −10.2 % … +1.6 % |
| Low demand | −5.1 % … +0.8 % |
| Delayed transition | −3.4 % … +0.6 % |
| Below 2°C | −3.0 % … +0.6 % |
| NDCs | −2.4 % … +0.4 % |
| Fragmented World | −1.5 % … +0.1 % |
| **Current Policies** | −0.3 % … +0.0 % |

Roughly **38× between the extremes** (11.7 pp against 0.3 pp). No other choice in the model — φ, the
incidence parameter, the damage coefficient, the base year — comes close. Any FX
number quoted from this framework is first and foremost a statement about which
scenario was assumed.

Note also that the ordering is not the warming ordering: *Low demand* produces
the second-largest FX dispersion despite being a comparatively mild-warming
scenario, because it carries a high carbon price. This is the finding that drove
the switch to a 2-D (ΔT₂₁₀₀, XCE₂₀₅₀) distance metric for the scenario transition
matrix — FX responds to the carbon *price*, not to the temperature.

## 5. Timing: the shock peaks around 2030, then fades

5-year forward under Net Zero 2050:

| | 2025 | 2030 | 2035 | 2040 | 2045 |
|---|--:|--:|--:|--:|--:|
| CHN | 0.0 | -12.5 | -10.2 | -9.3 | -9.1 |
| IND | 0.0 | -13.0 | -10.5 | -10.0 | -10.1 |
| USA | 0.0 | -1.4 | -1.2 | -1.5 | -1.9 |
| NOR | 0.0 | 2.3 | 2.0 | 1.7 | 1.6 |

**The path is hump-shaped, not monotone** — China peaks at −12.5 % in 2030 and
recovers to −9.1 % by 2045. This is a direct consequence of making intensities
scenario-consistent (§7): the carbon *price* keeps rising, but the emissions it is
levied on fall faster, so the burden peaks and then declines as decarbonisation
outruns the price.

Under static intensities the same paths rose monotonically to 2045, because
nothing ever abated. The hump is the more defensible shape and it changes the
stress-testing message: the binding horizon is **the early 2030s**, not the end of
the projection.

## 6. Scenario uncertainty: the prior matters as much as the scenario

![mixture](../figures/fig3_mixture_expected_fx.png)

Mixing the seven scenarios under a Dirichlet prior (§2.2) gives the expected
5-year forward at 2040:

| prior | CNY | INR | USD | NOK |
|---|--:|--:|--:|--:|
| ambition | -4.41 | -4.71 | -0.61 | +0.83 |
| uniform | -3.36 | -3.59 | -0.43 | +0.63 |
| policy-sceptic | -2.17 | -2.30 | -0.23 | +0.42 |
| **consensus** | -0.50 | -0.52 | -0.00 | +0.07 |

A **9× range on CNY** purely from the choice of prior. The consensus prior —
anchored on published current-policy warming estimates of ~2.7 °C — puts almost
all weight on the mild scenarios and nearly extinguishes the result. Whether that
is the right anchor is a modelling judgement, not a data question, and it should
be stated as prominently as the scenario choice.

![at-risk band](../figures/fig4_fx_at_risk_band.png)

Stressing the inputs by 1.64σ — temperature from the MAGICC fan, carbon price
from the cross-model spread — widens the tail beyond the central path. At 2040
the CNY forward goes -9.3 % → **-11.3 %** and KZT -4.1 % → **-5.9 %**;
by 2045 the CNY tail reaches **-14.8 %** against a central -9.1 %.

Note the tail is not uniformly adverse: NOK and GBP move *further* positive under
stress. The stress widens dispersion rather than shifting a level, which is the
correct behaviour for a relative-price channel.

## 7. Carbon intensities are scenario-consistent

Every number here scales carbon intensities along **the scenario's own emissions
path**: `CI_r(t) = CI_r(2022) · E_r(t)/E_r(2022)`, with E from NGFS
`Emissions|Kyoto Gases` at R5 zone level — the same basis as our GHGFP Scope-1
intensities, and the same dataset that supplies the carbon prices.

Without it the model applies a *scenario* carbon price to *base-year*
intensities, which are from different worlds. The entire reason a Net Zero price
reaches \$421/t by 2040 is to abate the emissions it would otherwise be charged
on: NGFS Net Zero cuts world emissions to **39.9 %** of 2020 levels by 2040. So
static intensities charge for emissions the scenario says were abated.

The correction is large and it is the reason these results differ from earlier
drafts:

| Net Zero, transition GVA at 2040 | static CI | scenario-consistent |
|---|--:|--:|
| CHN | −11.40 % | **−4.74 %** |
| IND | −10.37 % | −4.31 % |
| EU27 | −2.66 % | −0.95 % |
| USA | −1.98 % | −0.70 % |

The static figures sat 3–10× above NGFS's own NiGEM Net Zero GDP impacts (about
−1 % to −4 %); the corrected ones sit inside that range. That is the first
external sanity check this model has passed, and it was the motivation.

Two limits. The scaling is **proportional within each zone** — NGFS does not
publish emissions at ICIO industry detail, so it corrects the *level* of
decarbonisation, not its *composition* across sectors. And it is a departure from
the paper, which holds the IO table and its intensities fixed; `CONSISTENT_INTENSITY
= False` in `run_fx.py` reproduces the paper's treatment, and the deviation is
registered in [PAPER_AUDIT.md](PAPER_AUDIT.md) §F2.

## 8. What this does not say

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
