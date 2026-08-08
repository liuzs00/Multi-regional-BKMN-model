# Chapter N — The Bayesian Scenario Mixture

*Draft chapter for the dissertation. Renumber to fit the final structure; suggested
placement is after the channel chapters (transition, physical, rates/FX) and before
the results chapter, since the mixture consumes their per-scenario outputs.*

---

## N.1 Motivation: the problem of scenario selection

Every climate stress-testing exercise must eventually answer a question that climate
science cannot: *which* future are we stressing against? The scenario providers are
explicit that they will not answer it. The NGFS states that its scenarios are not
forecasts and publishes no probabilities over them; the IPCC's SSP–RCP framework is
likewise a set of internally consistent storylines rather than a distribution. The
modeller is therefore handed a menu and no prices.

The conventional response in industry practice is to select one scenario — typically
the regulator's — and report its consequences as *the* stress. This has two defects.
The first is presentational: a single-scenario result invites the reader to treat a
conditional statement ("if Net Zero 2050 occurs, the Indian rupee moves by −25.8%")
as an unconditional one. The second is analytical, and more serious in a
multi-channel model such as this one. As Chapter [physical] shows, the scenario
ranking *reverses* between channels: ambitious mitigation maximises transition cost
and minimises physical damage, while Current Policies does the opposite. A
transition-only reading of a single ambitious scenario therefore makes decarbonisation
look unambiguously the most damaging future available — an artefact of the selection,
not a finding.

The BKMN paper's response, which this chapter implements and extends, is to refuse the
selection. Every scenario receives a probability, and every model output is reported
as a probability-weighted expectation across the full set (paper §2.2 and §3.1.5,
Eq. 20–21):

$$\mathbb{E}[\Delta X] \;=\; \sum_{s\in\mathcal{S}} p_s\, \Delta X_s .$$

Two features of this construction deserve emphasis at the outset.

**It is strictly a post-processing layer.** The per-scenario results $\Delta X_s$ are
computed once by the channel models and are never modified here. The mixture adds
weights and aggregates; it does not re-simulate. This is a deliberate design property
inherited from the paper, whose central claim is that policy-level integrated
assessment models are too expensive to re-run for routine risk work. A degenerate
prior — all mass on one scenario — must therefore reproduce that scenario's table
exactly, and this is enforced as a numerical gate (§N.6).

**It separates two distinct kinds of uncertainty.** The uncertainty *within* a
scenario (what the model does, given a carbon-price and temperature path) is handled
by the channel models and by the volatility band of Chapter [volatility]. The
uncertainty *across* scenarios (which path we are on) is handled here. Conflating the
two is a common error in the literature; keeping them separate lets us make the
sharper statement developed in §N.5.2 — that under a defensible prior, transition risk
is a tail phenomenon rather than an expectation.

### N.1.1 Why NGFS rather than SSP–RCP

The paper works in the IPCC's SSP–RCP coordinates, whereas this implementation uses
the seven NGFS Phase 5 narratives, and the substitution should be justified rather
than assumed. Three considerations drive it. First, the model's purpose is
supervisory stress testing, and NGFS is the scenario set that central banks and
supervisors actually mandate for that purpose; results expressed in SSP–RCP
coordinates would require translation before a risk function could use them. Second,
and decisively for a *multi-region* model, NGFS publishes carbon-price paths
**disaggregated by R5 region** for every narrative — precisely the input the
transition channel requires when it must price policy across twenty economies rather
than one, whereas the SSP marker runs were designed principally to drive climate
models. Third, the NGFS narratives are organised along the axis to which this model
is sensitive — policy timing, ambition, and international coordination — rather than
socioeconomic storyline crossed with radiative forcing.

The substitution is also sanctioned by the paper itself, whose Table 17 anticipates
it: the model "could be easily adjusted to allow transition between story lines
within NGFS, assuming the later provides the required data like Carbon price, GDP and
Temperature across time." Nor is it as large a departure as it first appears, since
NGFS scenarios are themselves built on SSP2 socioeconomics (paper §1). In effect the
socioeconomic dimension is held fixed at the same storyline the paper's own prior
weights at 90 %, and only the policy dimension varies. That observation matters
beyond provenance: it is precisely *why* the NGFS narratives are flat rather than
paired, and hence why the transition matrix developed in §N.4.2 is dense rather than
block diagonal.

The implementation is `bkmn/mixture.py`, with scenario coordinates supplied by
`bkmn/scenarios.py::Scenarios.coords()`.

