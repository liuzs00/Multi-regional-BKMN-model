# Abstract

A climate stress test has to join two things that do not naturally meet. On one
side sits a climate scenario, which speaks of emissions, carbon prices and
temperatures over the course of a century; on the other sit the quantities a
financial institution actually holds, which are quoted daily and re-marked
continuously. The framework of Berrahoui, Kenyon, Macrina and Nathanael (2025)
makes that join through a short chain of individually simple and individually
auditable relations, running from a carbon price and a temperature path to
inflation, policy rates, the yield curve, equity and credit. It does so, however,
for a single economy, and a single economy has no exchange rate.

This dissertation extends the framework to a system of economies. The world is
resolved into thirteen regions built from the 2022 OECD inter-country
input–output tables, covering 81 economies and 650 region–industry pairs, with
the region set derived from a stated linkage rule rather than asserted. A carbon
charge levied in one region then propagates to every other through the Leontief
price dual, so cross-border leakage is measured rather than assumed, and the
exchange rate becomes a well-defined object: following the original study's own
suggestion, it is the difference between two economies' yield-curve changes,
which separates exactly into a spot leg governed by relative purchasing-power
parity and a forward leg governed by covered interest parity.

Scenario uncertainty is handled by treating the seven NGFS narratives as
components of a Dirichlet-categorical mixture rather than as competing forecasts,
and by carrying four priors over them. The resulting sensitivity is the
organising empirical result: channels carrying the carbon charge inherit the
narratives' full disagreement — a factor of 22.7 on the spot exchange rate —
while channels carrying physical damage barely notice it, at 1.03 to 1.04,
because warming to 2040 is largely determined by emissions already made. Under a
prior anchored on published current-policy warming, the Indian rupee's five-year
forward against the euro moves by $-1.35\%$ at 2040 against $+0.35\%$ for
sterling, and appreciation is a symptom of harm rather than of resilience. Two
results are structurally unavailable to a single-region model: that ranking
regions by exchange rate, policy rate, credit spread and equity gives four
different answers from the same two underlying shocks, and that a dollar-pegged
region whose own conditions call for a policy rate some twenty-five basis points
below the anchor's carries that wedge as the climate component of the peg's cost.

The extension is validated structurally rather than by backtest, on synthetic
economies whose answers are known in advance, and the validation suite is itself
tested by mutation — which exposed that a suite built on symmetry gates is
sign-blind, since zero has no sign. As a stretch objective the same machinery is
applied to trade policy, since a tariff and a carbon charge are the same
mathematical object placed on different blocks of the input–output matrix.

---

# 1 Introduction

Supervisors have spent the better part of a decade asking banks and insurers a
question the industry is not well equipped to answer: what does climate change do
to the value of what you hold? The exercises that have addressed it at scale — the
European Central Bank's climate risk stress test (ECB, 2022) and the Bank of
England's Climate Biennial Exploratory Scenario (Bank of England, 2022) — reach
their answers through large macro-financial models whose internal workings are
not, in general, reproducible by the institutions being tested. Their outputs are
credible; their mechanisms are opaque. An institution asked to hold capital
against a number it cannot reconstruct is in an uncomfortable position, and an
institution asked to *manage* a risk it cannot decompose is in a worse one, since
it has no way of knowing which of its exposures the number is about.

Berrahoui, Kenyon, Macrina and Nathanael (2025) — hereafter BKMN — take the
opposite approach, and it is their framework that this dissertation extends. They
propose what they call an *ensemble*: a short chain of relations, each simple
enough to be checked on its own, running from a climate scenario to a set of
market shocks. A carbon price becomes a cost on each sector in proportion to its
emissions intensity; an input–output description of the economy propagates that
cost to every other sector; a temperature path becomes a loss of output allocated
across sectors by vulnerability; the resulting change in value added drives
inflation, and inflation drives the policy rate, the yield curve, equity indices
and credit spreads in turn. Two of the links are stated as propositions with
proofs, which is unusual in this literature and is much of the framework's
appeal. The price of that transparency is that every relation is visible, and can
therefore be disagreed with individually — which is exactly the property a
supervised institution needs and a black box cannot offer.

