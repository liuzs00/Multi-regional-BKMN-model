# 2 Literature Review

Two bodies of work meet in climate stress testing without sharing a vocabulary.
Climate economics produces scenarios on horizons of decades; financial risk
management produces valuations on horizons of months. The literature reviewed
here is the sequence of attempts to connect them, and it divides into five
strands: the framing of climate as a prudential problem and the supervisory
exercises that followed; the climate-economy models that supply the scenarios and
the long argument about their damage functions; the competing macroeconomic
frameworks that translate a scenario into economic quantities; the input–output
tradition and its extension across borders; and the individual empirical
relations by which a real shock becomes a market price.

## From a speech to a supervisory practice

Carney (2015) supplied the framing. Speaking at Lloyd's, he argued that climate
change presents a *tragedy of the horizon*: its costs fall beyond the planning
horizons of the business cycle, the political cycle and the mandate of a central
bank, so the incentive to act expires before the damage becomes legible. His
prescription — forward-looking scenario analysis in place of realised-loss
accounting — is the instruction the following decade of supervisory work
implements. The two largest implementations are the European Central Bank's
economy-wide climate stress test (ECB, 2022) and the Bank of England's Climate
Biennial Exploratory Scenario (Bank of England, 2022), which share a structure:
an externally supplied scenario, a mapping onto counterparty exposures, a
propagation step, and a revaluation.

Acharya et al. (2023) review what that decade produced and identify three
deficiencies. Transition risks are handled as exogenous shocks when they are in
substance dynamic policy choices; feedback between the climate and the economy is
largely absent; and compound scenarios, in which several risks arrive together,
are rarely constructed. A fourth observation is more corrosive than these: the
exercises are not reproducible by the institutions being tested, since the models
are large, proprietary and opaque, so a bank asked to hold capital against a
supervisory number cannot reconstruct it and therefore cannot localise which of
its exposures the number is about.

The academic response to Carney begins with Battiston et al. (2017), who conduct
the first climate stress test of a financial system and whose contribution is
procedural as much as empirical. They classify economic activities into
climate-policy-relevant sectors, map bank and investor portfolios onto that
classification, and propagate a policy shock through the network of interbank
exposures. Their central finding is that indirect exposure, arriving through
counterparties, is comparable in magnitude to direct exposure, and that the
affected share of bank loan portfolios is of the same order as bank capital. The
methodological point that survives them is that indirect exposure cannot be
inferred from direct exposure and must be computed through an explicit network.

Two strands develop from there. Bolton and Kacperczyk (2023) ask whether markets
already price the risk, estimating a carbon premium across roughly 14,000 firms
in 77 countries and finding higher returns for firms with higher emissions levels
and emissions growth, with the premium larger where domestic climate policy is
stricter. Their result implies transition risk is partially in prices already,
which constrains what any stress test can claim to be revealing. Desnos et al.
(2023) take the other route, extending a deterministic stress test into a
stochastic climate value-at-risk on the argument that a scenario is a draw from a
distribution rather than a state of the world.

## Where the scenarios come from, and what is wrong with them

Scenarios originate in integrated assessment models, and the lineage runs through
Nordhaus's DICE, which couples a Ramsey growth model to a simple carbon cycle and
a damage function mapping temperature to lost output (Nordhaus, 2017), most
recently recalibrated as DICE-2023 (Barrage and Nordhaus, 2024). The damage
function is the component carrying the least empirical weight, and the literature
saying so is substantial.

Pindyck (2013) is the sharpest statement: the functional forms embedded in
integrated assessment models have, in his assessment, no theoretical or empirical
foundation for their curvature at high temperatures, and their outputs should be
read as illustrative rather than as estimates. Weitzman (2012) makes the
structural version of the argument, showing that a quadratic specification
implies implausibly small losses under large warming and proposing an additional
high-exponent term so that catastrophic outcomes are admitted at all. Dietz and
Stern (2015) reach a compatible conclusion from a different direction: allowing
damage to erode the capital stock and the growth rate, rather than only the level
of output, raises the implied social cost of carbon substantially and supports
deeper abatement than Nordhaus's own calibration recommends. Grubb et al. (2021)
survey the accumulated criticism and argue that DICE's dynamic structure embeds
assumptions its users rarely examine, so that the model's apparent neutrality is
itself a claim. Against this background the calibration of Swiss Re Institute
(2024), roughly five times the DICE central coefficient at any given temperature,
is better read as one end of an unsettled range than as a competing point
estimate.