---

## N.2 The Dirichlet–categorical framework

### N.2.1 Two layers of uncertainty

The scenario set $\mathcal{S}$ contains the seven NGFS Phase 5 narratives: Net Zero
2050, Below 2 °C, Low demand, Delayed transition, Nationally Determined Contributions
(NDCs), Fragmented World, and Current Policies. "Which scenario obtains" is a
categorical random variable over $|\mathcal{S}| = 7$ outcomes with probability vector
$\mathbf{p}$ lying on the 6-simplex.

We do not, however, know $\mathbf{p}$ either. The natural Bayesian move is to place a
distribution over it, and the standard choice — used by the paper and retained here —
is the Dirichlet:

$$\mathbf{p} \sim \mathrm{Dir}(\boldsymbol{\alpha}), \qquad
\boldsymbol{\alpha} = (\alpha_1,\dots,\alpha_7), \quad \alpha_s > 0 .$$

The parameters $\alpha_s$ have a natural reading as **pseudo-counts**: setting
$\boldsymbol{\alpha} = (2,2,\dots,2)$ encodes a belief equivalent to having previously
observed two pieces of evidence in favour of each narrative. This interpretation is
what makes the framework operational for a risk function, because it lets a
qualitative narrative judgment ("I find delayed transition twice as plausible as net
zero") be written down as a number and then updated by evidence.

We report the Dirichlet **mean** as the working probability vector:

$$p_s \;=\; \frac{\alpha_s}{\sum_{k}\alpha_k} \qquad \text{(\texttt{mixture.weights})} .$$

Using the mean rather than sampling from the Dirichlet is a simplification, and it is
the paper's own (§2.2 states "with similar expected categorical probabilities... and
we use these"). It discards the second-order uncertainty — the variance of
$\mathbf{p}$ itself — which would matter if we wished to report confidence intervals
*on the weights*. For expectations of the form $\mathbb{E}[\Delta X]$ the mean is
sufficient, since expectation is linear in $\mathbf{p}$.

### N.2.2 Conjugacy and the update rule

The Dirichlet is the conjugate prior of the categorical distribution. Consequently,
updating on observed evidence requires no integration — it is addition:

$$\underbrace{\mathrm{Dir}(\boldsymbol{\alpha})}_{\text{prior}}
\;+\;
\underbrace{\mathbf{c}}_{\text{observed counts}}
\;\longrightarrow\;
\underbrace{\mathrm{Dir}(\boldsymbol{\alpha} + \mathbf{c})}_{\text{posterior}} .$$

This is the analytical property that makes the scheme attractive for practical risk
work: a bank can maintain a prior, attribute observed policy events to narratives as
they occur, and obtain a posterior in closed form without re-running anything. The
paper describes exactly this workflow — picking a date for the prior and counting
events up to the present (§2.2) — and notes that it also provides a natural route to
representing tipping points, since a tipping event is simply a large count in favour
of the high-warming narratives.

### N.2.3 Prior strength versus prior direction: the $\sum\alpha$ normalisation

A subtlety arises that the paper does not address, and resolving it required a
modelling decision.

The Dirichlet concentration $\sum_k \alpha_k$ carries information distinct from the
implied probabilities. The probabilities depend only on the *proportions* of
$\boldsymbol{\alpha}$; the concentration governs how much evidence is required to
overturn the prior. A prior with $\sum\alpha = 3$ is displaced substantially by three
observed events, whereas one with $\sum\alpha = 300$ is barely moved by them. In
short: **proportions encode the direction of belief, concentration encodes its
stiffness.**

If several priors are to be compared — as they are here — and they carry different
concentrations, then any difference in their posteriors after an update confounds the
two. To prevent this, all priors in this work are rescaled to a common concentration

$$\sum_{s} \alpha_s = \alpha_0 = 14 ,$$

so that switching prior changes the direction of belief and never its strength. The
value 14 is itself arbitrary (it is twice the number of scenarios, i.e. a nominal two
pseudo-observations per narrative); what matters is that it is *common*. Because
rescaling leaves proportions unchanged, the static expectations are invariant to this
choice — verified numerically, with expected-FX tables moving by at most
$5\times10^{-15}$ percentage points. The normalisation therefore costs nothing and
buys interpretability under the event-count update of §N.3.4.

---

## N.3 Prior specification

Four priors are carried through the analysis. Their provenance differs sharply, and
being explicit about this is a matter of research integrity rather than presentation:
one is anchored on published assessments and is citable; one is the conventional
uninformative choice; two are asserted by the author as illustrative bookends.

| Prior | Provenance | Belief encoded |
|---|---|---|
| `consensus` | **Citable** — UNEP EGR 2025 / CAT COP30 2025 | *"We are on the published current-policy trajectory"* |
| `uniform` | Conventional (uninformative) | *"I have no view"* |
| `policy-sceptic` | **Asserted** | *"Policy will disappoint"* |
| `ambition` | **Asserted** | *"The transition actually happens"* |

The resulting probabilities are:

| Scenario | `consensus` | `uniform` | `policy-sceptic` | `ambition` |
|---|--:|--:|--:|--:|
| Net Zero 2050 | 0.0 % | 14.3 % | 6.2 % | 23.5 % |
| Below 2 °C | 0.3 % | 14.3 % | 6.2 % | 23.5 % |
| Low demand | 0.0 % | 14.3 % | 6.2 % | 17.6 % |
| Delayed transition | 0.5 % | 14.3 % | 12.5 % | 11.8 % |
| NDCs | 6.7 % | 14.3 % | 25.0 % | 11.8 % |
| Fragmented World | 11.8 % | 14.3 % | 18.8 % | 5.9 % |
| Current Policies | **80.7 %** | 14.3 % | 25.0 % | 5.9 % |

### N.3.1 The `consensus` prior: construction from published warming assessments

The `consensus` prior is the methodological contribution of this section, and it is
built by transposing the paper's own construction into the NGFS setting.

The paper's procedure (§3.1.4) is: take an authoritative statement about where current
policy leads, identify the scenario that matches it, and concentrate the prior mass
there. Its authoritative statement is IPCC (2023) — that the world is on "a path
closer to SSP2 (Middle of the Road) combined with RCP4.5 or RCP6.0" — and it assigns
90 % of the mass to that pair.

That statement is expressed in SSP–RCP coordinates, which the NGFS narratives do not
possess. The transposition therefore requires a common currency, and the natural one
is **end-of-century warming**, which both the external assessments and the NGFS
scenarios report. Two current assessments are used:

| Source | Current policies | NDCs | Optimistic |
|---|--:|--:|--:|
| UNEP *Emissions Gap Report 2025* | **2.8 °C** | 2.3–2.5 °C | — |
| Climate Action Tracker, COP30 update (Nov 2025) | **≈2.6 °C** | 2.6 °C | 1.6 °C |

From these, the anchor is taken as the midpoint $\mu = 2.7\ ^\circ\mathrm{C}$ with
$\mathrm{sd} = 0.3\ ^\circ\mathrm{C}$ reflecting the spread across the two assessments
and their stated ranges. Prior weights are then Gaussian in each scenario's *own*
end-century warming $T_{2100,s}$:

$$\alpha_s \;\propto\; \exp\!\left(-\tfrac{1}{2}\left(\frac{T_{2100,s}-\mu}{\mathrm{sd}}\right)^{\!2}\right),
\qquad \sum_s \alpha_s = \alpha_0 .$$

Current Policies reaches $T_{2100} = 2.75\ ^\circ\mathrm{C}$, within 0.05 K of the
anchor, and consequently receives 80.7 % of the mass. That the result is concentrated
is not an artefact of the Gaussian form — it mirrors the paper's own 90 %, and it
reflects a genuine feature of the current evidence base, which is that the published
assessments agree closely with one another and point at one end of the NGFS range.

Two properties of this construction are worth defending explicitly. First, it is
*falsifiable and updatable*: when UNEP and CAT publish revised estimates, $\mu$ and
$\mathrm{sd}$ change and the prior changes with them, without any discretionary
re-weighting. Second, it is *auditable*: the reader can disagree with the anchor and
recompute, whereas a directly asserted weight vector offers no such handle.

**A mapping caveat must be recorded.** NGFS's own *NDCs* scenario reaches 2.03 °C,
whereas UNEP and CAT place full NDC implementation at 2.3–2.6 °C. The NGFS NDC
narrative is thus systematically more optimistic than the external assessments of the
same policy commitments. Part of the reason weight concentrates on Current Policies
rather than NDCs is this discrepancy in the underlying scenario design, not a
judgment about policy. Any reader taking the `consensus` weights at face value should
be aware that they partly encode a labelling difference between institutions.

### N.3.2 The uniform prior and the asserted bookends

`uniform` ($\alpha_s$ equal for all $s$) is the conventional uninformative choice and
requires no defence beyond the observation that it is the natural reference point
against which the informative priors are read.

`policy-sceptic` and `ambition` are **asserted by the author**. Their *directions*
follow narrative logic — mass placed on the low-ambition end (Current Policies, NDCs,
Fragmented World) and the high-ambition end (Net Zero, Below 2 °C, Low demand)
respectively — but their *magnitudes* are arbitrary round numbers chosen to produce a
visible spread. No external standard was available to borrow, because NGFS declines
to publish scenario probabilities as a matter of policy.

These two priors should therefore be read as illustrative bookends and never as
estimates. Their function in the analysis is to bracket: the spread of results across
all four priors is the honest measure of how much the prior choice matters, and it is
reported as such rather than any single prior being advanced as correct. This is the
least data-grounded input in the entire model, and the dissertation's limitations
section should say so plainly.

### N.3.3 Updating on observed events

The conjugate update of §N.2.2 is exposed through
`mixture.alphas(prior, counts=...)`. Counts are events that the user attributes to
narratives — the paper's own suggested workflow. For instance, three observed policy
rollbacks and one net-zero commitment since the prior date would be entered as

```python
counts = {"Current Policies": 3, "Net Zero 2050": 1}
```

Under this evidence the weight on Current Policies moves from 14.3 % to 27.8 % under
`uniform`, from 25.0 % to 36.1 % under `policy-sceptic`, and from 5.9 % to 21.2 %
under `ambition`. Because all priors share $\sum\alpha = 14$, the same evidence moves
each by a comparable amount — which is precisely the interpretability that the
normalisation of §N.2.3 was introduced to secure.

Attribution of real-world events to narratives is of course a judgment, and a
contestable one; the framework makes that judgment explicit and auditable rather than
eliminating it.

---

## N.4 Scenario drift: the transition matrix

### N.4.1 The paper's formulation

The mixture as described so far is static: the weights assigned at the base date apply
at every horizon. The paper observes that this is unrealistic, since "policy makers
can change, so it may be possible to move between scenarios" (§2.2), and introduces an
annual transition matrix (Eq. 1):

$$q(j,k) \;=\; \frac{\exp\!\big(-\lambda\, d(j,k)\big)}{\sum_{h}\exp\!\big(-\lambda\, d(j,h)\big)} .$$

This is a softmax over a distance $d$ between narratives: nearby scenarios are easy to
move between, distant ones are not, and the parameter $\lambda$ sets how sharply
distance is penalised. Weights are then propagated forward by repeated multiplication,

$$\mathbf{p}_T \;=\; \mathbf{p}_0\, Q^{\,T-t_0},$$

with $t_0 = 2022$ the base year of the model's calibration data.

### N.4.2 A structural difference from the paper: dense $7\times7$ versus block-diagonal $25\times25$

The paper's transition matrix is $25 \times 25$ over SSP–RCP *pairs*, and it is block
diagonal by construction. Transitions between RCP states are permitted; transitions
between SSP states are not (§2.2). The justification is substantive rather than
technical: an SSP is an immutable socioeconomic storyline — a description of how
society is organised — whereas an RCP is a mutable policy outcome. One can legislate
one's way from RCP6.0 to RCP4.5; one cannot legislate one's way from "Regional
Rivalry" to "Sustainability". The resulting matrix comprises five $5\times5$ blocks
with structurally zero off-diagonal blocks, i.e. 20 % density.

The NGFS narratives used here do not admit this factorisation. They are *flat*: each
is a single storyline bundling socioeconomics and policy together, with no
mutable × immutable product structure to exploit. The transition matrix is therefore a
**dense $7\times7$**, and implausible transitions are suppressed not by structural
zeros but by the distance metric producing *soft* zeros. The suppression is effective:
the annual probability of moving directly from Net Zero 2050 to Current Policies is
0.00012.

An attempt was made to recover a block structure by partitioning on "international
coordination" (cooperative versus fragmented narratives). It was tested and rejected:
NGFS Phase 5 contains only one fragmented narrative, so its block becomes absorbing —
once entered, never left — which is an artefact of scenario-set composition rather
than a feature of the world.

One property of Eq. 1 should be flagged before it is mistaken for a defect of the
present implementation. **The stationary distribution of $Q$ is not uniform**, because
an exponential kernel on a bounded set gives interior states more inflow than edge
states. This is inherent to the paper's specification: applying Eq. 1 to the paper's
own five RCP concentration levels yields a stationary distribution of
$[0.194, 0.222, 0.225, 0.204, 0.155]$, already non-uniform. Under the metric adopted
below, the isolated scenarios — Net Zero (0.089) and Current Policies (0.091) —
receive least stationary weight, which is at least an economically sensible reading:
the extremes are hard to reach and hard to sustain.

### N.4.3 The distance metric: the central methodological problem

Eq. 1 requires a distance $d(j,k)$, and the paper's choice is
$d(j,k) = |j-k|$ measured on **RCP concentration labels** (1.9, 2.6, 3.4, 4.5, 6.0
W m⁻²). This works because the label is a physical number that the scenario set itself
supplies: RCP4.5 is nearer to RCP6.0 than to RCP1.9 in a sense that requires no
modelling judgment.

**NGFS narratives carry no such number.** "Delayed transition" is not a quantity. A
distance therefore had to be constructed, and this is the single largest discretionary
choice in the chapter. Eq. 1 explicitly sanctions the construction — the distance "can
be generalized to include any function of RCP characteristics" — but sanctioning it
does not determine it.

The choice adopted is the **Euclidean distance in standardised
$(T_{2100},\, \mathrm{XCE}_{2050})$ space**: end-of-century warming and the 2050 carbon
price, the two characteristics that distinguish the narratives and that drive this
model's two channels. Formally, with $z$ denoting the $z$-scored coordinates,

$$d(j,k) \;=\; \lVert \mathbf{z}_j - \mathbf{z}_k \rVert_2 ,
\qquad
\mathbf{z}_s = \left(\frac{T_{2100,s}-\bar T}{\sigma_T},\ \frac{\mathrm{XCE}_{2050,s}-\overline{\mathrm{XCE}}}{\sigma_{\mathrm{XCE}}}\right).$$

Standardisation is not cosmetic: without it, a spread of hundreds of dollars per tonne
would entirely swamp a spread of about one kelvin, and $\lambda$ would carry units.
With it, $\lambda$ is dimensionless and the two axes contribute comparably.

**Why not one dimension?** The obvious first choice — warming alone — is the direct
analogue of an RCP level, and it fails empirically. Measuring how well each candidate
coordinate predicts *how differently the model actually behaves* (correlation between
pairwise distance and the mean absolute FX difference across the 14 currencies at
2040):

| Coordinate | Correlation with model-behaviour difference |
|---|--:|
| $\lvert \Delta T_{2100}\rvert$ | 0.28 |
| $\lvert \Delta \mathrm{XCE}\rvert$ | **0.98** |

The decisive counterexample is the pair **Net Zero 2050 and Low demand**. They differ
by 0.01 K in end-century warming — a warming-only metric therefore treats them as the
same state — yet they differ by $306/t in carbon price and by 3.2 percentage points in
mean FX impact, the largest gap of any near-neighbour pair in the set. They arrive at
the same temperature by different economic means, and every channel in this model
cares about the means.

That result might suggest using carbon price alone. Warming is retained as the second
axis for a forward-looking reason: the physical channel's magnitude is currently
suppressed by the Barrage–Nordhaus damage function and the incremental-$\Delta T$
convention (see the audit's §B1 sensitivity, spanning roughly 90×). Under the SwissRe
damage function or the pre-industrial $\Delta T$ reading, warming *would* materially
drive results, and a price-only metric would then be misspecified. The two-dimensional
metric is robust across that range; the one-dimensional alternatives are each
misspecified at one end of it.

**A methodological note on circularity.** The metric is defined on scenario
*characteristics*, which are model *inputs*. The correlation table above uses model
*outputs*, and it is presented as a diagnostic — evidence that the chosen coordinates
separate scenarios the model treats differently — not as the definition. Defining the
distance on outputs would be circular, and is not done.

### N.4.4 Computing the matrix: a worked example

The construction proceeds in four steps.

**Step 1 — coordinates, taken directly from the NGFS data.** No choices enter here.

| Scenario | $T_{2100}$ (K) | $\mathrm{XCE}_{2050}$ ($/t) |
|---|--:|--:|
| Net Zero 2050 | 1.45 | 626 |
| Low demand | 1.47 | 320 |
| Below 2 °C | 1.69 | 153 |
| Delayed transition | 1.75 | 168 |
| NDCs | 2.03 | 90 |
| Fragmented World | 2.11 | 120 |
| Current Policies | 2.75 | 3 |

**Step 2 — standardise each axis.** $T$: mean 1.893, sd 0.421 K.
$\mathrm{XCE}$: mean 211.4, sd 191.1 $/t.

**Step 3 — pairwise Euclidean distance.** Two sanity checks bracket the range:
Below 2 °C ⇄ Delayed transition = 0.17 (near-identical narratives), and
Net Zero ⇄ Current Policies = 4.49 (the opposite corners of the set).

**Step 4 — apply the kernel and normalise rows.** Taking the row from Below 2 °C at
$\lambda = 2$:

```
exp(-2d):  Below2C 1.0000   Delayed 0.7105   NDCs 0.1729   LowDem 0.1312
           Fragm   0.1304   NetZero 0.0063   CurrPol 0.0050
row sum  =  2.1562   →  divide through
         =  0.464     0.330      0.080       0.061
            0.060     0.003      0.002
```

The resulting annual matrix at $\lambda = 2$ is:

| from ↓ / to → | Below 2 °C | CurrPol | Delayed | Fragm | LowDem | NDCs | NetZero |
|---|--:|--:|--:|--:|--:|--:|--:|
| **Below 2 °C** | 0.464 | 0.002 | **0.330** | 0.060 | 0.061 | 0.080 | 0.003 |
| **Current Policies** | 0.005 | **0.928** | 0.006 | 0.034 | 0.001 | 0.026 | 0.000 |
| **Delayed transition** | **0.319** | 0.003 | 0.449 | 0.076 | 0.056 | 0.095 | 0.003 |
| **Fragmented World** | 0.066 | 0.019 | 0.086 | 0.507 | 0.012 | **0.309** | 0.001 |
| **Low demand** | 0.097 | 0.001 | 0.092 | 0.018 | **0.741** | 0.020 | 0.030 |
| **NDCs** | 0.084 | 0.014 | 0.103 | **0.297** | 0.013 | 0.487 | 0.001 |
| **Net Zero 2050** | 0.006 | 0.000 | 0.006 | 0.002 | 0.038 | 0.002 | **0.945** |

The matrix reads sensibly. The isolated extremes are sticky — Current Policies and Net
Zero have annual self-persistence of 0.928 and 0.945 — because they sit far from
everything else and the kernel penalises long jumps. The close pairs are nearly
interchangeable: Below 2 °C ⇄ Delayed transition ≈ 0.32, NDCs ⇄ Fragmented World ≈
0.30. And the extreme-to-extreme transition is effectively unreachable at 0.0001,
which is the desired behaviour: an economy does not move from a net-zero trajectory to
an unmitigated one in a single year.

$\lambda$ is the **only free parameter** in the construction, and the paper supplies no
value for it (Table 17: "the narrative users set the value of $\lambda$"). It is
therefore swept over $\lambda \in \{5.0,\ 2.0,\ 0.5\}$ rather than fixed, and results
are reported for the sweep.

### N.4.5 Propagating the prior forward

With $Q$ in hand, weights at horizon $T$ follow from
$\mathbf{p}_T = \mathbf{p}_0 Q^{T-2022}$, and the expectation becomes
horizon-dependent:

$$\mathbb{E}_T[\Delta X] \;=\; \sum_s p_T[s]\, \Delta X_s .$$

Under the `ambition` prior at $\lambda = 2$:

| | NetZero | Below 2 °C | Delayed | NDCs | Fragm | CurrPol |
|---|--:|--:|--:|--:|--:|--:|
| **2022** (prior) | 0.235 | 0.235 | 0.118 | 0.118 | 0.059 | 0.059 |
| **2040** | 0.145 | 0.172 | 0.178 | 0.160 | 0.154 | 0.073 |

The prior erodes toward the stationary distribution: Net Zero falls from 0.235 to
0.145 while Fragmented World rises from 0.059 to 0.154. This is the mechanism's
essential behaviour — conviction decays with horizon.

---

## N.5 Results

### N.5.1 Expected outputs under the four priors

Taking the 5-year forward FX shift against the euro at horizon 2040 as the
representative output (%, negative = appreciation against EUR):

| Prior | IND | CHN | KAZ | NOR | Provenance |
|---|--:|--:|--:|--:|---|
| **`consensus`** | **−0.54** | **−0.52** | **−0.40** | **+0.09** | **citable** |
| `uniform` | −6.20 | −6.34 | −4.03 | +1.31 | uninformative |
| `policy-sceptic` | −3.55 | −3.59 | −2.24 | +0.79 | asserted |
| `ambition` | −8.53 | −8.75 | −5.56 | +1.79 | asserted |

The *ordering* of regions is invariant across priors — carbon-intensive economies
appreciate against the euro under every belief, because in every scenario they face
deeper transition-driven rate cuts. What the prior changes is the *magnitude*, and it
changes it by more than an order of magnitude between `consensus` and `ambition`.

The honest summary is therefore that the model's cross-sectional ranking is robust to
the prior while its absolute levels are not. For a risk application, the ranking is
the more usable output.

### N.5.2 The concentration finding: transition risk lives in the tail

The most substantive result of this chapter follows from the `consensus` prior being
concentrated. Because 80.7 % of the mass sits on Current Policies, and because Current
Policies carries a carbon price of roughly $3/t — effectively zero — the expected
transition shock nearly vanishes. The Indian rupee's expected 2040 move collapses from
−6.20 % under `uniform` to **−0.54 %** under `consensus`.

This is not a defect of the calculation but its point. Conditional on the published
current-policy trajectory being correct, *there is very little expected transition
risk*, because on that trajectory very little transition occurs. Transition risk is
therefore properly understood as a **tail phenomenon**: it is large in the ambitious
scenarios, which the consensus evidence assigns low probability, and near-zero in the
scenario that evidence favours.

Two implications follow for how the model's results should be used. First, an
expectation is the wrong summary statistic for transition risk; the quantile band of
Chapter [volatility] (`mixture.quantile`, weighted across the discrete scenario
distribution) is the appropriate one. Second, the ambitious scenarios should be
presented as **stress cases** rather than central forecasts — which is, in fact,
precisely what a stress-testing framework is for. A framework that reported only
expectations under a consensus prior would conclude that climate transition poses
negligible financial risk, and would be wrong for the same reason that reporting only
the mean of a loss distribution is wrong.

### N.5.3 Drift: the horizon at which the prior stops mattering

The drift sensitivity yields a result worth stating in its own right. Because $Q$
erodes any prior toward the same stationary distribution, **the four priors converge**
as the horizon lengthens. At $\lambda = 0.5$ they are effectively indistinguishable by
2045, whereas the static mixture keeps them roughly 6 percentage points apart at the
same horizon.

The interpretation is that the choice of narrative matters at 5–10 years and ceases to
matter by 20. This is intuitively right — near-term outcomes are largely determined by
current policy settings, long-term outcomes are open — and it provides a principled
answer to the question of how much effort to spend defending a prior: considerable, if
the reporting horizon is short; little, if it is long.

### N.5.4 Status: static mixture as the headline, drift as a sensitivity

The static mixture is reported as the base case
(`out_ext_fx_expected_*.csv`, Figure 3) and drift as a sensitivity
(`out_sens_fx_drift_*_lam*.csv`, Figure 9). The reason is a count of assumptions: the
static mixture rests on **one** discretionary input (the prior), whereas drift requires
**three** (the prior, $\lambda$, and a distance over narratives). Where a result can be
obtained with fewer assumptions, it belongs in the headline; the additional machinery
belongs in the sensitivity analysis, where its assumptions can be varied and their
influence displayed.

---

## N.6 Validation

The mixture layer is covered by numerical gates in `tests/test_extensions.py`, executed
on every run. They fall into three groups.

**Internal consistency.** Weights sum to one under every prior; all priors share the
concentration $\sum\alpha = 14$; the rows of $Q$ are probability vectors; the diagonal
of $Q$ is its row mode, i.e. remaining in the current scenario is always the single
likeliest annual outcome.

**Reduction properties.** These are the strongest tests, since they check the layer
against known limits. A degenerate prior reproduces its scenario's table exactly,
confirming that the mixture is genuinely additive post-processing. The expectation
always lies within the range spanned by the component scenarios. And $\lambda \to
\infty$ collapses $Q$ to the identity and reproduces the static mixture exactly,
confirming that drift nests the static case rather than replacing it.

**Behavioural properties.** Adding counts shifts the posterior toward the counted
scenario under all priors. The `consensus` prior places its greatest weight on the
scenario nearest the warming anchor, with weights falling monotonically in distance
from it.

One gate deserves specific mention because it caught a live defect. The requirement
that **all seven scenarios carry strictly positive weight** was violated in an earlier
build: the IIASA API returns the label `Below 2?C`, substituting an ASCII question mark
for the degree sign, so an exact string match against the module's literal
`Below 2°C` failed silently and that scenario was dropped from every mixture. The
weights still summed to one — the failure was invisible to every other check — and the
error would have propagated into all expected results. The fix was to match on
normalised alphanumeric keys (`mixture._key`), and the gate now prevents recurrence.
The episode is a useful illustration of why reduction and coverage gates are worth
writing even for code whose logic is simple.

---

## N.7 Limitations and critical appraisal

**The priors are asserted, not estimated.** This is the binding limitation, and it is
inherited from the paper, which simply assigns 90 % to SSP2/RCP4.5. The `consensus`
prior mitigates it by anchoring on published assessments, but even there the choice of
Gaussian kernel, the value of $\mathrm{sd}$, and the decision to weight on end-century
warming rather than some other characteristic are all discretionary. Reporting four
priors side by side is a disclosure of this uncertainty, not a resolution of it.

**Using the Dirichlet mean discards second-order uncertainty.** The framework knows
that $\mathbf{p}$ is itself uncertain but reports only its mean. Confidence intervals
on the weights — and hence on the expectations — could be obtained by sampling from
$\mathrm{Dir}(\boldsymbol{\alpha})$, at the cost of departing from the paper's stated
method.

**The distance metric is a construction, not a datum.** Where the paper could rely on
RCP concentration labels, this work had to invent a coordinate system. The choice is
defended empirically in §N.4.3, but a different pair of characteristics would produce
a different $Q$, and the sensitivity of results to that choice has not been mapped
beyond the 1-D versus 2-D comparison presented.

**$\lambda$ is unidentified.** The paper offers no value and no estimation strategy,
and none is obvious: calibrating a scenario-transition rate would require a history of
observed scenario transitions, which does not exist. The sweep over
$\{5.0, 2.0, 0.5\}$ is a disclosure of ignorance rather than a resolution of it.

**Event attribution is judgmental.** The conjugate update is exact, but deciding that
a given policy announcement constitutes evidence "for" one narrative rather than
another is a qualitative act. The framework's virtue is that it forces this judgment
into the open, where it can be argued with.

**The scenario set itself is a constraint.** Weights are defined over seven NGFS
narratives, and no probability mass can be assigned to futures those narratives do not
describe. The block-structure test of §N.4.2 illustrates the sharper form of this
problem: a scenario set containing only one fragmented narrative cannot represent
transitions *within* fragmentation, and any structure imposed on it inherits that
limitation as an artefact.

---

## N.8 Summary

This chapter has implemented the paper's Bayesian scenario layer and extended it in
three respects. First, it introduces a **citable prior** built by transposing the
paper's §3.1.4 construction into the NGFS setting via published current-policy warming
estimates, replacing an asserted weight vector with an auditable and updatable one.
Second, it resolves the problem that the paper's Eq. 1 distance metric has no NGFS
analogue, by constructing a **standardised two-dimensional metric** over end-century
warming and carbon price, and defending that choice against the one-dimensional
alternatives on empirical grounds. Third, it enforces a **common Dirichlet
concentration** across priors so that comparisons isolate the direction of belief from
its strength.

The substantive finding is that under the only prior with a source, expected
transition risk is an order of magnitude smaller than under an uninformative prior,
because the published trajectory implies almost no carbon price. Transition risk is a
tail phenomenon, and the model's ambitious scenarios are properly read as stress cases
rather than forecasts — which is the conclusion a stress-testing framework should
reach, and one that a single-scenario or expectation-only analysis would have
obscured.

---

### Source map for this chapter

| Content | Location |
|---|---|
| Implementation | `bkmn/mixture.py` |
| Scenario coordinates | `bkmn/scenarios.py::Scenarios.coords()` |
| Gates | `tests/test_extensions.py` (Phase M block) |
| Static-mixture results | `out_ext_fx_expected_{consensus,uniform,policy-sceptic,ambition}.csv`, Figure 3 |
| Drift sensitivity | `out_sens_fx_drift_*_lam{0.5,2,5}.csv`, Figure 9 |
| Quantile band | `out_ext_fx_q95_scen.csv` |
| Supporting audit | `docs/PAPER_AUDIT.md` §E, §H |
| Technical note | `docs/MIXTURE_METHOD.md` |