The framework is developed for one economy and calibrated on the United Kingdom.
That is a coherent choice for a first exposition, but it forces an assumption
that is plainly false, and it forecloses a question that matters. The false
assumption is that a carbon price levied in one country stays there. Production
is international: a charge on Chinese steel is paid, in part, by whoever buys
goods made with Chinese steel, and a single-region model has no way of seeing
that leakage, because it has nowhere for the cost to leak to. The foreclosed
question is the exchange rate. An exchange rate is a *relative* price — the value
of one economy expressed in terms of another — and it is not merely difficult to
compute in a one-country model but undefined in it. BKMN say as much themselves,
observing that while their model "does not provide stressed FX, it could be
expanded to include multiple economies, enabling such calculations via the
difference in the changes of yield curves." That sentence is the specification
this dissertation implements.

The objective, then, is to build a multi-regional version of the BKMN model that
produces climate-attributable exchange-rate moves alongside the interest-rate and
inflation shifts the original already produces, using published regional
projections of carbon prices and temperature as inputs. Three requirements shape
the construction. The world must be resolved into a manageable number of regions,
and the choice of regions must be argued for rather than asserted. The sectoral
input–output model must be replaced by an international one, in the sense of
Miller and Blair (2022). And the exchange-rate result must fall out of the
existing machinery rather than being bolted on as a separate behavioural
equation, since a currency model estimated independently of the rest of the chain
would sacrifice precisely the auditability that motivates the framework. A fourth
and more speculative objective is taken up at the end: whether the same apparatus
can price shocks that are not carbon prices at all, tariffs being the obvious
candidate.

It is worth setting out the mathematical core at once, because the whole
dissertation is an elaboration of four objects. The first is the technical
coefficient matrix $\mathbf{A} = \mathbf{Z}\hat{\mathbf{x}}^{-1}$, formed from the
inter-country flow table $\mathbf{Z}$ and gross output $\mathbf{x}$, whose entry
$a_{ij}$ records how much of good $i$ sector $j$ requires per unit of its own
output. In the multi-regional setting $\mathbf{A}$ is blocked by region, and the
off-diagonal blocks are trade. Equilibrium output solves
$\mathbf{x} = \mathbf{A}\mathbf{x} + \mathbf{f}$, hence
$\mathbf{x} = (\mathbf{I}-\mathbf{A})^{-1}\mathbf{f}$, and the inverse is the
entire content of the method: it sums the infinite regress in which steel needs
coal which needs steel. That the sum converges is a substantive economic
condition rather than a technical convenience, and Appendix A establishes it.

The second object is the *dual*, which is what this model actually needs. The
Leontief inverse answers the question "how much output does a demand shock
require?"; a carbon charge poses the transposed question, "how much do prices
rise when costs do?". Writing $\mathbf{ct}$ for the vector of per-unit charges,
with $ct_j = \mathrm{CI}_j \times \mathrm{XCE} \times 10^{-6}$ the product of
sector $j$'s carbon intensity and the carbon price its region faces, and
$\hat{\boldsymbol\phi}$ for the diagonal matrix of pass-through shares, prices
respond as

$$\Delta\mathbf{p} \;=\; \widetilde{\mathcal{L}}(\phi)\,\mathbf{ct},
\qquad
\widetilde{\mathcal{L}}(\phi) \;=\;
\bigl(\mathbf{I}-\mathbf{A}^{\!\top}\hat{\boldsymbol\phi}\bigr)^{-1}\hat{\boldsymbol\phi},$$

and value added per unit of output changes by

