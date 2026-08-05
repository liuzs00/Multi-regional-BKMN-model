# Tariffs as a tax: the method

The project brief's second objective is to *"study alternative shocks to CO2
prices, e.g. tariffs, or changes in trade flows between regions"*. This note sets
out how a tariff enters the model and illustrates it on one assumed case. It is
deliberately short: the mechanism is simple, and the complications belong to
calibration, not to the method.

Code: [`bkmn/tariff.py`](../bkmn/tariff.py); the worked example is
[`tools/run_tariff_illustration.py`](../tools/run_tariff_illustration.py)
(`out_illus_eu_tariff_*.csv`). Gates in
[`tests/test_extensions.py`](../tests/test_extensions.py). For the harder problem
of matching real announced measures — US and EU tariffs in force in 2026, CBAM at
published carbon prices, and the base-year sensitivity that comes with it — see
[TARIFF_CALIBRATION.md](TARIFF_CALIBRATION.md).

---

## 1. A tariff is the carbon charge in a different place

The model already has an ad-valorem cost wedge that propagates through the
Leontief dual: the carbon charge. A tariff is the same object, moved.

| | levied on | enters through |
|---|---|---|
| Carbon charge | a sector's **own production** (Scope-1 emissions) | a per-sector charge `ct` |
| Tariff | a sector's **imported inputs** | the **off-diagonal blocks** of **A** |

Both are dimensionless — a fraction of the value of the good — so a tariff needs
no new mathematics. It reuses the modified Leontief dual of §2.4 exactly.

A schedule is a matrix

$$\mathrm{TAU}[k, d] \;=\; \text{ad-valorem rate on good } k \text{ entering region } d$$

with *k* over the 1000 region–industry pairs and *d* over the 20 destinations.
`tariff.add_rule` builds bilateral or universal schedules and never charges
intra-regional supply: a tariff falls on imports, not on domestic sourcing.

Because a shock is specified as an *increment* from a zero-tariff baseline, **no
tariff database is needed** to run one. A rate is an input, not a lookup.

## 2. Who pays: the incidence parameter θ

Statutorily the importer pays, so the charge raises costs in the destination in
proportion to the tariffed inputs each industry uses:

$$c_{\text{importer}}(j) \;=\; \theta \sum_{r \neq d}\sum_{i} A[(r,i),(d,j)]\; \tau(r,i)$$

Under elastic demand part would instead be absorbed by the exporter as a lower
price received. The model holds final demand fixed and so cannot resolve which
happens; **θ** brackets it. θ = 1 puts the whole charge on the importer (the legal
position), θ = 0 on the exporter, scaled by the share of that sector's output
sold into the tariffing region. Both are reported. Which is right depends on
elasticities this framework excludes.

## 3. Two routes for the charge, no double counting

**Intermediate imports** raise production costs and propagate through the dual —
this is what enters `ct`.

**Final-demand imports** are charged too (a tariff does not care what a good is
used for), but they raise *consumer* prices rather than producer costs, so they
generate revenue without entering the production chain.

## 4. Reaching FX

Because the tariff charge is in the same units as `ct`, it goes *inside* the main
chain and inherits the whole downstream: Taylor rule, Hull–White term structure,
FX, equity, operational risk.

The one route it cannot inherit is **inflation**. §2.6's Moessner relation is
estimated on carbon prices and takes ΔXCE as input, so a tariff has nothing to
feed it. The tariff price effect comes instead from the model's own dual
(`tariff.price_effect`):

$$\Delta \Pi^{\text{tariff}}_{d} \;=\; \frac{\sum_k \big[(\widetilde{\mathcal{L}}(\phi)\,\mathbf{ct}^{\text{tariff}})_k + \mathrm{TAU}[k,d]\big]\, y_{k,d}}{\sum_k y_{k,d}}$$

— producer-price change from tariffed intermediate imports, weighted to a
consumer index by the destination's final-demand basket **y**, plus the direct
charge on tariffed final-demand imports. This is the cleaner route anyway: it
comes from the model rather than a borrowed regression, and leaves §2.6 exactly
as the paper specifies it for carbon.

A permanent tariff is a price **level** shift, not an ongoing inflation rate, so
it enters the cumulative term — and hence spot/PPP FX — but not the inflation
*rate* at later horizons. Central banks look through one-off level jumps.

Every result is the **increment** over the same scenario run without the tariff,
so the carbon baseline cancels.

---

## 5. Illustration: the EU levies 10 % on imported goods

One assumed case, chosen to be simple and EU-centred rather than realistic:
**EU27 imposes a uniform 10 % ad-valorem tariff on all imported goods**, from
every origin. Goods industries only — services are not charged at customs.
Reported at 2040, φ = 0.5, statutory incidence, against the Current Policies
carbon baseline.

