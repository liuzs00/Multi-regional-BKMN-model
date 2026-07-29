# FX extension — coding plan (before any code)

Goal (from the project description, Kenyon 2026-03-16): generalise BKMN
(Berrahoui–Kenyon–Macrina–Nathanael 2025) to multiple regions **to predict FX
changes**. This plan covers the **FX-only early stage**: climate scenario →
per-region rates/inflation → FX shifts vs EUR. Physical risk, op-risk, credit/
equity, and the tariff stretch goal are explicitly deferred.

---

## 0. Preconditions — RESOLVED (2026-07-29)

1. **Region count.** Supervisor has approved extending to **up to 20 regions**
   (supersedes the 5–12 wording in the original project description). The 20R
   build stands as the headline model; the ROW-sufficiency test remains the
   supporting granularity evidence.
2. **Single-region reference code.** The verified single-region reproduction
   code is in hand — use it to pin the Taylor-rule accumulation convention
   (Eq 15) and cross-check the macro channels before wiring FX. (Our own
   earlier implementation also survives in `git stash@{0}`, 2026-07-16.)

---

## 1. The causal chain to implement

For each scenario `s`, horizon `t`, region `r` (base = EU27/EUR):

```
NGFS scenario s ──► XCE_z(t)  regional carbon-price path (zone z of region r)
                └─► ΔT(t)     global temperature (deferred: physical channel off)

XCE_r(t) ──► ct_r = CI_r × XCE_r × 1e-6        (per-region price now, not flat $70)
        ──► MRIO Eq 8/10 (existing core) ──► sector GVA shocks ──► ΔY_r(t)  GDP
ΔXCE_r(t) ──► ΔΠ_r(t) = 0.08%/10 × ΔXCE_r × scope_r          (Moessner, §2.6)

Taylor (§2.7):  Δr_r(t) = φΠ·ΔΠ_r(t) + φY·ΔY_r(t)
HW1F (§2.8):    ΔR_r(t,T) = B(t,T)/(T−t) · Δr_r(t),  B = (1−e^{−aτ})/a

FX vs EUR (paper §4.3: "difference in the changes of yield curves"):
  forward (CIP, mechanical):  Δlog F_r(t,T) = [ΔR_r(t,T) − ΔR_EUR(t,T)]·(T−t)
                                            = B(t,T)·[Δr_r(t) − Δr_EUR(t)]  (same a)
  spot (assumption, rel. PPP): Δlog S_r(t)  = Σ_{u≤t} [ΔΠ_r(u) − ΔΠ_EUR(u)]·Δu
```

Convention: `S_r` = units of currency *r* per 1 EUR; **positive Δlog = r
depreciates vs EUR**. Because every FX pair is a difference of per-region rate
shifts, triangular consistency (A/B = A/EUR − B/EUR) holds by construction.

Key modelling choices (state in write-up, confirm with supervisor):
- **CIP forwards are assumption-free**; the spot channel needs an economic
  anchor — we propose relative PPP (inflation differentials) for climate
  horizons, and report the two channels separately and combined.
- Within one NGFS zone (e.g. USA vs EU27, both OECD) the carbon-price *path* is
  identical, so their FX differential comes purely from **economic structure**
  (carbon intensity, IO linkages, pricing scope) — a feature worth highlighting.
- Uniform φ=50%, φΠ=φY=0.5, a=0.04 initially (paper defaults); region-specific
  values are a later refinement.
- **Δr accumulates** (Eq 15 integrates policy shocks) — treat ΔΠ, ΔY as level
  deviations from the no-climate baseline at t; verify against example code.

FX coverage: analytical currencies vs EUR — USD, CNY, GBP, JPY, INR, CAD, NOK,
IDR, CLP, AUD, SGD, TRY, KRW, KZT (14 pairs). MEA = USD-peg (report as
USD-linked or exclude); RUS/AFR/LAM/ROW structural → **no FX output**.

---

## 2. Data to acquire (Phase 0) — ✅ COMPLETE (2026-07-29)

Delivered: `data/ngfs/price_carbon_r5.csv` (+ GSAT p10/p50/p90) via the
**anonymous IIASA API** (`tools/download_ngfs.py` — no login needed after all);
`carbon_scope` column in `region_carbon_map.csv` built from the OWID/World
Carbon Pricing Database country coverage (2025 vintage), emissions-weighted to
regions by GHGFP Scope-1 (`tools/build_carbon_scope.py`); loaders
`bkmn/regions.py` + `bkmn/scenarios.py` (annual interp, USD2010→2022 ×1.342,
zone→region join, ΔT vs base year) with passing smoke test.
Verified: GSAT is anomaly vs 1850-1900 (2022 = 1.29 K); NZ2050 OECD 2030 price
$338 (2022 USD); Delayed transition ≈ $0 until 2030 as per narrative.

