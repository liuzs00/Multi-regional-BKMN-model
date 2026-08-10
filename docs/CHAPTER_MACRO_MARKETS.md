# Macro-Financial Transmission: Inflation, Interest Rates and Market Prices

## 1. Purpose and role in the model

The two preceding chapters deliver a shock to sector value added: a carbon charge
propagated through the multi-regional Leontief dual, and a temperature-driven damage
allocated by vulnerability. Neither is yet a financial quantity. This chapter
implements the four remaining links of the ensemble — §2.6 to §2.9 of Berrahoui,
Kenyon, Macrina and Nathanael (2025) — which convert those real-economy shocks into
prices that a risk function can act on.

The chain is deliberately shallow, and each link is a single, standard, published
relationship:

$$\underbrace{\Delta \mathrm{XCE}}_{\text{carbon price}} \;\to\; \underbrace{\Delta \Pi}_{\S2.6}
\;\;\Big\}\;\to\; \underbrace{\Delta r}_{\S2.7\ \text{Taylor}} \;\to\; \underbrace{\Delta R(t,T)}_{\S2.8\ \text{Hull–White}}
\qquad
\underbrace{\Delta Y}_{\text{GDP shock}} \;\to\; \underbrace{\Delta S/S}_{\S2.9\ \text{equity}}$$

with the GDP shock $\Delta Y$ entering the Taylor rule alongside inflation. The
shallowness is a design property inherited from the paper, whose objection to
policy-level integrated assessment models is that they are too complex to audit. Every
relationship below can be written in one line and its parameters traced to a citation.

Two things change relative to the single-region original. First, every quantity
acquires a region index: each region has its own carbon price, its own inflation
response, its own policy rule and its own equity market, so the chapter produces
twenty parallel transmission chains rather than one. Second, the equity elasticity is
**calibrated per region** rather than borrowed from the FTSE 100. The credit channel
is not implemented, for reasons given in §5.2.

Implementation: `bkmn/macro.py` (§2.6–2.7), `bkmn/rates.py` (§2.8), `bkmn/equity.py`
(§2.9).

---

## 2. Inflation (§2.6)

### 2.1 The relationship

The paper takes its inflation response from Moessner (2022), who estimates across
emissions-trading jurisdictions that a $\$10$ per tonne rise in the carbon price
raises headline inflation by $0.08$ percentage points. As a coefficient,

$$k \;=\; \frac{0.08\,\%}{\$10/\mathrm{t}} \;=\; 8\times 10^{-5}
\quad\text{(fraction of inflation) per }\$1/\mathrm{t}.$$

The annual inflation deviation in region $r$ at year $t$ is that coefficient applied
to the year's carbon-price increment, scaled by the fraction of the region's
emissions the price actually reaches:

$$\boxed{\;\Delta\Pi_r(t) \;=\; k\,\big[\mathrm{XCE}_r(t)-\mathrm{XCE}_r(t-1)\big]\,
\Omega^{\mathrm{XCE}}_r\;}\tag{2.6a}$$

This is a deviation in the inflation **rate**, carried as a fraction throughout
(multiply by $10^{4}$ for basis points). Implementation: `macro.inflation_dev`.

The scope factor $\Omega^{\mathrm{XCE}}_r\in[0,1]$ is not decorative. Moessner's
coefficient is identified on marginal ETS prices in jurisdictions that operate a
carbon market; applied unscaled to a region pricing none of its emissions it would
attribute inflation to a policy not in force. §2.6's own text is explicit that
inflation increases "must be understood with respect to the scope of carbon pricing".

### 2.2 Units

Two conversions sit between the scenario file and $k$, and both change the magnitude.