Distributing an aggregate loss across economies requires a second measure
entirely, and the standard one is the Notre Dame Global Adaptation Initiative
(2024) index, which combines exposure, sensitivity and adaptive capacity into a
cross-economy score. It is a relative ranking rather than an estimate of loss: it
can order economies but cannot say how much any of them loses, which is why work
using it pairs it with a damage function rather than in place of one.

The scenario set supervisory work has converged on is that of the Network for
Greening the Financial System, and its architecture determines what downstream
users must supply themselves. Transition pathways are generated by three
integrated assessment models — GCAM, MESSAGEix-GLOBIOM and REMIND-MAgPIE — whose
carbon-price and energy trajectories are passed to the macroeconometric model
NiGEM for macroeconomic variables, with chronic physical risk entering through an
aggregate damage function and acute physical risk through hazard-specific models
(NGFS, 2024). Because the macroeconomic layer is a separate model attached to the
integrated assessment layer rather than derived from it, the published scenarios
contain no internally consistent mapping from a carbon price to a sectoral cost.
That absence is what every sectoral application of these scenarios must fill.

## Four ways to translate a scenario into an economy

The NGFS's own modelling handbook (NGFS, 2019) and the classification of Hafner
et al. (2020) distinguish four families of macroeconomic model beyond the
integrated assessment models themselves. Each has produced a result the others
structurally cannot, and together they map the cost of each modelling choice.

Environmental computable general equilibrium models impose optimising behaviour
and market clearing, and are the conventional instrument for carbon-tax
incidence. The Energy Modeling Forum study synthesised by Böhringer, Balistreri
and Rutherford (2012) compares twelve such models on common unilateral-policy and
border-adjustment experiments, and its finding is as much about the family as
about the policy: leakage rates cluster between five and twenty per cent, but the
dispersion across models is driven by the substitution elasticities each assumes,
which are estimated with wide uncertainty and are not observable in an
input–output table.

Macroeconometric models retain an input–output core but replace optimisation with
estimated behavioural equations, permitting persistent slack. Mercure et al.
(2018) use E3ME in this mode to value stranded fossil-fuel assets, arriving at a
discounted global wealth loss of one to four trillion dollars — a result that
depends on the economy failing to clear and is therefore unobtainable from a
general-equilibrium treatment of the same shock.

Ecological stock-flow consistent models track interlocking balance sheets so that
financial feedback becomes explicit. Dafermos, Nikolaidi and Galanis (2018) show
in such a model that climate damage raises corporate defaults and deflates asset
prices, and that the resulting financial instability then reinforces the
growth-reducing effect of the damage itself. That loop is absent from every
framework discussed above.

Ecological agent-based models build upward from heterogeneous firms and
households. The Dystopian Schumpeter meeting Keynes model of Lamperti et al.
(2018) reports damages substantially larger than standard integrated assessment
models under comparable scenarios, with growth shifting from a self-sustaining
path to stagnation and high volatility — a direct challenge to the damage
calibrations above, suggesting that the smoothness of the DICE damage function
does more work than its coefficient.

The pattern across the four is consistent. Substitution, disequilibrium,
financial feedback and heterogeneity each matter, each is absent from a
fixed-coefficient input–output system, and three of the four literatures indicate
the direction of the resulting bias is toward understatement.

## The input–output tradition

Leontief (1936, 1941) introduced the input–output description of an economy as a
system of linear production relations in which each sector's requirement is a
fixed combination of every other sector's output. Writing $\mathbf{A}$ for the
matrix of technical coefficients and $\mathbf{f}$ for final demand, equilibrium
output solves $\mathbf{x} = \mathbf{A}\mathbf{x} + \mathbf{f}$, so that
$\mathbf{x} = (\mathbf{I}-\mathbf{A})^{-1}\mathbf{f}$. Hawkins and Simon (1949)
established the condition under which that inverse exists and is economically
meaningful, in terms of the leading principal minors of $\mathbf{I}-\mathbf{A}$,
converting a computational convenience into a statement about whether an economy
is productive.

