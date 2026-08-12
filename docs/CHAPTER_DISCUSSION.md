# 5 Discussion

## 5.1 Assumption

It is worth separating two things that are easily confused. An assumption is a
modelling choice: a place where the mathematics required a commitment and one was
made. A limitation, treated in §5.2, is what that commitment costs. Almost every
assumption below could be relaxed, and the reason none of them is relaxed here is
that each would require data the exercise does not have or would obscure the
mechanism the model is meant to isolate.

The production side rests on a Leontief technology. The technical matrix
$\mathbf{A} = \mathbf{Z}\hat{\mathbf{x}}^{-1}$ is fixed, so a sector that needs
electricity and steel in a given proportion continues to need them in that
proportion however their relative prices move. This is the oldest assumption in
input-output analysis and the most consequential one here, because the entire
transition channel is a statement about how a cost wedge propagates through
$\mathbf{A}$. In a world where firms substitute away from carbon-intensive
inputs, the propagated cost is smaller than the model reports; the results should
therefore be read as an upper bound on the transition cost, conditional on the
carbon price. Appendix A establishes that the Leontief inverse
$(\mathbf{I}-\mathbf{A})^{-1}$ exists and that its Neumann expansion converges,
which is what allows the indirect requirements of any final demand to be summed
at all — a mathematical fact with an economic reading, namely that the infinite
regress of "steel needs coal needs steel" is summable precisely because no sector
recovers its own output entirely from itself.

A second commitment sits on top of the first. The carbon charge does not simply
fall on the sector that emits: some share $\varphi$ of it is passed downstream in
the sector's price, and the rest is absorbed in its own value added. The
dual $\tilde{\mathbf{L}}(\varphi) = (\mathbf{I}-\varphi\mathbf{A}^{\top})^{-1}\varphi$
carries this through the network, and the results are reported at
$\varphi = 0.5$, uniform across every sector and every region. Uniformity is a
convenience rather than a belief: market power, contract structure and the
elasticity of final demand all differ by industry, and a sector selling into a
competitive export market plainly passes through less than a regulated utility.
The choice is defensible only because §4.5 sweeps the whole range and shows that
two of the four financial channels do not depend on it at all.

The two shocks themselves are each a single equation. Transition risk enters as
an ad-valorem cost wedge $c_{t,j} = \mathrm{CI}_j \times \mathrm{XCE}_t \times
10^{-6}$ on Scope-1 emissions, with the intensity declining along each scenario's
own emissions path so that a decarbonising economy is not charged as though it
had stood still. Physical risk enters through a quadratic global damage function
$\Omega(\Delta T) = \kappa\,\Delta T^{2}$, calibrated on the DICE-2023 central
estimate of a $1.6768\%$ output loss at $2.2\,^\circ$C so that
$\kappa = 1.6768\times10^{-2}/2.2^{2} \approx 0.00346$, and then allocated across
regions by Proposition 3.1 in proportion to a vulnerability-weighted output
vector built from ND-GAIN scores. Two features of this deserve to be stated
plainly rather than buried. The damage is a *level* effect on value added, not a
growth effect, so the model says nothing about whether a damaged economy grows
more slowly thereafter; and the allocation conserves the global total by
construction, so a region's damage is a *share*, which means the cross-section of
physical harm is as reliable as ND-GAIN and no more.

The macro-financial transmission is a chain of four linear relations, each
inherited from the original study and each taken as given here. Inflation
responds to the change in the carbon price through the Moessner relation, at
$8\times10^{-5}$ per dollar per tonne, scaled by the share of a region's
emissions actually priced — so a region that prices nothing imports no carbon
inflation, however carbon-intensive it is. The policy rate follows a Taylor rule
$\Delta r = \varphi_\Pi \Delta \Pi + \varphi_Y \Delta Y$ with
$\varphi_\Pi = \varphi_Y = 0.5$, in which the output gap is the physical damage
*alone*. That last point is a genuine modelling judgement rather than an
inherited one: a carbon charge is a tax wedge, and a wedge redistributes output
rather than destroying it, so it does not belong in the term a central bank
responds to. The short-rate shift is then mapped onto the curve by Proposition
3.2 through the Hull–White one-factor loading $B(\tau)/\tau$ with mean reversion
$a = 0.04$, which is volatility-independent and shared by every region. Finally,
exchange rates follow relative purchasing-power parity on the spot leg and
covered interest parity on the forward leg, with the euro as numéraire.

The market translations are the least theoretical part of the model and the most
borrowed. Equity applies a market beta to the total value-added shock; credit
blends sector shocks into published index baskets and applies a published
regression slope; operational risk runs the physical shock through Okun's law
into unemployment and then into loss frequencies. All three elasticities are
estimated on a single national sample in the original study and applied unchanged
to every region here. This is not defended as realistic. It is defended as
honest: the coefficients are published, the histories needed to re-estimate them
region by region are not, and inventing them would replace a stated borrowing
with an unstated fabrication.