The rate is a round number, not a calibration. Every number below scales
essentially linearly with it, so the illustration is about mechanism, not
magnitude.

| | |
|---|--:|
| Revenue | **\$157 bn/yr** |
| of which intermediate imports (enters `ct`) | \$84 bn |
| of which final-demand imports (consumer prices only) | \$73 bn |
| EU27 consumer price level | **+0.603 %** |
| EU27 GVA | **−0.0842 %** |
| EU27 policy rate | **−4.21 bp** |

**The rate response is a clean check on the plumbing.** A permanent tariff is a
level shift, so the Taylor rule sees only the output term: 0.5 × (−0.0842 %) =
−4.21 bp, exactly. The ECB cuts, because in this model a tariff is a negative
supply shock whose inflation component the central bank looks through.

### 5.1 The euro weakens — the currency that levies the tariff

Every one of the 14 analytical currencies strengthens against the euro, in a
tight band:

| | vs EUR |
|---|--:|
| IDN | −0.600 % |
| CHN | −0.599 % |
| IND | −0.599 % |
| … | |
| TUR | −0.576 % |
| NOR | −0.572 % |

(Convention: `S_r` is units of *r* per euro, so a negative figure means *r*
strengthens.) The mechanism is direct — the tariff raises EU consumer prices by
0.60 %, and under relative PPP the currency with the higher price level weakens.

This is the central result, and it is counter-intuitive: **protection weakens the
protecting currency.** The common intuition that a tariff supports a currency
comes from a trade-balance argument that a price-level channel does not contain.
Note also how uniform the band is (0.57–0.60 %): with the EU as the sole
tariffing region, the cross-section is dominated by the common EU price move
rather than by anything specific to each partner.

### 5.2 Incidence decides who actually bears it

The same schedule, run at both ends of θ:

| GVA at 2040 | EU27 | TUR | KOR | RUS | NOR |
|---|--:|--:|--:|--:|--:|
| θ = 1 (EU importer pays) | **−0.0842 %** | −0.0126 % | −0.0074 % | −0.0058 % | −0.0124 % |
| θ = 0 (exporter absorbs) | −0.0120 % | **−0.0782 %** | **−0.0525 %** | **−0.0507 %** | −0.0412 % |

The burden moves almost entirely from the EU to its export-dependent suppliers —
Turkey, Korea, Russia, Norway — economies selling a large share of their output
into the EU. The seven-fold swing in the EU's own figure is the honest measure of
how much θ matters, and why both ends are always reported rather than one.

---

## 6. Limitations

**No trade diversion.** The binding one. With final demand fixed (§2.4) nobody
re-sources away from a tariffed origin, so what is measured is the cost-push
incidence of the charge, not the reallocation of trade — often a tariff's actual
purpose. Every result therefore *understates* a tariff's effect. The fix is
Armington elasticities (available from published tables, e.g. Caliendo & Parro
2015) applied to reallocate **A**'s off-diagonal blocks before inversion, but it
departs from the paper's inelastic-demand assumption and belongs as a labelled
extension.

**Incidence is assumed, not derived.** θ brackets the range rather than resolving
it, for the same reason.

**No retaliation.** Each schedule is unilateral; a real trade war is a sequence.

**Static structure.** The 2022 input–output table is used throughout, so the
supply-chain reconfiguration a sustained tariff would cause is absent by
construction. This matters more for tariffs than for carbon, because trade
structure is the thing being shocked — see
[TARIFF_CALIBRATION.md](TARIFF_CALIBRATION.md) §5.1.

## 7. Validation

Gates cover the schedule shape; that `add_rule` targets only the named origin,
destination and industries; that a tariff never applies to intra-regional supply;
that θ = 1 charges only the importer and θ = 0 only the exporter; that revenue is
invariant to the incidence split; that final-demand imports raise revenue; and
that a tariff moves both rates and FX.

Two structural properties are also gated, because the analysis depends on them:

* **Exact additivity.** The chain is linear in τ end to end — charges are linear
  in τ, `ct` is additive, the dual and the Taylor rule are linear, spot PPP is a
  difference of logs, equity is `β·ΔY`. Two schedules run jointly give what they
  give summed, to 2.7e-17. So contributions decompose exactly, with no Shapley
  machinery and no order dependence.
* **Overlap is not the same as double counting.** Two schedules touching the same
  cells may still both apply — the test is whether one shipment pays both charges.
  A customs duty and a CBAM certificate obligation stack; two competing estimates
  of one duty do not.
