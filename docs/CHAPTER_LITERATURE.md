# 2 Literature Review

Climate stress testing asks a question that sits awkwardly between two
literatures. The climate-economics literature produces scenarios: emissions
pathways, carbon prices and temperature trajectories, usually from integrated
assessment models calibrated over decades. The financial-risk literature produces
valuations: discount curves, credit spreads, exchange rates, usually calibrated
over months. A stress test has to join them, and the join is where the difficulty
lies, because a scenario says nothing about a yield curve and a yield curve says
nothing about emissions. The supervisory exercises that have addressed this — the
NGFS scenario suite and the exercises built on it by the ECB and the Bank of
England — do so through large macro-financial models whose internal workings are
not, in general, reproducible by the institutions being tested. Their outputs are
credible but their mechanisms are opaque, and an institution asked to hold
capital against a number it cannot reconstruct is in an uncomfortable position.

The framework this dissertation extends takes the opposite approach. Berrahoui,
Kenyon, Macrina and Nathanael (2025) propose what they call an *ensemble*: a
short chain of individually simple, individually auditable relations running from
a climate scenario to a set of market shocks. A carbon price becomes a cost on
each sector in proportion to its emissions intensity; an input–output description
of the economy propagates that cost to every other sector; a temperature path
becomes a loss of output allocated by sector vulnerability; the resulting change
in value added drives inflation through an empirical pass-through relation, the
policy rate through a Taylor rule, the yield curve through a one-factor
short-rate model, and equity and credit spreads through estimated regression
slopes. Two of the links are stated as propositions with proofs — the allocation
of aggregate damage across sectors, and the mapping of a short-rate shift onto
the term structure — which is unusual in this literature and is much of the
framework's appeal. Each step can be checked in isolation, and a disagreement
about the answer can be localised to a disagreement about one relation.

The cost of that transparency is scope. The framework is developed for a single
economy, and the economy it is calibrated on is the United Kingdom. That is a
coherent choice for a first exposition, but it forces an assumption that is
plainly false: that a carbon price levied in one country stays in that country.
Production is international, and a charge on Chinese steel is paid, in part, by
whoever buys goods made with Chinese steel. A single-region model cannot see that
leakage, and it cannot see anything that is defined only in relation to another
economy — of which the exchange rate is the obvious and, for this dissertation,
the central example. Extending the framework to a system of economies is
therefore not merely a matter of running it thirteen times.

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
convenience. Miller and Blair (2022) give the modern treatment, and this
dissertation follows them for three things in particular. The first is the *price
dual*, which runs the same matrix transposed to answer the question this model
actually asks — not how much output a demand shock requires, but how much a cost
shock raises prices. The second is the inter-country generalisation, in which the
flow matrix is blocked by region and the off-diagonal blocks record trade, so
that propagation across borders is handled by exactly the same algebra as
propagation across sectors. The third is the aggregation problem: an
inter-country table with eighty-one economies is not tractable, aggregation is
therefore unavoidable, and Miller and Blair are careful that aggregation is not
neutral — it introduces bias whose direction depends on how heterogeneous the
merged units are. That warning is the reason §4.2 derives its region set from a
stated rule rather than asserting one.

Between the input–output foundations and the stress-testing framework sits the
question of what, exactly, a carbon tax does to an economy that produces in a
network. Treating the charge as an ad-valorem wedge on each sector's output, and
then asking how much of it a sector absorbs in its own margin and how much it
passes downstream in its price, is the formulation this dissertation adopts in
§3.3, and the pass-through share $\varphi$ that governs the split turns out to be
the single widest source of uncertainty in the whole model. The economic-cost
literature on carbon taxation is what motivates treating incidence as a free
parameter rather than a known one: the burden of a tax levied at one point in a
production chain is not generally borne at that point, and where it settles
depends on market structure, contract length and demand elasticity, none of which
an input–output table records.<sup>[†]</sup>

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
this model can report a curve without calibrating one. The damage function is
Barrage and Nordhaus's (2024) DICE-2023 central calibration, and the allocation
of that global damage across regions uses the ND-GAIN vulnerability index. The
exchange-rate relations are the two textbook parities, relative purchasing power
on the spot leg and covered interest parity on the forward leg, for which Sarno
and Taylor (2002) remains the standard reference and is candid that the first
performs poorly at horizons shorter than the ones considered here.

What this survey leaves is a reasonably clear gap. There is a transparent
single-region stress-testing framework with proved internal relations; there is a
mature and well-documented multi-regional input–output apparatus; and there is no
treatment joining them. Joining them is worth doing for a reason beyond
completeness. Several of the quantities a financial institution actually holds
are *relative*: an exchange rate is a price of one economy in terms of another, a
cross-currency basis is a difference of two curves, and the climate exposure of a
currency position is therefore not a property of either economy alone. Those
quantities are not merely harder to compute in a single-region model; they are
undefined in it. That is the space this dissertation occupies.

---

### References

Barrage, L. and W. Nordhaus (2024). Policies, projections, and the social cost of
carbon: results from the DICE-2023 model. *PNAS* 121(13).

Berrahoui, M., C. Kenyon, A. Macrina and G. Nathanael (2025). *Simple climate
stress testing: an ensemble framework.* Working paper.

Hull, J. and A. White (1994). Numerical procedures for implementing term
structure models I: single-factor models. *Journal of Derivatives* 2(1), 7–16.

Leontief, W. (1986). *Input–Output Economics*, 2nd edn. Oxford University Press.

Miller, R. E. and P. D. Blair (2022). *Input–Output Analysis: Foundations and
Extensions*, 3rd edn. Cambridge University Press.

Moessner, R. (2022). *Effects of carbon pricing on inflation.* CESifo Working
Paper.

Notre Dame Global Adaptation Initiative (2024). *ND-GAIN Country Index*, 2024
release.

OECD (2025). *Inter-Country Input–Output Tables, 2025 edition.*

Sarno, L. and M. P. Taylor (2002). *The Economics of Exchange Rates.* Cambridge
University Press.

Taylor, J. B. (2007). *Monetary Policy Rules.* University of Chicago Press.

Taylor, J. B. and J. C. Williams (2010). Simple and robust rules for monetary
policy. In *Handbook of Monetary Economics*, vol. 3, 829–859. Elsevier.

<sup>[†]</sup> *The Economic Cost of the Carbon Tax* — **citation to be
completed.** This reference is not recorded anywhere in the project's existing
material, so its authors, year and venue need supplying, and the paragraph above
should be checked against what it actually argues before submission.
