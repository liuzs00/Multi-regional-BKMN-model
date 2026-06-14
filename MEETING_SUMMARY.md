# Meeting Summary — BKMN Model Reproduction

**Date:** 2026-06-15
**Topic:** Reproducing the BKMN climate stress-testing model (SSRN-5130573) in Python

## Objective
Reproduce the BKMN model from the paper *"Simple climate stress testing: an
ensemble framework"* (Berrahoui, Kenyon, Macrina, Nathanael, 2025), using the
data provided in the paper and simulating any missing inputs.

## Key discussion points
- **Data availability review.** The paper provides all UK structural/calibration
  data (Input-Output table, carbon intensity, vulnerability, CDS↔GVA mapping,
  regression betas, op-risk betas, std-devs) but **does not** provide the climate
  scenario term-structures or market curves.
- **Missing data identified:** temperature & CO2e price paths per SSP/RCP, the
  GBP yield/inflation curves, transition parameter λ, and carbon-pricing scope.
- **External data located:** temperature anchors from IPCC AR6 WG1 Table SPM.1;
  carbon prices available (not turnkey) from the IIASA SSP Scenario Database.

## Decisions
- Build a modular Python package; isolate all non-paper inputs in a single
  `assumptions.py` with `[PAPER]` / `[SIMULATED]` / `[MARKET]` tags.
- Validate against the one fully-reproducible result in the paper: **Table 4**.
- Simulate temperature (IPCC-anchored) and CO2e-price paths to make the model run.

## Outcome
- **Table 4 reproduced to within 0.04 percentage points** — confirms the IO core,
  carbon-charge units, and modified Leontief dual are correct.
- Finding: Table 2 carbon intensity must be treated as **kilo-tonnes/£m** (×1000)
  for Table 4 to reproduce — a units discrepancy in the paper.
- Full ensemble runs end-to-end (rates, inflation, credit, equity, op-risk),
  reproducing the paper's qualitative signatures (Utilities largest credit impact,
  rates fall, FTSE negative).

## Open questions / next steps
- Confirm simulation **start year** (paper uses 2024 only in a damage worked
  example; structural data is 2021, IPCC anchor is 2023).
- Swap simulated temperature/CO2e paths for real IPCC/IIASA series (annual,
  2024–2044, 5 RCP series each).
- Optional: add the volatility extension (§3.3) and the multi-regional / FX
  extension implied by the repo name.

## Status
Rates/inflation/credit/equity outputs are **illustrative** (driven by simulated
inputs); only the Table 4 transition-risk block is a validated reproduction.