| | |
|---|---|
| NGFS `Price\|Carbon` is quoted in **US\$2010/t CO₂** | rescaled by the US CPI-U ratio $292.655/218.056 = 1.342$ to **US\$2022/t**, matching the ICIO's current-2022-USD world (`scenarios.USD2010_TO_USD2022`) |
| Scenario data arrives on a five-year grid | linearly interpolated to annual (paper Table 17), so within a segment $\mathrm{XCE}(t)-\mathrm{XCE}(t-1)$ is one fifth of the grid step |

Skipping the deflator would understate every inflation figure by a factor of 1.342.

**A third conversion is unresolved, and it is the largest of the three.** The
paper writes the Moessner relation with a dollar input, but its own printed
results are only reproduced if $k$ is applied to the **sterling** carbon price:
$8\times10^{-5}\times \pounds 11.45 \to 9.2$ bp against a printed 9 bp, where the
dollar price of \$15.36 would give 12.3 bp. The single-region reproduction
established this against every horizon of the paper's inflation row.

We apply $k$ to a **US-dollar** price, because USD is this model's numéraire. If
the paper's calibration is the correct reading of Moessner, our inflation channel
is overstated by the GBP/USD rate, **1.341×**.

The consequence is not confined to the inflation row, and it is worth being
precise about what it does and does not touch, because a common factor on $k$ is
easy to wave away:

| quantity | effect of rescaling $k$ by $1/1.341$ |
|---|---|
| $\Delta\Pi$, cumulative $\Pi$ | scaled by 0.746 |
| **spot FX** | **scaled by 0.746** — it does *not* cancel |
| ratios between currencies, and their ranking | **unchanged** |
| the policy rate | changes *non*-proportionally: only the $\phi_\Pi\Delta\Pi$ term moves, not $\phi_Y\Omega$ |

Spot FX is a *difference* of two cumulative inflations, and a common factor
factors out of a difference rather than cancelling in it:
$c\,a - c\,b = c\,(a-b)$. So every spot move in this model would shrink by a
quarter — USD/EUR at 2040 under Net Zero from $-1.95\,\%$ to $-1.46\,\%$ — while
the cross-section, which is what §2 of [FX_REPORT.md](FX_REPORT.md) interprets,
would be untouched. EU27's 2030 policy rate would deepen from $-16.7$ to
$-21.1$ bp, because removing an inflation offset leaves the damage term exposed.

This is recorded rather than resolved: settling it needs Moessner's own units,
which we have not verified independently, and the choice is registered in
[PAPER_AUDIT.md](PAPER_AUDIT.md) §23.

### 2.3 From rate to level — the quantity that reaches FX

(2.6a) is a rate. Every downstream use in this model — relative PPP for spot FX
above all — needs the price **level**. Because $\Omega^{\mathrm{XCE}}_r$ is held
constant in $t$, the annual deviations telescope:

$$\sum_{s=t_0+1}^{t}\Delta\Pi_r(s)
\;=\; k\,\Omega^{\mathrm{XCE}}_r\sum_{s=t_0+1}^{t}\big[\mathrm{XCE}_r(s)-\mathrm{XCE}_r(s-1)\big]
\;=\; \boxed{\;k\,\Omega^{\mathrm{XCE}}_r\big[\mathrm{XCE}_r(t)-\mathrm{XCE}_r(t_0)\big]\;}\tag{2.6b}$$

with $t_0 = 2022$. Two consequences follow, and both are load-bearing.

**The telescoping is a property of constant scope.** Let $\Omega$ vary with $t$
(§2.5) and the product no longer collapses; the cumulative term must then be summed
year by year. `run_extensions.chain` branches on exactly this, and the two forms
disagree whenever coverage moves.

**The base-year price is zero.** In NGFS Phase 5 the carbon price is $0$ at both
2020 and 2025 in every scenario, so $\mathrm{XCE}_r(t_0)=0$ and (2.6b) collapses
further to

$$\mathrm{cum}\Pi_r(t) \;=\; k\,\Omega^{\mathrm{XCE}}_r\,\mathrm{XCE}_r(t).\tag{2.6c}$$