The scenario treatment is the last assumption and in some ways the largest. The
seven NGFS narratives are not treated as competing forecasts to be chosen between
but as components of a Dirichlet-categorical mixture, so every reported quantity
is an expectation $\mathbb{E}[X] = \sum_s w_s X_s$ against a distribution over
narratives. Only the mean of the Dirichlet is used, which makes the concentration
parameter inert for every number reported and leaves the prior fully described by
where it places its mass. Four priors are carried, and the headline is the one
anchored on published current-policy warming. Weights are held static across the
horizon: the possibility that beliefs migrate between narratives as policy
unfolds is examined as a sensitivity but does not enter the reported results.

Underlying all of it is a comparative-static frame. The model computes the
difference between a world with climate policy and warming and a counterfactual
world without, at a set of horizon dates. There is no accumulation, no
expectations formation, no capital reallocation and no adaptation. Results are
reported as *shifts* rather than levels, because the market curve that would
anchor them is deliberately omitted in order to isolate the climate-attributable
component.

## 5.2 Limitation

The limitations follow the assumptions closely, and it is more useful to say what
each one costs than to list them again.

The fixed technology makes the transition results an upper bound. How loose a
bound is unknown, because the substitution elasticities that would answer the
question are precisely what an input-output table cannot reveal. The pass-through
parameter compounds this. At $\varphi = 0$ a region absorbs its entire carbon
bill and at $\varphi = 1$ it collects it, so India's transition shock swings from
$-378$ to $+578$ per cent of its reported value across the range — the widest
single uncertainty in the model. The mitigating finding is structural rather than
empirical: every region's shock crosses zero somewhere in $[0.568, 0.917]$ across
all thirteen regions and all seven narratives, so at the reported midpoint every
region is still a net loser in every scenario, and the policy rate and the
exchange rate do not move with $\varphi$ at all. The uncertainty is therefore
large but confined to value added and credit.

The scenario prior is not data. NGFS publishes no probabilities over its
narratives, and three of the four priors used here are the modeller's
construction; only the consensus prior answers to an external estimate, and that
estimate is itself a projection. Reporting four side by side is a way of being
honest about this rather than a way of resolving it, and the prior-sensitivity
result identifies which conclusions survive the choice: channels carrying the
carbon charge inherit the narratives' full disagreement — the rupee's spot move
ranges over a factor of 22.7 — while channels carrying physical damage barely
notice it, at 1.03 to 1.04. An institution exposed through interest rates or
employment can use these numbers without holding a view on climate policy; one
exposed through carbon-intensive credit or the spot currency cannot, and should
quote a range.

The borrowed elasticities are the weakest link in the market layer, and one piece
of evidence for that is visible in the results themselves. The original study's
own estimates give financials and real estate positive regression slopes, so in
this model a fall in value added *compresses* their spreads. That is a property
of the period and market those regressions were fitted on, inherited wholesale,
and it should not be read as a finding that climate stress improves bank credit.
If the sign can be wrong for two of twelve indices in the sample where it was
estimated, there is little reason to expect the magnitudes to travel to Indian or
Turkish credit. The same caution applies, more weakly, to the operational-risk
slopes, and the equity cross-section carries a related problem: three of the nine
currency regions share a proxy beta of 2.00 for want of an accessible index
history, so part of what looks like a cross-section of exposure is a
cross-section of data availability.

The exchange-rate results carry three distinct caveats. Relative purchasing-power
parity is a poor description of exchange rates at short horizons; the covered
interest parity leg is much the sounder of the two, which is fortunate, since it
is also the larger. The cross-section rests on six floating currencies and one
peg, so correlations computed on it are indicative and none should be quoted with
a standard error. And there is an unresolved ambiguity in the currency to which
the inflation coefficient should be applied: the original study writes it against
a dollar carbon price, but its published results are reproduced only when it is
applied to a sterling price. This model applies it to dollars. If the original
reading is correct, every spot level reported here is overstated by roughly a
third. Ratios between currencies and their ordering are unaffected, since the
factor is common to both legs of every difference, but the levels are not, and
resolving this would require access to the original implementation.

Two structural choices limit what the results can be asked to do. A single
mean-reversion parameter shared by all regions means the term structure rescales
the short-rate shift without ever reshaping it, so the model cannot express that
some economies' curves would steepen under climate stress while others flatten;
all cross-region variation comes from $\Delta r$ and none from the curve.
Reporting shifts rather than levels means nothing imposes a zero lower bound on
the implied policy rate, so a sufficiently large damage term produces a cut the
world could not actually deliver. Both are defensible at the horizons considered
and both would need revisiting before the framework were used for pricing.