The extension that makes the framework environmental is also Leontief's. Leontief
(1970) adds pollutants as rows of the accounting system, so that emissions are
attributed to the production generating them and propagate with the goods
themselves. That paper originates the environmentally extended input–output
literature and is the ancestor of the sectoral carbon intensities in use today.
Miller and Blair (2022) give the modern synthesis, and three of their treatments
recur throughout the applied literature: the price dual, which transposes the
same matrix to answer how far prices move when costs change rather than how much
output a demand shock requires; the inter-country generalisation, in which the
flow matrix is blocked by region and the off-diagonal blocks record trade; and
the aggregation problem, since aggregation is demonstrably not neutral and
introduces bias whose direction depends on how heterogeneous the merged units
are.

## The multi-regional problem, and its resolution by measurement

For half a century the multi-regional literature was organised around a single
obstacle: the inter-regional flows are the object one needs and the object one
rarely has. Isard (1951) states the exact formulation, in which $a_{ij}^{rs}$
records how much of good $i$ from region $r$ sector $j$ in region $s$ requires.
It is also the least usable, since it demands a full bilateral flow matrix that
statistical agencies do not collect.

Two responses take opposite routes around the missing data. Chenery (1953) and
Moses (1955) preserve the accounting exactly and weaken the behavioural content,
assuming every user of a good within a region draws on the same mix of origins,
so that a single trade coefficient suffices across all using sectors and
$a_{ij}^{rs} = t_i^{rs}\,a_{ij}^{s}$. This requires only regional trade totals,
at the cost of assuming that a car plant and a hospital in the same region source
their steel identically. Leontief and Strout (1963) instead estimate the flows,
treating regional outputs as entering a national pool and postulating a gravity
relation,

$$z_i^{rs} \;=\; \frac{x_i^{r}\,d_i^{s}}{x_i^{\bullet}}\;Q_i^{rs},$$

with $Q_i^{rs}$ an interregional friction decreasing in transport cost. Because
the frictions must reproduce known row and column totals, the system is solved
iteratively by the biproportional fitting Stone (1961) introduced for
input–output work and Bacharach (1970) analysed formally. The cost of that
elegance is that the resulting trade pattern is a model output, so any subsequent
result depending on how a shock crosses a border inherits the gravity
specification's error alongside the model's own.

The obstacle dissolved when the flows were measured rather than inferred. Tukker
and Dietzenbacher (2013) review the research programme that assembled global
multi-regional tables from national accounts and bilateral trade statistics
during the 2000s, which produced four major databases within a few years of one
another: WIOD, documented by Timmer et al. (2015), alongside EXIOBASE, Eora and
the GTAP-based compilations. Their plurality raised the question of whether
findings are database-dependent. Moran and Wood (2014) address it by harmonising
satellite accounts and comparing consumption-based carbon accounts across
databases, finding agreement within roughly ten per cent for most major
economies; Owen (2017) reaches compatible conclusions at book length and
attributes residual disagreement to industry aggregation, emissions data sources
and modelling assumptions. The inter-country tables of the OECD (2025) belong to
the same generation and supply the off-diagonal blocks directly.

What measured inter-country tables make possible, beyond propagation, is
consumption-based accounting: attributing emissions to the final demand that
occasions them rather than to the territory where they are released. Davis and
Caldeira (2010) established the magnitude of the gap between the two accounts,
finding that a substantial share of the emissions consumed in developed economies
is produced elsewhere. The consequence for any exercise ranking economies by
climate relevance is that a ranking on trade weight and a ranking on embodied
emissions are different orderings.

## Carbon pricing: instrument, incidence and leakage

The choice between taxing emissions and capping them descends from Weitzman
(1974), whose comparison of prices and quantities under uncertainty establishes
that the preferred instrument depends on the relative slopes of marginal cost and
marginal benefit. The stock-pollutant case was taken up by Hoel and Karp (2002)
and Newell and Pizer (2003) and reassessed by Karp and Traeger (2018); Hepburn
(2006) and Stavins (2022) review the accumulated arguments for the climate
application. Green (2021) supplies the ex post counterweight, surveying empirical
evaluations of carbon pricing and concluding that measured emissions reductions
have been modest relative to expectations, while Peñasco, Anadón and Verdolini
(2021) compare ten decarbonisation instruments on both outcomes and distributional
trade-offs. The standing implication is that a carbon price is a contested policy
variable, not a state of nature.