$$\Delta\mathbf{v} \;=\;
\Bigl[\bigl(\mathbf{I}-\mathbf{A}^{\!\top}\bigr)\widetilde{\mathcal{L}}(\phi)
\;-\;\mathbf{I}\;+\;\hat{\boldsymbol\phi}\Bigr]\mathbf{ct}.$$

The financial reading is direct. The parameter $\phi$ is the share of the charge a
sector passes downstream in its price rather than absorbing in its own margin, and
the two limiting cases are exactly what one would want: at $\phi = 0$ the bracket
collapses to $-\mathbf{I}$ and the sector bears its whole carbon bill, while at
$\phi = 1$ it collapses to $+\mathbf{I}$ and, with final demand held fixed, the
sector ends up collecting the charge rather than paying it. Everything between is
the network doing its work, and the network can be perverse: a sector that emits
little but buys from those who emit a great deal reaches its worst outcome at
*intermediate* pass-through, where it is already paying more for its inputs but
cannot yet recover the cost in its own price. No sector-by-sector calculation
reveals that; only the matrix does.

The third object is the physical channel, which enters through a quadratic global
damage function $\Omega(\Delta T) = \kappa\,\Delta T^{2}$, calibrated on the
DICE-2023 central estimate (Barrage and Nordhaus, 2024) of a $1.6768\%$ output
loss at $2.2\,^{\circ}\mathrm{C}$, and is then allocated across regions in
proportion to a vulnerability-weighted output vector built from ND-GAIN scores.
The allocation conserves the global total by construction, so a region's physical
damage is a *share*: the cross-section of harm is exactly as reliable as the
vulnerability index and no more.

The fourth object is the chain that turns a real shock into a market price.
Inflation responds to the change in the carbon price, scaled by the share of a
region's emissions actually priced — so a region that prices nothing imports no
carbon inflation however carbon-intensive it is, which turns out to matter a great
deal. The policy rate follows a Taylor rule
$\Delta r = \varphi_\Pi \Delta \Pi + \varphi_Y \Delta Y$ with equal weights, in
which the output gap is the *physical* damage alone: a carbon charge is a tax
wedge, and a wedge redistributes output rather than destroying it, so it does not
belong in the term a central bank responds to. The short-rate shift is mapped onto
the curve by the Hull–White one-factor loading, $\Delta R(\tau) =
\bigl(B(\tau)/\tau\bigr)\Delta r$ with $B(\tau) = (1-e^{-a\tau})/a$. And then,
finally, the exchange rate falls out as a difference:

$$\Delta\log F_r(t,\tau)
\;=\; \underbrace{\mathrm{cum}\Pi_r(t)-\mathrm{cum}\Pi_{\mathrm{EUR}}(t)}_{\text{spot: relative PPP}}
\;+\; \underbrace{B(\tau)\,\bigl[\Delta r_r(t)-\Delta r_{\mathrm{EUR}}(t)\bigr]}_{\text{forward points: CIP}}.$$

No parameter is introduced at this last step; the exchange-rate result is a pure
recombination of quantities the earlier links already produce, which is why its
credibility rests on theirs. One feature of the algebra deserves to be pointed out
early, because it explains why the currency numbers in this dissertation are an
order of magnitude larger than the interest-rate numbers that generate them. The
tenor factor cancels: the per-annum rate shift scales as $B(\tau)/\tau$, which
*decays* from $1$ towards $0$, while the forward point scales as $B(\tau)$ itself,
which *grows* towards the limit $1/a$. A hundred basis points of differential is
worth $0.98\%$ at one year and $13.77\%$ at twenty. That is arithmetic of forward
pricing rather than anything climatic, but it means the exchange-rate channel
inherits and amplifies every uncertainty in the rate channel.

