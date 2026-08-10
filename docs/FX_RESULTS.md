# FX extension — method reference

The chain, its parameters and its caveats. **Findings live in
[FX_REPORT.md](FX_REPORT.md)** — deliberately not duplicated here, because this
note drifted out of date once already when the numbers moved.

Multi-regional BKMN model (project: Kenyon, UCL MSc Math Finance). Implements the
paper's route to FX (§4.3: *"the difference in the changes of yield curves"*)
across **13 regions**, EUR as base. Code `bkmn/{regions,scenarios,transition,macro,
rates,fx,physical,run_fx}.py`; gates `tests/test_fx.py` and
`tests/test_validation.py`; plan `docs/FX_PLAN.md`.

The region set is derived by the selection algorithm
([CHAPTER_REGION_SELECTION.md](CHAPTER_REGION_SELECTION.md)) and calibrated in
[`DATA_final/`](../DATA_final/). Which dataset is active is decided in one place,
`bkmn/regions.py`:

```python
DATASET = "DATA_final"    # 13 regions, derived        (default)
DATASET = "DATA_20R"      # 20 regions, hand-chosen    (earlier build)
```

Modules needing per-region auxiliary series resolve them through `regions.aux()`,
so the switch moves the whole pipeline — IO core, carbon intensity, vulnerability,
unemployment and equity together. `BKMN_DATASET` overrides it from the
environment.

## 1. The chain (per scenario, horizon year t, region r)

```
NGFS XCE_r(t)  ─► transition core (Eq 8/10)      ─► GVA shock  ΔY^tr_r(t)
                  intensities scaled by E_r(t)/E_r(2022)          [§7c of FX_REPORT]
NGFS GSAT(t)   ─► Ω(ΔT) = 0.003467·ΔT²,  ΔT vs pre-industrial
                  Prop-1 allocation via VL_r  ─► damage    Ω_r(t)
ΔXCE_r(t)      ─► inflation dev ΔΠ_r(t) = 8e-5 · ΔXCE_r · scope_r   (Moessner §2.6)

Taylor (§2.7):   Δr_r(t) = 0.5·ΔΠ_r(t) + 0.5·Ω_r(t)      ← output gap ≡ −Ω
Hull-White (§2.8, Prop 2): ΔR_r(t,τ) = B(τ)/τ · Δr_r(t), B(τ)=(1−e^{−aτ})/a, a=0.04

FX vs EUR (S_r = units of r per EUR; +Δlog = r depreciates):
  spot / rel-PPP :  Δlog S_r(t)   = cumΠ_r(t) − cumΠ_EUR(t)
  fwd pts / CIP  :  Δpts_r(t,τ)   = B(τ)·[Δr_r(t) − Δr_EUR(t)]
  total forward  :  Δlog F_r(t,τ) = Δlog S_r(t) + Δpts_r(t,τ)
```

**Note what does *not* enter the Taylor rule.** The transition GVA shock and any
tariff charge are ad-valorem tax wedges, not output gaps — with final demand and
**A** fixed they move value to the tax authority rather than destroying it. §2.7's
output-gap change is ≡ −Ω, the damage function. The transition channel reaches FX
through **prices** (the Moessner inflation route → spot), and reaches GVA, equity
and op-risk directly. Full argument and evidence: [FX_REPORT.md](FX_REPORT.md)
§7a.

φ = 0.5, base year 2022, horizons 2025–2045, forward tenors 1/5/10y. **6
analytical currencies** vs EUR (USD, CNY, GBP, CHF, INR, TRY); RUS, RASIA, LAM,
MEA, AFR and ROW are structural → no FX, though they carry every other channel.

## 2. Switches

Both live in `bkmn/run_fx.py`, which `run_extensions.py` imports, so the two
orchestrators cannot diverge.

