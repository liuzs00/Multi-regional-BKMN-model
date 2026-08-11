# Tariffs calibrated to announced policy

> Companion to [TARIFF_METHOD.md](TARIFF_METHOD.md), which sets out the mechanism
> and illustrates it on a single assumed case. This note is the harder half:
> matching the machinery to measures actually in force as of mid-2026, running
> them together, and separating out what each one contributes. Read the method
> note first.

Four trade measures were in force in mid-2026 that this model can represent. They
are applied here as one stack, on top of the carbon charge, and the combined
result is attributed back to its parts.

| | Measure | What it is |
|---|---|---|
| 1 | US applied tariffs, May 2026 | 4.4 % on all origins entering the US, 23.4 % on China |
| 2 | EU–US framework, Jul 2026 | the US caps EU goods at an all-inclusive 15 %; the EU drops its MFN on US industrial goods |
| 3 | EU steel safeguard 2026/1384 | out-of-quota duty doubled to 50 %, quota cut to 18.3 Mt |
| 4 | CBAM (EU, applied prices) | carbon-price differential on embedded carbon, at the published €75.36 certificate price |

Code: [`bkmn/tariff.py`](../bkmn/tariff.py), [`bkmn/cbam.py`](../bkmn/cbam.py),
driver [`tools/run_tariff_stack.py`](../tools/run_tariff_stack.py). Results:
`out_stack_gva.csv`, `out_stack_fx.csv`, `out_stack_decomp.csv`,
`out_stack_prices.csv`. Everything is
reported at 2040, $\phi = 0.5$, statutory incidence ($\theta = 1$), against the
Current Policies carbon baseline, on the thirteen-region `DATA_final` build.

---

## 1. Why a tariff needs no new machinery

A tariff is structurally the same object as the model's carbon charge: an
ad-valorem cost wedge that propagates through the Leontief dual. The only
difference is where the wedge sits.

| | Levied on | Touches |
|---|---|---|
| Carbon charge | a sector's own production (Scope-1 emissions) | the per-sector charge $\mathbf{ct}$ |
| Tariff | a sector's imported inputs | the off-diagonal blocks of $\mathbf{A}$ |

Both are dimensionless — a fraction of the value of the good — so both enter the
same modified Leontief dual with no change to the mathematics. A schedule is a
matrix

$$\mathrm{TAU}[k, d] \;=\; \text{ad-valorem rate on good } k \text{ entering region } d$$

with $k$ indexing the 650 region–industry pairs and $d$ the 13 destinations.
`tariff.add_rule` builds bilateral or universal schedules and never applies a rate
to intra-regional supply, since a tariff falls on imports and not on domestic
sourcing.

Because schedules are specified as *increments* from a zero-tariff baseline, no
tariff database is needed. What each measure still needs is a rate, and §2 sets
out where each one comes from.

---

## 2. Calibration of the four measures

### 2.1 US applied tariffs, May 2026

Effective rates are the right object to compare with an ad-valorem wedge on an
aggregated table, because duties actually collected divided by import value
already net out exemptions, de-minimis treatment and tariff-line composition.

