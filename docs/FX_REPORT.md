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
(§4.3). In a multi-regional setting that splits into two channels of similar
size that nonetheless carry **different information** — correlation 0.96, but
they disagree in *sign* for 2 of 14 currencies.

| | mechanism | driven by | size at 2045 (Net Zero) |
|---|---|---|--:|
| **Spot** | relative PPP — cumulative inflation differential | the carbon **price** | ±2.6 pp |
| **5y forward** | spot + CIP rate differential | + physical **damage** | ±4.0 pp |

## 2. The two channels price different risks

Correlating each against what a region can be — a carbon *taxer* or a
*climate-vulnerable* economy:

| | vs carbon-pricing **scope** | vs physical **damage** | vs carbon intensity |
|---|--:|--:|--:|
| **Spot** | **+0.9997** | — | −0.262 |
| **5y forward** | +0.605 | **+0.662** | −0.419 |

**Spot prices transition risk.** It runs through the Moessner relation
(ΔΠ = 8e-5 · ΔXCE · scope), so a region's spot move is very nearly a function of its
carbon-pricing coverage alone (corr +0.9997). A country that prices carbon imports inflation and its
currency weakens under PPP.

**The forward adds physical risk.** The rate differential comes from the Taylor
rule, whose output-gap term is the damage function Ω(ΔT) — see §7. So the
forward blends *who taxes carbon* with *who suffers warming*, and the two
attributes are largely independent.

That independence is the sign flips: **Japan** and **Australia** price carbon
more than the EU (so spot weakens their currency) but are damaged less (so the
rate differential strengthens it).

## 3. The cross-section: who moves

![FX ranking](../figures/fig2_fx_forward_ranking.png)

5-year forward against the euro at 2045 (the figure is drawn at 2040):

| strengthens most | | weakens | |
|---|--:|---|--:|
| INR | -4.00 % | NOK | +0.46 % |
| TRY | -3.37 % | KRW | +0.45 % |
| IDR | -2.94 % | | |
| USD | -2.24 % | | |
| CNY | -1.49 % | | |

India, Turkey and Indonesia lead on **both** attributes — little carbon pricing
(so no offsetting inflation) and high ND-GAIN vulnerability (so deep rate cuts).
Norway and Korea sit at the other end.

A currency "strengthening" here is not good news: it reflects damage forcing
rate cuts, which under covered interest parity produces a forward premium. It is
a distress signal.

## 4. Physical risk puts a floor under FX dispersion that policy cannot remove

Range across regions at 2045, split by channel:

| scenario | spot range | forward range |
|---|--:|--:|
| **Net Zero 2050** | 3.25 pp | 4.46 pp |
| Low demand | 1.76 pp | 2.93 pp |
| Below 2°C | 0.76 pp | 2.17 pp |
| Delayed transition | 0.78 pp | 2.13 pp |
| NDCs | 0.50 pp | 1.98 pp |
| Fragmented World | 0.22 pp | 1.86 pp |
| **Current Policies** | 0.06 pp | 1.84 pp |

**This reverses an earlier claim of ours.** Under the paper's specification,
scenario choice spans only **2.4×** on the forward (4.46 pp against 1.84 pp), not
the ~40× we previously reported. The reason is that the two channels move in
*opposite* directions across scenarios:

* ambitious policy → **high** carbon price (large spot dispersion) but **low**
  warming;
* weak policy → **low** carbon price but **high** warming.

And warming to 2040 is largely locked in whatever the policy: mean physical
damage varies only −0.99 % to −1.06 % across all seven scenarios. So the rate
channel contributes a near-constant **~1.8 pp floor** of FX dispersion in every
scenario, and only the spot component is policy-dependent — 0.06 pp under Current
Policies against 3.25 pp under Net Zero.

The policy-relevant statement is that **transition risk is a choice; physical
risk, at this horizon, is not.** No scenario removes the floor.

## 5. Timing

5-year forward under Net Zero 2050:

| | 2025 | 2030 | 2035 | 2040 | 2045 |
|---|--:|--:|--:|--:|--:|
| CHN | -0.48 | -1.30 | -1.43 | -1.39 | -1.49 |
| IND | -0.84 | -3.53 | -3.29 | -3.60 | -4.00 |
| USA | 0.09 | -2.07 | -1.73 | -1.92 | -2.24 |
| NOR | 0.03 | 0.42 | 0.37 | 0.40 | 0.46 |

The paths rise steeply to 2030 and are then broadly flat. Two effects nearly
cancel: the transition component peaks and fades as decarbonisation outruns the
carbon price (§7), while the physical component grows with cumulative warming.

