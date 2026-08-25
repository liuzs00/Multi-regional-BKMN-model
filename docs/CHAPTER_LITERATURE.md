# 2 Literature Review

Climate stress testing draws on two literatures that grew up apart. One produces
scenarios reaching out decades; the other produces valuations re-marked monthly.
What follows traces the attempts to join them, moving from the supervisory
practice that created the demand, through the climate-economy models that supply
the scenarios and the competing frameworks that translate them into economic
quantities, to the input–output tradition, the long struggle to extend it across
borders, and the empirical relations that turn a real shock into a market price.

The terms were set by Carney (2015), whose address at Lloyd's named the obstacle
a *tragedy of the horizon*: the costs of climate change fall beyond the planning
horizons of the business cycle, the political cycle and a central bank's mandate,
so the incentive to act expires before the damage becomes visible. His remedy —
forward-looking scenario analysis in place of realised-loss accounting — is what
the decade of supervisory work that followed attempted to carry out. The largest
of those exercises, the European Central Bank's economy-wide climate stress test
(ECB, 2022), established the shape the field has kept: a scenario taken from
outside, mapped onto counterparty exposures, propagated, and revalued.

Whether that shape works is assessed by Acharya et al. (2023), and their verdict
is mixed. They find transition risk treated as an exogenous shock when it is in
substance a dynamic policy choice, no feedback between climate and economy, and
few compound scenarios in which several risks arrive at once. Their fourth
objection cuts deeper than the other three. The exercises are not reproducible by
the institutions being tested, because the models are large, proprietary and
opaque; a bank required to hold capital against a supervisory number cannot
rebuild that number, and so cannot discover which of its own exposures the number
is about.

The academic literature that grew alongside those exercises begins with the
network stress test of Battiston et al. (2017), whose contribution is as much
procedural as empirical. Sorting economic activities into
climate-policy-relevant sectors, mapping bank and investor portfolios onto them,
and pushing a policy shock through the network of interbank exposures, they find
that exposure arriving indirectly through counterparties is comparable in size to
direct exposure, and that the affected share of bank loan books is of the same
order as bank capital. The general lesson is that indirect exposure cannot be
inferred from direct exposure and has to be computed through an explicit network.

Two lines run on from there. Whether markets have already priced the risk is
asked by Bolton and Kacperczyk (2023), who estimate a carbon premium across some
14,000 firms in 77 countries and find higher returns for firms with higher
emissions, the premium larger where domestic climate policy is stricter — which
is evidence that transition risk sits partly in prices already, and a limit on
what any stress test can claim to be uncovering. A different move is made by
Desnos et al. (2023), who convert a deterministic stress test into a stochastic
climate value-at-risk on the argument that a scenario is a draw from a
distribution rather than a state of the world.

Both lines take the scenario as given, and the scenarios come from integrated
assessment models. The lineage runs through DICE, which couples a Ramsey growth
model to a simple carbon cycle and a quadratic damage function mapping
temperature to lost output, recalibrated most recently by Barrage and Nordhaus
(2024). Of the components in that structure the damage function rests on the
least evidence, and the criticism of it is well developed. The sharpest statement
is Pindyck's (2013): the functional forms have, on his reading, no theoretical or
empirical basis for their curvature at high temperatures, so their outputs should
be treated as illustrations rather than as estimates. A separate objection is
raised by Dietz and Stern (2015), who let damage erode the capital stock and the
growth rate rather than only the level of output and find the implied social cost
of carbon rising sharply, supporting deeper cuts than the standard calibration
recommends. Set against those arguments, the coefficient of Swiss Re Institute
(2024) — roughly five times the DICE central value at any temperature — reads
less as a rival estimate than as the other end of an unsettled range.

