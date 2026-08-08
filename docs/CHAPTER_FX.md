# Exchange Rates: From Yield Curves to Currency Moves

## 1. Purpose and the paper's route to FX

The single-region model produces no exchange rate, and cannot: an exchange rate is a
relative price between two economies, and a one-country model has only one. The
authors are explicit that this is the natural extension, noting that while the current
version "does not provide stressed FX, it could be expanded to include multiple
economies, enabling such calculations via **the difference in the changes of yield
curves**" (§4.3).

That sentence is the specification this chapter implements. It is a strong constraint
and a useful one, because it fixes the mechanism: FX is not modelled by a separate
behavioural equation but is *derived* from quantities the model already produces.
Nothing new is estimated. The exchange-rate result is a rearrangement of the interest
rate and inflation shifts of the previous chapter into differential form, and its
credibility rests on theirs.

The chapter sets out the two parity relations used, derives the central formula,
establishes the structural properties that follow from it, and reports results.
Implementation is `bkmn/fx.py` — four functions and no free parameters.

---

## 2. Setup and conventions

### 2.1 Quotation

Let $S_r(t)$ denote the spot exchange rate of region $r$ against the base currency,
quoted as **units of currency $r$ per one euro**. Under this convention an increase in
$S_r$ means more of currency $r$ buys one euro, i.e.

$$\Delta \log S_r > 0 \;\;\Longleftrightarrow\;\; \text{currency } r \text{ \textbf{depreciates} against the euro.}$$

The sign convention is stated explicitly because it is the most common source of error
in reading the results, and because the economically interesting cases below involve
currencies that *appreciate* — and therefore carry negative numbers.

All quantities are **log changes relative to the no-climate-shock counterfactual**,
not levels. The model does not forecast the euro–dollar rate; it computes the
displacement of that rate attributable to a climate scenario.

### 2.2 Base currency and coverage

The euro is the base. The choice is not innocuous — every result is a statement about
a currency *pair* — but §2.5 below shows that the choice of base is immaterial to the
information content, since any cross rate can be recovered exactly.

Of the twenty regions, fourteen carry an analytical currency: USD, CNY, GBP, JPY, INR,
CAD, NOK, IDR, CLP, AUD, SGD, TRY, KRW, KZT. The EU27 is the base itself. The
remaining five — Russia, the Middle East, Africa, Latin America and the
rest-of-world closure — are retained as *structural* regions: they participate fully in
the input–output propagation and therefore influence every other region's GDP shock,
but no exchange rate is reported for them. For the aggregates this is because a
composite of many currencies has no exchange rate; for Russia it is because the
post-2022 dislocation of its financial markets makes a parity-based calculation
uninterpretable.

---

## 3. The two channels

The model separates the exchange-rate response into a **spot** channel driven by
inflation differentials and a **forward** channel driven by interest-rate
differentials. They are reported separately as well as combined, because they have
different epistemic status: one is assumption-free, the other is a modelling choice.

### 3.1 Spot: relative purchasing power parity

Absolute PPP equates the exchange rate to the ratio of price levels,
$S_r = P_r/P_{\mathrm{EUR}}$. Taking logs and differencing gives **relative PPP**, in
which the change in the exchange rate equals the inflation differential:

$$\boxed{\;\Delta\log S_r(t) \;=\; \mathrm{cum}\Pi_r(t) \;-\; \mathrm{cum}\Pi_{\mathrm{EUR}}(t)\;}$$

where $\mathrm{cum}\Pi_r(t)=\sum_{s\le t}\Delta\Pi_r(s)$ is the cumulative
climate-induced inflation deviation from the previous chapter. The currency of the
economy with the larger carbon-driven inflation depreciates.

This channel has a closed form. Because the annual deviation is
$\Delta\Pi_r(s) = k\,[\mathrm{XCE}_r(s)-\mathrm{XCE}_r(s-1)]\,\Omega_r$, the sum
telescopes:

$$\mathrm{cum}\Pi_r(t) \;=\; k\,\big[\mathrm{XCE}_r(t)-\mathrm{XCE}_r(t_0)\big]\,\Omega_r,
\qquad k = 8\times10^{-5},$$

so the spot shift depends only on the *level* of the carbon price at the horizon, not
on its path. Substituting,

