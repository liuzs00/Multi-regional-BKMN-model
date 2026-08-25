# 2 Literature Review

Climate stress testing draws on two bodies of work that do not share a
vocabulary. Climate economics produces scenarios reaching out decades; financial
risk management produces valuations that are re-marked monthly. What follows
traces the attempts to connect them, in five steps: how climate came to be
treated as a prudential problem, where the scenarios come from and what is wrong
with them, the competing ways of turning a scenario into economic quantities, the
input–output tradition and the long struggle to extend it across borders, and the
individual empirical relations that turn a real shock into a market price.

Carney (2015) set the terms. Speaking at Lloyd's, he called climate change a
*tragedy of the horizon*: its costs fall beyond the planning horizons of the
business cycle, the political cycle and a central bank's mandate, so the
incentive to act expires before the damage becomes visible. His remedy was
forward-looking scenario analysis in place of realised-loss accounting, and the
decade of supervisory work that followed is largely an attempt to carry it out.
The largest of those exercises is the European Central Bank's economy-wide
climate stress test (ECB, 2022), and it set the pattern the others follow: take
a scenario from outside, map it onto counterparty exposures, propagate, revalue.

Acharya et al. (2023) review what that decade produced, and their verdict is
mixed. Transition risks are treated as exogenous shocks when they are really
dynamic policy choices; feedback between climate and economy is largely missing;
compound scenarios, in which several risks arrive at once, are rarely built. Their
fourth objection cuts deeper than the others. The exercises are not reproducible
by the institutions being tested, because the models are large, proprietary and
opaque. A bank required to hold capital against a supervisory number cannot
rebuild that number, and so cannot work out which of its exposures the number is
about.

Academic work on the problem starts with Battiston et al. (2017), who ran the
first climate stress test of a financial system. Their contribution is as much
procedural as empirical. They sort economic activities into
climate-policy-relevant sectors, map bank and investor portfolios onto those
sectors, and push a policy shock through the network of interbank exposures. What
they find is that exposure arriving indirectly, through counterparties, is
comparable in size to direct exposure, and that the affected share of bank loan
books is of the same order as bank capital. The lesson is simple and general:
indirect exposure cannot be inferred from direct exposure, and has to be computed
through an explicit network.

Two lines of work follow. Bolton and Kacperczyk (2023) ask whether markets have
already priced the risk, estimating a carbon premium across roughly 14,000 firms
in 77 countries. They find higher returns for firms with higher emissions, and a
larger premium where domestic climate policy is stricter — which suggests
transition risk is partly in prices already, and limits what any stress test can
claim to be uncovering. Desnos et al. (2023) go the other way, turning a
deterministic stress test into a stochastic climate value-at-risk on the argument
that a scenario is a draw from a distribution, not a state of the world.

Both lines take the scenario as given. The scenarios themselves come from
integrated assessment models, and the lineage runs through Nordhaus's DICE, which
joins a Ramsey growth model to a simple carbon cycle and a damage function
mapping temperature to lost output (Nordhaus, 2017), most recently recalibrated
as DICE-2023 (Barrage and Nordhaus, 2024). Of all the components, the damage
function rests on the least evidence, and a substantial literature says so.

Pindyck (2013) puts it most bluntly: the functional forms in these models have,
on his reading, no theoretical or empirical basis for their curvature at high
temperatures, and their outputs should be treated as illustrations rather than
estimates. Weitzman (2012) makes the structural case, showing that a quadratic
specification implies implausibly small losses under large warming, and adding a
high-exponent term so that catastrophe is admitted at all. Dietz and Stern (2015)
arrive somewhere similar from another direction: let damage erode the capital
stock and the growth rate, rather than only the level of output, and the implied
social cost of carbon rises sharply, supporting deeper cuts than Nordhaus's own
calibration recommends. Seen against that argument, the coefficient of Swiss Re
Institute (2024) — roughly five times the DICE central value at any temperature —
looks less like a rival estimate than like the other end of an unsettled range.