Splitting an aggregate loss across economies calls for a different instrument,
and the one in common use is the vulnerability index of the Notre Dame Global
Adaptation Initiative (2024), which folds exposure, sensitivity and adaptive
capacity into a single cross-economy score. It ranks rather than measures: it can
order economies by vulnerability, but says nothing about how much any of them
loses. That is why work using it pairs it with a damage function instead of
substituting it for one.

The scenario set supervisors have converged on is published by the Network for
Greening the Financial System (2024), and its architecture decides what users
must supply for themselves. Transition pathways come from three integrated
assessment models — GCAM, MESSAGEix-GLOBIOM and REMIND-MAgPIE — whose
carbon-price and energy trajectories are handed to the macroeconometric model
NiGEM for macroeconomic variables, with chronic physical risk entering through an
aggregate damage function and acute risk through hazard-specific models. Because
the macroeconomic layer is attached to the integrated assessment layer rather
than derived from it, the published scenarios carry no consistent mapping from a
carbon price to a sectoral cost. Filling that gap is what every sectoral
application of these scenarios must do, and it has been done in four broadly
different ways.

A classification of the four is offered by Hafner et al. (2020). Environmental
computable general equilibrium models impose optimising behaviour and market
clearing, and are the conventional instrument for carbon-tax incidence; twelve of
them are compared on common unilateral-policy and border-adjustment experiments
by Böhringer, Balistreri and Rutherford (2012), in a study that says as much
about the family as about the policy. Leakage rates cluster between five and
twenty per cent, but the spread across models is driven by the substitution
elasticities each one assumes — elasticities estimated with wide uncertainty, and
invisible in an input–output table.

Macroeconometric models keep an input–output core and replace optimisation with
estimated behavioural equations, which lets the economy carry persistent slack.
That capacity is used by Mercure et al. (2018) to value stranded fossil-fuel
assets at a discounted global wealth loss of one to four trillion dollars, a
figure that depends on the economy failing to clear and could not have come out
of a general-equilibrium treatment of the same shock.

Interlocking balance sheets are tracked instead by ecological stock-flow
consistent models, which makes financial feedback explicit rather than assuming
it away. Working in such a model, Dafermos, Nikolaidi and Galanis (2018) show
climate damage raising corporate defaults and deflating asset prices, with the
resulting instability feeding back to worsen the damage itself. Nothing discussed
above contains that loop.

Building upward from heterogeneous firms and households, ecological agent-based
models arrive at different magnitudes altogether. Damages well above those of
standard integrated assessment models are reported by Lamperti et al. (2018)
under comparable scenarios, with growth tipping from a self-sustaining path into
stagnation and volatility — a direct challenge to the calibrations above, and a
suggestion that the smoothness of the damage function matters more than its
coefficient.

The pattern across the four is consistent. Substitution, disequilibrium,
financial feedback and heterogeneity each turn out to matter; none survives in a
fixed-coefficient input–output system; and three of the four literatures point
the resulting bias in the same direction, toward understatement.

The input–output core that the macroeconometric family retains is older than any
of these, and it acquired an environmental branch early. An economy was first
described as a system of linear production relations by Leontief (1936), each
sector's requirement a fixed combination of every other sector's output, so that
with $\mathbf{A}$ the matrix of technical coefficients and $\mathbf{f}$ final
demand, equilibrium output solves $\mathbf{x} = \mathbf{A}\mathbf{x} + \mathbf{f}$
and hence $\mathbf{x} = (\mathbf{I}-\mathbf{A})^{-1}\mathbf{f}$. The condition
under which that inverse exists and means anything was established by Hawkins and
Simon (1949) in terms of the leading principal minors of
$\mathbf{I}-\mathbf{A}$, which turns what looks like a computational convenience
into a statement about whether an economy is productive.

