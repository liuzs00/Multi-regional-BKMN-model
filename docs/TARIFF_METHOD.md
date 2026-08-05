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
and including them raises CBAM revenue from \$8.4 bn to **\$9.4 bn**.

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

Three shocks, at 2040, φ = 0.5, statutory incidence.

| Shock | Revenue (\$bn/yr) | of which intermediate | Consumer-price level effect |
|---|--:|--:|---|
| CBAM (EU, applied prices) | 9.4 | 8.4 | EU27 +0.019 % |
| USA 25 % on Chinese manufactures | 112.8 | 39.6 | USA +0.333 % |
| Global 10 % on all imports | 2,251.9 | 1,350.4 | SGP +4.29 %, EU27 +1.25 %, USA +1.03 % |

### 5.1 A tariff weakens the currency that levies it

The 25 % US tariff on Chinese manufactures moves **USD +0.33 % against the euro** —
the dollar *depreciates*. The mechanism is direct: the tariff raises US consumer
prices by 0.33 %, and under relative purchasing-power parity the currency with the
higher price level weakens. The common intuition that protection strengthens a
currency does not survive in a price-level channel.

Note the asymmetry with the incidence assumption. Under θ = 1 the tariff is a tax
on American consumers and the dollar bears it; under θ = 0 the burden moves to
Chinese exporters' margins and the dollar effect largely disappears.

### 5.2 The cross-section of a trade war is import dependence

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

### 5.3 CBAM: enormous sector rates, negligible macro effect

The CBAM rate is the price differential applied to embodied carbon,

$$\tau(r,i) \;=\; \max\!\left(0,\; \mathrm{XCE}_{\mathrm{EU}} - \mathrm{XCE}_r\right)\cdot \mathrm{CI}(r,i)\cdot 10^{-6}$$

with coverage from CBAM Annex I mapped to ICIO industries (C23 cement, C24A
steel, C24B aluminium, D electricity, and 15 % of C20 for fertilisers and
hydrogen). Origin prices are the carbon price each region *already applies*, since
a border adjustment only exists where prices differ.

Sector rates are extreme:

| Origin – sector | Carbon intensity (t/\$m) | CBAM rate |
|---|--:|--:|
| Kazakhstan – electricity | 18,830 | **149 %** |
| India – electricity | 9,095 | 73 % |
| Indonesia – electricity | 7,614 | 59 % |
| Indonesia – steel / aluminium | ~5,520 | 43 % |

Kazakh electricity carries a charge larger than the electricity is worth: at
\$80/t its embodied carbon exceeds the value of the good. Yet the macro effect is
**−0.010 %** of EU GVA on \$9.4 bn of revenue. Covered sectors are a small share of
EU imports, so a policy with extreme sectoral rates barely registers in aggregate.
**Coverage, not the rate, is the binding constraint.**

Incidence flips the burden entirely:

| θ | EU27 | TUR | RUS | KAZ |
|---|--:|--:|--:|--:|
| 1 (EU importer pays) | **−0.0100 %** | −0.0015 % | −0.0005 % | −0.0002 % |
| 0.5 | −0.0056 % | −0.0110 % | −0.0100 % | −0.0068 % |
| 0 (exporter absorbs) | −0.0012 % | **−0.0204 %** | **−0.0194 %** | **−0.0133 %** |

### 5.4 CBAM self-extinguishes under policy convergence

Repricing the same mechanism at NGFS Net-Zero carbon prices — where the scenario
assumes near-uniform global carbon pricing — cuts revenue from \$9.4 bn to
**\$1.6 bn**, a fall of 83 %. CBAM is a response to policy *fragmentation*: if the
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

Eleven gates cover the tariff machinery: the schedule shape; that `add_rule`
targets only the named origin and destination; that a tariff never applies to
intra-regional supply; that θ = 1 charges only the importer and θ = 0 only the
exporter; that revenue is invariant to the incidence split; that final-demand
imports raise revenue; that the CBAM rate is zero for the levying region, zero
outside covered industries, and zero where the origin already pays more (Norway
at \$85 against the EU's \$80); that CBAM shrinks when carbon prices converge; and
that a tariff now moves both rates and FX — the check that would have caught the
original omission.