Splitting an aggregate loss across economies needs a different instrument
altogether, and the usual one is the Notre Dame Global Adaptation Initiative
(2024) index, which folds exposure, sensitivity and adaptive capacity into a
single cross-economy score. It ranks rather than measures: it can say which
economies are more vulnerable, not how much any of them loses. That is why work
using it pairs it with a damage function instead of substituting it for one.

The scenario set supervisors have settled on is the Network for Greening the
Financial System's, and its architecture decides what users must supply
themselves. Transition pathways come from three integrated assessment models —
GCAM, MESSAGEix-GLOBIOM and REMIND-MAgPIE — whose carbon-price and energy
trajectories are handed to the macroeconometric model NiGEM for macroeconomic
variables, with chronic physical risk entering through an aggregate damage
function and acute physical risk through hazard-specific models (NGFS, 2024).
Because the macroeconomic layer is bolted onto the integrated assessment layer
rather than derived from it, the published scenarios carry no consistent mapping
from a carbon price to a sectoral cost. Filling that gap is what every sectoral
application of these scenarios has to do, and it has been done in four broadly
different ways.

Hafner et al. (2020) classify them. Environmental computable general equilibrium
models impose optimising behaviour and market clearing, and are the standard
instrument for carbon-tax incidence; the twelve models compared by Böhringer,
Balistreri and Rutherford (2012) belong to this family, and their study says as
much about the family as about the policy. Leakage rates cluster between five and
twenty per cent, but the spread across models is driven by the substitution
elasticities each one assumes — elasticities estimated with wide uncertainty and
invisible in an input–output table.

Macroeconometric models keep an input–output core but replace optimisation with
estimated behavioural equations, which lets the economy carry persistent slack.
Mercure et al. (2018) use E3ME in exactly this way to value stranded fossil-fuel
assets, reaching a discounted global wealth loss of one to four trillion dollars.
The result depends on the economy failing to clear, and could not have come out
of a general-equilibrium treatment of the same shock.

Ecological stock-flow consistent models follow interlocking balance sheets, so
financial feedback becomes explicit rather than assumed away. Dafermos, Nikolaidi
and Galanis (2018) show in such a model that climate damage raises corporate
defaults and deflates asset prices, and that the resulting instability then feeds
back to worsen the damage. Nothing discussed so far contains that loop.

Ecological agent-based models build upward from heterogeneous firms and
households. The Dystopian Schumpeter meeting Keynes model of Lamperti et al.
(2018) reports damages well above those of standard integrated assessment models
under comparable scenarios, with growth tipping from a self-sustaining path into
stagnation and volatility. That is a direct challenge to the calibrations above,
and it suggests the smoothness of the DICE damage function matters more than its
coefficient.

The pattern across the four is consistent. Substitution, disequilibrium,
financial feedback and heterogeneity each turn out to matter; none survives in a
fixed-coefficient input–output system; and three of the four literatures point
the resulting bias in the same direction, toward understatement.

The input–output core that the macroeconometric family retains is older than any
of these, and has an environmental branch worth following on its own. Leontief
(1936) described an economy as a system of linear production relations, each
sector's requirement a fixed combination of every other sector's output. With
$\mathbf{A}$ the matrix of technical coefficients and $\mathbf{f}$ final demand,
equilibrium output solves $\mathbf{x} = \mathbf{A}\mathbf{x} + \mathbf{f}$, so
that $\mathbf{x} = (\mathbf{I}-\mathbf{A})^{-1}\mathbf{f}$. Hawkins and Simon
(1949) established when that inverse exists and means anything, in terms of the
leading principal minors of $\mathbf{I}-\mathbf{A}$, turning what looks like a
computational convenience into a statement about whether an economy is
productive.

