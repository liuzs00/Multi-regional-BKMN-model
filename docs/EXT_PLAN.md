# Extensions plan — physical, mixture, volatility, equity, op-risk

Scope agreed 2026-07-30: the remaining paper sections **except** CDS calibration
and the tariff/trade-flow stretch goal. Builds directly on the FX stage
(`docs/FX_PLAN.md`, `docs/FX_RESULTS.md`); nothing upstream changes — every
phase is additive and gated on leaving the existing results intact.

Order (dependencies): **P → E → O → M → V**. P completes the climate input side;
E/O add downstream channels consuming ΔY; M and V are generic wrappers that turn
every per-scenario table into expectations and tail bands.

---

## Phase P — Physical risk (§2.5): the missing climate channel

FX is currently transition-only. Physical damage adds the temperature half:
Ω(ΔT) → sector GVA damage → ΔY_r → Taylor → rates → FX. Temperature paths are
**already loaded** (`data/ngfs/temperature_gsat_p50.csv`).

**Multi-region generalisation of Proposition 1 (design decision — flag to
supervisor):** apply the damage allocation at the *world* level across all 1000
region-sectors:

```
VL(r,i) = pattern(i) × scale(r)
   pattern(i): the paper's Table-6 sector relativities (health=1)   [PAPER]
   scale(r):   region physical-vulnerability scale from ND-GAIN,
               country index aggregated to regions (GDP-weighted)   [DATA]
α(t) = Ω(ΔT(t)) / Σ_i VL_i·f_i ,   f_i = GVA_i / world GDP          (Prop 1)
direct:    ΔGVA_i/GVA_i = −VL_i·α(t)
cascading: ct_i += VL_i·α(t)  → through the SAME operator M(φ)       (Prop 1)
```

Per-region damage then *emerges* from aggregation — vulnerable regions (AFR,
IND, IDN) lose more than NOR/GBR for the same global ΔT. Damage function
Ω(ΔT) = 0.003467·ΔT² (Barrage–Nordhaus, Eq 11; SwissRe variant as sensitivity).
Physical enters Taylor via ΔY only (paper's inflation channel is carbon-price
driven, §2.6 — unchanged).

- Data: **ND-GAIN country index** (free, gain.nd.edu) → `tools/download_ndgain.py`
  → `data/physical/ndgain.csv` + `scale` column per region; Table-6 pattern
  hard-coded in `bkmn/paper_tables.py` with the ICIO-industry mapping (20-sector
  SIC → 50-industry ISIC, documented).
- Code: `bkmn/physical.py` (VL build, α, direct+cascading shocks);
  `run_fx.py` flag `include_physical` (default on; off preserves current CSVs).
- Gates: ΔT=0 ⇒ zero physical shock; allocation identity Σf·VL·α = Ω(ΔT) to
  machine precision (the Prop-1 proof identity); monotone in ΔT.
- **Expected headline:** the transition/physical trade-off — Net Zero maximises
  transition-FX, Current Policies maximises physical-FX at long horizons; the
  scenario ranking *flips* across horizons. Dissertation-grade result.

## Phase E — Equity (§2.9), region-index level, no CDS

ΔS_r/S_r = β_r · ΔGVA_r/GVA_r per region (log-linear regression, paper §2.9).
Sector-level equity needs index-composition maps — deferred; region headline
indices first.

- Data (free): annual closes for one index per FX region (S&P 500, STOXX 600,
  FTSE 100, Nikkei 225, KOSPI, TSX, …) via stooq.com CSV endpoints →
  `tools/download_equity.py`; World Bank annual GDP (API already used for PPP)
  as the GVA regressor → β_r per region calibrated on ~2000–2022.
- Fallback [PROXY]: the paper's FTSE β = 2.00 (Table 9) applied to all regions;
  report calibrated-vs-proxy side by side.