Finally, three limits on scope. Restricting the financial channels to regions
with a legal currency is a reporting choice, not a claim that the excluded
regions face no financial risk: Africa carries one of the largest real shocks in
the model, and a bank lending there is exposed to it — what the model cannot do
is name the currency that exposure is denominated in. The peg result assumes the
peg holds, which is precisely what a large enough differential would eventually
call into question. And no external benchmark exists for the exchange-rate or
credit numbers themselves. The value-added shocks do sit inside the range of
NGFS's own macroeconomic estimates, which is some comfort about the scale of the
underlying real shock, but an expected forward on the rupee has nothing to be
compared against. Validation here establishes internal consistency and structural
correctness, not external accuracy, and §4.4 is careful to claim only the former.

## 5.3 Conclusion

This dissertation set out to extend a single-region climate stress-testing
framework to a multi-regional one, and the extension turns out to be more than
bookkeeping. Replacing the economy with a system of economies linked by an
international input-output table changes what the model can say, because it makes
the *relative* position of a region a first-class object. The clearest instance is
the exchange rate. In a single-region model there is no exchange rate to speak
of; here it emerges as the difference between two countries' yield-curve changes
and separates cleanly into a spot leg driven by relative carbon-price inflation
and a forward leg driven by the rate differential under covered interest parity.
That channel exists only in the multi-regional setting, and it is where the most
distinctive results of this work sit.

Three findings seem worth carrying forward. The first is that transition risk is
a policy choice and physical risk, at this horizon, is not. The mean transition
cost varies by a factor of thirty-seven across the seven NGFS narratives while
the mean physical damage varies by eight per cent, because warming to 2040 is
largely determined by emissions already made. This asymmetry propagates cleanly
into the financial channels and explains, without further argument, why the
policy rate is nearly indifferent to the scenario prior while the spot exchange
rate is extremely sensitive to it.

The second is that "climate exposure" is not one quantity. Ranking the
worst-affected regions by exchange rate, policy rate, credit spread and equity
produces four different answers from the same two underlying shocks, because each
channel weights them differently — exchange rates by *relative* carbon pricing,
policy rates by *absolute* damage, credit by *sectoral composition*, and equity
partly by the availability of a market beta. China is the sharpest illustration:
first on credit and last on equity, on an identical value-added shock, because
its sectoral composition is heavily weighted toward the industries the credit
channel punishes while its estimated market beta is the lowest in the set. Two
institutions looking at the same country through two instruments would reach
opposite conclusions, and neither would be wrong about its own instrument.

The third is a result the multi-regional setting produces and the single-region
one structurally cannot. A region pegged to an anchor currency has no exchange
rate of its own — its bilateral rate against the euro *is* the anchor's, by
construction. But its Taylor rule still responds to its own damage, and the
Middle East is among the most physically exposed regions in the model, so its own
conditions call for a policy rate cut some twenty-five basis points deeper than
the dollar delivers. That wedge is the climate component of the peg's cost. It is
almost invariant to the scenario prior, because both legs of the difference are
driven by physical damage, the part of the problem the narratives agree about. It
is a small number and a familiar mechanism — a pegged economy imports the
anchor's monetary policy — but the framework puts a figure on it using nothing
beyond machinery the rate channel already contained.

Alongside the results, two methodological points may be of wider use. Region
selection was derived rather than asserted: the thirteen regions are the output
of a stated rule applied to European final-demand footprints, so the aggregation
can be argued with on its own terms instead of being defended as judgement. And
the validation work in §4.4 produced a finding about validation itself. A suite
built on symmetry and invariance gates — of the form "this quantity must be
zero" — is *sign-blind*, because zero has no sign. Deliberately flipping the sign
of the spot channel left every gate passing, which means a model asserting the
exact reverse of the economics would have been certified correct. Symmetry
establishes internal consistency, not orientation, and any suite built on it
needs at least one asymmetric, direction-pinning test per channel. The way to
find out whether it has one is to break the model on purpose.

The natural extensions are visible from here. Relaxing the fixed technology, even
crudely, would convert the transition results from an upper bound into a range.
Estimating the credit and equity elasticities regionally, where histories permit,
would remove the least defensible layer of the model. Carrying the value-added
shocks through to expected credit losses under IFRS 9 would connect the framework
to the quantity a bank actually provisions against, which is the obvious next
step for supervisory use. And the reporting convention adopted here — an
expectation over narratives, with the prior varied and its influence measured
channel by channel — seems worth applying more widely than this exercise, since
it separates conclusions that depend on a view about climate policy from those
that do not, and the second set turns out to be larger than one might expect.
