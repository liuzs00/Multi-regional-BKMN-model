# DATA_13R — Multi-regional BKMN calibration tables

13-region Inter-Country Input-Output tables built from the **OECD ICIO 2025
edition** (SML format, current USD millions) for the multi-regional BKMN
project. Produced by [`tools/build_multiregion.py`](../tools/build_multiregion.py)
from `D:\Download\2016-2022_SML\` (source ZIP kept at
`data/icio/ICIO2025_2016-2022_SML.zip`, gitignored).

## Regions (13)

| Code | Region | Construction | Why chosen |
|---|---|---|---|
| GBR | United Kingdom | single country | Home region of the original BKMN model — the validated single-country calibration (ONS/BoE data) anchors the multi-region extension. Deep markets for all financial channels. |
| EU27 | European Union | **sum of all 27 member states** | Largest trading bloc, one currency/policy unit, and home of the world's most mature carbon market (EU ETS) — the benchmark transition-policy region. |
| ZAF | South Africa | single country | The most coal-dependent power sector among major economies (highest electricity carbon intensity in our data), and Africa's representative — activates the R5.2MAF scenario region. |
| RUS | Russia | single country | Major fossil-fuel exporter: the supply side of transition risk. Financial-market channels are assumption-driven (post-2022 market isolation); maps to R5.2REF. |
| CHN | China | single country | Largest emitter and the world's central manufacturing/supply-chain node — indispensable for trade-propagated stress. |
| KOR | Korea | single country | Advanced-manufacturing hub (semiconductors, shipbuilding, steel) inside the East-Asia supply chain, with its own ETS (K-ETS). Maps to R5.2ASIA, not OECD. |
| JPN | Japan | single country | G3 economy and deep financial markets; large energy importer, so exposed to fossil-price transmission rather than production. |
| IND | India | single country | Third-largest emitter with the fastest-growing coal demand and among the highest physical climate vulnerability — the key forward-looking climate economy. |
| AUS | Australia | single country | Major coal/mining exporter (directly exposed via the new B05/C24A sectors) with severe physical risk (fire/drought), yet OECD-grade financial data. |
| CAN | Canada | single country | Policy-heterogeneity anchor: the most aggressive legislated carbon-tax schedule in the G20, plus oil-sands exposure and a G10 commodity currency for the FX extension. |
| USA | United States | single country | Largest economy and deepest markets; no federal carbon price, making it the natural policy contrast to EU27/CAN in transition scenarios. |
| BRA | Brazil | single country | Largest Latin-American economy with an agriculture/land-use-heavy emission profile (high CH4/N2O intensity); activates the R5.2LAM scenario region. |
| ROW | Rest of World | **sum of the remaining 42 economies + OECD's RoW** | Not a modeled choice: the closure region required for the global IO accounting to balance. Gets no financial outputs. |

## Files

- `GHG_S1_13R_2022.csv` — **Scope-1 GHG emissions** (Mt CO2e), rows = 50
  industries, cols = 13 regions. From OECD GHGFP 2025 (`SCOPE` dataflow,
  `EMISSIONS_SCOPE = S1`), TeCO2's successor, built on the same ICIO 2025
  system. GHGFP's `WXD` residual is mapped to `ROW`; GHGFP industry codes
  `C241_2431/C242_2432/C30X301` renamed to ICIO's `C24A/C24B/C302T309`.
  Households' direct emissions are excluded (not an industry), as in the paper.
- `CARBON_INTENSITY_13R_2022.csv` — **direct carbon intensity**
  CI(r,j) = Scope-1 emissions / gross output, in **tonnes CO2e per million
  USD of output** — the multi-region analogue of the paper's Table 2, and the
  input for the transition charge: with XCE in USD/t, the per-output rate is
  `ct = CI × XCE × 1e-6`. Produced by `tools/build_ghg_13r.py`.
- `ICIO2025_13R_2022.csv` 
2022 — aggregated tables, shape 653 × 729:
  - **rows**: 13 regions × 50 industries (`REGION_INDUSTRY`, e.g. `GBR_C24A`),
    then `TLS` (taxes less subsidies), `VA` (value added), `OUT` (total output)
  - **columns**: 13 × 50 industry columns, then 13 × 6 final-demand columns
    (`HFCE, NPISH, GGFC, GFCF, INVNT, DPABR`), then `OUT`
- `region_mapping.csv` — all 81 source economies → assigned region
- `industries.csv` — the 50 ISIC Rev.4 industry codes (2025-edition detail:
  A01/A02 split, B05/B06/B07/B08 mining splits, C24A/C24B metals, C301/C302T309)
- `industry_mapping.csv` — industry code map: ICIO code, full description,
  ISIC Rev.4 divisions, and the GHGFP code variant (`C24A ↔ C241_2431` etc.)


## Units & conventions

### Units by file

| File | Unit | Notes |
|---|---|---|
| `ICIO2025_13R_*.csv` | **current USD millions**, basic prices | as in the source ICIO; all cells (flows `Z`, final demand, `TLS`, `VA`, `OUT`) share this unit |
| `GHG_S1_13R_2022.csv` | **Mt CO2e** (million tonnes CO2-equivalent) | all greenhouse gases, Scope 1 (direct emissions of the industry itself) |
| `CARBON_INTENSITY_13R_2022.csv` | **tonnes CO2e per million USD of gross output** | with a carbon price `XCE` in USD/tCO2e, the per-output charge rate is `ct = CI × XCE × 1e-6` (dimensionless fraction of output value) |

### How CARBON_INTENSITY is constructed

`CI(r, j) = E_S1(r, j) / x(r, j)` where

- `E_S1(r, j)` = Scope-1 GHG emissions of industry `j` in region `r`, in tonnes,
  from the OECD **GHGFP 2025** `SCOPE` dataflow (`EMISSIONS_SCOPE = S1`,
  year 2022), aggregated to the 13 regions with the same country mapping as the
  ICIO tables. Two reconciliations: GHGFP's rest-of-world residual `WXD` is
  mapped to `ROW`, and GHGFP industry codes `C241_2431 / C242_2432 / C30X301`
  are renamed to ICIO's `C24A / C24B / C302T309`. Households' direct emissions
  (home heating, private vehicles) are not an industry and are excluded, as in
  the paper.
- `x(r, j)` = gross output of industry `j` in region `r`, in USD millions, from
  the `OUT` row of `ICIO2025_13R_2022.csv` — so numerator and denominator come
  from the same ICIO 2025 accounting system and industry classification.
- Cells with zero output get `CI = 0` (rather than NaN).

Reproducible via `py -3 tools/build_ghg_13r.py`.

### How the EU27 region is constructed

Plain **summation of all 27 member states' rows and columns** of the source
ICIO (and of their emissions in GHGFP): flows between two EU members thereby
become *intra-regional* flows on the diagonal block, exactly as domestic flows
are for single-country regions. Summation of current-price flows is the
standard, exact aggregation for IO tables — no weighting or averaging involved.
The same applies to `VA`, `TLS`, `OUT` and final-demand columns.

### How the ROW region is constructed

Sum of the **remaining 42 economies plus OECD's own "Rest of the World"**
entry, built identically to EU27. ROW is the *closure region*: the global IO
system only balances (every export has an importer) if all economies outside
the 12 chosen ones are retained as one aggregate. It carries no financial-market
outputs in the model — it exists so the Leontief accounting is globally
consistent, not as an analytical region.

### General conventions

- Aggregation = plain summation of flows (correct for current-price IO tables).
- OECD's published `OUT` values are kept as canonical (they embed the source's
  own ≤0.1% imbalances; see Validation above).
- Cross-check magnitudes, 2022: world gross output ≈ 300 T$, world VA ≈ 94 T$
  (basic prices), world industry Scope-1 GHG ≈ 44.2 Gt CO2e.
