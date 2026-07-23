# DATA_12R — Multi-regional BKMN calibration tables


Produced by [`tools/build_multiregion.py`](../tools/build_multiregion.py) (IO
tables) and [`tools/build_ghg.py`](../tools/build_ghg.py) (emissions +
intensity) from `D:\Download\2016-2022_SML\` (source ZIP kept at
`data/icio/ICIO2025_2016-2022_SML.zip`, gitignored).

## Regions (12)

Split into **FX-analytical** regions (one sovereign currency each → produce an
X/EUR FX shock) and **structural** regions (multi-country aggregates: included
for trade, embodied carbon, CBAM exposure and physical damage, but **no FX**).

| Code | Region | Class | Currency | Why chosen |
|---|---|---|---|---|
| EU27 | European Union (27 members summed) | FX **base** | EUR | CBAM levier; climate-policy leader; the numeraire for the FX objective |
| USA | United States | FX | USD | Largest economy, **no federal carbon price** — the policy contrast; deepest markets |
| CHN | China | FX | CNY | Largest emitter + supply-chain node; **#1 CBAM-exposed exporter**; national ETS |
| GBR | United Kingdom | FX | GBP | UK ETS + own CBAM (2027); the validated single-country BKMN calibration |
| JPN | Japan | FX | JPY | G3, energy importer (fossil-price transmission), deep markets |
| IND | India | FX | INR | Fast-growing emitter, **high physical vulnerability**, CBAM-exposed steel, no carbon price |
| CAN | Canada | FX | CAD | G10 commodity currency + carbon tax + oil sands |
| NOR | Norway | FX | NOK | **Petrocurrency**; EU's #1 gas supplier; fossil exporter *with* high carbon price |
| IDN | Indonesia | FX | IDR | SE Asia anchor; coal export + peatland land-use; severe sea-level physical risk |
| MEA | Middle East (SAU, ARE, ISR, JOR) | structural | USD-peg | Fossil **supply-side** of transition risk; heat/water-vulnerable |
| AFR | Africa (ZAF, EGY, MAR, TUN, NGA, SEN, CIV, CMR, COD, AGO, STP) | structural | mixed | Physical-risk **frontier** (highest vulnerability); CBAM via ZA metals |
| ROW | Rest of World (all remaining economies + OECD's RoW, summed) | closure | — | Required for global IO balance; carries no financial outputs |

Notes: `MEA` here means **Middle East only** (not "Middle East & Africa"); it
and `AFR` both draw the same climate-scenario zone, R5.2**MAF**. Only the ICIO's
individually-listed economies are broken out, so `MEA`/`AFR` are the *major*
economies of each region — smaller ones fall into ROW.

## Two mapping layers

The economic and carbon dimensions come from different source datasets and do
not align, so they are kept as **two maps**:

- **`region_mapping.csv` — economic-flow map.** Each ICIO economy → region.
  Drives the MRIO (`Z`, GVA, output, trade, embodied carbon). Emissions and
  carbon intensity (from GHGFP, per economy) ride on this map.
- **`region_carbon_map.csv` — carbon/scenario map.** One row per region:
  `currency`, `fx_role`, `scenario_zone` (the NGFS/IAM R5.2 region supplying the
  carbon-price and temperature paths — the key bridge to climate-scenario data),
  `carbon_price_regime` (the *applied* policy price), `cbam_role`
  (levier / exposed-exporter / inside-perimeter), and `phys_vuln_tier`.

## Robustness — is the single ROW sufficient?

ROW lumps ~31 economies into one block; does that bias the 11 **analytical**
regions? (ROW's own outputs are never interpreted, so only they matter.) Tested
by aggregation-invariance ([`tools/test_row_sufficiency.py`](../tools/test_row_sufficiency.py)):
rebuild the model with ROW split into its largest, most carbon-intensive, most
EU-linked economies (RUS, KOR, TWN, MEX, BRA, TUR) + a residual, and compare.

Result (2022): breaking out those six worst-case economies changes every
analytical region's transition GVA shock by **< 0.005 pp** (vs shocks of
0.1–4.6%) and every Leontief output multiplier by **< 0.11%**. Because the six
are precisely the economies most able to bias the result, any finer ROW split
moves less — the aggregation has **converged**. The single-ROW closure is
therefore sufficient: analytical results are invariant to ROW granularity to
within rounding. (Consistent with the materiality bound: ROW is only 3–9% of any
analytical region's intermediate inputs.)

## Files

- `region_mapping.csv` — 81 source economies → 12 regions (economic map).
- `region_carbon_map.csv` — the 12 regions → currency / scenario zone / carbon
  policy / CBAM role / physical-vulnerability tier (carbon map).
- `industry_mapping.csv` — the 50 ISIC Rev.4 industry codes (unchanged from the
  ICIO 2025 edition; region choice does not affect industries).
- `ICIO2025_12R_2022.csv` — *(to be generated)* aggregated 12-region IO table,
  shape 603 × 673: rows = 12×50 industries + `TLS`/`VA`/`OUT`; columns = 12×50
  industry + 12×6 final-demand + `OUT`. Current USD millions.
- `GHG_S1_12R_2022.csv` — *(to be generated)* Scope-1 GHG (Mt CO2e), 50
  industries × 12 regions.
- `CARBON_INTENSITY_12R_2022.csv` — *(to be generated)* direct carbon intensity
  `CI = Scope-1 / gross output`, tonnes CO2e per USD-million. With `XCE` in
  USD/t the per-output charge is `ct = CI × XCE × 1e-6`.


## Units & conventions

- ICIO cells: current **USD millions**, basic prices (flows `Z`, final demand,
  `TLS`, `VA`, `OUT`).
- `GHG_S1_12R`: **Mt CO2e**, all gases, Scope 1 (industry's own direct emissions;
  household direct emissions excluded, as in the paper).
- `CARBON_INTENSITY_12R`: **tonnes CO2e per USD-million** of gross output;
  `CI(r,j) = E_S1(r,j) / x(r,j)`, numerator and denominator from the same ICIO
  2025 accounting system.
- Aggregation = plain **summation** of current-price flows (exact for IO tables;
  no weighting). EU27, MEA, AFR and ROW are summations of their member economies'
  rows/columns, so intra-region flows fall on the diagonal block exactly as
  domestic flows do for single-country regions.
