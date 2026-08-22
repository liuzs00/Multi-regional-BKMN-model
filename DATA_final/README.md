# DATA_final — Multi-regional BKMN calibration tables (13-region)

13-region Inter-Country Input-Output tables from the **OECD ICIO 2025 edition**
(SML, current USD millions, 2022). The region set is **derived** by the selection
algorithm rather than asserted — see
[`docs/CHAPTER_REGION_SELECTION.md`](../docs/CHAPTER_REGION_SELECTION.md) for the
method and [`tools/select_regions_threshold.py`](../tools/select_regions_threshold.py)
for the code. Supersedes the earlier 20-region build, since removed, which
was chosen by argument.

Produced by [`tools/build_data_final.py`](../tools/build_data_final.py), which
**imports the region definition from the selection module and re-derives it at
build time**, so the data cannot drift from the method that justifies it.

## How the 13 regions were chosen

Shares below are of the EU27 final-demand footprint
$\mathbf{x}_{\mathrm{EU}} = (\mathbf{I}-\mathbf{A})^{-1}\mathbf{f}_{\mathrm{EU}}$
= \$32.16 tn — how much the EU depends on each economy, directly and through
supply chains. Two measures are carried: **economic** linkage, and **carbon**
linkage (the same weighted by carbon intensity).

1. **Threshold rule** — keep a candidate if it is top-10 by economic linkage, or
   above 1 % on economic *or* carbon linkage → 11 named regions. The carbon
   clause is what admits **AFR** (2.06 % carbon on 0.54 % economic) and **TUR**
   (1.10 % on 0.50 %), which a size ranking would discard.
2. **Residual split** — what is left would outrank China on both measures, so it
   is split by **NGFS R5 zone** (the resolution at which scenario carbon prices
   are published, so each group takes exactly one price path).
3. **Zone cleaning** — drop members whose carbon intensity exceeds 1.5× their own
   zone's average. Asia spans 15× uncleaned (Korea 85 t/\$m beside Cambodia
   1,268); cleaning cuts it to 4.0× for 0.21 % of economic linkage. Dropped
   economies fall into ROW.
4. **Promotion** — promote cleaned zones until ROW no longer dominates. One
   promotion suffices (**RASIA**), giving 13 regions.

## Regions (13)

| Code | Region | Class | Currency | econ % | carb % | CI (t/\$m) |
|---|---|---|---|--:|--:|--:|
| EU27 | European Union (27) | FX **base** | EUR | 81.00 | 58.73 | 88 |
| CHN | China | FX | CNY | 4.49 | **11.11** | 299 |
| USA | United States | FX | USD | 2.68 | 2.62 | 118 |
| GBR | United Kingdom | FX | GBP | 1.60 | 0.80 | 61 |
| **CHE** | **Switzerland** | **FX** | CHF | 1.00 | 0.16 | 20 |
| RUS | Russia | structural | RUB | 0.97 | **3.75** | 467 |
| IND | India | FX | INR | 0.59 | **2.80** | 574 |
| TUR | Türkiye | FX | TRY | 0.50 | **1.10** | 264 |
| **RASIA** | **Rest of Asia** (10) | structural | mixed | 1.82 | 3.22 | 214 |
| LAM | Latin America (7) | structural | mixed | 0.69 | 1.57 | 274 |
| MEA | Middle East (4) | structural | USD-peg | 0.64 | 1.27 | 240 |
| AFR | Africa (11) | structural | mixed | 0.54 | 2.06 | 462 |
| ROW | Rest of World (15) | closure | — | 3.47 | 10.80 | 376 |

**Members of the multi-economy regions**

- **EU27** — AUT BEL BGR CYP CZE DEU DNK ESP EST FIN FRA GRC HRV HUN IRL ITA LTU
  LUX LVA MLT NLD POL PRT ROU SVK SVN SWE
- **RASIA** — BGD BRN HKG KOR MYS PHL SGP THA TWN VNM
- **LAM** — ARG BRA **CHL** COL CRI MEX PER
- **MEA** — ARE ISR JOR SAU
- **AFR** — AGO CIV CMR COD EGY MAR NGA SEN STP TUN ZAF
- **ROW** — AUS BLR CAN IDN ISL JPN KAZ KHM LAO MMR NOR NZL PAK UKR + the ICIO's
  own unallocated residual

## What changed from the earlier 20-region build

| | 20-region build | DATA_final |
|---|---|---|
| Regions | 20, chosen by argument | 13, derived by rule |
| Switzerland | inside ROW at an assumed \$2/t | **own region**, CHF 120/t (≈\$133) |
| Chile | own region (0.05 % / 0.07 %) | folded into **LAM** |
| Japan, Korea, Norway, Canada, Australia, Indonesia, Singapore, Kazakhstan | own regions | Korea/Singapore → RASIA; rest → ROW |
| Latin America | ex-Chile (6) | **includes Chile** (7) |
| Residuals | one ROW (18 economies) | RASIA (promoted) + ROW (15) |

