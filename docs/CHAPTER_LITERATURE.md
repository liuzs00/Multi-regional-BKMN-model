# 2 Literature Review

Climate stress testing asks a question that sits awkwardly between two
literatures. The climate-economics literature produces scenarios: emissions
pathways, carbon prices and temperature trajectories, usually from integrated
assessment models calibrated over decades, of which the reference set for
supervisory work is now that of the Network for Greening the Financial System
(NGFS, 2024). The financial-risk literature produces valuations: discount curves,
credit spreads, exchange rates, calibrated over months. A stress test has to join
them, and the join is where the difficulty lies, because a scenario says nothing
about a yield curve and a yield curve says nothing about emissions. The
supervisory exercises that have addressed this — the euro-area climate risk
stress test (ECB, 2022) and the Bank of England's Climate Biennial Exploratory
Scenario (Bank of England, 2022) — do so through large macro-financial models
whose internal workings are not, in general, reproducible by the institutions
being tested. Their outputs are credible but their mechanisms are opaque, and an
institution asked to hold capital against a number it cannot reconstruct is in an
uncomfortable position.

The framework this dissertation extends takes the opposite approach. Berrahoui,
Kenyon, Macrina and Nathanael (2025) propose what they call an *ensemble*: a
short chain of individually simple, individually auditable relations running from
a climate scenario to a set of market shocks. A carbon price becomes a cost on
each sector in proportion to its emissions intensity; an input–output description
of the economy propagates that cost to every other sector; a temperature path
becomes a loss of output allocated by sector vulnerability; the resulting change
in value added drives inflation, the policy rate, the yield curve, and equity and
credit spreads in turn. Two of the links are stated as propositions with proofs —
the allocation of aggregate damage across sectors and the mapping of a short-rate
shift onto the term structure, reproduced as Propositions 3.1 and 3.2 below —
which is unusual in this literature and is much of the framework's appeal. Each
step can be checked in isolation, and a disagreement about the answer can be
localised to a disagreement about one relation.

The cost of that transparency is scope. Berrahoui et al. (2025) develop the
framework for a single economy and calibrate it on the United Kingdom. That is a
coherent choice for a first exposition, but it forces an assumption that is
plainly false: that a carbon price levied in one country stays in that country.
Production is international, and a charge on Chinese steel is paid, in part, by
whoever buys goods made with Chinese steel. A single-region model cannot see that
leakage, and it cannot see anything defined only in relation to another economy —
of which the exchange rate is the obvious and, for this dissertation, the central
example. Extending the framework to a system of economies is therefore not merely
a matter of running it thirteen times.

The machinery for that extension is old and well understood. Leontief (1986)
introduced the input–output description of an economy as a system of linear
production relations, in which each sector's output requirement is a fixed
combination of every other sector's output. Writing $\mathbf{A}$ for the matrix
of technical coefficients and $\mathbf{f}$ for final demand, the equilibrium
output vector solves $\mathbf{x} = \mathbf{A}\mathbf{x} + \mathbf{f}$, so that
$\mathbf{x} = (\mathbf{I}-\mathbf{A})^{-1}\mathbf{f}$. The inverse in that
expression is the whole content of the method: it sums the infinite regress of
indirect requirements, in which steel needs coal which needs steel, and its
existence is a substantive economic condition rather than a technical
convenience, as Appendix A sets out. Miller and Blair (2022) give the modern
treatment, and this dissertation follows them for three things in particular. The
first is the *price dual*, which runs the same matrix transposed to answer the
question this model actually asks — not how much output a demand shock requires,
but how much a cost shock raises prices. The second is the inter-country
generalisation, in which the flow matrix is blocked by region and the off-diagonal
blocks record trade, so that propagation across borders is handled by exactly the
same algebra as propagation across sectors. The third is the aggregation problem:
Miller and Blair (2022) are careful that aggregation is not neutral, and
introduces bias whose direction depends on how heterogeneous the merged units
are. That warning is the reason §4.2 derives its region set from a stated rule
rather than asserting one.

The multi-regional literature is largely a history of one obstacle: the
inter-regional flows are the object one needs and the object one rarely has. The
interregional model of Isard (1951) is the exact formulation, in which the
coefficient $a_{ij}^{rs}$ records how much of good $i$ from region $r$ sector $j$
in region $s$ requires. It is also the least usable, because it demands a full
bilateral flow matrix that statistical agencies do not collect. The two classical
responses take opposite routes around this. The Chenery–Moses model (Chenery,
1953; Moses, 1955) keeps the accounting exact but weakens the behavioural
content: it assumes that every user of a good within a region draws on the same
mix of origins, so that a single trade coefficient $t_i^{rs}$ — region $r$'s
share of region $s$'s total supply of good $i$ — can be applied across all using
sectors, giving $a_{ij}^{rs} = t_i^{rs}\,a_{ij}^{s}$. This requires only regional
trade totals rather than a full flow matrix, at the cost of assuming that a car
plant and a hospital in the same region source their steel from the same places
in the same proportions.