Pollutants were added as rows of the same accounting system by Leontief (1970),
so that emissions are attributed to the production generating them and travel
with the goods themselves; that paper begins the environmentally extended
input–output literature and is the ancestor of the sectoral carbon intensities in
use today. The modern synthesis is Miller and Blair's (2022), and three of their
treatments recur throughout applied work: the price dual, which transposes the
same matrix to ask how far prices move when costs change rather than how much
output a demand shock requires; the inter-country generalisation, in which the
flow matrix is blocked by region and the off-diagonal blocks hold trade; and the
aggregation problem, since merging units is demonstrably not neutral and the
direction of the bias depends on how unlike the merged units are.

Extending that apparatus across borders proved harder than extending it across
sectors, and for fifty years the multi-regional literature circled one obstacle:
the inter-regional flows are the object one needs and the object one rarely has.
The exact formulation was written down by Isard (1951), in which $a_{ij}^{rs}$
records how much of good $i$ from region $r$ sector $j$ in region $s$ requires.
It is also the least usable, since it demands a full bilateral flow matrix that
statistical agencies do not collect.

Two responses went opposite ways around the missing data. Exact accounting was
preserved at the cost of behavioural detail by Chenery (1953) and Moses (1955),
who assume that every user of a good within a region draws on the same mix of
origins, so that one trade coefficient serves all using sectors and
$a_{ij}^{rs} = t_i^{rs}\,a_{ij}^{s}$; that needs only regional trade totals, at
the cost of assuming a car plant and a hospital in the same region buy their
steel from the same places. The missing flows were instead estimated by Leontief
and Strout (1963), who treat regional output as entering a national pool and
suppose that bilateral flows obey a gravity relation,

$$z_i^{rs} \;=\; \frac{x_i^{r}\,d_i^{s}}{x_i^{\bullet}}\;Q_i^{rs},$$

with $Q_i^{rs}$ a friction term falling in transport cost. Since the frictions
have to reproduce known row and column totals, the system is solved iteratively,
by the biproportional fitting brought into input–output work by Stone (1961). The
cost of that elegance is that the trade pattern becomes a model output, so any
result turning on how a shock crosses a border inherits the gravity
specification's error on top of the model's own.

The obstacle dissolved once the flows were measured instead of inferred. The
programme that assembled global multi-regional tables from national accounts and
bilateral trade statistics through the 2000s is reviewed by Tukker and
Dietzenbacher (2013), and it produced four major databases within a few years of
each other: WIOD, documented by Timmer et al. (2015), alongside EXIOBASE, Eora
and the GTAP-based compilations. Whether findings depend on which database is
chosen was tested by Moran and Wood (2014), who harmonise satellite accounts and
compare consumption-based carbon accounts across them, finding agreement within
roughly ten per cent for most major economies and attributing what remains to
industry aggregation, emissions data and modelling assumptions. Belonging to the
same generation, the inter-country tables of the OECD (2025) supply the
off-diagonal blocks directly.

Beyond propagation, measured inter-country tables make consumption-based
accounting possible: attributing emissions to the final demand that occasions
them rather than to the territory where they are released. How wide the gap
between the two accounts runs was measured by Davis and Caldeira (2010), who find
that much of what developed economies consume was produced elsewhere. For anyone
ranking economies by climate relevance, the implication is that a ranking on
trade weight and a ranking on embodied emissions are not the same list.

What such a system is usually asked to price is a carbon charge, whose design has
a history of its own, beginning with the comparison of prices and quantities
under uncertainty in Weitzman (1974). That debate need not be settled here, but a
caution from Green (2021) is worth carrying: reviewing ex post evaluations of
carbon pricing, he concludes that measured emissions reductions have been modest
against expectations. A carbon price is a contested policy variable rather than a
fact of nature.

Given a price, who bears it has mostly been worked out through the input–output
price model. One is applied to a carbon tax driven by the NGFS scenarios by Kay
and Jolley (2023), who find price increases of ten to thirty per cent in
carbon-intensive industries under a two-hundred-dollar tax, for a single economy.
The cost-push formulation is developed further by Roncalli and Semet (2024), who
follow a tax from the sectors it is levied on to the sectors that end up paying
it, and separate the charge on a firm's own emissions from the charge embodied in
what it buys. Two of their findings matter for anything built on that apparatus:
the indirect burden is often the larger of the two, and the split between what a
firm absorbs and what it passes on is genuinely open, turning on market
structure, contract length and demand elasticity, none of which an input–output
table records.