- Code: `bkmn/equity.py`; output `out_equity_shift.csv` (scenario × region × horizon).
- Gates: β>0 and ΔY<0 ⇒ equity falls; calibration R² reported per region
  (low R² expected — the paper's own Table 9 is honest about this).

## Phase O — Operational risk (§2.11)

ΔU_r = κ_r·ΔY_r (Okun; Phillips β=0 per paper), then
ΔOpRisk_i/OpRisk_i = β1_i · ΔU_r/U_r for i ∈ {Execution, Conduct}.

- Data (free): **Okun κ per region** from Goto & Burgi (2020) cross-country
  table, hard-coded with citation [DATA]; **base unemployment 2022** per region
  from the World Bank API (`SL.UEM.TOTL.ZS`, emissions- or labour-weighted for
  aggregates) → `tools/download_wb_macro.py`; op-risk betas from the paper's
  Table 10 (Conduct 1.306, Execution 1.567) [PROXY — UK-calibrated].
- Code: `bkmn/oprisk.py`; output `out_oprisk_shift.csv`.
- Gates: sign chain (ΔY<0 ⇒ U up ⇒ losses up); zero shock ⇒ zero.

## Phase M — Bayesian scenario mixture (§2.2 + §3.1.5)

Additive wrapper: per-scenario tables stay byte-identical; the mixture adds
expected values and discrete scenario-distribution quantiles.

```
Dirichlet-categorical: prior α over the 7 NGFS scenarios (+ optional observed
event counts c → posterior);  E[X] = Σ_s p_s · X_s
```

- Data: none — priors are a *narrative config*, e.g. three named priors:
  `uniform`, `policy-sceptic` (mass on CP/NDCs/Fragmented), `ambition`
  (mass on NZ/Below-2C). Supervisor sets/blesses the defaults.
- The paper's RCP transition matrix (Eq 1) needs a scenario distance — for NGFS
  narratives use an ambition-ordering distance; implement as optional second step.
- Code: `bkmn/mixture.py`, generic over any (scenario × region × horizon) table
  → applies to FX, rates, GDP, equity, op-risk alike. Outputs
  `out_*_expected.csv` + `out_*_mixture_q{05,50,95}.csv` per named prior.
- Gates: weights sum to 1; degenerate prior reproduces that scenario exactly;
  E[X] within [min_s, max_s].

## Phase V — Volatility (§3.3): within-scenario tails

Turns each scenario's point path into a band, giving climate FX-at-risk /
PFE-style quantiles.

- Temperature σ(t): **already have** p10/p50/p90 → σ ≈ (p90−p10)/2.563
  (normal assumption, per §3.3's Gaussian ΔT).
- Carbon-price σ(t): NGFS **cross-model spread** — extend `tools/download_ngfs.py`
  to also pull `Price|Carbon` from REMIND-MAgPIE and GCAM, σ across the three
  models per scenario/zone/year; fallback the paper's Table 15 values [PAPER].
- Method (paper's own §4.3 simplification): stress the inputs by z_q·σ and re-run
  the (monotone) chain — quantile-of-output = output-of-quantile-input; document
  the monotonicity argument (Eq 10 linear in XCE; Ω monotone in ΔT).
- Code: `bkmn/volatility.py`; outputs `out_fx_q95.csv`, `out_fx_q99.csv` (and
  optionally for rates/GDP). Combined with Phase M: mixture-of-bands = the full
  ensemble distribution — the paper's "ensemble framework" realised for FX.
- Gates: q50 ≈ central run; band width grows with horizon; q95 ⊂ q99.

---

## Data acquisition summary (all free; no licensed sources)

| # | Data | Source | Tool |
|---|---|---|---|
| 1 | ND-GAIN country vulnerability | gain.nd.edu (free CSV) | `tools/download_ndgain.py` |
| 2 | Okun κ by country | Goto & Burgi (2020), published table | hard-coded [DATA] |
| 3 | Unemployment 2022 by country | World Bank API `SL.UEM.TOTL.ZS` | `tools/download_wb_macro.py` |
| 4 | GDP annual (equity regressor) | World Bank API `NY.GDP.MKTP.CD` | same tool |
| 5 | Equity index histories | stooq.com free CSV endpoints | `tools/download_equity.py` |
| 6 | Carbon-price cross-model σ | IIASA API (REMIND, GCAM) — anonymous | extend `tools/download_ngfs.py` |
| 7 | Paper Tables 6 / 9 / 10 constants | the BKMN paper itself | `bkmn/paper_tables.py` [PAPER/PROXY] |

## Validation & non-regression

`tests/test_extensions.py`, one gate block per phase (as listed above), plus the
global non-regression rule: with `include_physical=False`, no mixture, no vol,
**every existing FX/transition output must reproduce byte-identically** — the
same discipline as the Phase-1 reduction test.

## Effort & deliverables

| Phase | Work | Est. |
|---|---|---|
| P | ND-GAIN + Table-6 pattern + `physical.py` + gates | ✅ done |
| E | equity data + β calibration + `equity.py` | ✅ done (12/13 fitted) |
| O | WB macro data + `oprisk.py` | ✅ done |
| M | `mixture.py` + named priors + expected/quantile tables | ✅ done (3 priors) |
| V | cross-model σ pull + `volatility.py` + FX-at-risk tables | ✅ done |
| — | write-up notes (`docs/EXT_RESULTS.md`) ✅ done; artifact panels — optional/next |

Deferred (unchanged): CDS calibration (licensed) and §2.10 IFRS 9 (hangs off
CDS-implied PDs — a paper-beta proxy version is possible later at zero data
cost if wanted); tariff/trade-flow stretch goal; §4.2 Green KVA/RWA.

## Decisions to confirm with supervisor

1. World-level Prop-1 damage allocation (vs per-region application) — Phase P.
2. ND-GAIN as the cross-region vulnerability scale (alternatives: IPCC AR6
   qualitative tiers already in `region_carbon_map.phys_vuln_tier`).
3. Region-index (not sector) equity at this stage; paper-β proxy acceptable.
4. Named mixture priors (the narrative weights are a judgment call).
5. Cross-model spread as carbon-price σ (vs paper Table 15).