Twenty regions map onto only six carbon-price paths — the five NGFS R5 zones plus a
blended World path for the residual — so $\mathrm{XCE}_r(t)$ is compressed across the
cross-section. At 2040 under Net Zero the fourteen FX regions take five distinct
values spanning \$417.06 (MAF) to \$445.84 (REF), a **6.9 %** spread, against a scope
vector running from 0 to 0.821. By (2.6c) the cumulative-inflation vector is therefore
close to a rescaling of the scope vector: the correlation between them across the
fourteen FX regions is $0.9990$ at 2040 and $0.9997$ at 2045
([FX_RESULTS](FX_RESULTS.md) §3). That is a data-granularity limit of the R5 grid,
not a modelling choice.

The compression is scenario-dependent and should not be over-generalised. Under
Current Policies the same cross-section at 2040 runs from \$1.53 (OECD) to \$15.88
(LAM) — an order of magnitude — so there the carbon price does discriminate between
regions and scope is not the whole story.

### 2.4 Worked example

EU27 under Net Zero 2050, $\Omega^{\mathrm{XCE}}_{\mathrm{EU27}} = 0.645$.
Interpolating between $\mathrm{XCE}(2025)=0$ and $\mathrm{XCE}(2030)=\$337.80$ gives
$\mathrm{XCE}(2029)=\$270.24$, an increment of \$67.56. By (2.6a),

$$\Delta\Pi_{\mathrm{EU27}}(2030) \;=\; 8\times10^{-5}\times 67.56\times 0.645
\;=\; 3.4861\times10^{-3} \;=\; \mathbf{34.86\ bp},$$

against the model's $34.861$ bp. At 2040, $\mathrm{XCE}=\$440.43$, so by (2.6c) the
level is $8\times10^{-5}\times0.645\times440.43 = \mathbf{2.2726\,\%}$. The United
States faces the same carbon price on $\Omega = 0.091$ and reaches only
$0.3206\,\%$; relative PPP turns the $1.9520$ pp differential into a $1.9520\,\%$
appreciation of the dollar against the euro, reproducing `out_fx_spot_ppp.csv`
($-1.95199$) to five figures.

### 2.5 The coverage assumption, and the artefact it leaves

Scope is held at its **observed 2025 value** throughout, from OWID coverage data
(`data/scope/carbon_scope_20R.csv`):

| Region | KOR | NOR | JPN | EU27 | AUS | SGP | CHN | GBR | USA | IND, TUR, RUS |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| $\Omega^{\mathrm{XCE}}_{2025}$ | 0.821 | 0.744 | 0.671 | 0.645 | 0.639 | 0.640 | 0.467 | 0.326 | 0.091 | **0.000** |

The paper does not settle this, and the choice has a visible cost. Under Net Zero
2050 the model charges India \$420/t in the transition channel at 2040 while
reporting an Indian carbon-inflation deviation of **exactly 0.0 bp** — the scenario
asserts a high Indian carbon price and no Indian carbon pricing at the same time.
**The base-case results carry that inconsistency; it is not repaired**, and by (2.6c)
it propagates: India and Türkiye have identical spot FX paths, each equal to minus
the EU's own cumulative inflation.

The alternative is the reading §2.6 gestures at when it notes that "increases in
scope of carbon pricing may have similar effects" to increases in price. Coverage is
tied to the scenario's own stringency signal, the carbon price:

$$\Omega^{\mathrm{XCE}}_r(t) \;=\; \Omega_{r,2025} + \big(1-\Omega_{r,2025}\big)
\min\!\left(1,\ \frac{\mathrm{XCE}_r(t)}{\mathrm{XCE}^{\text{full}}}\right),
\qquad \mathrm{XCE}^{\text{full}} = \$100/\mathrm{t},$$