That openness is confirmed rather than closed by the pass-through literature.
Theory and measurement are surveyed by RBB Economics (2014), who find rates
varying widely with market structure and with the kind of cost shock involved. A
stronger claim is made by Weber and Wasner (2023), who argue that under general
cost pressure firms with market power can pass on more than their cost increase,
which makes rates above one a live possibility rather than an arithmetic ceiling.

Whether a unilateral price merely moves emissions elsewhere is the leakage
question, and the literature answers it by comparing models rather than trusting
any one, because the answer turns on trade and energy-market elasticities that no
single framework pins down. Already met above for what it shows about
general-equilibrium models, the study of Böhringer, Balistreri and Rutherford
(2012) is the reference point on substance too: leakage clusters between five and
twenty per cent, and border carbon adjustment reduces it without removing it. In
that literature's terms, a border adjustment is a tariff differentiated by
embodied carbon.

An industrial cost becomes a financial quantity only through a further chain of
relations, each borrowed from a separate empirical literature, and the first link
is the shakiest. New-Keynesian Phillips curves are estimated across OECD
economies over 1995–2020 by Moessner (2022), who finds that a ten-dollar rise in
the carbon price raises headline inflation by roughly 0.08 percentage points.
That estimate is disputed. Working with carbon taxes actually implemented in
Europe and Canada over three decades, Konradt and Weder di Mauro (2023) find
dynamic effects on headline inflation indistinguishable from zero, and read their
evidence as relative price change — energy dearer, other things cheaper — rather
than inflation. The two are only partly reconciled by Bauer and Känzig (2024),
who find carbon pricing moving inflation *expectations* even where realised
inflation barely moves. Adopting a point estimate here means taking a side in a
live dispute.

The rest of the chain is firmer. The monetary reaction function is Taylor's
(2007). The term structure follows Hull and White (1994), whose one-factor model
gives the shift at maturity $\tau$ as a deterministic multiple $B(\tau)/\tau$ of
the short-rate shift, independent of volatility, so that a curve displacement
follows without calibrating a volatility surface. On the two exchange-rate
parities the standard reference remains Sarno and Taylor (2002), candid that
relative purchasing power parity does badly at short horizons while covered
interest parity is close to an arbitrage identity.

Those relations are assembled into what its authors call an ensemble by
Berrahoui, Kenyon, Macrina and Nathanael (2025): a short sequence of individually
simple, individually auditable steps running from a climate scenario to a set of
market shocks, two of them stated as propositions and proved — the allocation of
aggregate damage across sectors, and the mapping of a short-rate shift onto the
term structure. The design descends from earlier work by the same authors on
pricing carbon consistently inside financial instruments (Kenyon, Macrina and
Berrahoui, 2022). Its distinguishing property is the one Acharya et al. (2023)
found missing from supervisory practice: every relation is visible, so a
disagreement about the answer can be traced to a disagreement about one relation.
Its cost is realism, in precisely the dimensions the four alternative model
families were built to capture.

It is also, as published, a single-economy framework calibrated on the United
Kingdom, and that restriction has two consequences given everything above.
Emissions, and the cost of pricing them, demonstrably cross borders through
production chains — that is the finding of Leontief (1970) and of the
consumption-based accounting tradition after Davis and Caldeira (2010) — and a
one-country model has nowhere for that cost to go. The exchange rate, the
cross-currency basis and every other relative price, meanwhile, are not merely
harder to compute in such a model; they are undefined in it.