## 6. Scenario uncertainty

![mixture](../figures/fig3_mixture_expected_fx.png)

Mixing the seven scenarios under a Dirichlet prior (§2.2) gives the expected
5-year forward at 2040:

| prior | CNY | INR | USD | NOK |
|---|--:|--:|--:|--:|
| ambition | -1.03 | -2.29 | -0.76 | +0.20 |
| uniform | -0.95 | -2.03 | -0.52 | +0.16 |
| policy-sceptic | -0.88 | -1.74 | -0.26 | +0.11 |
| **consensus** | -0.74 | -1.33 | +0.09 | +0.05 |

The prior still matters, but far less than before: **1.7× on INR** rather
than the 9–17× reported in earlier drafts. That follows directly from §4 — with
physical risk providing a scenario-independent floor, reweighting the scenarios
moves the answer much less.

![at-risk band](../figures/fig4_fx_at_risk_band.png)

Stressing the inputs by 1.64σ — temperature from the MAGICC fan, carbon price
from the cross-model spread — widens the tail. At 2040 the CNY forward goes
-1.39 % → **-2.20 %** and INR -3.60 % → **-4.08 %**.

The tail is not uniformly adverse: NOK and KRW move *further* positive under
stress. The stress widens dispersion rather than shifting a level, which is
correct for a relative-price channel.

## 7. Three specification choices, all following the paper

Three choices set the numbers above. All three follow the paper's own
specification, and two of them correct earlier drafts of this project.

### 7a. The Taylor output gap is the damage function, not the carbon charge

Appendix A.6 step 6 forms the shift as `dr = market + φΠ·ΔΠ − φY·Ω`, and §2.7
defines the output-gap change as **≡ −Ω** — the damage function of temperature.
The carbon charge does *not* enter it.

Earlier drafts fed the transition GVA shock into the Taylor rule. That was
wrong, and not only by reference: with final demand and **A** fixed, real
quantities cannot change, so the transition "GVA shock" is the incidence of a
tax wedge, not lost output. It tracks the tax bill — 26 % of it at φ=0.5, exactly
100 % at φ=0 or φ=1 — and the money moves to the tax authority rather than
vanishing. A Taylor rule responds to a real output gap; feeding it a fiscal
transfer overstates the response. The same argument removes tariffs from the
rate channel, leaving them to act on the price level (see
[TARIFF_METHOD.md](TARIFF_METHOD.md) §4).

### 7b. Damage uses warming vs pre-industrial, not warming since 2022

`Ω(t) = 0.003467 · ΔT(t)²` with ΔT measured against 1850–1900, which is what
NGFS GSAT already reports. This closes the ambiguity flagged in
[PAPER_AUDIT.md](PAPER_AUDIT.md) §B1: the reference implementation validates the
level convention against the paper's printed rows (op-risk 3.62 / 3.02 against
3.6 / 3.0; 1-day rate −25.8 bp against −25). Our earlier incremental-from-2022
reading understated Ω by **20.4×** (0.046 % against 0.947 % at 2040).

Physical damage is consequently no longer negligible: it now runs −0.67 % to
−1.35 % of GVA across regions, about **49 %** of the transition shock rather than
1 %.

### 7c. Carbon intensities are scenario-consistent

Intensities scale along **the scenario's own emissions
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

**Spot carries almost exactly one piece of information.** Its **+0.9997**
correlation with scope is *mechanical*: 20 regions map onto only 5 NGFS R5 zones,
so the carbon price varies just 495–516 across the 14 currencies (cv 0.013) and
spot is very nearly a rescaled scope vector. The residual 0.0003 *is* all the
regional carbon-price information the model carries — visible only in pairs like
AUS and SGP, which share a scope of 0.64 but differ on spot.
That is a data-granularity limit, not a modelling choice, and it makes spot the
less trustworthy channel despite being the more intuitive.

**We report shifts, not levels.** The paper's A.6 step 6 also carries a `market`
term — the change the observed yield curve already implies — which we omit
deliberately, since we want the climate-attributable component and a
region-specific market term would inject non-climate FX moves into it. The cost
is that no absolute stressed level can be quoted, and **there is no zero lower
bound**: nothing stops an implied rate going deeply negative, and because we
report shifts it would be invisible.

**The FX numbers have no external validation.** §7c benchmarks the *GDP* shocks
against NGFS's NiGEM range. A −4 % INR forward has no comparison at all.

**The 2045 horizon is a choice, not a limit.** NGFS runs to 2100 and the OECD
carbon price peaks around 2070; we stop before the scenarios get most extreme.

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
