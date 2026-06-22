# Multi-regional BKMN model

A Python reproduction of the **BKMN climate stress-testing model**
(Berrahoui, Kenyon, Macrina, Nathanael, 2025 — *"Simple climate stress testing:
an ensemble framework"*, SSRN-5130573).

It takes the two outputs of government climate models — **temperature** and
**CO2e price** — and runs them through an ensemble of simple models to produce
sector, macro and financial-market climate stresses (rates, inflation, credit,
equity, operational risk).

## Quick start

```bash
py -3 run_bkmn.py          # validate Table 4 + print a Table-11 style output
py -3 tests/check_table4.py  # full Table 4 reproduction check
```

Requires `numpy` and `pandas` (see `requirements.txt`).

## What is validated vs. simulated

The paper provides all the **UK structural/calibration data** but **not** the
climate scenario term-structures or the market curves. The reproduction is
therefore split:

| Block | Status | Basis |
|---|---|---|
| Input-Output carbon-tax → sector GVA shocks (**Table 4**) | ✅ **Validated** (max error 0.04pp) | Tables 2, 3 + Eq. 8/10 |
| Physical risk (GDP damage + vulnerability) | ✅ Implemented per Eq. 11 / Prop. 1 | Tables 2, 6 |
| Inflation, Taylor rule, HW1F rates, CDS/equity, op-risk | ⚙️ Implemented per Sec. 2.6–2.11 | Tables 8, 9, 10 + paper constants |
| SSP/RCP Bayesian mixture + transition matrix | ⚙️ Implemented per Eq. 1, 18–21 | paper priors |
| **Temperature & CO2e price paths** | ✅ **REAL** | MESSAGE-GLOBIOM SSP2 marker (IIASA SSP DB): World MAGICC6 temp + R5.2OECD carbon price |
| **GBP yield + inflation curves** | ✅ **REAL** | Bank of England GLC snapshot 2026-06-11 (nominal + implied-inflation spot) |
| **Carbon-pricing scope (Ω_XCE), HW1F σ** | 🔶 **ASSUMED** | scope=1.0 (paper gives no value); σ unused (shift is σ-independent) |

> The Table 4 block is a like-for-like reproduction (max error 0.04pp). Climate
> and market inputs are now real (`data/*.csv`, ingested from the supplied Excel
> by `tools/ingest_data.py`). The model reports both climate *shifts* and
> *absolute stressed levels* (base curve + shift). The rates/inflation/credit/
> equity figures still differ from the paper's Tables 11–14 because the paper used
> much *flatter* carbon/temperature paths than the MESSAGE marker (see the paper's
> own §3.3 note that "IPCC data shows minimal variation... a flat trend"). The only
> remaining assumed input is carbon-pricing scope; all non-paper values are tagged
> in [`bkmn/assumptions.py`](bkmn/assumptions.py).

## Layout

```
bkmn/
  data.py         paper tables (IO matrix, carbon intensity, vulnerability,
                  CDS↔GVA map, regression betas, op-risk betas, std-devs)
  assumptions.py  every value NOT in the paper, tagged [PAPER]/[DATA]/[ASSUMED]
  economy.py      Input-Output core, transition risk (Table 4), physical risk
  climate.py      REAL temperature & CO2e-price term structures per RCP (data/*.csv)
  curves.py       REAL BoE nominal + inflation spot curves (data/*.csv)
  scenarios.py    SSP/RCP priors, transition matrix (Eq 1), mixture evolution
  markets.py      inflation, Taylor rule, Hull-White 1F, CDS/equity, op-risk
  model.py        orchestrator → shifts + absolute stressed levels (RCP-weighted)
data/             ingested CSVs (temperature, carbon price, nominal & inflation curves)
tools/
  ingest_data.py  ETL: Excel sources -> data/*.csv
  inspect_xlsx.py  structure inspector for the Excel sources
run_bkmn.py       entry point
tests/check_table4.py  validation against Table 4
```

## Refreshing the data

The CSVs in `data/` were produced from the supplied Excel sources by:

```bash
py -3 tools/ingest_data.py   # reads D:\Download\{Temperature,price-carbon}.xlsx
                             #   and the BoE GLC yield-curve workbooks
```

## To make it a true reproduction

Replace the 🔶 simulated inputs with real data:

1. **Temperature paths** — IPCC AR6 WG1 (Table SPM.1 / climate-emulator output),
   per SSP/RCP, as incremental change from the start year.
2. **CO2e price paths** — IIASA SSP Scenario Database (`Price|Carbon`), converted
   USD2005 → GBP, per SSP/RCP marker.
3. **GBP yield + inflation curves** — observed market curves for the base date;
   calibrate Hull-White (`a`, `σ`).

These are wired through `bkmn/climate.py` and `bkmn/assumptions.py`, so swapping
them in does not touch the model logic.