Two design decisions sit between this machinery and the results, and both are
treated as quantities to be derived rather than asserted. The first is the region
set. Any multi-regional exercise must decide how finely to resolve the world, and
the decision is usually made by listing the economies judged important and
sweeping the rest into a residual. The trouble is that within an aggregate every
member necessarily shares one carbon price, one carbon intensity, one
vulnerability score and one currency, so promoting an economy out of a block buys
not *size* but *resolution*. The relevant question is therefore not which
economies are largest but which, if left inside a block, would cause that block to
misrepresent them. Chapter 4 answers it with two linkage measures computed from
the European Union's final-demand footprint, one economic and one weighted by
embodied emissions, a greedy agglomerative procedure to establish which economies
merit individual resolution, an explicit threshold rule to supply the cut the
clustering cannot, and a constraint requiring the residual not to dominate the
largest named region. The procedure returns thirteen regions covering $96.5\%$ of
the Union's economic and $89.2\%$ of its carbon footprint. Twelve of these are
analytical regions whose results are interpreted; the thirteenth is a closure term
whose outputs are never reported, and whose sufficiency is tested by rebuilding
the model at finer granularity and confirming that no analytical region's shock
moves by more than $0.036$ percentage points. The carbon measure earns its keep:
Africa and Türkiye enter on carbon linkage alone and would be discarded by any
ranking on trade weight, while India's emissions embodied in European demand are
nearly five times its trade share and Switzerland's are one sixth of its.

The second decision concerns scenarios. NGFS publishes seven narratives and no
probabilities over them, and reporting results under one narrative silently
assigns it probability one. Following the single-region study, the narrative is
therefore treated as a categorical draw with a Dirichlet prior on its probability
vector, so that every reported quantity is an expectation
$\mathbb{E}[X] = \sum_s w_s X_s$ with $w_s = (\alpha_s + n_s)/(\alpha_0 + n)$ by
conjugacy. Only the mean of the Dirichlet is used, which leaves the concentration
parameter inert for every number reported and a prior fully described by where it
places its mass. Four priors are carried — uniform, two asserted bookends, and one
anchored on the roughly $2.7\,^{\circ}\mathrm{C}$ of end-century warming that
published assessments place current policy on — and the headline is the anchored
one, because it is the only member of the set that answers to anything outside the
model. Carrying four rather than one is not hedging. It is what makes the
prior-sensitivity result available, and that result turns out to be the most
useful thing the exercise produces.

The principal findings can be previewed briefly. The first and most general is
that transition risk is a policy choice and physical risk, at this horizon, is
not: the mean transition cost varies by a factor of thirty-seven across the seven
narratives while the mean physical damage varies by eight per cent, because
warming to 2040 is largely determined by emissions already made. This asymmetry
propagates cleanly into the financial channels and sorts them into two groups.
Those carrying the carbon charge — the spot exchange rate, transition value added,
carbon-intensive credit — inherit the full disagreement between the narratives.
Those carrying physical damage — the policy rate, the term structure, operational
risk — move by three or four per cent across the whole range of priors. An
institution whose exposure runs through interest rates can use these numbers
without holding a view on climate policy; one whose exposure runs through
carbon-intensive credit cannot, and should quote a range rather than a number.

The second finding is that "climate exposure" is not one quantity. Ranking the
worst-affected regions by exchange rate, policy rate, credit spread and equity
produces four different answers from the same two underlying shocks, because each
channel weights them differently: exchange rates by *relative* carbon pricing,
policy rates by *absolute* damage, credit by *sectoral composition*, and equity
partly by the availability of an estimated market beta. China is the sharpest
illustration, first on credit and last on equity on an identical value-added
shock, because its industrial composition is heavily weighted toward the sectors
the credit channel punishes while its estimated beta of $0.26$ mutes everything
the equity channel would otherwise transmit. Two desks looking at the same country
through two instruments would reach opposite conclusions, and neither would be
wrong about its own instrument.