The gap is therefore narrow and specific. An auditable stress-testing chain with
proved internal relations exists for one economy (Berrahoui et al., 2025). A
mature multi-regional input–output apparatus exists (Miller and Blair, 2022;
Tukker and Dietzenbacher, 2013), together with measured inter-country tables that
remove the estimation step the Leontief–Strout tradition had to live with.
Input–output treatments of carbon-tax incidence exist for single economies (Kay
and Jolley, 2023; Roncalli and Semet, 2024). Nothing joins them, and until
something does, the quantities that exist only between economies stay outside the
reach of an auditable stress test.

---

### References

Acharya, V. V., R. Berner, R. Engle, H. Jung, J. Stroebel, X. Zeng and Y. Zhao
(2023). Climate stress testing. *Annual Review of Financial Economics* 15,
291–326.

Barrage, L. and W. Nordhaus (2024). Policies, projections, and the social cost of
carbon: results from the DICE-2023 model. *Proceedings of the National Academy of
Sciences* 121(13).

Battiston, S., A. Mandel, I. Monasterolo, F. Schütze and G. Visentin (2017). A
climate stress-test of the financial system. *Nature Climate Change* 7(4),
283–288.

Bauer, M. D. and D. R. Känzig (2024). *Carbon pricing and inflation
expectations.* Working paper.

Berrahoui, M., C. Kenyon, A. Macrina and G. Nathanael (2025). *Simple climate
stress testing: an ensemble framework.* Working paper, SSRN 5130573.

Böhringer, C., E. J. Balistreri and T. F. Rutherford (2012). The role of border
carbon adjustment in unilateral climate policy: overview of an Energy Modeling
Forum study (EMF 29). *Energy Economics* 34, S97–S110.

Bolton, P. and M. T. Kacperczyk (2023). Global pricing of carbon-transition risk.
*Journal of Finance* 78(6).

Carney, M. (2015). *Breaking the tragedy of the horizon — climate change and
financial stability.* Speech at Lloyd's of London, 29 September 2015.

Chenery, H. B. (1953). Regional analysis. In *The Structure and Growth of the
Italian Economy*, ed. H. B. Chenery, P. G. Clark and V. Cao-Pinna. Rome: US
Mutual Security Agency.

Dafermos, Y., M. Nikolaidi and G. Galanis (2018). Climate change, financial
stability and monetary policy. *Ecological Economics* 152, 219–234.

Davis, S. J. and K. Caldeira (2010). Consumption-based accounting of CO₂
emissions. *Proceedings of the National Academy of Sciences* 107(12), 5687–5692.

Desnos, B., T. Le Guenedal, P. Morais and T. Roncalli (2023). *From climate
stress testing to climate value-at-risk: a stochastic approach.* SSRN 4497124.

Dietz, S. and N. Stern (2015). Endogenous growth, convexity of damage and climate
risk: how Nordhaus' framework supports deep cuts in carbon emissions. *Economic
Journal* 125(583), 574–620.

European Central Bank (2022). *2022 Climate Risk Stress Test.* July 2022.

Green, J. F. (2021). Does carbon pricing reduce emissions? A review of ex-post
analyses. *Environmental Research Letters* 16(4), 043004.

Hafner, S., A. Anger-Kraavi, I. Monasterolo and A. Jones (2020). Emergence of new
economics energy transition models: a review. *Ecological Economics* 177, 106779.

Hawkins, D. and H. A. Simon (1949). Note: some conditions of macroeconomic
stability. *Econometrica* 17, 245–248.

Hull, J. and A. White (1994). Numerical procedures for implementing term
structure models I: single-factor models. *Journal of Derivatives* 2(1), 7–16.

Isard, W. (1951). Interregional and regional input–output analysis: a model of a
space-economy. *Review of Economics and Statistics* 33(4), 318–328.

Kay, D. and G. J. Jolley (2023). Using input–output models to estimate sectoral
effects of carbon tax policy: applications of the NGFS scenarios. *American
Journal of Economics and Sociology* 82, 187–222.

