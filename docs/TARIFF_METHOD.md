# Tariffs as a tax: method and results

The project brief's second objective is to *"study alternative shocks to CO2
prices, e.g. tariffs, or changes in trade flows between regions"*. This note sets
out how tariffs are implemented, why they required almost no new machinery, and
what they produce — including the one carbon tariff that actually exists, the EU
Carbon Border Adjustment Mechanism.

Code: [`bkmn/tariff.py`](../bkmn/tariff.py) (general), [`bkmn/cbam.py`](../bkmn/cbam.py)
(the CBAM special case). Results: `out_sens_tariff_fx.csv`,
`out_sens_tariff_gva.csv`, `out_sens_cbam_gva.csv`, `out_sens_cbam_rates.csv`,
`figures/fig11`. Gates in [`tests/test_extensions.py`](../tests/test_extensions.py).

---

## 1. Why a tariff needs no new machinery

A tariff is structurally **the same object as the model's carbon charge**: an
ad-valorem cost wedge that propagates through the Leontief dual. The only
difference is where the wedge sits.

| | levied on | touches |
|---|---|---|
| Carbon charge | a sector's **own production** (Scope-1 emissions) | a per-sector charge `ct` |
| Tariff | a sector's **imported inputs** | the **off-diagonal blocks** of **A** |

Both are dimensionless — a fraction of the value of the good — so both enter the
same modified Leontief dual with no change to the mathematics of §2.4.

A tariff schedule is represented as a matrix

$$\mathrm{TAU}[k, d] \;=\; \text{ad-valorem rate on good } k \text{ entering region } d$$

where *k* indexes the 1000 region–industry pairs and *d* the 20 destination
regions. `tariff.add_rule` builds bilateral or universal schedules and never
applies a rate to intra-regional supply — a tariff falls on imports, not on
domestic sourcing.

**Consequently no new data is required.** A shock is specified by its *increment*
("the US raises tariffs on Chinese manufactures by 25 points"), not by a baseline
tariff database. WITS or the WTO Tariff Download Facility would be needed only to
model existing levels or the removal of specific agreements.

What a shock still needs is a *rate*, and a rate chosen for illustration carries
no evidential weight. §5.1 therefore calibrates one schedule to published
effective tariff rates so that at least one result describes a policy that exists;
§5.2 does the same for the EU side, which matters most here because the euro is
the base currency. §§5.3–5.4 report the mechanism findings, which are
qualitative and hold at any rate.

## 2. Incidence

Statutorily the importer pays, so the charge raises costs in the destination in
proportion to the tariffed inputs each industry uses:

$$\mathrm{cbam}_{\text{importer}}(j) \;=\; \theta \sum_{r \neq d}\sum_{i} A[(r,i),(d,j)]\; \tau(r,i)$$

Under elastic demand part of it would instead be absorbed by the exporter as a
lower price received. Since the model holds final demand fixed it cannot resolve
which happens, so an incidence parameter **θ** brackets the two: θ = 1 places the
whole charge on the importer (the legal position), θ = 0 on the exporter, scaled
by the share of that sector's output sold into the tariffing region.

Both are reported. Which is right depends on elasticities the framework excludes.

## 3. Where the charge goes: two routes, no double counting

**Intermediate imports** raise production costs and propagate through the dual —
this is what enters `ct`.

**Final-demand imports** are also charged (a tariff does not care what a good is
used for) but they raise *consumer* prices rather than producer costs, so they
generate revenue without entering the production chain. They were initially
omitted; 12.6 % of EU imports of CBAM-covered goods go straight to final demand,
and including them raises CBAM revenue from \$9.1 bn to **\$10.1 bn**.

## 4. Reaching FX — the project's actual deliverable

A tariff was at first computed as a side calculation that stopped at GVA. That is
the wrong structure: because the tariff charge is in the same units as `ct`, it
belongs *inside* the main chain, where it inherits the whole downstream —
Taylor rule, Hull–White term structure, FX, equity and operational risk.

The one route a tariff cannot inherit is **inflation**. §2.6's Moessner relation
is estimated on carbon prices and takes ΔXCE as its input, so it has nothing to
consume from a tariff. The tariff price effect is instead derived from the model's
own dual (`tariff.price_effect`):

$$\Delta \Pi^{\text{tariff}}_{d} \;=\; \frac{\sum_k \big[(\widetilde{\mathcal{L}}(\phi)\,\mathbf{ct}^{\text{tariff}})_k + \mathrm{TAU}[k,d]\big]\, y_{k,d}}{\sum_k y_{k,d}}$$

— the producer-price change from tariffed intermediate imports, weighted to a
consumer index by the destination's final-demand basket **y**, plus the direct
charge on tariffed final-demand imports. This is arguably the cleaner route, since
it comes from the model rather than a borrowed regression, and it leaves §2.6
exactly as the paper specifies it for carbon.