| # | Data | Source (concrete) | Notes |
|---|---|---|---|
| 1 | **Regional carbon-price paths** `Price\|Carbon` per scenario × R5 zone | **NGFS Phase 5 Scenario Explorer**, data.ece.iiasa.ac.at/ngfs (free login) | Model: MESSAGEix-GLOBIOM 2.0-M-R12-NGFS (stay single-model). Regions: the R5 buckets — OECD & EU, Reforming (REF), Asia, Middle East & Africa (MAF), Latin America (LAM). Joins to `DATA_20R/region_carbon_map.csv: scenario_zone`. Units US$2010/t → convert; 5-yr steps → linear-interp annual 2022–2045 |
| 2 | **Global temperature** per scenario | same NGFS explorer, `Temperature\|Global Mean` (MAGICC, 50th pct) | one series per scenario; needed later for physical channel, cheap to grab now |
| 3 | **Carbon-pricing scope** per region | **World Bank Carbon Pricing Dashboard** (carbonpricingdashboard.worldbank.org) | share of emissions covered — scales the inflation channel, a first-order FX lever (EU≈0.4, USA≈0.0, CHN≈0.4 power-only, …). Add `carbon_scope` column to region_carbon_map |
| 4 | Scenario set | start with 3 contrasting: **Net Zero 2050, Delayed Transition, Current Policies** | spans ambition; extend later; Bayesian mixture layer optional afterwards |
| 5 | *(optional, levels only)* base yield curves per currency | BoE GLC, ECB AAA curve, FRED/UST; EM harder | **not needed for FX/rate shifts** — all outputs are differentials; collect only when absolute stressed levels are wanted |
| 6 | Sanity references | old MESSAGE SSP2 CSVs recoverable via `git show 1760a2d:data/...` | temperature + OECD-zone carbon price used in the old single-region run |

Zone-mapping caveat: check which R5 bucket the chosen model assigns TUR, KOR,
MEX (conventions differ across IAMs); our current map (TUR→MAF, KOR→ASIA) must
match the downloaded data's own assignment.

Refinement to discuss (not blocking): NGFS prices are *shadow* prices — a
hybrid path (today's applied policy price per region, converging to the zone
path) would differentiate USA vs EU27 more realistically at short horizons.

---

## 3. Code structure (new files; existing core reused untouched)

```
bkmn/                      new package (flat scripts stay for reproducibility)
  scenarios.py    NGFS loader → {scenario: {zone: XCE(t)}}, {scenario: ΔT(t)};
                  annual interpolation, USD conversion, zone→region expansion
  regions.py      loads DATA_20R tables + region_carbon_map (currency, fx_role,
                  scenario_zone, carbon_scope); exposes vectors aligned to ICIO order
  transition.py   existing Eq 8/10 core from compute_transition.py, generalised:
                  ct vector built from PER-REGION XCE_r(t) (vector, not scalar 70)
  macro.py        ΔΠ_r (Moessner × scope_r), ΔY_r (GVA aggregation), Taylor Δr_r(t)
  rates.py        hw_B(τ,a), ΔR_r(t,T) (Prop 2)
  fx.py           CIP forward shift, PPP spot drift, peg/structural handling,
                  triangular-consistency helper
  run_fx.py       orchestrator: scenario × horizon grid (1d,10d,3m,1y,5y,10y,20y)
                  → out_fx_*.csv tables (Table-11-style layout, per scenario)
tests/
  test_fx.py      sanity suite (below)
docs/FX_PLAN.md   this plan
```

Outputs:
- `out_rate_shift_by_region.csv` — Δr and ΔR(t,T) per region × horizon × scenario
- `out_inflation_shift_by_region.csv`
- `out_fx_forward_shift.csv` — Δlog F (%) per currency-pair × horizon × scenario
- `out_fx_spot_ppp.csv` — cumulative PPP spot drift per pair × horizon × scenario

## 4. Validation gates (each phase must pass before the next)

1. **Reduction test**: with XCE_r ≡ 70 flat and scope=1, transition outputs must
   equal today's `out_gva_shock_*` exactly (regression against committed CSVs).
2. EUR/EUR shift ≡ 0; every pair antisymmetric; triangular identity to 1e-12.
3. φ=0 / φ=1 endpoint identities still hold per region (±CT/GVA).
4. Sign sanity: under Net Zero 2050, carbon-intensive-zone currencies (KZT, INR
   zone…) should show larger inflation → larger Δr → predictable forward-point
   sign vs EUR; document the economic reading of one worked pair (e.g. TRY/EUR).
5. Scenario monotonicity: |shifts| Current Policies < NDCs < Net Zero at short
   horizons (carbon-price ordering).

## 5. Phases & effort

| Phase | Work | Status |
|---|---|---|
| 0 | NGFS download + scope data + `scenarios.py` loader + zone join | ✅ done |
| 1 | `transition.py` with per-region XCE(t); reduction test green | ✅ done (reduction 4e-16) |
| 2 | `macro.py` + `rates.py` (inflation, Taylor, HW shift) | ✅ done |
| 3 | `fx.py` + `run_fx.py` + output tables | ✅ done (5 out_fx_* tables) |
| 4 | Validation suite (9 gates), worked-pair narrative, write-up notes | ✅ done — see `docs/FX_RESULTS.md`; artifact FX panel optional/next |

Deferred (explicitly out of scope now): physical channel (needs per-region VL),
credit/equity/op-risk channels, Dirichlet scenario mixture, tariff/trade-flow
shocks (stretch goal), absolute stressed levels (needs curves + spot FX).