Kenyon, C., A. Macrina and M. Berrahoui (2022). *The carbon equivalence
principle: methods and applications.* SSRN 4035833.

Konradt, M. and B. Weder di Mauro (2023). Carbon taxation and greenflation:
evidence from Europe and Canada. *Journal of the European Economic Association.*

Lamperti, F., G. Dosi, M. Napoletano, A. Roventini and A. Sapio (2018). Faraway,
so close: coupled climate and economic dynamics in an agent-based integrated
assessment model. *Ecological Economics* 150, 315–339.

Leontief, W. (1936). Quantitative input and output relations in the economic
system of the United States. *Review of Economics and Statistics* 18(3), 105–125.

Leontief, W. (1970). Environmental repercussions and the economic structure: an
input–output approach. *Review of Economics and Statistics* 52(3), 262–271.

Leontief, W. and A. Strout (1963). Multiregional input–output analysis. In
*Structural Interdependence and Economic Development*, ed. T. Barna, 119–150.
London: Macmillan.

Mercure, J.-F., H. Pollitt, J. E. Viñuales, N. R. Edwards, P. B. Holden,
U. Chewpreecha, P. Salas, I. Sognnaes, A. Lam and F. Knobloch (2018).
Macroeconomic impact of stranded fossil fuel assets. *Nature Climate Change* 8,
588–593.

Miller, R. E. and P. D. Blair (2022). *Input–Output Analysis: Foundations and
Extensions*, 3rd edn. Cambridge University Press.

Moessner, R. (2022). *Effects of carbon pricing on inflation.* CESifo Working
Paper; published in *Climate Policy* (2025).

Moran, D. and R. Wood (2014). Convergence between the Eora, WIOD, EXIOBASE and
OpenEU's consumption-based carbon accounts. *Economic Systems Research* 26(3),
245–261.

Moses, L. N. (1955). The stability of interregional trading patterns and
input–output analysis. *American Economic Review* 45(5), 803–826.

Network for Greening the Financial System (2024). *NGFS Climate Scenarios for
Central Banks and Supervisors*, Phase V, and *Technical Documentation.*

Notre Dame Global Adaptation Initiative (2024). *ND-GAIN Country Index.*

OECD (2025). *OECD Inter-Country Input–Output Database*, 2025 edition. Paris:
OECD.

Pindyck, R. S. (2013). Climate change policy: what do the models tell us?
*Journal of Economic Literature* 51(3), 860–872.

RBB Economics (2014). *Cost Pass-through: Theory, Measurement and Potential
Policy Implications.* Report for the Office of Fair Trading.

Roncalli, T. and R. Semet (2024). *The Economic Cost of the Carbon Tax.* Amundi
Investment Institute Working Paper 156, SSRN 4755259.

Sarno, L. and M. P. Taylor (2002). *The Economics of Exchange Rates.* Cambridge
University Press.

Stone, R. (1961). *Input–Output and National Accounts.* Paris: OECD.

Swiss Re Institute (2024). *Changing Climates: The Heat Is (Still) On.* Zurich.

Taylor, J. B. (2007). *Monetary Policy Rules.* University of Chicago Press.

Timmer, M. P., E. Dietzenbacher, B. Los, R. Stehrer and G. J. de Vries (2015). An
illustrated user guide to the World Input–Output Database: the case of global
automotive production. *Review of International Economics* 23(3), 575–605.

Tukker, A. and E. Dietzenbacher (2013). Global multiregional input–output
frameworks: an introduction and outlook. *Economic Systems Research* 25(1),
1–19.

Weber, I. M. and E. Wasner (2023). Sellers' inflation, profits and conflict: why
can large firms hike prices in an emergency? *Review of Keynesian Economics*
11(2), 183–213.

Weitzman, M. L. (1974). Prices vs. quantities. *Review of Economic Studies*
41(4), 477–491.