A permanent tariff is a price **level** shift, not an ongoing inflation rate, so
it enters the cumulative term — and hence spot/PPP FX — but not the inflation
*rate* at later horizons. Central banks look through one-off level jumps.

All results are reported as the **increment** over the same scenario run without
the tariff, so the underlying carbon baseline cancels.

---

## 5. Results

Six shocks, at 2040, φ = 0.5, statutory incidence. The first four are calibrated
to measures actually in force (§§5.1–5.2); the last two are stylised, and carry
the mechanism results, which hold at any rate.

| Shock | Revenue (\$bn/yr) | of which intermediate | Consumer-price level effect |
|---|--:|--:|---|
| **US applied tariffs, May 2026** | **260.0** | **109.3** | **USA +0.714 %** |
| **EU–US framework, Jul 2026** | **105.7** | **44.8** | **USA +0.295 %** |
| **EU steel safeguard 2026/1384** | **10.3** | **10.1** | **EU27 +0.015 %** |
| CBAM (EU, applied prices) | 10.1 | 9.1 | EU27 +0.020 % |
| USA 25 % on Chinese manufactures | 112.8 | 39.6 | USA +0.333 % |
| Global 10 % on all imports | 2,251.9 | 1,350.4 | SGP +4.29 %, EU27 +1.25 %, USA +1.03 % |

### 5.1 A scenario calibrated to announced policy

The stylised rates above were chosen for illustration. To ground at least one
case, a schedule is calibrated to published *effective* rates — duties actually
collected divided by import value, which already nets out exemptions,
de-minimis treatment and the tariff-line composition of trade, and is therefore
the right object to compare with an ad-valorem wedge on an aggregated IO table.