$$\Delta\log S_r(t) \;=\; k\Big\{\big[\mathrm{XCE}_r(t)-\mathrm{XCE}_r(t_0)\big]\Omega_r
-\big[\mathrm{XCE}_{\mathrm{EUR}}(t)-\mathrm{XCE}_{\mathrm{EUR}}(t_0)\big]\Omega_{\mathrm{EUR}}\Big\}. \tag{1}$$

Equation (1) has a consequence worth drawing out. When carbon prices are near-uniform
across regions — as they are under Net Zero 2050, where the NGFS zone prices span only
$\$332$–$389$ per tonne — the bracketed price changes are approximately equal, say
$\Delta X$, and (1) collapses to

$$\Delta\log S_r(t) \;\approx\; k\,\Delta X\,\big(\Omega_r-\Omega_{\mathrm{EUR}}\big).$$

**Under an ambitious global scenario the entire spot channel is a coverage
differential.** A region that prices a smaller share of its emissions than the EU
imports less carbon inflation and its currency appreciates, regardless of its
emissions or its industrial structure. A testable signature follows: every region with
zero coverage must show *identical* spot shifts, since all that survives in (1) is the
euro term. India and Turkey, both with $\Omega=0$, indeed show exactly $-2.27\%$ at
2040 under Net Zero.

### 3.2 Forward: covered interest parity

Covered interest parity is an arbitrage relation rather than a behavioural hypothesis:
a forward contract hedged with borrowing and lending in the two currencies must price
so that no riskless profit exists. In continuously compounded form, for delivery at
$t+\tau$,

$$F_r(t,\tau) \;=\; S_r(t)\,\exp\!\Big[\big(R_r(t,t+\tau)-R_{\mathrm{EUR}}(t,t+\tau)\big)\tau\Big],$$

so that in logs $\log F_r = \log S_r + \tau\,[R_r - R_{\mathrm{EUR}}]$. Differencing
between the climate-stressed state and the counterfactual, at fixed tenor,

$$\Delta\log F_r(t,\tau) \;=\; \Delta\log S_r(t) \;+\; \tau\,\big[\Delta R_r(t,t+\tau)-\Delta R_{\mathrm{EUR}}(t,t+\tau)\big]. \tag{2}$$

The second term is the **forward-point shift**. Its evaluation is where the previous
chapter's term-structure result enters.

---

## 4. The central formula

Proposition 2 of the previous chapter gives the zero-coupon rate shift as
$\Delta R_r(t,t+\tau) = \tfrac{B(\tau)}{\tau}\,\Delta r_r(t)$ with
$B(\tau) = (1-e^{-a\tau})/a$. Substituting into (2), the maturity factor cancels
exactly:

$$\tau\,\Delta R_r(t,t+\tau) \;=\; \tau\cdot\frac{B(\tau)}{\tau}\,\Delta r_r(t) \;=\; B(\tau)\,\Delta r_r(t),$$

leaving the model's central exchange-rate result:

$$\boxed{\;\Delta\log F_r(t,\tau)
\;=\; \underbrace{\mathrm{cum}\Pi_r(t)-\mathrm{cum}\Pi_{\mathrm{EUR}}(t)}_{\text{spot, relative PPP}}
\;+\; \underbrace{B(\tau)\,\big[\Delta r_r(t)-\Delta r_{\mathrm{EUR}}(t)\big]}_{\text{forward points, CIP}}\;}
\tag{3}$$

Every term on the right is produced by earlier chapters. No parameter is introduced
here: $k$ comes from the inflation channel, $a$ from the term-structure model, and the
policy-rate shifts from the Taylor rule. The FX result is a pure recombination.

### 4.1 The amplification property

The cancellation in the derivation is not merely tidy — it inverts the tenor
behaviour, and this is the single most consequential mathematical feature of the
chapter.

The *rate* shift decays with tenor, scaling as $B(\tau)/\tau$, which falls from $1$ to
$0.688$ over twenty years. The *forward point* scales as $B(\tau)$ itself, which
**increases** without bound in $\tau$ up to the limit $1/a$:

| $\tau$ | 1 y | 5 y | 10 y | 20 y | $\tau\to\infty$ |
|---|--:|--:|--:|--:|--:|
| $B(\tau)/\tau$ — rate shift | 0.980 | 0.906 | 0.824 | 0.688 | $\to 0$ |
| $B(\tau)$ — forward point | 0.980 | **4.532** | 8.242 | 13.767 | $\to 25.0$ |