monotone, bounded in $[\Omega_{2025},1]$, and reducing to the static case where the
price does not rise. Current Policies (\$1.53–\$15.88/t at 2040) leaves coverage
largely unchanged; Net Zero (above \$300/t in every zone from 2030) takes it to full.

It is implemented (`macro.scope_at`) but reported as a **sensitivity only**
(`out_sens_fx_*_dynscope.csv`), because $\mathrm{XCE}^{\text{full}}$ is asserted
rather than estimated. Holding the static case as the headline keeps the one free
parameter out of the main results and makes the two directly comparable.

### 2.6 Departures from the paper

| | Paper §2.6 | Here | Why |
|---|---|---|---|
| Driver | $\Delta\Pi \propto \Delta\mathrm{XCE}\cdot\Delta\Omega_{\mathrm{XCE}}$ — a product of two *changes* | $\Delta\mathrm{XCE}\cdot\Omega$, scope as a **level** | the literal form is second-order and reads as a typo; the surrounding text supports a level, as does the single-region reference implementation |
| Second equation | an inflation **term structure**, $\Pi(t,T,T{+}1)=\Pi^{\text{market}}+\int\Delta\Pi\,f\,ds$, anchored on observed inflation curves | the annual deviation only | we report shifts rather than levels throughout, so no market curve is loaded (deviation register items 9–10) |
| Index | a single economy | one relationship per region, $r=1,\dots,20$ | the multi-regional extension |

---

## 3. The policy rate: the Taylor rule (§2.7)

Central banks are assumed to respond to the climate shock through a Taylor rule
(Taylor, 2007). In levels,

$$r^{\text{Policy}}(t) = R^{*}(t)+\Pi^{*}(t)+\phi_{\Pi}\big(\Pi(t)-\Pi^{*}(t)\big)+\phi_{Y}\big(Y(t)-Y^{*}(t)\big),$$

but the model requires only the *deviation* induced by the climate shock. Differencing
the rule before and after, the equilibrium real rate and the inflation target drop
out, leaving

$$\boxed{\;\Delta r_r(t) \;=\; \phi_{\Pi}\,\Delta\Pi_r(t) \;+\; \phi_{Y}\,\Delta Y_r(t)\;}
\qquad \phi_{\Pi}=\phi_{Y}=0.5 ,$$

with $\Delta\Pi_r$ from §2.6 and $\Delta Y_r$ the total GDP shock — transition plus
physical — from the two preceding chapters. The weights are the paper's, and are the
conventional values in the Taylor-rule literature.

That the unobservable terms cancel is worth noting: the model never needs to estimate
a neutral rate or an inflation target, only the *change* in the gaps. This is the same
device used in §2.8 below and is what allows the chain to be calibrated to observed
market curves rather than to a structural macro model.

**The output gap dominates.** Because carbon-driven inflation deviations are of order
single-digit basis points while GDP shocks are of order whole percentage points, the
second term is larger by roughly two orders of magnitude. Taking the EU27 under Net
Zero at 2040, with $\Delta\Pi = +4.9$ bp and $\Delta Y = -2.70\%$:

$$\Delta r \;=\; 0.5\times(+4.9\ \text{bp}) \;+\; 0.5\times(-270.0\ \text{bp}) \;=\; -132.6\ \text{bp},$$

against the model's computed $-132.3$ bp. The inflation channel contributes $2.5$ bp
of a $132$ bp cut. Two consequences follow. Climate stress in this model is
**disinflationary in net effect** — the demand destruction from lost output swamps the
cost-push from carbon pricing, so policy rates fall rather than rise. And the results
are correspondingly insensitive to the scope construction of §2.2, which affects only
the smaller term.

---

## 4. The term structure: Hull–White (§2.8)

### 4.1 From the short rate to the curve

A policy-rate shock is a statement about the very short end. Valuing a banking or
trading book requires the whole curve, and §2.8 obtains it by assuming a one-factor
Hull–White short-rate model (Hull and White, 1994) calibrated to the observed term
structure:

$$dr(t) = \big(\theta(t)-a\,r(t)\big)dt + \sigma\,dW(t),$$

with $\theta(t)$ chosen to fit today's curve exactly. Because the model is Markov in
one factor, knowing the future short rate determines the entire future zero-coupon
curve.

> **Proposition 2 (Berrahoui et al., §2.8).** Given a short-rate shift $\Delta r(t)$
> and an otherwise unchanged Hull–White model, the zero-coupon rate shift at maturity
> $T$ is
> $$\Delta R(t,T) \;=\; \frac{B(t,T)}{T-t}\,\Delta r(t),
> \qquad B(t,T) = \frac{1-e^{-a(T-t)}}{a}.$$

*Proof.* In the Hull–White model the zero-coupon bond price is affine in the short
rate, $P(t,T) = A(t,T)e^{-B(t,T)r(t)}$, with $A$ and $B$ deterministic. The
zero-coupon rate is therefore

$$R(t,T) = -\frac{\ln P(t,T)}{T-t} = \frac{B(t,T)\,r(t)-\ln A(t,T)}{T-t},$$

which is **affine in $r(t)$** with slope $B(t,T)/(T-t)$. Differencing two states of
the world that share the same $A$ and $B$,

$$\Delta R(t,T) = \frac{B(t,T)}{T-t}\,\Delta r(t). \qquad\blacksquare$$

Because $R$ is affine rather than merely differentiable in $r$, the relation is
**exact for a shift of any size**, not a first-order approximation — a point worth
making since the paper obtains it by differentiation, which understates the result.

### 4.2 What the proposition implies

Two features do substantial work in the results.

**The shift is independent of volatility.** $\sigma$ does not appear. The transmission
of a policy shock along the curve is governed entirely by the mean-reversion speed
$a$, so the model requires no swaption calibration. This is fortunate, since $\sigma$
is the parameter the model would otherwise have to source from options markets for
twenty currencies.

**The decay profile is universal.** The factor $B(\tau)/\tau$ depends on nothing but
the tenor $\tau=T-t$ and $a$, so with $a=0.04$ (Table 17) every region and every
scenario shares the same term-structure shape:

| Tenor $\tau$ | 1D | 6M | 1Y | 5Y | 10Y | 20Y |
|---|--:|--:|--:|--:|--:|--:|
| $B(\tau)/\tau$ | 0.9999 | 0.9901 | 0.9803 | 0.9063 | 0.8242 | **0.6883** |

The limits behave: $B(\tau)/\tau\to1$ as $\tau\to0$, recovering the short-rate shift,
and decays monotonically thereafter. A twenty-year rate therefore moves $68.8\%$ as
much as the overnight rate — for every region, every scenario and every horizon. The
climate scenario determines the *level* of the shift; the mean-reversion parameter
alone determines its *shape*.

Applying this to the computed short-rate shifts, at 2040 under Net Zero (bp):

| Region | 1D | 6M | 1Y | 5Y | 10Y | 20Y |
|---|--:|--:|--:|--:|--:|--:|
| EU27 | $-132$ | $-131$ | $-130$ | $-120$ | $-109$ | $-91$ |
| USA | $-101$ | $-100$ | $-99$ | $-91$ | $-83$ | $-69$ |
| India | $-522$ | $-517$ | $-511$ | $-473$ | $-430$ | $-359$ |
| Norway | $-47$ | $-47$ | $-46$ | $-43$ | $-39$ | $-33$ |

This is the same qualitative shape as the paper's Table 11 — largest at the short end,
roughly 30 % smaller at twenty years — reproduced across twenty regions.

---

## 5. Equity and credit (§2.9)

### 5.1 Equity

Section 2.9 links market prices to value added by a log-linear regression,

