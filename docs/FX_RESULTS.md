# FX extension — methodology, results, and caveats

> Method reference. The figure-led results narrative on the current numbers is
> [FX_REPORT.md](FX_REPORT.md); read that first for findings, this for the chain.

Early-stage FX-only build of the multi-regional BKMN model (project: Kenyon,
UCL MSc Math Finance). Implements the paper's own route to FX (§4.3: *"the
difference in the changes of yield curves"*) across 20 regions, EUR as base.
Code: `bkmn/{regions,scenarios,transition,macro,rates,fx,run_fx}.py`;
validation `tests/test_fx.py`; plan `docs/FX_PLAN.md`.

## 1. The chain (per scenario, horizon year t, region r)

```
NGFS XCE_r(t)  ─► transition core (Eq 8/10, per-region price) ─► GDP shock ΔY_r(t)
ΔXCE_r(t)      ─► inflation dev ΔΠ_r(t) = 8e-5 · ΔXCE_r · scope_r    (Moessner §2.6)
Taylor (§2.7): Δr_r(t) = 0.5·ΔΠ_r(t) + 0.5·ΔY_r(t)
Hull-White (§2.8, Prop 2): ΔR_r(t,τ) = B(τ)/τ · Δr_r(t),  B(τ)=(1−e^{−aτ})/a, a=0.04

FX vs EUR (S_r = units of r per EUR; +Δlog = r depreciates):
  spot / rel-PPP :  Δlog S_r(t)   = cumΠ_r(t) − cumΠ_EUR(t)
  fwd pts / CIP  :  Δpts_r(t,τ)   = B(τ)·[Δr_r(t) − Δr_EUR(t)]
  total forward  :  Δlog F_r(t,τ) = Δlog S_r(t) + Δpts_r(t,τ)
```
φ = 0.5, base year 2022, horizons 2025–2045, forward tenors 1/5/10y. 14
analytical currencies vs EUR (USD, CNY, GBP, JPY, INR, CAD, NOK, IDR, CLP, AUD,
SGD, TRY, KRW, KZT); RUS/MEA/AFR/LAM/ROW are structural → no FX.

## 2. Headline result — the forward (rate) channel dominates

Two channels, very different sizes (Net Zero 2050, horizon 2040):

| | mechanism | typical size | driver |
|---|---|---|---|
| **Spot (PPP)** | cumulative inflation differential | **±0.5 – 2%** | carbon-pricing **scope** relative to EU |
| **Forward (CIP)** | rate-differential forward points | **up to ±11%** | transition **GDP shock → Taylor rate cut** |

So the model's FX signal is **dominated by the forward/rate channel**: a carbon
tax is a recessionary supply shock, the central bank cuts (Taylor φY·ΔY), and the
rate differential drives large CIP forward moves. The spot PPP channel is a
smaller, scope-driven overlay.

### Worked pairs (Net Zero 2050, 2040)

- **USD/EUR** — spot **−1.95%**, 5y-forward **−0.52%**. US carbon-pricing scope
  (0.09) ≪ EU (0.65), so US carbon inflation is far lower → under PPP the **dollar
  appreciates vs EUR** (−); its GDP shock is modest so its rate cut (−99bp) is
  close to the EU's (−130bp), leaving small forward points.
- **KRW/EUR** — spot **+0.49%** (Korea's scope 0.82 > EU 0.65 → *more* carbon
  inflation → KRW **depreciates** on PPP), but 5y-forward **−6.38%**: Korea's
  large industrial GDP shock forces a deep rate cut (−282bp vs EU −130bp), and CIP
  turns that rate gap into a big forward appreciation. **The two channels pull
  opposite ways** — the pair to explain in the write-up.
- **TRY/EUR** — the largest: spot −2.27%, 5y-forward **−11.17%** (Turkey's high
  carbon intensity → −327bp rate cut).

### Scenario monotonicity (|USD spot|, 2040)
Current Policies 0.007% ≪ NDCs 0.345% ≪ Net Zero 2050 1.952% — climate-FX size
tracks carbon-price ambition, exactly as expected.

## 3. A structural finding worth stating

Under **Net Zero 2050 the NGFS zone carbon prices are near-uniform** ($332–389/t
across R5 zones at 2030 — MESSAGE models an almost-global price). So when prices
are uniform, cross-region FX comes **entirely from economic structure**: the
**spot** channel is driven by *carbon-pricing scope* differences, the **forward**
channel by *carbon-intensity / IO-linkage* differences (which set the GDP shock).
The genuinely price-divergent scenarios (Delayed transition, NDCs, Fragmented
World) add a zone-price contribution on top.

## 4. Caveats (state these in the dissertation)

1. **Linear IO scaling.** The transition GVA shock is linear in the carbon price
   (Eq 10), so a Net-Zero $340/t price gives ≈5× the $70 shock. At high prices,
   real demand response / substitution would dampen this — the large forward moves
   are an **upper bound / illustrative**, not a point forecast.
2. **Spot = PPP, forward = CIP.** CIP forwards are assumption-free; the spot
   anchor is relative PPP (a modelling choice for climate horizons). We do **not**
   claim an uncovered-parity spot response to rate differentials.
3. **Current scope, static.** `carbon_scope` is 2025 applied-policy coverage; under
   Net Zero, coverage would widen over time (a Phase-2 refinement). Regions with
   scope = 0 (IND, TUR, RUS, MEA) get no PPP inflation and cluster on the spot side.
4. **Transition only.** No physical-damage channel (temperature is loaded but off),
   no credit/equity/op-risk, no scenario mixture. FX = rates + inflation only.
5. **Shadow vs applied price.** NGFS `Price|Carbon` is a shadow price; a hybrid
   (today's applied price → zone path) would differentiate short horizons more.

## 5. Validation — 9 gates, all pass (`tests/test_fx.py`)

Reduction to the committed model (flat XCE≡70 reproduces
`out_gva_shock_by_region_phi.csv` to **4e-16 pp**), φ=0 endpoint = −CT/GVA
exactly, HW limits, EUR-base self-consistency, forward-points triangular
consistency (2e-17), scenario monotonicity.

## 6. Outputs & run

Tables (rows = scenario × region, cols = horizon year):
`out_fx_spot_ppp.csv` (%), `out_fx_forward_5y.csv` (%), `out_rate_shift.csv` (bp),
`out_inflation_shift.csv` (bp), `out_gdp_shock_fx.csv` (%).

Run: `py -3 -m bkmn.run_fx` (results) · `py -3 tests/test_fx.py` (gates).

## 7. Next (deferred, for discussion)

Physical channel (needs per-region vulnerability VL); scope widening under
scenarios; scenario-probability mixture (Dirichlet, paper §2.2); absolute stressed
FX levels (needs spot FX + curves); the tariff / trade-flow stretch goal.