Leontief and Strout (1963) instead estimate the flows that are missing. Regional
outputs are treated as entering a national pool from which regions draw, and the
bilateral flow of good $i$ is postulated to obey a gravity relation,

$$z_i^{rs} \;=\; \frac{x_i^{r}\,d_i^{s}}{x_i^{\bullet}}\;Q_i^{rs},$$

in which $x_i^{r}$ is supply in $r$, $d_i^{s}$ is demand in $s$, $x_i^{\bullet}$
is the national total, and $Q_i^{rs}$ is an interregional friction term,
decreasing in transport cost or distance. Since the $Q_i^{rs}$ must be chosen so
that the implied flows reproduce known row and column totals, the model is solved
iteratively, by the biproportional fitting that Stone (1961) introduced for
input–output work and Bacharach (1970) analysed formally. It is an elegant
solution to a genuine data problem, and it is worth being clear about what it
costs: the resulting trade pattern is a *model output*, so any subsequent result
that depends on how a shock crosses a border inherits the gravity specification's
error along with the model's own.

This dissertation needs neither device. The inter-country tables of the OECD
(2025a) supply the off-diagonal blocks $\mathbf{Z}^{rs}$ directly, so the trade
structure enters as data rather than as an estimate, and the propagation of a
carbon charge across borders — precisely the quantity the multi-regional
extension exists to measure — does not rest on an assumed distance decay or a
uniform sourcing assumption. That is a substantive advantage of building on an
inter-country table rather than assembling one from national tables, and it is
worth stating because it removes an entire layer of estimation error that much of
the multi-regional literature must carry. The same alignment extends to the two
quantities the transition channel needs alongside the flows: sectoral emissions
come from the greenhouse-gas footprint accounts of the OECD (2025b), built on the
same economy and industry classification as the tables themselves, and the share
of each economy's emissions actually facing a carbon price is taken from the
coverage series of Our World in Data (2025), which republishes the World Carbon
Pricing Database. Section 4.1 sets out the calibration in full.

Between the input–output foundations and the stress-testing framework sits the
question of what a carbon tax actually does to an economy that produces in a
network. Roncalli and Semet (2024) address it directly, using an input–output
system to trace a carbon tax from the sectors on which it is levied through to
the sectors that ultimately bear it, and their central distinction — between the
charge on a firm's own emissions and the charge embodied in the inputs it buys —
is the same one that separates the direct term from the propagated term in §3.3
here. Two points from that work bear on this one. The first is that the indirect
burden is frequently the larger of the two, which is an argument for taking the
network seriously rather than charging sectors on their own emissions alone. The
second is that the incidence of the tax is genuinely open: how much a sector
absorbs in its own margin and how much it passes downstream in its price depends
on market structure, contract length and demand elasticity, none of which an
input–output table records. That is why the pass-through share $\varphi$ enters
this model as a free parameter to be swept rather than a quantity to be
calibrated, and why §4.5 reports the whole range of it.

The remaining links are each borrowed from a specific empirical literature, and
it is worth being explicit about which, since the credibility of the chain is the
credibility of its weakest link. The inflation response comes from Moessner
(2022), who estimates across emissions-trading jurisdictions that a \$10 per
tonne rise in the carbon price raises headline inflation by roughly 0.08
percentage points. The monetary reaction is a Taylor (2007) rule with equal
weights on inflation and the output gap, the specification Taylor and Williams
(2010) defend as robust across model specifications precisely because it is not
tuned to any of them. The term structure follows Hull and White (1994), whose
one-factor model gives the shift at maturity $\tau$ as a deterministic multiple
$B(\tau)/\tau$ of the short-rate shift, independent of volatility — which is why
this model can report a curve without calibrating one. The damage function is the
DICE-2023 central calibration of Barrage and Nordhaus (2024), and the allocation
of that global damage across regions uses the vulnerability index of the Notre
Dame Global Adaptation Initiative (2024). The exchange-rate relations are the two
textbook parities, relative purchasing power on the spot leg and covered interest
parity on the forward leg, for which Sarno and Taylor (2002) remains the standard
reference and is candid that the first performs poorly at horizons shorter than
those considered here.