Given a price, the question of who bears it has been approached through the
input–output price model. Kay and Jolley (2023) apply such a model to a carbon
tax driven by the NGFS scenarios, finding price increases of ten to thirty per
cent in carbon-intensive industries under a two-hundred-dollar per tonne tax.
Roncalli and Semet (2024) develop the cost-push formulation in more detail,
tracing a tax from the sectors on which it is levied to those that ultimately
bear it and separating the charge on a firm's own emissions from the charge
embodied in its purchased inputs. Two of their findings are load-bearing for
anything built on the same apparatus: the indirect burden is frequently the
larger of the two, and the division between what a firm absorbs and what it
passes downstream is genuinely open, depending on market structure, contract
length and demand elasticity, none of which an input–output table records.

The pass-through literature confirms that openness rather than resolving it. RBB
Economics (2014) survey the theory and measurement of cost pass-through and find
rates varying widely with market structure and with the nature of the cost shock.
Weber and Wasner (2023) argue that under generalised cost pressure firms with
market power may pass through more than their cost increase, which makes rates
above unity a live possibility rather than an arithmetic boundary.

Whether a unilateral price merely relocates emissions is the leakage question,
and the literature answers it by model comparison rather than through any single
framework, since the answer turns on trade and energy-market elasticities that no
one model pins down. The Energy Modeling Forum study of Böhringer, Balistreri and
Rutherford (2012), discussed above for what it reveals about general-equilibrium
models, is also the reference point on the substance: leakage rates cluster
between five and twenty per cent, and border carbon adjustment reduces them
without eliminating them. A border adjustment is, in that literature's terms, a
tariff differentiated by embodied carbon.

## The transmission relations

The link from carbon price to consumer prices is the least settled quantity in
the chain, and the disagreement is worth stating precisely, because a single
coefficient is often quoted as though it were established. Moessner (2022)
estimates New-Keynesian Phillips curves across OECD economies over 1995–2020 and
finds that a ten-dollar per tonne rise in the carbon price raises headline
inflation by roughly 0.08 percentage points. Konradt and Weder di Mauro (2023),
using carbon taxes implemented in Europe and Canada over three decades, find
dynamic effects on headline inflation statistically indistinguishable from zero
and read their evidence as relative price change — energy dearer, other goods
cheaper — rather than inflation. Bauer and Känzig (2024) reconcile the two only
partly, finding that carbon pricing moves inflation *expectations* even where
realised inflation moves little, and the International Monetary Fund (2024)
reaches intermediate estimates for the euro area. Any model adopting a point
estimate here adopts one side of a live dispute.

The remaining relations are better settled. Taylor (2007) supplies the monetary
reaction function, and Taylor and Williams (2010) defend the equal-weight
specification as robust across model specifications precisely because it is not
tuned to any of them. Hull and White (1994) supply the term structure: their
one-factor model gives the shift at maturity $\tau$ as a deterministic multiple
$B(\tau)/\tau$ of the short-rate shift, independent of volatility, so a curve
displacement follows without calibrating a volatility surface. Sarno and Taylor
(2002) remain the standard reference on the two exchange-rate parities and are
candid that relative purchasing power parity performs poorly at short horizons
while covered interest parity is close to an arbitrage identity.

## The framework and the gap

Berrahoui, Kenyon, Macrina and Nathanael (2025) assemble these relations into
what they call an ensemble: a short sequence of individually simple, individually
auditable steps running from a climate scenario to a set of market shocks, two of
them stated as propositions and proved — the allocation of aggregate damage
across sectors, and the mapping of a short-rate shift onto the term structure.
The design descends from earlier work by the same authors on pricing carbon
consistently within financial instruments (Kenyon, Macrina and Berrahoui, 2022).
Its distinguishing property is the one Acharya et al. (2023) identify as missing
from supervisory practice: because every relation is visible, a disagreement
about the answer can be localised to a disagreement about one relation. Its cost
is realism, in the dimensions the four alternative model families were built to
capture.

It is also, as published, a single-economy framework calibrated on the United
Kingdom, and that restriction has two consequences given the literature above.
Leontief (1970) and the consumption-based accounting tradition after Davis and
Caldeira (2010) establish that emissions, and the costs of pricing them, cross
borders through production chains; a one-country model has nowhere for that cost
to go. And the exchange rate, the cross-currency basis and every other relative
price are not merely harder to compute in such a model but undefined in it.

The gap is therefore narrow and specific. A transparent stress-testing framework
with proved internal relations exists for one economy (Berrahoui et al., 2025). A
mature multi-regional input–output apparatus exists (Miller and Blair, 2022;
Tukker and Dietzenbacher, 2013), together with measured inter-country tables that
remove the estimation step the Leontief–Strout tradition required. Input–output
treatments of carbon-tax incidence exist for single economies (Kay and Jolley,
2023; Roncalli and Semet, 2024). No treatment joins them, and until one does, the
quantities that exist only between economies remain outside the reach of an
auditable stress test.