Switzerland is the substantive correction: it is the **4th-largest non-EU
economic linkage**, ahead of India, Japan and Korea, and was being modelled at
roughly a 65-fold error in its carbon price.

**Cost of the change.** The FX cross-section narrows from 14 analytical
currencies to **6** (USD, CNY, GBP, CHF, INR, TRY), because a currency exists in
the model only if its economy is a region. That follows from the linkage rule,
not from any judgement about FX, and is the main trade-off in adopting this set.

## Files

- `ICIO2025_13R_2022.csv` — aggregated IO table, shape **653 × 729**: rows =
  13×50 industries + `TLS`/`VA`/`OUT`; columns = 13×50 industry + 13×6
  final-demand + `OUT`. Current USD millions. World gross output **\$199.69 T**,
  value added **\$93.81 T**, intermediate flows **\$103.41 T** — all identical to
  the 20-region build, as they must be: a different partition of the same world.
- `GHG_S1_13R_2022.csv` — Scope-1 GHG (Mt CO₂e), 50 industries × 13 regions;
  world total **44.2 Gt**.
- `CARBON_INTENSITY_13R_2022.csv` — `CI = Scope-1 / gross output`, tonnes CO₂e
  per USD-million (`ct = CI × XCE × 1e-6`).
- `region_mapping.csv` — all 81 ICIO economies → region (economic layer).
- `region_carbon_map.csv` — currency, FX role, NGFS R5.2 zone, carbon-price
  regime, CBAM role, physical-vulnerability tier, PPP-GDP welfare weight,
  carbon-pricing scope, applied carbon price (carbon/scenario layer).
- `industries.csv`, `industry_mapping.csv` — the 50 ISIC Rev.4 codes and the
  crosswalk to GHGFP activity codes (region-independent; carried over unchanged).

## Units & conventions

- ICIO cells: current **USD millions**, basic prices.
- `GHG_S1_13R`: **Mt CO₂e**, all gases, Scope 1 (household direct emissions
  excluded). The GHGFP unit field reads `T_CO2E` but the magnitudes are millions
  of tonnes — China's 13,501 is 13.5 Gt.
- `CARBON_INTENSITY_13R`: **tonnes CO₂e per USD-million** of gross output.
- Aggregation = plain **summation** of current-price flows, which is exact for IO
  tables because the entries are values in a common currency. EU27, RASIA, LAM,
  MEA, AFR and ROW are summations of their members' rows and columns, so
  intra-region flows fall on the diagonal block exactly as domestic flows do.
- `carbon_scope` is the emissions-weighted mean of member economies' OWID
  carbon-price coverage; `ppp_gdp_weight` is the World Bank PPP-GDP share, with
  ROW as the residual so the column sums to exactly 1.000.

## Known artefacts

- **Small-denominator carbon intensities.** Switzerland's `B06` (oil & gas
  extraction) shows CI ≈ 6,811 t/\$m on gross output of **\$9.4 m** — a
  negligible sector that only became visible because CHE was promoted out of
  ROW. Any per-cell charge there is economically immaterial, but the intensity
  itself should not be quoted as a Swiss characteristic.
- **ROW is heterogeneous by design.** Its members span 69 t/\$m (Norway) to
  1,268 (Cambodia), an 18.3× range, because cleaning improves the reported
  blocks by moving their outliers into the one that is not interpreted. ROW is a
  closure term; its outputs should not be read as results.
- **ROW's carbon margin is thin.** It sits at 10.80 % carbon linkage against
  China's 11.11 %, and 6.73 pp of that is the ICIO's own unallocated block,
  which cannot be promoted or decomposed.
- The source table carries small OUT imbalances (worst ≈ 2 % relative on one
  small cell); linear aggregation passes them through unchanged, and OECD's
  published `OUT` is kept rather than recomputed.

## Regenerate

```
py -3 tools/build_data_final.py
```

Needs `D:\2016-2022_SML\2022_SML.csv`, `data/ghgfp/SCOPE/2022.csv.gz`,
`data/scope/owid_carbon_price_coverage.csv`, and network access for the World
Bank PPP series. If the World Bank API is unreachable the script leaves
`ppp_gdp_weight` **blank for every region** rather than carrying the 20-region
values, which would be wrong here because the groupings differ.

## Status

**In force.** This is the only calibration the model runs on. `bkmn.regions`
loads it, every table in `results/` and every figure is computed from it, and
the gate suites are baselined against it. The earlier 20-region build has been
removed; the per-region inputs outside this folder (`data/scope/`,
`data/physical/`, `data/macro/`, equity betas) were rebuilt for this region set
when it was adopted.