The third is a result the multi-regional setting produces and the single-region
one structurally cannot. A region pegged to an anchor currency has no exchange
rate of its own — its bilateral rate against the euro *is* the anchor's, by
construction rather than by computation. Its Taylor rule, however, still responds
to its own damage. The Middle East is among the most physically exposed regions in
the model, so its own conditions call for a cut of $-65.7$ basis points at 2040
where the dollar it is pegged to delivers $-40.9$. That twenty-five-basis-point
wedge is the climate component of the peg's cost, and it is almost invariant to
the scenario prior, because both legs of the difference are driven by the part of
the problem the narratives agree about. The mechanism is familiar; what is new is
that the framework puts a number on it using nothing beyond machinery the rate
channel already contained.

A fourth result is structural rather than empirical, and is included because it
bounds the model's largest uncertainty. The pass-through share $\phi$ is a
convention rather than an estimate, and value added is extremely sensitive to it —
India's transition shock swings from $-378$ to $+578$ per cent of its reported
value across the range. Sweeping $\phi$ inside every narrative shows, first, that
every region's shock crosses zero somewhere in $[0.568, 0.917]$ across all
thirteen regions and all seven narratives, so at the reported midpoint every
region is still a net loser in every scenario and the midpoint is emphatically not
the neutral point; and second, that the policy rate and the exchange rate do not
move with $\phi$ at all, to machine precision, because the Taylor rule responds to
inflation and to physical damage and neither passes through the Leontief dual. The
widest uncertainty in the model is therefore confined to two of the four financial
channels, and the two treated most carefully here are immune to it.

Because a climate stress test cannot be backtested — there is no realised 2040 to
compare a projected exchange-rate move against, and there never will be in time to
matter — validation is structural. Synthetic economies are constructed whose
answers are known in advance: cut one region out of world trade and its spillover
must be exactly zero; make every region identical and every result must be
identical; change one attribute of one region and the asymmetry must appear only
where it was put. The real model code is run on these economies untouched, at a
tolerance of $10^{-15}$. The suite is then itself tested by deliberately breaking
the model and checking that the gates notice, and that exercise produced a finding
worth more than the gates themselves: a suite built on symmetry and invariance
gates is *sign-blind*, because zero has no sign. Flipping the sign of the spot
exchange-rate channel left every gate passing, which means a model asserting the
exact reverse of the economics would have been certified correct. Symmetry
establishes internal consistency, not orientation.

Finally, the stretch objective. A tariff is structurally the same object as a
carbon charge — an ad-valorem cost wedge propagating through the same dual — and
differs only in where it sits: the carbon charge falls on a sector's own
production and therefore lives on the diagonal blocks of $\mathbf{A}$, while a
tariff falls on imported inputs and lives off-diagonal. No new mathematics is
required, and the four trade measures in force in mid-2026 that the model can
represent are calibrated and run as a stack. The exercise yields one result worth
advertising here: under the full stack the dollar *depreciates* by $0.89\%$
against the euro, and almost all of it comes from tariffs the United States itself
levies, because the measures raise domestic prices and relative purchasing-power
parity weakens the currency with the higher price level. The common intuition that
protection strengthens a currency does not survive contact with the model.

The remainder of the dissertation is organised as follows. Chapter 2 surveys the
two literatures this work sits between and identifies the gap it occupies, giving
particular attention to the classical multi-regional input–output methods —
Isard's interregional model, Chenery–Moses, and the Leontief–Strout gravity
formulation — and to why an inter-country table makes all three unnecessary here.
Chapter 3 develops the model: the stress-testing frame, the multi-regional
input–output apparatus, the transition and physical channels, the macro-financial
transmission, the exchange-rate derivation, and the tariff extension. Chapter 4
turns to the numerical example: the data and calibration, the derivation of the
region set, the scenario mixture, the validation programme, the results, and the
tariff stack. Chapter 5 separates the model's assumptions from what those
assumptions cost and draws the conclusions. Three appendices carry the
mathematics that would otherwise interrupt the argument: the existence and
convergence of the Leontief inverse, and the proofs of the two propositions
inherited from the original study.