| switch | default | alternative |
|---|---|---|
| `TAYLOR_OUTPUT_GAP` | `"physical"` — the paper's §2.7 | `"total"` — transition + physical + tariff (our earlier reading; overstates) |
| `OPRISK_INPUT` | `"physical"` — matches the reference, which never passes op-risk the carbon shock | `"total"` — our earlier reading; overstated by 1.5×–7.3× by region |
| `WARMING_BASELINE` | `"preindustrial"` — Ω(ΔT) vs 1850–1900 | `"incremental"` — since 2022; ~20× smaller |
| `CONSISTENT_INTENSITY` | `True` — intensities follow the scenario's emissions path | `False` — the paper's static intensities |

## 3. Caveats

1. **Shifts, not levels.** The paper's Appendix A.6 step 6 also carries a
   `market` term — the change the observed yield curve already implies. We omit
   it deliberately: we want the climate-attributable component, and a
   region-specific market term would inject non-climate FX moves into it. Cost:
   no absolute stressed level can be quoted, and **there is no zero lower
   bound** — nothing stops an implied rate going deeply negative, and reporting
   shifts makes that invisible.
2. **Spot = PPP, forward = CIP.** CIP forwards are assumption-free; the spot
   anchor is relative PPP, a modelling choice at climate horizons. We do not
   claim an uncovered-parity spot response to rate differentials.
3. **Spot carries almost one piece of information.** The 6 FX regions map onto
   only 3 NGFS carbon-price paths, so the price varies just \$494.89–\$505.61 at
   2045 (cv 0.0099) and spot is very nearly a rescaled `carbon_scope` vector —
   correlation **+0.9999**, the residual being all the regional price
   information there is.
   That is a data-granularity limit, not a modelling choice. Regions with
   scope = 0 (IND, TUR) are indistinguishable on spot; the dynamic-scope
   sensitivity separates them.
4. **Linear in the carbon price.** The transition GVA shock is linear in XCE
   (Eq 10). Real substitution would dampen it at high prices, so transition
   magnitudes are an upper bound. Scenario-consistent intensities remove the
   largest part of that overstatement but not the behavioural part.
5. **No trade diversion, no retaliation, A fixed at 2022.**
6. **Shadow vs applied price.** NGFS `Price|Carbon` is a shadow price; a hybrid
   (today's applied price → zone path) would differentiate short horizons more.
7. **No external validation of the FX numbers.** The *GDP* shocks are benchmarked
   against NGFS's own NiGEM range (FX_REPORT §7c); the FX moves are not
   benchmarked against anything.

## 4. Validation — 136 gates

| suite | n | covers |
|---|--:|---|
| `tests/test_fx.py` | 9 | reduction to the committed model (flat XCE ≡ 70), φ=0 endpoint = −CT/GVA exactly, Hull-White limits, EUR-base self-consistency, forward-points triangular consistency, scenario monotonicity |
| `tests/test_extensions.py` | 83 | physical, mixture, volatility, tariff and specification layers — including that the transition shock is *absent* from both the rate shift and the op-risk channel |
| `tests/test_validation.py` | 44 | **structural** — isolation, symmetry, superposition, reduction to the single-region case, and the sign and composition conventions. See [CHAPTER_VALIDATION.md](CHAPTER_VALIDATION.md) |

The third suite is the one that tests whether the multi-regional generalisation
is *correct* rather than merely reproducible: it runs the production code on
economies whose answer is known in advance by symmetry — identical regions, an
isolated region, autarky — and checks the model returns it.

## 5. Outputs & run

Tables (rows = scenario × region, cols = horizon year):
`out_fx_spot_ppp.csv` (%), `out_fx_forward_5y.csv` (%), `out_rate_shift.csv` (bp),
`out_inflation_shift.csv` (bp), `out_gdp_shock_fx.csv` (%).

Run: `py -3 -m bkmn.run_fx` · gates `py -3 tests/test_fx.py`.

## 6. Deferred

Market-curve anchoring for absolute levels and a zero lower bound; trade
diversion and carbon leakage; external benchmarking. Prioritised in
[FURTHER_WORK.md](FURTHER_WORK.md).