The environmental extension is Leontief's too. Leontief (1970) adds pollutants as
rows of the accounting system, so emissions are attributed to the production that
generates them and travel with the goods. That paper begins the environmentally
extended input–output literature and is the ancestor of the sectoral carbon
intensities in use today. Miller and Blair (2022) give the modern synthesis, and
three of their treatments recur throughout applied work: the price dual, which
transposes the same matrix to ask how far prices move when costs change rather
than how much output a demand shock requires; the inter-country generalisation,
in which the flow matrix is blocked by region and the off-diagonal blocks hold
trade; and the aggregation problem, since merging units is demonstrably not
neutral and the direction of the bias depends on how unlike the merged units are.

Extending the apparatus across borders proved harder than extending it across
sectors, and for fifty years the multi-regional literature circled one obstacle:
the inter-regional flows are the object one needs and the object one rarely has.
Isard (1951) wrote down the exact formulation, in which $a_{ij}^{rs}$ records how
much of good $i$ from region $r$ sector $j$ in region $s$ requires. It is also
the least usable, because it demands a full bilateral flow matrix that
statistical agencies do not collect.

Two responses went opposite ways around the missing data. Chenery (1953) and
Moses (1955) kept the accounting exact and gave up behavioural detail, assuming
every user of a good within a region draws on the same mix of origins, so one
trade coefficient serves all using sectors and
$a_{ij}^{rs} = t_i^{rs}\,a_{ij}^{s}$. That needs only regional trade totals, at
the cost of assuming a car plant and a hospital in the same region buy their
steel from the same places. Leontief and Strout (1963) instead estimated the
missing flows, treating regional output as entering a national pool and
supposing that bilateral flows obey a gravity relation,

$$z_i^{rs} \;=\; \frac{x_i^{r}\,d_i^{s}}{x_i^{\bullet}}\;Q_i^{rs},$$

with $Q_i^{rs}$ a friction term falling in transport cost. Since the frictions
have to reproduce known row and column totals, the system is solved iteratively,
by the biproportional fitting Stone (1961) brought into input–output work. The
cost of that elegance is that the trade pattern becomes a model output, so any
result turning on how a shock crosses a border inherits the gravity
specification's error on top of the model's own.

The obstacle dissolved once the flows were measured instead of inferred. Tukker
and Dietzenbacher (2013) review the programme that assembled global multi-regional
tables from national accounts and bilateral trade statistics through the 2000s,
which produced four major databases within a few years of each other: WIOD,
documented by Timmer et al. (2015), alongside EXIOBASE, Eora and the GTAP-based
compilations. Their plurality raised an obvious worry about whether findings
depend on the database chosen. Moran and Wood (2014) tested it, harmonising
satellite accounts and comparing consumption-based carbon accounts across
databases, and found agreement within roughly ten per cent for most major
economies, with what remained traceable to industry aggregation, emissions data
and modelling assumptions. The OECD's inter-country tables (OECD, 2025) belong to
the same generation and supply the off-diagonal blocks directly.

Beyond propagation, measured inter-country tables make consumption-based
accounting possible: attributing emissions to the final demand that occasions
them rather than to the territory where they are released. Davis and Caldeira
(2010) measured how wide the gap between the two accounts is, finding that much
of what developed economies consume was produced elsewhere. For anyone ranking
economies by climate relevance, the implication is that a ranking on trade weight
and a ranking on embodied emissions are not the same list.

What such a system is usually asked to price is a carbon charge, and the design
of that charge has a history of its own, beginning with Weitzman (1974) and the
question of whether to tax emissions or cap them. That debate need not be settled
here, but Green (2021) supplies a caution worth carrying: reviewing ex post
evaluations of carbon pricing, he concludes that measured emissions reductions
have been modest against expectations. A carbon price is a contested policy
variable, not a fact of nature.

Given a price, who bears it has mostly been worked out through the input–output
price model. Kay and Jolley (2023) apply one to a carbon tax driven by the NGFS
scenarios and find price increases of ten to thirty per cent in carbon-intensive
industries under a two-hundred-dollar tax. Roncalli and Semet (2024) develop the
cost-push formulation further, following a tax from the sectors it is levied on
to the sectors that end up paying it, and separating the charge on a firm's own
emissions from the charge embodied in what it buys. Two of their findings matter
for anything built on the same apparatus. The indirect burden is often the larger
of the two. And the split between what a firm absorbs and what it passes on is
genuinely open, turning on market structure, contract length and demand
elasticity — none of which an input–output table records.