The [Penn Wharton Budget Model](https://budgetmodel.wharton.upenn.edu/p/2026-07-13-effective-tariff-rates-and-revenues-updated-july-13-2026/)
(13 July 2026) puts the **US average effective tariff rate at 7.2 %** as of May
2026, against 2.3 % in January 2025, with **China the highest major partner at
23.4 %** ([USAFacts](https://usafacts.org/answers/what-is-the-average-us-tariff-rate-overall/countries/china/)).
Rates fell back from their 2025 peak after the Supreme Court held the IEEPA
tariffs unconstitutional in February 2026; the residual reflects the
statutory authorities that survived (MFN, Section 301, Section 232).

Two published numbers pin the schedule, because China's import share is known
from the table itself:

| | |
|---|--:|
| China's share of US imports (intermediate + final, 2022 table) | 14.7 % |
| Effective rate on China (published) | 23.4 % |
| ⇒ implied rate on all other origins | **4.4 %** |
| check: 0.147 × 23.4 + 0.853 × 4.4 | **7.2 %** ✓ |

So the calibrated schedule is **23.4 % on China, 4.4 % on everyone else**, and it
reproduces the published aggregate by construction — a gate asserts this to
within 0.2 pp. Two independent checks support the base it is applied to: the
table's US import total is \$3.61 tn against BEA's \$3.96 tn for 2022 goods and
services, and the resulting revenue of **\$260 bn/yr** is the right order for
recent US customs receipts.

The results are materially larger than the stylised US shock, and for a reason
worth stating: a 25 % tariff on Chinese manufactures sounds more aggressive than
"7.2 % on average", but it touches one origin and one part of one origin's
exports, whereas the real schedule taxes **every** import. Breadth dominates
depth. The dollar moves **+0.71 % against the euro** — a depreciation, per §5.2 —
against +0.33 % for the stylised China shock, and US GVA falls 0.056 %. China
supplies 48 % of the revenue on 14.7 % of the imports.

The stylised 25 % on Chinese manufactures turned out close to the observed 23.4 %
effective rate on China; the stylised 10 % universal tariff overstates the actual
US average by a factor of about 1.4.

### 5.2 EU-side measures

The US calibration above says nothing about the EU, which is this model's base
currency and therefore the region whose policy matters most for an FX result.
The EU is a **low-tariff jurisdiction acting through instruments rather than
rates** — its weighted applied MFN tariff is about 1.3 % ([World Bank](https://tradingeconomics.com/european-union/tariff-rate-applied-weighted-mean-all-products-percent-wb-data.html),
2022) — so the measures worth modelling are specific ones, not an average.

**The EU carbon price is no longer an estimate.** CBAM entered its definitive
regime on 1 January 2026, and the Commission now publishes a quarterly
certificate price defined as the weighted average of EU ETS auction clearing
prices: **€75.36** for Q1 2026 and **€75.28** for Q2
([DG TAXUD](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/price-cbam-certificates_en)).
At EUR/USD 1.144 that is **\$86/t**, which replaces the \$80 `[ESTIMATE]`
previously carried for EU27 in `region_carbon_map.csv` — and it is exactly the
right series, since the same published price defines both the EU ETS level and
the CBAM reference. Raising the EU price from \$80 to \$86 lifts CBAM revenue
from \$9.4 bn to **\$10.1 bn** and the EU GVA cost from −0.0100 % to −0.0108 %.
Every CBAM figure below is at the published price.

**CBAM is phased in, and our reporting year is past the end of it.** The charge
does not apply in full from day one: it tracks the phase-out of EU ETS free
allocation to the covered sectors, so only **2.5 %** of embedded emissions
generate a certificate obligation in 2026, rising 5 %, 10 %, 22.5 %, 48.5 %,
61 %, 73.5 %, 86 % and reaching **100 % in 2034**. `cbam.phase_in` carries this
schedule. It leaves the headline result unchanged — everything here is reported
at 2040, past full phase-in — but it means a CBAM number quoted for any year
before 2034 is wrong without it, by up to 40× in 2026 (\$0.25 bn, not \$10.1 bn).
Presenting the fully phased-in figure as though it were current would have been a
real error, and the schedule is now gated.

**The EU's steel safeguard costs the EU more than its carbon border does.**
Regulation (EU) 2026/1384, applying from 1 July 2026, replaces the old safeguard:
the tariff-free quota falls 47 % to **18.3 Mt** and the out-of-quota duty
**doubles from 25 % to 50 %** across 30 product categories. A tariff-rate quota
is not an ad-valorem rate, so it is converted to the average rate paid on the
flow — 50 % times the above-quota share. With EU steel imports near 30 Mt in
2025 ([EUROFER](https://gmk.center/en/news/steel-imports-into-the-eu-rose-by-14-y-y-in-2025-eurofer/)),
roughly 39 % sits above quota, giving an average **19.5 %** on EU steel imports.

That single-sector measure costs EU27 **−0.0127 %** of GVA against CBAM's
**−0.0108 %**, on comparable revenue (\$10.3 bn vs \$10.1 bn) — despite CBAM
spanning five industries and steel being one. The EU's protectionist instrument
is a larger drag on the EU economy than its climate instrument, which is worth
stating plainly given that CBAM attracts far more attention as a trade barrier.

**The EU–US framework is a tariff the US pays.** In force 1 July 2026, it caps
most EU goods entering the US at an all-inclusive **15 %** while the EU
eliminates tariffs on US industrial goods
([European Commission](https://commission.europa.eu/topics/trade/eu-us-trade-deal_en)).
Because schedules here are increments from a zero-tariff baseline, the EU-side
liberalisation enters as a *negative* wedge of 1.33 % — the MFN rate it removes.
The result is asymmetric in the direction the mechanism predicts: US GVA
**−0.023 %** and the dollar **+0.30 % weaker against the euro**, against EU27
GVA of **−0.0003 %**, essentially nil. Under statutory incidence the 15 % is
paid by American importers, so the deal's measured cost falls on the country that
levied it, while the EU's own concession is too small to register.

Two caveats on that last result, both from §6. With no trade diversion the model
cannot capture the lost EU export volumes that are the deal's actual bite for
European exporters, and under θ = 0 the burden moves to those exporters' margins.
The finding is about where a tariff's *cost-push* incidence lands, not a welfare
verdict on the agreement.

Not modelled, for want of a clean mapping to ICIO industries: the EU's definitive
countervailing duties on Chinese battery electric vehicles (7.8–35.3 % on top of
the 10 % MFN car tariff, in force since October 2024, with a minimum-import-price
alternative agreed in principle in January 2026 but not implemented), which sit
inside ICIO's motor-vehicles industry C29 and cannot be separated from it at this
aggregation.

### 5.3 A tariff weakens the currency that levies it

The 25 % US tariff on Chinese manufactures moves **USD +0.33 % against the euro** —
the dollar *depreciates*. The mechanism is direct: the tariff raises US consumer
prices by 0.33 %, and under relative purchasing-power parity the currency with the
higher price level weakens. The common intuition that protection strengthens a
currency does not survive in a price-level channel.

Note the asymmetry with the incidence assumption. Under θ = 1 the tariff is a tax
on American consumers and the dollar bears it; under θ = 0 the burden moves to
Chinese exporters' margins and the dollar effect largely disappears.

### 5.4 The cross-section of a trade war is import dependence

Under the universal 10 % tariff, the spot FX response correlates **0.926** with
each region's imported share of intermediate inputs:

| Region | Imported input share | Spot vs EUR |
|---|--:|--:|
| Singapore | 50.8 % | **+3.04 %** |
| Turkey | 26.6 % | +0.99 % |
| Korea | 23.7 % | +0.45 % |
| Norway | 22.6 % | +1.12 % |
| Australia | 10.5 % | +0.23 % |
| United States | 8.2 % | **−0.22 %** |
| China | 7.7 % | **−0.58 %** |

Import-dependent economies see their price level rise most and depreciate; closed
economies *appreciate* in relative terms because their prices rise least. To a
first approximation the FX consequence of a global trade war is a ranking of who
depends on imports — the same openness ordering that emerges from the
input–output flow structure, now expressed in currencies.

### 5.5 CBAM: enormous sector rates, negligible macro effect

The CBAM rate is the price differential applied to embodied carbon,

$$\tau(r,i) \;=\; \max\!\left(0,\; \mathrm{XCE}_{\mathrm{EU}} - \mathrm{XCE}_r\right)\cdot \mathrm{CI}(r,i)\cdot 10^{-6}$$

with coverage from CBAM Annex I mapped to ICIO industries (C23 cement, C24A
steel, C24B aluminium, D electricity, and 15 % of C20 for fertilisers and
hydrogen). Origin prices are the carbon price each region *already applies*, since
a border adjustment only exists where prices differ.

Sector rates are extreme:

| Origin – sector | Carbon intensity (t/\$m) | CBAM rate |
|---|--:|--:|
| Kazakhstan – electricity | 18,830 | **160 %** |
| India – electricity | 9,095 | 78 % |
| Indonesia – electricity | 7,614 | 64 % |
| Africa – electricity | 5,865 | 50 % |
| Middle East – electricity | 5,739 | 49 % |

Kazakh electricity carries a charge larger than the electricity is worth: at
\$86/t its embodied carbon is worth more than the good itself. Yet the macro
effect is **−0.011 %** of EU GVA on \$10.1 bn of revenue. Covered sectors are a small share of
EU imports, so a policy with extreme sectoral rates barely registers in aggregate.
**Coverage, not the rate, is the binding constraint.**

Incidence flips the burden entirely:

| θ | EU27 | TUR | RUS | KAZ |
|---|--:|--:|--:|--:|
| 1 (EU importer pays) | **−0.0108 %** | −0.0017 % | −0.0006 % | −0.0002 % |
| 0.5 | −0.0061 % | −0.0118 % | −0.0107 % | −0.0073 % |
| 0 (exporter absorbs) | −0.0013 % | **−0.0220 %** | **−0.0208 %** | **−0.0144 %** |

### 5.6 CBAM self-extinguishes under policy convergence

Repricing the same mechanism at NGFS Net-Zero carbon prices — where the scenario
assumes near-uniform global carbon pricing — cuts revenue from \$10.1 bn to
**\$1.6 bn**, a fall of 84 %. CBAM is a response to policy *fragmentation*: if the
world converges on a common carbon price there is nothing left to adjust at the
border. That is a policy-relevant result that follows directly from the scenario
set rather than from any additional assumption.

---

## 6. Limitations

**No trade diversion.** This is the binding one. With final demand fixed (§2.4)
nobody re-sources away from a tariffed origin, so what is measured is the
cost-push incidence of the charge and not the reallocation of trade — often a
tariff's principal purpose. Every result here therefore *understates* the effect
of a tariff, and the CBAM figure of −0.010 % should be read with that in mind. The
fix is Armington elasticities (available free from published tables, e.g.
Caliendo & Parro 2015) applied to reallocate **A**'s off-diagonal blocks before
inversion — but it departs from the paper's inelastic-demand assumption and would
belong as a labelled extension.

**Incidence is assumed, not derived.** θ brackets the range rather than resolving
it, for the same reason.

**No retaliation.** Each schedule is applied unilaterally; a real trade war is a
sequence of responses.

**Coverage estimates.** The 15 % share of chemicals attributed to fertilisers and
hydrogen is an estimate, as are the applied carbon prices used for the CBAM
differential. Both are tagged in the code and are natural sweep parameters.

**Static structure.** The 2022 input–output table is applied throughout, so the
supply-chain reconfiguration a sustained tariff would cause is absent by
construction.

---

## 7. Validation

Fourteen gates cover the tariff machinery: that the CBAM phase-in follows the
statutory schedule and scales revenue linearly; that the calibrated US schedule
reproduces the published 7.2 % effective rate; the schedule shape; that `add_rule`
targets only the named origin and destination; that a tariff never applies to
intra-regional supply; that θ = 1 charges only the importer and θ = 0 only the
exporter; that revenue is invariant to the incidence split; that final-demand
imports raise revenue; that the CBAM rate is zero for the levying region, zero
outside covered industries, and zero where the origin already pays more than the EU; that CBAM shrinks when carbon prices converge; and
that a tariff now moves both rates and FX — the check that would have caught the
original omission.
