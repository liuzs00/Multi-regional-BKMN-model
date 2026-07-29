# Extensions — results and caveats (physical, equity, op-risk, mixture, volatility)

Implements the remaining paper sections except CDS and the tariff stretch goal
(plan: `docs/EXT_PLAN.md`). Additive to the FX stage: `bkmn/run_fx.py` and its
transition-only `out_fx_*.csv` are untouched, so the transition-vs-physical
comparison is available directly. Run `py -3 -m bkmn.run_extensions`;
gates `py -3 tests/test_extensions.py` (**21/21 pass**).

**Figures**: see [`figures/`](../figures/) — `fig1` (headline trade-off), `fig2`/`fig8` (FX),
`fig3` (mixture), `fig4` (FX-at-risk), `fig5` (vulnerability), `fig6` (equity/op-risk),
`fig7` (scenario inputs). Regenerate with `py -3 tools/make_figures.py`.

## 1. Headline — the transition/physical trade-off

The central result of adding §2.5. GDP shock at 2040, φ=0.5 (%):

| Region | Net Zero: transition | Net Zero: physical | Current Policies: transition | Current Policies: physical |
|---|--:|--:|--:|--:|
| EU27 | −2.66 | −4.01 | **−0.02** | **−5.15** |
| CHN | −11.40 | −5.49 | −0.13 | −7.06 |
| IND | −10.37 | −6.63 | −0.12 | −8.51 |
| AFR | −5.05 | −6.56 | −0.03 | −8.42 |
| NOR | −0.96 | −3.93 | −0.01 | −5.05 |

**The scenario ranking flips by channel.** Ambitious policy maximises
*transition* cost and minimises *physical* damage; Current Policies does the
reverse (transition ≈ 0, physical largest). A transition-only model therefore
makes Net Zero look unambiguously the most damaging scenario — adding the
physical channel removes that artefact. This is the dissertation's core
climate-economics point.

Vulnerability ordering behaves: for the same global ΔT, AFR/IND (ND-GAIN scale
1.34) lose ~1.7× what NOR (0.74) loses.

## 2. FX with both channels (5y forward vs EUR, 2040, Net Zero, %)

IND −25.8 · CHN −23.9 · KAZ −15.7 · IDN −15.5 · TUR −14.1 · KOR −7.6 · SGP −5.5 ·
CHL −4.4 · JPN −2.8 · AUS −0.2 · **USA +0.1** · CAN +0.9 · GBR +3.1 · NOR +4.4

Ordering is intuitive: carbon-intensive, climate-vulnerable economies face the
deepest rate cuts and hence the largest forward appreciation vs EUR; low-carbon,
low-vulnerability economies (NOR, GBR) sit on the other side. Magnitudes are
much larger than the transition-only FX stage (`docs/FX_RESULTS.md`) because the
physical damage adds to ΔY — see caveat 1.

## 3. Scenario mixture (Phase M) — expected FX

Expected 5y-forward vs EUR at 2040 (%), by named prior:

| Prior | IND | CHN | USA | NOR |
|---|--:|--:|--:|--:|
| uniform | −13.7 | −10.7 | +0.6 | +1.6 |
| policy-sceptic | −11.0 | −7.8 | +0.7 | +1.0 |
| ambition | −16.6 | −13.9 | +0.4 | +2.3 |

The prior is a *narrative* choice, so all three are reported. Note the mixture is
strictly additive — per-scenario tables are unchanged and a degenerate prior
reproduces its scenario exactly (gate).

## 4. Volatility band (Phase V) — climate FX-at-risk

Central vs 95th-percentile inputs (Net Zero, 2040, 5y forward %):
IND −25.8 → **−36.1**, CHN −23.9 → **−30.8**, USA +0.1 → +0.3.
Input σ at 2040: temperature **0.274 K** (MAGICC p10/p90 fan), carbon price
**$211/t** for the OECD zone (cross-model spread over MESSAGEix / REMIND / GCAM).
Band widens for 14/14 currencies. Combined with the mixture this is the paper's
"ensemble" — expected FX **plus** a tail — realised for currencies.

## 5. Equity (Phase E) and op-risk (Phase O)

Equity ΔS/S at 2040 Net Zero: USA −9.1%, IND −23.5%, EU27 −5.3%.
β calibrated per region (log index ~ log GDP, annual 2000–2023): 12 of 13 fit
(R² 0.20–0.98; IDN/IND/KOR > 0.95), **JPN falls back to the paper's β = 2.00**
because its fitted slope is negative — the "lost decades" pattern, index flat
while GDP grew. CHL/KAZ have no free index series → proxy β.

Op-risk (Conduct) at 2040 Net Zero: EU27 +42.4%, GBR +30.1%, TUR +22.1%. The
level differences are driven mostly by *base unemployment* (the shift scales with
ΔU/U, so low-unemployment regions show larger relative jumps) — read these as
relative, not absolute, and see caveat 4.

## 6. Caveats (carry into the dissertation)

1. **Linear scaling, compounded.** The transition shock is linear in the carbon
   price and the damage function is quadratic in ΔT with no adaptation, so at
   $340/t and +2 K the combined ΔY reaches −10…−17% for some regions. Real
   economies substitute and adapt; treat the FX magnitudes as an **upper bound /
   illustrative ordering**, not point forecasts. Damping this is the single
   highest-value modelling refinement.
2. **World-level Prop 1.** Ω is a *world* GDP damage allocated across all 1000
   region-sectors by relative vulnerability (our generalisation of a
   single-region proposition). Per-region damage emerges from aggregation.
   Alternative: apply Prop 1 within each region — worth testing as a sensitivity.
3. **ND-GAIN as the vulnerability scale.** A country-level composite index, not
   sector-specific; the sector *pattern* is the paper's UK Table 6 assumed common
   across regions. Only the region *scale* varies.
4. **Proxy betas.** Op-risk slopes are the paper's UK values (region-specific
   calibration needs licensed ORX data); Okun κ is −0.182 for GBR [PAPER] and
   literature-range defaults elsewhere [ESTIMATE] — the WB unemployment panel is
   committed so κ can be estimated from data as a refinement.
5. **Physical enters via ΔY only.** The paper's inflation channel is
   carbon-price driven (§2.6); physical damage is supply-side and would plausibly
   also be inflationary — not modelled.
6. Still excluded: CDS/IFRS 9 (licensed data), tariff/trade-flow shocks,
   Green KVA/RWA.

## 7. Outputs

`out_ext_gdp_{transition,physical,total}.csv`, `out_ext_rate_shift.csv`,
`out_ext_fx_{spot,forward_5y}.csv`, `out_ext_equity.csv`,
`out_ext_oprisk_{conduct,execution}.csv`,
`out_ext_fx_expected_{uniform,policy-sceptic,ambition}.csv`,
`out_ext_fx_q95_scen.csv`, `out_ext_fx_forward_q95.csv`.