The [Penn Wharton Budget Model](https://budgetmodel.wharton.upenn.edu/p/2026-07-13-effective-tariff-rates-and-revenues-updated-july-13-2026/)
(13 July 2026) puts the US average effective rate at **7.2 %** as of May 2026,
against 2.3 % in January 2025, with **China the highest major partner at 23.4 %**
([USAFacts](https://usafacts.org/answers/what-is-the-average-us-tariff-rate-overall/countries/china/)).
Rates fell back from the 2025 peak after the Supreme Court held the IEEPA tariffs
unconstitutional in February 2026; what remains reflects the statutory authorities
that survived.

Two published numbers pin the schedule, because China's import share follows from
the table itself:

| | |
|---|--:|
| China's share of US imports (2022 table) | 14.7 % |
| Effective rate on China (published) | 23.4 % |
| ⇒ implied rate on all other origins | **4.4 %** |
| check: $0.147\times23.4 + 0.853\times4.4$ | **7.2 %** ✓ |

A gate asserts the reproduction of 7.2 % to within 0.2 pp.

### 2.2 EU–US framework, Jul 2026

In force from 1 July 2026, the framework caps most EU goods entering the US at an
all-inclusive **15 %**, while the EU eliminates tariffs on US industrial goods
([European Commission](https://commission.europa.eu/topics/trade/eu-us-trade-deal_en)).
The EU-side liberalisation enters as a *negative* wedge of 1.33 %, the World Bank
weighted applied MFN rate it removes.

### 2.3 EU steel safeguard 2026/1384

Applying from 1 July 2026, Regulation (EU) 2026/1384 replaces the earlier
safeguard: the tariff-free quota falls 47 % to 18.3 Mt and the out-of-quota duty
doubles from 25 % to 50 % across 30 product categories. A tariff-rate quota is not
an ad-valorem rate, so it is converted to the average rate paid on the flow — 50 %
times the above-quota share. With EU steel imports near 30 Mt in 2025
([EUROFER](https://gmk.center/en/news/steel-imports-into-the-eu-rose-by-14-y-y-in-2025-eurofer/)),
roughly 39 % sits above quota, giving an average **19.5 %** on EU steel imports.

Under fixed demand nothing re-sources, so this is an upper bound: the measure's
purpose is to push imports back toward the quota, which would cut the above-quota
share and hence the average rate.

### 2.4 CBAM

CBAM entered its definitive regime on 1 January 2026, and the Commission publishes
a quarterly certificate price defined as the weighted average of EU ETS auction
clearing prices: **€75.36** for Q1 2026 and €75.28 for Q2
([DG TAXUD](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/price-cbam-certificates_en)).
At EUR/USD 1.144 that is **\$86/t**, and it is exactly the right series, since the
same published price defines both the EU ETS level and the CBAM reference.

The rate is the price differential applied to embodied carbon,

$$\tau(r,i) \;=\; \max\!\bigl(0,\; \mathrm{XCE}_{\mathrm{EU}} - \mathrm{XCE}_r\bigr)\cdot \mathrm{CI}(r,i)\cdot 10^{-6},$$

with coverage from CBAM Annex I mapped to ICIO industries — C23 cement, C24A
steel, C24B aluminium, D electricity, and 15 % of C20 for fertilisers and
hydrogen. Origin prices are the carbon price each region already applies, since a
border adjustment only exists where prices differ.

CBAM is phased in with the withdrawal of free allocation, reaching 100 % only in
2034; `cbam.phase_in` carries the schedule. Reporting here is at 2040, past full
phase-in, but a CBAM figure quoted for any earlier year is wrong without it — by
about 40× in 2026.

---

## 3. Applying the four together without double counting

Running measures in parallel is not simply a matter of adding the schedules. Three
pairs need checking, and one of them genuinely overlaps.

**Measures 1 and 2 overlap, and the overlap is corrected.** Both price the EU→US
flow. The framework's 15 % is *all-inclusive*: it caps the total rate rather than
sitting on top of the existing one. Adding the schedules naively would charge
$4.4 + 15 = 19.4\%$ on EU goods entering the US. Measure 2 is therefore entered as
the increment over measure 1 on that flow, $15 - 4.4 = 10.6$ pp, so that the stack
totals exactly 15 % and the four schedules remain additive. The assembled matrix
is asserted to satisfy this:

```
EU->US stacked rate       0.1500   (cap 0.1500)
naive sum would have been 0.1940   -> 4.4 pp of double counting avoided
```

**Measures 3 and 4 overlap by design, and should.** Both fall on EU steel imports —
11 region–industry cells carry each — but they are separate legal instruments and
stack in law. CBAM's double-protection provision concerns the phase-out of ETS free
allocation, not trade-defence measures, so no offset applies.

**CBAM and the carbon charge cannot double-count, structurally.** The carbon charge
is levied on a sector's own Scope-1 production and therefore lives on the diagonal
blocks; CBAM is levied on imported inputs and lives off-diagonal. The two never
touch the same cell, which is asserted numerically: CBAM's rate on the EU's own
supply is exactly zero.

One consequence of the correction is worth stating. Measure 2 standing alone raises
**\$105.7 bn**; as an increment within the stack it contributes **\$74.1 bn**. Both
figures are correct for their respective questions, and the difference is precisely
the double counting the correction removes.

---

## 4. Results

### 4.1 Revenue and consumer prices

| Shock | Revenue (\$bn/yr) | of which intermediate | US consumer prices | EU consumer prices |
|---|--:|--:|--:|--:|
| US applied tariffs, May 2026 | 260.0 | 109.3 | $+0.713\%$ | $+0.004\%$ |
| EU–US framework, Jul 2026 | 74.1 | 31.4 | $+0.208\%$ | $-0.007\%$ |
| EU steel safeguard 2026/1384 | 10.3 | 10.1 | $+0.001\%$ | $+0.015\%$ |
| CBAM (EU, applied prices) | 10.4 | 9.3 | $0.000\%$ | $+0.021\%$ |
| **All four combined** | **354.8** | **160.1** | $\mathbf{+0.923\%}$ | $\mathbf{+0.033\%}$ |
| *residual* | $-0.000$ | $0.000$ | $0.000$ | $0.000$ |

The US measures dominate the stack, supplying 94 % of the revenue and essentially
all of the consumer-price effect. The two EU measures are comparable to each other
and an order of magnitude smaller.

### 4.2 Value added, by region and by source

Percentage change in regional value added at 2040. The carbon column is the
transition charge under Current Policies, shown alongside so the two policy types
can be compared on the same scale.

| Region | Carbon charge | US applied | EU–US framework | EU steel safeguard | CBAM | **All four** | Carbon + tariffs |
|---|--:|--:|--:|--:|--:|--:|--:|
| EU27 | $-0.0135$ | $-0.0028$ | $+0.0001$ | $-0.0127$ | $-0.0111$ | $\mathbf{-0.0266}$ | $-0.0401$ |
| USA | $-0.0089$ | $-0.0558$ | $-0.0165$ | $-0.0002$ | $-0.0002$ | $\mathbf{-0.0727}$ | $-0.0816$ |
| China | $-0.1330$ | $-0.0017$ | $-0.0004$ | $-0.0003$ | $-0.0003$ | $-0.0028$ | $-0.1357$ |
| India | $-0.1181$ | $-0.0020$ | $-0.0006$ | $-0.0003$ | $-0.0003$ | $-0.0033$ | $-0.1214$ |
| Latin America | $-0.1346$ | $-0.0100$ | $-0.0024$ | $-0.0006$ | $-0.0005$ | $-0.0135$ | $-0.1481$ |
| Russia | $-0.0964$ | $-0.0008$ | $-0.0002$ | $-0.0008$ | $-0.0006$ | $-0.0024$ | $-0.0988$ |
| Rest of Asia | $-0.0794$ | $-0.0053$ | $-0.0014$ | $-0.0006$ | $-0.0005$ | $-0.0079$ | $-0.0873$ |
| Türkiye | $-0.0528$ | $-0.0022$ | $-0.0005$ | $-0.0024$ | $-0.0017$ | $-0.0068$ | $-0.0596$ |
| Switzerland | $-0.0072$ | $-0.0026$ | $-0.0005$ | $-0.0031$ | $-0.0026$ | $-0.0089$ | $-0.0161$ |
| UK | $-0.0092$ | $-0.0031$ | $-0.0009$ | $-0.0011$ | $-0.0009$ | $-0.0061$ | $-0.0152$ |

Three readings follow.

**Each economy is hurt most by its own measures.** The United States bears
$-0.0727\%$, of which $-0.0558$ comes from its own applied tariffs and $-0.0165$
from the framework it signed — that is, from tariffs the US itself levies. The EU
bears $-0.0266\%$, of which $-0.0238$ comes from its own two instruments. Under
statutory incidence a tariff is a tax on the importer, so the cost-push burden
falls where the tariff is levied rather than where the goods come from.

**The EU's protectionist instrument costs it more than its climate instrument.**
The steel safeguard takes $-0.0127\%$ of EU value added against CBAM's $-0.0111\%$,
on comparable revenue — despite CBAM spanning five industries and steel being one
of them. Given that CBAM attracts considerably more attention as a trade barrier,
this is worth stating plainly.

**For most regions the carbon charge dominates the tariffs by an order of
magnitude.** China loses $-0.133\%$ to carbon and $-0.003\%$ to all four trade
measures combined; India, Latin America and Russia show the same pattern. The
exceptions are the two economies levying the tariffs: for the United States the
trade measures cost eight times what the carbon charge does, and for the EU roughly
twice. Trade policy is a first-order shock for those who impose it and a
second-order one for everyone else, whereas carbon pricing is the reverse.

### 4.3 Exchange rates

Spot rate against the euro, percentage change at 2040. Positive is depreciation.

| Region | US applied | EU–US framework | EU steel safeguard | CBAM | **All four** |
|---|--:|--:|--:|--:|--:|
| USA | $+0.7099$ | $+0.2149$ | $-0.0143$ | $-0.0209$ | $\mathbf{+0.8895}$ |
| China | $-0.0020$ | $+0.0071$ | $-0.0144$ | $-0.0210$ | $-0.0303$ |
| India | $-0.0013$ | $+0.0074$ | $-0.0143$ | $-0.0210$ | $-0.0293$ |
| UK | $+0.0014$ | $+0.0081$ | $-0.0128$ | $-0.0197$ | $-0.0229$ |
| Türkiye | $-0.0007$ | $+0.0073$ | $-0.0108$ | $-0.0187$ | $-0.0229$ |
| Switzerland | $+0.0003$ | $+0.0075$ | $-0.0113$ | $-0.0187$ | $-0.0222$ |

The dollar depreciates by **0.89 %** against the euro under the full stack, and
almost all of it comes from tariffs the United States itself levies. The mechanism
is the price-level channel: the tariffs raise US consumer prices by 0.92 %, and
under relative purchasing power parity the currency with the higher price level
weakens. The common intuition that protection strengthens a currency does not
survive here.

The two EU measures push the other way for every currency including the dollar,
because they raise EU prices and so weaken the euro against everything. Their
magnitudes are small — around $-0.02\%$ — but their sign is uniform, which is what
a measure levied by the base-currency region must produce.

**Tariffs do not move policy rates at all.** Every entry in the rate table is
exactly zero. This is a specification consequence rather than a numerical accident:
the Taylor output gap in this model is the damage function, and a tariff is a tax
wedge rather than a loss of real output, so it never enters the rule. Tariffs
therefore reach exchange rates only through the spot channel and never through
forward points — which is a structural difference from the carbon channel, where
the rate response dominates.

### 4.4 Consumer prices: carbon against tariffs

Both policies raise consumer prices, but by different routes. The carbon effect
comes from the Moessner relation of §2.6, cumulating to a price level
$k\,\Omega_r\,\mathrm{XCE}_r(t)$; the tariff effect is derived from the model's own
dual, because Moessner is estimated on carbon prices and has nothing to consume
from a tariff. Both are *level* effects in the same units, and the chain adds them,
so they decompose exactly.

Consumer price level at 2040 (%), tariffs shown by measure and carbon under two
scenarios:

| Region | US applied | EU–US | Steel | CBAM | **Tariffs** | Carbon (Curr. Pol.) | Carbon (Net Zero) |
|---|--:|--:|--:|--:|--:|--:|--:|
| USA | $+0.7135$ | $+0.2082$ | $+0.0005$ | $+0.0004$ | $\mathbf{+0.9225}$ | $+0.0011$ | $+0.3206$ |
| EU27 | $+0.0036$ | $-0.0068$ | $+0.0148$ | $+0.0213$ | $\mathbf{+0.0330}$ | $+0.0079$ | $+2.2726$ |
| China | $+0.0016$ | $+0.0004$ | $+0.0004$ | $+0.0003$ | $+0.0027$ | $+0.0178$ | $+1.5717$ |
| Switzerland | $+0.0039$ | $+0.0007$ | $+0.0035$ | $+0.0027$ | $+0.0108$ | $+0.0052$ | $+1.4975$ |
| UK | $+0.0050$ | $+0.0013$ | $+0.0021$ | $+0.0017$ | $+0.0101$ | $+0.0040$ | $+1.1486$ |
| Latin America | $+0.0138$ | $+0.0033$ | $+0.0010$ | $+0.0007$ | $+0.0189$ | $+0.0366$ | $+1.0016$ |
| Türkiye | $+0.0029$ | $+0.0005$ | $+0.0040$ | $+0.0026$ | $+0.0101$ | $0.0000$ | $0.0000$ |
| India | $+0.0023$ | $+0.0006$ | $+0.0005$ | $+0.0004$ | $+0.0037$ | $0.0000$ | $0.0000$ |
| Russia | $+0.0019$ | $+0.0004$ | $+0.0015$ | $+0.0011$ | $+0.0050$ | $0.0000$ | $0.0000$ |

Which policy dominates depends on the region and the scenario, and the pattern is
not uniform in either.

**For the United States, tariffs dominate carbon under every scenario.** They raise
US prices by $0.92\%$ against $0.001\%$ from carbon on the current-policy
trajectory — a factor of roughly eight hundred — and still by three times as much
under Net Zero, where the carbon contribution reaches only $0.32\%$. The reason is
coverage: the US prices about 9 % of its emissions, so even a $\$440$ carbon price
reaches very little of the economy, whereas a tariff reaches every import.

**For the European Union the ordering reverses with the scenario.** Under Current
Policies the four trade measures raise EU prices by $0.033\%$ against $0.008\%$
from carbon, so tariffs dominate fourfold. Under Net Zero, carbon reaches $2.27\%$
and dominates the tariffs by a factor of sixty-nine. The EU is the mirror image of
the US: it prices 65 % of its emissions, so an ambitious carbon path passes through
almost in full.

**For zero-coverage regions the carbon price effect is exactly zero, in every
scenario.** India, Türkiye, Russia and the Middle East price none of their
emissions, so by construction $k\,\Omega_r\,\mathrm{XCE}_r = 0$ regardless of how
high the scenario price goes. Every penny of their consumer-price impact is
imported through the tariff channel. This is a direct consequence of the coverage
term in §2.6, and it means the model attributes no domestic inflation to carbon
pricing in the regions with the highest carbon intensities.

**Two orderings reverse relative to the value-added table.** CBAM contributes more
to EU consumer prices than the steel safeguard does ($+0.0213\%$ against
$+0.0148\%$), which is the opposite of their effect on EU value added, where the
safeguard was the larger. And the EU–US framework is the only *deflationary* entry
in the table for the EU, at $-0.0068\%$, because the EU's side of the agreement
removes its MFN tariff on US industrial goods. A liberalising measure shows up
correctly as a price reduction.

### 4.5 The decomposition is exact

The charge channel is linear in $\mathbf{ct}$ and shocks superpose exactly, so
attributing the combined result to its four components involves no approximation
and no dependence on the order in which the measures are applied. Reported rather
than assumed, the residual between the combined run and the sum of the parts is

| Quantity | Max \|residual\| |
|---|--:|
| Value added | $3.5\times10^{-18}$ pp |
| Spot exchange rate | $6.7\times10^{-16}$ pp |
| Policy rate | $0.0$ bp |
| Revenue | $<10^{-3}$ \$bn |

These are machine precision. The practical consequence is that any subset of the
four measures can be costed by adding the relevant columns, and that a claim such
as "the safeguard accounts for 48 % of the EU's tariff burden" is exact rather than
an approximation from a particular decomposition order.

---

## 5. Limitations

**No trade diversion.** This is the binding one. With final demand fixed, nobody
re-sources away from a tariffed origin, so what is measured is the cost-push
incidence of the charge and not the reallocation of trade — often a tariff's
principal purpose. Every result here therefore understates a tariff's effect, and
the steel safeguard in particular is an upper bound on the rate and a lower bound
on the response.

**Incidence is assumed, not derived.** Results are at $\theta = 1$, the statutory
position in which the importer pays. At $\theta = 0$ the burden moves to exporters'
margins and the currency effects largely disappear. The framework cannot resolve
which occurs, because that depends on elasticities it excludes.

**No retaliation.** Each schedule is applied as legislated; a real trade dispute is
a sequence of responses.

**Base-year composition.** The calibration divides by China's share of US imports,
and the 2022 table puts that at 14.7 % where the current figure is nearer 10 % — the
trade war being modelled is itself the reason. `tools/sweep_china_share.py` sweeps
it from 7 % to 20 %: the aggregate results are robust, with US spot FX moving over a
0.04 pp band and revenue not moving at all, because the calibration pins the total
effective rate. What is *not* robust is the attribution to China, which runs from
23 % to 65 % of the revenue. Statements about aggregate effects survive; statements
about who bears a US tariff are base-year-determined.

**Coverage estimates.** The 15 % share of chemicals attributed to fertilisers and
hydrogen is an estimate, as is the 39 % above-quota share for steel. Both are
tagged in the code and are natural sweep parameters.

**Static structure.** The 2022 input–output table is applied throughout, so the
supply-chain reconfiguration a sustained tariff would cause is absent by
construction.

---

## 6. Validation

Gates in [`tests/test_extensions.py`](../tests/test_extensions.py) cover the tariff
machinery: that the calibrated US schedule reproduces the published 7.2 % effective
rate; that the China-share sweep holds it at every point, and that the aggregate FX
result is robust to the sweep while the attribution is not; that the CBAM phase-in
follows the statutory schedule and scales revenue linearly; that the CBAM rate is
zero for the levying region, zero outside covered industries, and zero where the
origin already prices carbon above the EU; that CBAM shrinks when carbon prices
converge; that `add_rule` targets only the named origin and destination and never
applies to intra-regional supply; that $\theta = 1$ charges only the importer and
$\theta = 0$ only the exporter; that revenue is invariant to the incidence split;
that final-demand imports raise revenue without entering the production chain; and
that a tariff moves both value added and FX.

The stack adds three checks of its own, asserted in
[`tools/run_tariff_stack.py`](../tools/run_tariff_stack.py): that the EU→US rate
totals the all-inclusive cap rather than the naive sum; that CBAM is exactly zero
on the EU's own supply, so it cannot double-count against the carbon charge; and
that the decomposition residual is at machine precision.