What this survey leaves is a reasonably clear gap. There is a transparent
single-region stress-testing framework with proved internal relations (Berrahoui
et al., 2025); there is a mature and well-documented multi-regional input–output
apparatus (Miller and Blair, 2022); and there is no treatment joining them.
Joining them is worth doing for a reason beyond completeness. Several of the
quantities a financial institution actually holds are *relative*: an exchange
rate is a price of one economy in terms of another, a cross-currency basis is a
difference of two curves, and the climate exposure of a currency position is
therefore not a property of either economy alone. Those quantities are not merely
harder to compute in a single-region model; they are undefined in it. That is the
space this dissertation occupies.

---

### References

Bacharach, M. (1970). *Biproportional Matrices and Input–Output Change.*
Cambridge University Press.

Bank of England (2022). *Results of the 2021 Climate Biennial Exploratory
Scenario (CBES).* May 2022.

Barrage, L. and W. Nordhaus (2024). Policies, projections, and the social cost of
carbon: results from the DICE-2023 model. *PNAS* 121(13).

Berrahoui, M., C. Kenyon, A. Macrina and G. Nathanael (2025). *Simple climate
stress testing: an ensemble framework.* Working paper.

Chenery, H. B. (1953). Regional analysis. In *The Structure and Growth of the
Italian Economy*, ed. H. B. Chenery, P. G. Clark and V. Cao-Pinna. Rome: US
Mutual Security Agency.

European Central Bank (2022). *2022 Climate Risk Stress Test.* July 2022.

Hull, J. and A. White (1994). Numerical procedures for implementing term
structure models I: single-factor models. *Journal of Derivatives* 2(1), 7–16.

Isard, W. (1951). Interregional and regional input–output analysis: a model of a
space-economy. *Review of Economics and Statistics* 33(4), 318–328.

Leontief, W. (1986). *Input–Output Economics*, 2nd edn. Oxford University Press.

Leontief, W. and A. Strout (1963). Multiregional input–output analysis. In
*Structural Interdependence and Economic Development*, ed. T. Barna, 119–150.
London: Macmillan.

Miller, R. E. and P. D. Blair (2022). *Input–Output Analysis: Foundations and
Extensions*, 3rd edn. Cambridge University Press.

Moessner, R. (2022). *Effects of carbon pricing on inflation.* CESifo Working
Paper.

Moses, L. N. (1955). The stability of interregional trading patterns and
input–output analysis. *American Economic Review* 45(5), 803–826.

Network for Greening the Financial System (2024). *NGFS Climate Scenarios for
Central Banks and Supervisors*, Phase V. Data obtained from the NGFS Scenario
Explorer hosted by IIASA, https://data.ece.iiasa.ac.at/ngfs (accessed July 2026);
carbon-price and temperature paths are taken from the MESSAGEix-GLOBIOM
realisation throughout, so that all seven narratives share one model.

Notre Dame Global Adaptation Initiative (2024). *ND-GAIN Country Index*, 2024
release. University of Notre Dame. https://gain.nd.edu/our-work/country-index
(accessed July 2026). The 2022 cross-section of the 1995–2024 panel is used, to
match the base year of the input–output and emissions data.

OECD (2025b). *OECD Greenhouse Gas Footprints Database*, 2025 edition. Paris:
OECD. Obtained via the OECD SDMX API (accessed July 2026). Scope-1 production
emissions in tonnes CO₂e, aligned to the same economy and industry classification
as the input–output tables.

OECD (2025a). *OECD Inter-Country Input–Output Database*, 2025 edition. Paris:
OECD. https://oe.cd/icio (accessed July 2026). Small-format (SML) tables,
1995–2022, 81 economies and 50 ISIC Rev. 4 industries, in current US dollars at
basic prices; the 2022 table is used throughout.

Our World in Data (2025). *Share of CO₂ emissions covered by a carbon price.*
https://ourworldindata.org/grapher/carbon-tax-trading-coverage (accessed July
2026), republishing the World Carbon Pricing Database of Dolphin, Pollitt and
Newbery, licensed CC BY.

Roncalli, T. and R. Semet (2024). *The Economic Cost of the Carbon Tax.* Amundi
Investment Institute, March 2024.

Sarno, L. and M. P. Taylor (2002). *The Economics of Exchange Rates.* Cambridge
University Press.

Stone, R. (1961). *Input–Output and National Accounts.* Paris: OECD.

Taylor, J. B. (2007). *Monetary Policy Rules.* University of Chicago Press.

Taylor, J. B. and J. C. Williams (2010). Simple and robust rules for monetary
policy. In *Handbook of Monetary Economics*, vol. 3, 829–859. Elsevier.