The economics is straightforward once seen: a forward contract accumulates the rate
differential over its whole life, so even though the *per-annum* differential narrows
with tenor, the *total* carry grows. A one-hundred-basis-point differential produces a
$0.98\%$ move at one year but a $4.53\%$ move at five and a $13.77\%$ move at twenty.

This is why exchange-rate results in this model are an order of magnitude larger than
the interest-rate shifts that generate them, and why the forward channel dominates the
spot channel by roughly a factor of ten. It is a property of the arithmetic of forward
pricing rather than an artefact of the climate calibration, but it does mean the FX
numbers inherit and amplify every uncertainty in the rate channel — a point returned
to in §7.

### 4.2 What the differential structure implies

Equation (3) depends on region $r$ only through *differences* against the base. Two
consequences follow that are easy to misread.

First, **the absolute size of a region's shock is irrelevant; only its shock relative
to the euro area matters.** A region that cuts rates by 74 bp when the EU cuts 132 bp
has *relatively higher* rates and its currency therefore trades at a forward discount —
it depreciates — despite having been hit by the same shock in the same direction. The
United Kingdom and Norway both appear on the depreciating side for exactly this reason,
not because they escape the climate shock.

Second, currencies do not rank by GDP damage. The ordering is set by
$\Delta r_r - \Delta r_{\mathrm{EUR}}$, which combines each economy's carbon intensity,
its input–output position and its coverage — a composite that need not track output
loss monotonically.

### 4.3 Triangular consistency

A set of bilateral exchange rates must be internally consistent: the $A/B$ rate must
equal the $A$/EUR rate less the $B$/EUR rate, or a triangular arbitrage exists. Here
this holds **identically, by construction**, since every reported quantity is a
difference against the same base:

$$\Delta\log F_{A/B} = \big(\Delta\log F_{A}-\Delta\log F_{\mathrm{EUR}}\big)-\big(\Delta\log F_{B}-\Delta\log F_{\mathrm{EUR}}\big)
= \Delta\log F_{A}-\Delta\log F_{B}.$$

The residual is exactly zero in the implementation, not merely small. This also
resolves the concern raised in §2.2: **the choice of euro as base carries no
information**, since any other base is recovered by subtraction. The euro is a
presentational convenience.

---

## 5. Results

Decomposition at horizon 2040 under Net Zero 2050, five-year forward tenor, with
$\phi = 0.5$. Rate shifts in basis points, FX in per cent; negative FX means
appreciation against the euro.

| Region | $\Delta r$ (bp) | $\Delta r - \Delta r_{\mathrm{EUR}}$ (bp) | Spot (%) | Fwd points (%) | **Total 5y fwd (%)** |
|---|--:|--:|--:|--:|--:|
| China | $-570$ | $-438$ | $-0.70$ | $-19.86$ | $\mathbf{-20.56}$ |
| India | $-522$ | $-389$ | $-2.27$ | $-17.65$ | $\mathbf{-19.92}$ |
| Turkey | $-329$ | $-197$ | $-2.27$ | $-8.93$ | $\mathbf{-11.20}$ |
| Korea | $-284$ | $-152$ | $+0.49$ | $-6.88$ | $\mathbf{-6.39}$ |
| Japan | $-175$ | $-43$ | $+0.09$ | $-1.94$ | $-1.85$ |
| USA | $-101$ | $+32$ | $-1.95$ | $+1.44$ | $-0.52$ |
| Australia | $-140$ | $-8$ | $-0.02$ | $-0.37$ | $-0.39$ |
| Canada | $-112$ | $+20$ | $-0.94$ | $+0.90$ | $-0.04$ |
| UK | $-74$ | $+58$ | $-1.12$ | $+2.64$ | $\mathbf{+1.51}$ |
| Norway | $-47$ | $+85$ | $+0.35$ | $+3.85$ | $\mathbf{+4.20}$ |

Each row satisfies (3) to displayed precision.

**The forward channel dominates.** Spot moves are contained within roughly
$\pm2.3\%$ while forward points reach $-19.9\%$. The mechanism is the amplification of
§4.1 acting on rate differentials that are themselves large because, as the previous
chapter established, the Taylor rule is driven almost entirely by the output gap. A
carbon price is transmitted to currencies primarily as a *recessionary* shock, not an
inflationary one.