The pass-through literature confirms that openness rather than closing it. RBB
Economics (2014) survey the theory and measurement and find rates varying widely
with market structure and with the kind of cost shock involved. Weber and Wasner
(2023) go further, arguing that under general cost pressure firms with market
power can pass on more than their cost increase, which makes rates above one a
live possibility rather than an arithmetic ceiling.

Whether a unilateral price merely moves emissions elsewhere is the leakage
question, and the literature answers it by comparing models rather than trusting
any one, because the answer turns on trade and energy-market elasticities that no
single framework pins down. The study of Böhringer, Balistreri and Rutherford
(2012), already met above for what it shows about general-equilibrium models, is
the reference point on substance too: leakage clusters between five and twenty
per cent, and border carbon adjustment reduces it without removing it. In that
literature's terms, a border adjustment is a tariff differentiated by embodied
carbon.

An industrial cost becomes a financial quantity only through a further chain of
relations, each borrowed from a separate empirical literature, and the first link
is the shakiest. Moessner (2022) estimates New-Keynesian Phillips curves across
OECD economies over 1995–2020 and finds that a ten-dollar rise in the carbon
price raises headline inflation by roughly 0.08 percentage points. Konradt and
Weder di Mauro (2023), working with carbon taxes actually implemented in Europe
and Canada over three decades, find dynamic effects on headline inflation
indistinguishable from zero, and read their evidence as relative price change —
energy dearer, other things cheaper — rather than inflation. Bauer and Känzig
(2024) only partly reconcile the two, finding that carbon pricing moves inflation
*expectations* even where realised inflation barely moves. Adopting a point
estimate here means taking a side in a live dispute.

The rest of the chain is firmer. Taylor (2007) supplies the monetary reaction
function. Hull and White (1994) supply the term structure: their one-factor model
gives the shift at maturity $\tau$ as a deterministic multiple $B(\tau)/\tau$ of
the short-rate shift, independent of volatility, so a curve displacement follows
without calibrating a volatility surface. Sarno and Taylor (2002) remain the
standard reference on the two exchange-rate parities, and are candid that
relative purchasing power parity does badly at short horizons while covered
interest parity is close to an arbitrage identity.

Berrahoui, Kenyon, Macrina and Nathanael (2025) assemble these relations into
what they call an ensemble: a short sequence of individually simple, individually
auditable steps running from a climate scenario to a set of market shocks, two of
them stated as propositions and proved — the allocation of aggregate damage
across sectors, and the mapping of a short-rate shift onto the term structure.
The design descends from earlier work by the same authors on pricing carbon
consistently inside financial instruments (Kenyon, Macrina and Berrahoui, 2022).
Its distinguishing property is the one Acharya et al. (2023) found missing from
supervisory practice: every relation is visible, so a disagreement about the
answer can be traced to a disagreement about one relation. Its cost is realism,
in precisely the dimensions the four alternative model families were built to
capture.

It is also, as published, a single-economy framework calibrated on the United
Kingdom, and that restriction has two consequences given everything above.
Leontief (1970) and the consumption-based accounting tradition after Davis and
Caldeira (2010) establish that emissions, and the cost of pricing them, cross
borders through production chains; a one-country model has nowhere for that cost
to go. And the exchange rate, the cross-currency basis and every other relative
price are not merely harder to compute in such a model — they are undefined in
it.

The gap is therefore narrow and specific. A transparent stress-testing framework
with proved internal relations exists for one economy (Berrahoui et al., 2025). A
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

Nordhaus, W. (2017). Revisiting the social cost of carbon. *Proceedings of the
National Academy of Sciences* 114(7), 1518–1523.

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

Weitzman, M. L. (2012). GHG targets as insurance against catastrophic climate
damages. *Journal of Public Economic Theory* 14(2), 221–244.
