# DATA_20R — Multi-regional BKMN calibration tables (20-region)

20-region Inter-Country Input-Output tables from the **OECD ICIO 2025 edition**
(SML, current USD millions, 2022). Extends the 16-region design with **Singapore,
Turkey, Korea, and Kazakhstan** — the dominant economies inside the old ROW by
EU trade and by carbon embodied in EU imports. Supersedes the earlier 12- and 16-region builds.

Produced by [`tools/build_multiregion.py`](../tools/build_multiregion.py) (IO)
and [`tools/build_ghg.py`](../tools/build_ghg.py) (emissions + intensity) from
`D:\2016-2022_SML\`.

## Regions (20)

**FX-analytical** (one sovereign currency → X/EUR FX shock) and **structural**
aggregates (multi-country: trade / embodied carbon / CBAM / physical damage, no FX).

| Code | Region | Class | Currency | Note |
|---|---|---|---|---|
| EU27 | European Union (27) | FX **base** | EUR | CBAM levier; numeraire |
| USA | United States | FX | USD | no federal carbon price |
| CHN | China | FX | CNY | top emitter; CBAM-exposed |
| GBR | United Kingdom | FX | GBP | UK ETS + CBAM 2027 |
| JPN | Japan | FX | JPY | energy importer |
| IND | India | FX | INR | high physical vuln.; carbon-intensive |
| CAN | Canada | FX | CAD | carbon tax; oil sands |
| NOR | Norway | FX | NOK | petrocurrency; EU gas |
| IDN | Indonesia | FX | IDR | coal + peatland |
| RUS | Russia | structural | RUB | fossil exporter; RUB non-convertible → no FX |
| CHL | Chile | FX | CLP | copper/lithium; carbon tax |
| AUS | Australia | FX | AUD | coal/LNG; severe physical risk |
| **SGP** | **Singapore** | **FX** | SGD | refining/petrochem + finance hub; carbon tax |
| **TUR** | **Turkey** | **FX** | TRY | **#1 ROW CBAM-steel exporter to EU**; EU customs union |
| **KOR** | **Korea** | **FX** | KRW | advanced manufacturing; K-ETS; deep FX |
| **KAZ** | **Kazakhstan** | **FX** | KZT | fossil (highest carbon intensity in the model); R5.2REF |
| MEA | Middle East (SAU, ARE, ISR, JOR) | structural | USD-peg | fossil supply-side |
| AFR | Africa (ZAF, EGY, MAR, TUN, NGA, SEN, CIV, CMR, COD, AGO, STP) | structural | mixed | physical-risk frontier |
| LAM | Latin America ex-Chile (ARG, BRA, COL, CRI, MEX, PER) | structural | mixed | agri/land-use carbon |
| ROW | Rest of World (remaining ~18 economies + OECD RoW) | closure | — | global IO balance; no financial outputs |

Two mapping layers: `region_mapping.csv` (economic — 81 ICIO economies → region)
and `region_carbon_map.csv` (carbon/scenario — currency, FX role, NGFS R5.2 zone,
carbon-price regime, CBAM role, physical-vulnerability tier, PPP-GDP welfare weight).

## Files

- `ICIO2025_20R_2022.csv` — aggregated IO table, shape **1003 × 1121**: rows =
  20×50 industries + `TLS`/`VA`/`OUT`; columns = 20×50 industry + 20×6
  final-demand + `OUT`. Current USD millions. Whole-table checksum $300.5T (preserved by aggregation; it
  sums Z + final demand + TLS + VA and so double-counts). Economic magnitudes:
  world gross output $199.7T, world value added $93.8T.
- `GHG_S1_20R_2022.csv` — Scope-1 GHG (Mt CO2e), 50 industries × 20 regions;
  world total 44.2 Gt.
- `CARBON_INTENSITY_20R_2022.csv` — `CI = Scope-1 / gross output`, tonnes CO2e
  per USD-million (`ct = CI × XCE × 1e-6`).
- `region_mapping.csv`, `region_carbon_map.csv`, `industry_mapping.csv`, `industries.csv`.

## Units & conventions

- ICIO cells: current **USD millions**, basic prices.
- `GHG_S1_20R`: **Mt CO2e**, all gases, Scope 1 (household direct emissions excluded).
- `CARBON_INTENSITY_20R`: **tonnes CO2e per USD-million** of gross output.
- Aggregation = plain **summation** of current-price flows (exact for IO tables).
  EU27, MEA, AFR, LAM and ROW are summations of their member economies' rows and
  columns, so intra-region flows fall on the diagonal block exactly as domestic flows.

## Regenerate

`py -3 tools/build_multiregion.py` → ICIO; `py -3 tools/build_ghg.py` → emissions +
intensity (needs `D:\2016-2022_SML\` + GHGFP `data/ghgfp/SCOPE/2022.csv.gz`).
`py -3 tools/build_ppp_weights.py` refreshes PPP weights (World Bank API).
`py -3 compute_transition.py` regenerates the `out_*.csv` transition results.