**Korea is the instructive case.** Its two channels pull in opposite directions.
Korean carbon-pricing coverage exceeds the EU's, so Korea imports *more* carbon
inflation and relative PPP implies depreciation: spot $+0.49\%$. But Korea's
industrial structure produces a large GDP shock and hence a rate cut of $284$ bp
against the EU's $132$ bp, and CIP turns that $152$ bp differential into $-6.88\%$ of
forward points. The forward channel overwhelms the spot channel by a factor of
fourteen and the net move is a $6.4\%$ appreciation. A model containing only a PPP
channel would have produced the opposite sign.

**Sign reversals identify relative, not absolute, resilience.** Sterling and the
Norwegian krone depreciate against the euro, despite suffering genuine GDP losses of
$1.5\%$ and $1.0\%$. Their carbon-intensity and input–output exposure is low enough
that their central banks cut less than the ECB, and CIP prices the resulting positive
rate differential as a forward discount. These are the model's *relative winners*, and
the euro base makes that visible.

**Structure, not price, drives the cross-section under Net Zero.** Because the NGFS
zone carbon prices are near-uniform in that scenario, essentially none of the spread
in the table comes from regions facing different carbon prices. It comes from
differences in coverage, which drive the spot channel through equation (1), and from
differences in carbon intensity and supply-chain position, which drive the forward
channel through the GDP shock. Scenarios with genuinely divergent regional prices —
Delayed transition, NDCs, Fragmented World — add a price contribution on top of this
structural core.

---

## 6. Validation

The FX layer is covered by gates in `tests/test_fx.py`, and three deserve mention.

**Triangular consistency** holds at machine zero, as §4.3 requires structurally.

**Reduction to the committed single-region model:** setting the carbon price to a flat
$\$70$ everywhere reproduces the published per-region GVA shocks to
$4\times10^{-16}$ percentage points, confirming that the multi-regional chain collapses
correctly onto the case the transition chapter validated against the paper.

**Scenario monotonicity:** the magnitude of the FX response increases with the
ambition of the scenario. Taking the absolute dollar spot shift at 2040, Current
Policies gives $0.007\%$, NDCs $0.345\%$ and Net Zero 2050 $1.952\%$. Climate-driven
currency displacement scales with the carbon price that causes it, which is a weak
test but one that would catch a sign or wiring error.

---

## 7. Assumptions and limitations

**The two channels differ in status, and should be reported separately.** Covered
interest parity is an arbitrage identity and the forward-point calculation inherits no
behavioural assumption beyond the term-structure model. Relative PPP is a *modelling
choice*: it holds poorly at short horizons and is defensible over the decades this
model spans, but it is an assumption and is presented as one.

**No uncovered parity is claimed.** The model does not assert that spot rates respond
to interest-rate differentials. Rate differentials enter only through the forward
points, where CIP makes them an identity. This is a deliberate restraint: a UIP channel
would have produced much larger spot moves on far weaker foundations.

**Amplification compounds upstream uncertainty.** By §4.1 a five-year forward
multiplies the rate differential by $4.53$. Every uncertainty in the transition shock,
the damage function and the Taylor rule is therefore magnified several-fold in the FX
output. Combined with the linearity of the transition channel in the carbon price, the
double-digit currency moves under ambitious scenarios should be read as an ordering and
an upper bound rather than as forecasts.

**A single mean-reversion parameter sets every currency's tenor profile.** Since
$B(\tau)$ depends only on $a = 0.04$, the term structure of forward points is identical
across all fourteen currencies. Region-specific calibration would change the relative
weighting of short- and long-dated forwards.

**Coverage is the dominant spot driver and is weakly grounded.** Equation (1) shows the
spot channel reduces to a coverage differential under uniform prices, making
$\Omega_r$ — an observed but coarse policy statistic, held static in the base case —
the sole determinant of the sign of every spot move.

**Structural regions have no exchange rate.** Russia and the four aggregates propagate
shocks into every other region's result but receive no currency of their own, so the
model is silent on precisely the economies where climate-driven currency stress might
be most severe.

**No FX volatility, and no level.** The model produces displacements of log exchange
rates, not stressed levels, and says nothing about the volatility of the currency pair.
Absolute stressed FX levels would require observed spot rates and both curves as an
additional input.

---

### References

Berrahoui, M., C. Kenyon, A. Macrina and G. Nathanael (2025). *Simple climate stress
testing: an ensemble framework.* Working paper.

Hull, J. and A. White (1994). Numerical procedures for implementing term structure
models I: single-factor models. *Journal of Derivatives* 2(1), 7–16.

Sarno, L. and M. P. Taylor (2002). *The Economics of Exchange Rates.* Cambridge
University Press.