---

### References

Acharya, V. V., R. Berner, R. Engle, H. Jung, J. Stroebel, X. Zeng and Y. Zhao
(2023). Climate stress testing. *Annual Review of Financial Economics* 15,
291–326.

Bacharach, M. (1970). *Biproportional Matrices and Input–Output Change.*
Cambridge University Press.

Bank of England (2022). *Results of the 2021 Climate Biennial Exploratory
Scenario (CBES).* May 2022.

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

Grubb, M., C. Wieners and P. Yang (2021). Modeling myths: on DICE and dynamic
realism in integrated assessment models of climate change mitigation. *WIREs
Climate Change* 12(3), e698.

Hafner, S., A. Anger-Kraavi, I. Monasterolo and A. Jones (2020). Emergence of new
economics energy transition models: a review. *Ecological Economics* 177, 106779.

Hawkins, D. and H. A. Simon (1949). Note: some conditions of macroeconomic
stability. *Econometrica* 17, 245–248.

Hepburn, C. (2006). Regulation by prices, quantities, or both: a review of
instrument choice. *Oxford Review of Economic Policy* 22(2), 226–247.

Hoel, M. and L. S. Karp (2002). Taxes versus quotas for a stock pollutant.
*Resource and Energy Economics* 24(4), 367–384.

Hull, J. and A. White (1994). Numerical procedures for implementing term
structure models I: single-factor models. *Journal of Derivatives* 2(1), 7–16.

International Monetary Fund (2024). *Carbon prices and inflation in the euro
area.* IMF Working Paper WP/24/31.

Isard, W. (1951). Interregional and regional input–output analysis: a model of a
space-economy. *Review of Economics and Statistics* 33(4), 318–328.

Karp, L. S. and C. P. Traeger (2018). *Prices versus quantities reassessed.*
CESifo Working Paper 7331.

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

Leontief, W. (1941). *The Structure of American Economy, 1919–1929.* Harvard
University Press.

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

Network for Greening the Financial System (2019). *Climate Macroeconomic
Modelling Handbook.*

Network for Greening the Financial System (2024). *NGFS Climate Scenarios for
Central Banks and Supervisors*, Phase V, and *Technical Documentation.*

Newell, R. G. and W. A. Pizer (2003). Regulating stock externalities under
uncertainty. *Journal of Environmental Economics and Management* 45(2), 416–432.

Nordhaus, W. (2017). Revisiting the social cost of carbon. *Proceedings of the
National Academy of Sciences* 114(7), 1518–1523.

Notre Dame Global Adaptation Initiative (2024). *ND-GAIN Country Index.*

OECD (2025). *OECD Inter-Country Input–Output Database*, 2025 edition. Paris:
OECD.

Owen, A. (2017). *Techniques for Evaluating the Differences in Multiregional
Input–Output Databases.* Springer.

Peñasco, C., L. D. Anadón and E. Verdolini (2021). Systematic review of the
outcomes and trade-offs of ten types of decarbonization policy instruments.
*Nature Climate Change* 11(3), 257–265.

Pindyck, R. S. (2013). Climate change policy: what do the models tell us?
*Journal of Economic Literature* 51(3), 860–872.

RBB Economics (2014). *Cost Pass-through: Theory, Measurement and Potential
Policy Implications.* Report for the Office of Fair Trading.

Roncalli, T. and R. Semet (2024). *The Economic Cost of the Carbon Tax.* Amundi
Investment Institute Working Paper 156, SSRN 4755259.

Sarno, L. and M. P. Taylor (2002). *The Economics of Exchange Rates.* Cambridge
University Press.

Stavins, R. N. (2022). The relative merits of carbon pricing instruments: taxes
versus trading. *Review of Environmental Economics and Policy* 16(1), 62–82.

Stone, R. (1961). *Input–Output and National Accounts.* Paris: OECD.

Swiss Re Institute (2024). *Changing Climates: The Heat Is (Still) On.* Zurich.

Taylor, J. B. (2007). *Monetary Policy Rules.* University of Chicago Press.

Taylor, J. B. and J. C. Williams (2010). Simple and robust rules for monetary
policy. In *Handbook of Monetary Economics*, vol. 3, 829–859. Elsevier.

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