$$\log S_j = \beta_{0,j} + \beta_{1,j}\log \mathrm{GVA}_j
\qquad\Longrightarrow\qquad
\frac{\Delta S_j}{S_j} = \beta_{1,j}\,\frac{\Delta \mathrm{GVA}_j}{\mathrm{GVA}_j},$$

so that the GDP shock enters as a systematic factor and $\beta_1$ is an elasticity of
the index to output. The intercept is irrelevant to the shock, which is why the
relationship survives the weak fits discussed below.

The single-region paper estimates one such elasticity, for the FTSE 100 against UK
GVA, obtaining $\beta_1 = 2.00$ with $R^{2}=74\%$. Applying a UK elasticity to twenty
heterogeneous equity markets would be indefensible, so $\beta_1$ is **estimated per
region**, regressing the log of each region's headline index on the log of its GDP,
annually over 2000–2023, using freely available sources. The results:

| Region | $\beta_1$ | $R^2$ | | Region | $\beta_1$ | $R^2$ |
|---|--:|--:|---|---|--:|--:|
| Indonesia | 1.36 | 0.98 | | China | 0.26 | 0.51 |
| India | 1.38 | 0.97 | | UK | 0.55 | 0.36 |
| Korea | 1.20 | 0.96 | | EU27 | 0.80 | 0.20 |
| USA | 1.59 | 0.83 | | Norway | 0.66 | 0.12 |
| Canada | 0.83 | 0.81 | | **Japan** | **2.00** | — (proxy) |
| Turkey | 1.89 | 0.73 | | | | |
| Singapore | 0.39 | 0.73 | | | | |
| Australia | 0.44 | 0.67 | | | | |

Twelve of thirteen regions with an available index series produce a usable fit.
**Japan does not**, and instructively so: its fitted slope is *negative*, the
statistical signature of the "lost decades" — an index that moved sideways for two
decades while nominal GDP grew. Rather than admit a negative elasticity, which would
make Japanese equities rise on a GDP contraction, the estimate is rejected by a
plausibility band $\beta_1\in[0.2,6.0]$ and the paper's FTSE value substituted.
Regions with no free index series (Chile, Kazakhstan) and the aggregate regions
likewise take the proxy.

The fits are weak for several regions, with $R^2$ as low as $0.12$ for Norway. This
is disclosed rather than concealed, and it is not out of line with the source: the
paper's own Table 9 reports $R^2$ below $30\%$ for most CDS sectors. The elasticity
should be read as a transmission convention with an empirical anchor, not as a
precisely estimated structural parameter.

### 5.2 Credit: why the CDS channel is not implemented

Section 2.9 applies the same log-linear form to CDS spreads, and §2.10 extends it to
IFRS 9 expected credit losses. Neither is implemented here, and the reason is data
access rather than method: the paper's Table 9 CDS regressions are estimated on
licensed sector CDS histories (Markit and equivalents), which were not available for
this work and for which no free substitute exists at sector granularity across twenty
regions.

The omission is a real limitation, since credit is the channel most directly relevant
to a banking book. It is worth recording that the machinery would transfer unchanged —
the model already produces the sector-level $\Delta\mathrm{GVA}/\mathrm{GVA}$ that the
CDS regression consumes, so the missing element is exclusively the calibration data.

---

## 6. Results

Bringing the chain together at 2040 under Net Zero 2050, with $\phi = 0.5$:

| Region | $\Delta Y$ (%) | $\Delta\Pi$ (bp) | $\Delta r$ (bp) | $\Delta R_{20Y}$ (bp) | $\Delta S/S$ (%) |
|---|--:|--:|--:|--:|--:|
| China | $-11.46$ | $+4.9$ | $-570$ | $-393$ | $-3.02$ |
| India | $-10.43$ | $0.0$ | $-522$ | $-359$ | $-14.40$ |
| Japan | $-3.55$ | $+5.1$ | $-175$ | $-121$ | $-7.11$ |
| EU27 | $-2.70$ | $+4.9$ | $-132$ | $-91$ | $-2.16$ |
| USA | $-2.02$ | $+0.7$ | $-101$ | $-69$ | $-3.21$ |
| UK | $-1.51$ | $+2.5$ | $-74$ | $-51$ | $-0.83$ |
| Norway | $-1.00$ | $+5.7$ | $-47$ | $-33$ | $-0.66$ |

Three features are worth drawing out.

**Rates fall everywhere.** No region experiences a policy tightening, because the
output-gap term dominates the inflation term throughout. A carbon price is, in this
model's transmission, a contractionary shock before it is an inflationary one.

**Equity does not rank with GDP.** India suffers a smaller GDP shock than China
($-10.4\%$ against $-11.5\%$) yet a far larger equity move ($-14.4\%$ against
$-3.0\%$), because the estimated elasticities differ by a factor of five ($1.38$
against $0.26$). Whether the Chinese equity index is genuinely that insensitive to
domestic output, or whether the low $R^2$ of $0.51$ reflects an index driven by other
forces, is a calibration question the model cannot settle — and it is a reminder that
this last link carries the most estimation risk of the chain.

**Curve effects are large in absolute terms.** A $-359$ bp shift in the Indian
twenty-year rate is a repricing of a different order from the fractions of a
percentage point typical of physical damage. Where climate stress becomes financially
material in this model, it does so through the rates channel.

---

## 7. Assumptions and limitations

**A single inflation coefficient, applied everywhere.** Moessner's $0.08$ pp per
$\$10$ is estimated on European ETS data and is applied to all twenty regions, scaled
only by coverage. Pass-through of carbon costs into consumer prices plausibly differs
with market structure and monetary regime.

**Coverage expansion is asserted.** The threshold $\mathrm{XCE}^{\text{full}} = \$100$
per tonne has no empirical basis; it is a bounded, monotone device for avoiding the
contradiction of §2.2 and is reported as a sensitivity.

**A common Taylor rule.** All regions are given $\phi_{\Pi}=\phi_{Y}=0.5$ and are
assumed to follow the rule mechanically. Regions with pegged exchange rates or
managed monetary policy do not conduct policy this way, and for them the rate response
should be read as indicative. The rule also omits the effective lower bound, so large
computed cuts may be unattainable from a low starting level.

**Mean reversion is fixed and uncalibrated.** $a = 0.04$ is the paper's value, applied
to all twenty curves. Since $B(\tau)/\tau$ depends only on $a$, this single number sets
the term-structure shape everywhere; a region-specific calibration to swaption or bond
data would be a direct improvement.

**Equity elasticities are weakly identified.** Several fits have low $R^2$, one region
required a proxy, and the aggregate regions have no market of their own. The ordering
across regions is more reliable than the magnitudes.

**No credit channel.** CDS and IFRS 9 are absent for want of licensed data, leaving
the banking-book application incomplete.

**The chain is one-directional and contemporaneous.** Rates do not feed back into
output, equity does not feed back into investment, and every link is instantaneous.
The model is a comparative-statics stress calculator, not a dynamic macro model, and
should be read as answering "what repricing does this scenario imply?" rather than
"what will happen?".

---

### References

Berrahoui, M., C. Kenyon, A. Macrina and G. Nathanael (2025). *Simple climate stress
testing: an ensemble framework.* Working paper.

Hull, J. and A. White (1994). Numerical procedures for implementing term structure
models I: single-factor models. *Journal of Derivatives* 2(1), 7–16.

Moessner, R. (2022). *Effects of carbon pricing on inflation.* CESifo Working Paper.

Taylor, J. B. (2007). *Monetary Policy Rules.* University of Chicago Press.

Taylor, J. B. and J. C. Williams (2010). Simple and robust rules for monetary policy.
In *Handbook of Monetary Economics*, vol. 3, 829–859. Elsevier.
