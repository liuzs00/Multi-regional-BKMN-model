# Physical Risk

## 1. Purpose and role in the model

Transition risk, developed in the preceding chapter, is a policy cost: it exists
because governments price carbon, and it vanishes if they do not. Physical risk is
the opposite — it is the cost of the climate change itself, and it is largest
precisely in the scenarios where policy does least. A model containing only the
transition channel therefore delivers a systematically misleading verdict, since it
makes ambitious decarbonisation appear unambiguously the most damaging future
available. Restoring the physical channel is what makes the scenario comparison
meaningful.

This chapter implements §2.5 of Berrahoui, Kenyon, Macrina and Nathanael (2025) and
generalises it to the twenty-region system. The structure of the original is retained:
a **damage function** converts warming into a loss of aggregate output, and a
**vulnerability weighting** distributes that loss across sectors. Two things change in
the multi-regional setting. First, the damage function now applies at world level, so
the object being allocated is world GDP rather than one country's. Second,
vulnerability acquires a regional dimension, so that the same global temperature rise
produces different losses in different economies — which is the entire point of
modelling physical risk across regions rather than one.

The implementation is `bkmn/physical.py`; results are in `out_ext_gdp_physical.csv`.

---

## 2. The damage function

### 2.1 Functional form

Following §2.5.1, the fraction of output lost is quadratic in the temperature
change $\Delta T$:

$$\Omega(\Delta T) \;=\; \kappa\,\Delta T^{2}, \qquad \Omega \ge 0 ,$$

with $\Omega$ interpreted as the **fraction of GDP lost** relative to a
counterfactual of no further warming. The paper offers two calibrations, which are
retained here as a central case and a sensitivity:

| Source | $\kappa$ | Loss at $\Delta T = 2.2\,^\circ$C |
|---|--:|--:|
| Barrage and Nordhaus (2024), DICE-2023 — **central** | $0.003467$ | $1.68\%$ |
| Swiss Re (2024) — sensitivity | $0.017562$ | $8.50\%$ |

The Swiss Re calibration is $5.07\times$ the Barrage–Nordhaus one. The quadratic
form is standard in the integrated-assessment literature and is adopted for
comparability rather than because the evidence strongly favours it; §6 returns to
this.

### 2.2 A correction to the paper's stated coefficient

Equation 11 of the paper writes the Barrage–Nordhaus calibration as

$$\Omega_{BN}(\Delta T) \;=\; \frac{1.6768}{2.2\times2.2}\,\Delta T^{2},$$

which evaluates to $\kappa = 0.34645$. Taken at face value this gives
$\Omega(2.2\,^\circ\mathrm{C}) = 1.677$ — a loss of **168 % of GDP** — which is not a
possible quantity. The resolution is that the numerator $1.6768$ is expressed in
*per cent*: DICE-2023 puts damages at $2.2\,^\circ$C at $1.68\%$ of output, so the
coefficient in fractional terms carries a factor $10^{-2}$,

$$\kappa \;=\; \frac{1.6768\times10^{-2}}{2.2^{2}} \;=\; 0.003467 .$$

That the intended value is the fractional one is confirmed by the paper itself: its
worked example at Equations 13 and 14 uses $0.003467$ explicitly. Equation 11 as
literally written is therefore a units error of two orders of magnitude, and the
figure $0.003467$ is used throughout this work. The point is recorded because the
error is easy to reproduce — an earlier build of this model did so, and the resulting
physical damages were large enough to rival transition costs, which was an artefact
rather than a finding.

### 2.3 The temperature convention

A second choice materially affects magnitudes and is not settled by the paper. The
damage function takes "the temperature change", but a scenario supplies warming
relative to the pre-industrial baseline, whereas the model's other channels measure
deviations from a base year. Two readings are therefore available:

$$\Delta T^{\text{inc}}(t) = T(t) - T(t_{0}),
\qquad
\Delta T^{\text{abs}}(t) = T(t) - T_{1850\text{–}1900}.$$

This work uses the **incremental** reading $\Delta T^{\text{inc}}$, with
$t_{0} = 2022$, for consistency with the rest of the model: the base year's economy is
observed data and already embodies whatever damage the warming to date has caused, so
charging that damage again would double-count. The choice is consequential — at 2040
the incremental reading gives roughly $0.3\,^\circ$C where the absolute reading gives
roughly $1.6\,^\circ$C, and because the function is quadratic the implied damages
differ by a factor of about seventeen. Combined with the choice of $\kappa$, the two
conventions span a range of roughly ninety-fold in physical damage, which is reported
as a sensitivity grid rather than concealed in a point estimate.

The honest summary is that the level of physical damage in this model is weakly
identified, while the *cross-scenario and cross-region ordering* — which is what the
results are used for — is robust to both choices, since they rescale all regions and
scenarios by the same factor.

---

## 3. Allocating damage across sectors: Proposition 1

### 3.1 Statement

The damage function delivers one number for the whole economy. To enter the
input–output system it must be distributed across sectors, and §2.5.2 does so by
assigning each sector a **vulnerability** $VL_i$ measuring its sensitivity relative to
a reference sector.

> **Proposition 1 (Berrahoui et al., §2.5.2).** Let $VL_i$ be the vulnerability of
> sector $i$, let $f_i = \mathrm{GVA}_i/\mathrm{GDP}$ be its output share, assumed
> constant, and let $\Omega(\Delta T)$ be the fraction of GDP lost. Then the relative
> damage to each sector is
>
> $$\frac{\Delta \mathrm{GVA}_i}{\mathrm{GVA}_i} \;=\; -\,VL_i\,\alpha,
> \qquad
> \alpha \;=\; \frac{\Omega(\Delta T)}{\sum_{k} VL_k f_k}.$$

*Sign convention.* The paper writes $\Omega$ both as a loss and as a signed change.
Here $\Omega \ge 0$ denotes the magnitude of the loss and the negative sign is carried
explicitly, so that $\alpha > 0$ and sector shocks are negative. This is a
clarification of the original, not a departure from it.

### 3.2 Proof

Value added sums to GDP by construction, $\mathrm{GDP} = \sum_i \mathrm{GVA}_i$, so
the same holds for changes, $\Delta\mathrm{GDP} = \sum_i \Delta\mathrm{GVA}_i$.
Dividing by GDP and multiplying each term by $\mathrm{GVA}_i/\mathrm{GVA}_i$,

$$\frac{\Delta\mathrm{GDP}}{\mathrm{GDP}}
\;=\; \sum_{i} \frac{\Delta \mathrm{GVA}_i}{\mathrm{GVA}_i}\cdot\frac{\mathrm{GVA}_i}{\mathrm{GDP}}
\;=\; \sum_{i} f_i\,\frac{\Delta \mathrm{GVA}_i}{\mathrm{GVA}_i}. \tag{1}$$

Now fix a reference sector $k$ with $VL_k = 1$ and define
$\alpha := -\Delta\mathrm{GVA}_k/\mathrm{GVA}_k$, the relative damage suffered by the
reference sector. Vulnerability is defined *relative to* that sector,

$$VL_i \;:=\; \frac{\Delta \mathrm{GVA}_i}{\mathrm{GVA}_i}\Big/\frac{\Delta \mathrm{GVA}_k}{\mathrm{GVA}_k}
\qquad\Longrightarrow\qquad
\frac{\Delta \mathrm{GVA}_i}{\mathrm{GVA}_i} = -VL_i\,\alpha .$$

Substituting into (1) and using $\Delta\mathrm{GDP}/\mathrm{GDP} = -\Omega$,

$$-\Omega \;=\; -\alpha\sum_i f_i VL_i
\qquad\Longrightarrow\qquad
\alpha \;=\; \frac{\Omega}{\sum_i f_i VL_i}. \qquad\blacksquare$$

The content of the proposition is worth stating plainly, because the algebra can
obscure it. Vulnerability scores are only ever *relative*: doubling every $VL_i$ leaves
every sector's damage unchanged, because $\alpha$ halves in compensation. What the
scores determine is the **distribution** of a loss whose total is fixed by the damage
function. The denominator $\sum_i f_i VL_i$ is exactly the normalising constant that
enforces this.

### 3.3 Direct and cascading forms

The proposition can be applied in two ways, both retained in the implementation.

The **direct** form applies $-VL_i\alpha$ to each sector's value added and stops
there. It is the literal reading of the proposition and is used for the headline
damage figures.

The **cascading** form instead adds $VL_i\alpha$ to the per-unit charge $ct_i$ of the
transition chapter,

$$ct_i \;\longrightarrow\; \underbrace{\mathrm{CI}_i \cdot \mathrm{XCE}^{r(i)} \cdot 10^{-6}}_{\text{transition}} \;+\; \underbrace{VL_i\,\alpha}_{\text{physical}},$$

so that physical damage propagates through the same modified Leontief dual as the
carbon charge. This is the paper's own suggestion and has an economic reading:
climate damage to one sector raises costs for the sectors that buy from it, exactly as
a carbon charge does. Because the operator $\mathbf{M}(\phi)$ is linear in $ct$, the
cascading form costs no additional inversion.

---

## 4. Vulnerability in a multi-regional system

### 4.1 The generalisation choice

Proposition 1 is stated for one economy, and there are two defensible ways to lift it
to twenty. One may apply it **within each region** — each region suffers $\Omega$ of
its own GDP, distributed across its own sectors — or **at world level**, treating
$\Omega$ as a loss of world GDP distributed across all $1000$ region–sectors by
vulnerability relative to the whole grid.

This work takes the world-level reading. The reason is that the alternative
contains an implicit assumption that defeats the purpose of the exercise: applying
$\Omega$ within each region forces every region to lose the *same fraction* of its own
GDP for a given global warming, so regional vulnerability could only ever affect the
sector composition of the loss, never its size. Since the object of a multi-regional
physical-risk model is precisely that some economies suffer more than others, that
reading would be self-defeating. Under the world-level reading, per-region damage
**emerges from aggregation**: a region loses more because its sectors carry higher
vulnerability weights within the global distribution.

The choice is flagged as a modelling decision rather than an inheritance from the
paper, and the within-region variant remains available as a sensitivity.

### 4.2 The vulnerability field: pattern times scale

The model requires $VL$ for every region–industry pair. No source supplies a
sector-by-country vulnerability field of that resolution, so it is constructed as a
separable product:

$$VL(r,i) \;=\; \underbrace{\text{pattern}(i)}_{\text{sector}} \times \underbrace{\text{scale}(r)}_{\text{region}} .$$

The **sector pattern** is the paper's Table 6, a twenty-sector UK vulnerability
ranking normalised so that human health takes the value $1$. It runs from $0.4$
(professional services) through $1.0$ (education, public administration) to $1.9$
(water and waste) and $1.8$ (agriculture), and is expanded onto the fifty ICIO
industries by holding it constant within each SIC section.

The **region scale** is the ND-GAIN country vulnerability index for 2024, aggregated
to the twenty regions and rescaled by a reference level of $0.3551$ so that a region
of median vulnerability scores approximately $1.0$. The resulting range is:

| Region | scale | | Region | scale |
|---|--:|---|---|--:|
| Africa (AFR) | **1.340** | | Korea | 1.002 |
| India | 1.337 | | Japan | 0.994 |
| Indonesia | 1.213 | | EU27 | 0.924 |
| Middle East (MEA) | 1.210 | | USA | 0.892 |
| Turkey | 1.114 | | Australia | 0.845 |
| China | 1.110 | | Canada | 0.795 |
| Latin America (LAM) | 1.104 | | UK | 0.793 |
| Singapore | 1.069 | | **Norway** | **0.742** |

The most vulnerable region scores $1.81\times$ the least.

Two limitations of this construction should be recorded. ND-GAIN is a country-level
composite covering exposure, sensitivity and adaptive capacity; it is not
sector-specific, so the *shape* of sectoral vulnerability is assumed common across
regions and only its *level* varies. And the pattern itself is a UK assessment applied
worldwide. A sector-by-region vulnerability field estimated directly would be a
substantial improvement, and is not available at this resolution.

### 4.3 The allocation identity

Whatever the vulnerability field, the construction must conserve the total: the
sector damages must sum back to the damage function. This is guaranteed by the
normalising denominator of Proposition 1, and holds in the implementation to exact
floating-point equality,

$$\sum_{i} f_i\,VL_i\,\alpha \;=\; \Omega(\Delta T),
\qquad \text{residual} = 0.00\times10^{0},$$

verified at each evaluation. The identity is the reason the vulnerability field can be
revised — a different pattern, a different index, a different regional aggregation —
without any risk of the total damage drifting: only the distribution changes.

---

## 5. Results

### 5.1 The scenario ranking reverses by channel

The headline result of adding this chapter's machinery is a reversal. GDP shock at
2040 with pass-through $\phi = 0.5$ (%):

| Region | Net Zero: transition | Net Zero: physical | Current Policies: transition | Current Policies: physical |
|---|--:|--:|--:|--:|
| EU27 | $-2.66$ | $-0.04$ | $\mathbf{-0.02}$ | $\mathbf{-0.05}$ |
| China | $-11.40$ | $-0.05$ | $-0.13$ | $-0.07$ |
| India | $-10.37$ | $-0.06$ | $-0.12$ | $-0.08$ |
| Africa | $-5.05$ | $-0.06$ | $-0.03$ | $-0.08$ |
| Norway | $-0.96$ | $-0.04$ | $-0.01$ | $-0.05$ |

Under Net Zero 2050 the transition cost exceeds physical damage by a factor of
roughly sixty; under Current Policies the ordering flips and physical damage is the
larger of the two, if only narrowly. **Neither scenario is worst on both channels.**
This is the central climate-economics point that the single-channel model cannot
express: a transition-only reading ranks Net Zero as by far the most damaging future,
and that ranking is an artefact of the channel selected rather than a property of the
world.

### 5.2 Magnitudes are small, and that is a finding about the damage function

Physical damages to 2040 are economically small in absolute terms — of order
$0.05\%$ of GDP. This follows from the two conventions of §2.2–2.3 rather than from
anything in the multi-regional machinery: Barrage–Nordhaus damages are mild by
construction, the horizon is short, and warming is measured incrementally from 2022.
Under the Swiss Re calibration the figures are about five times larger, and under the
pre-industrial temperature reading about seventeen times larger.

The appropriate conclusion is not that physical risk is negligible but that **its
magnitude is a function of assumptions the literature has not settled**, whereas the
*ranking* it induces across scenarios and regions is stable. The results are used for
the latter.

### 5.3 Regional incidence behaves as the vulnerability field requires

For a common global $\Delta T$, the most vulnerable regions suffer the largest
relative damage. At $\Delta T = 0.3\,^\circ$C the loss is $0.0446\%$ for India and
$0.0441\%$ for Africa against $0.0264\%$ for Norway — a ratio of $1.67$.

That ratio is instructive for being *smaller* than the underlying scale ratio of
$1.81$. The difference is sector composition: Norway's output is concentrated in
industries carrying higher pattern weights, which partially offsets its lower regional
scale. Regional damage is therefore not simply a rescaling of the ND-GAIN index — it
is the interaction of the index with the region's industrial structure, which is
precisely what the input–output grid is there to supply.

---

## 6. Assumptions and limitations

**The damage function is quadratic and adaptation-free.** Damage scales as
$\Delta T^{2}$ without limit and no adaptive response is modelled, so at large warming
the function extrapolates a relationship calibrated at small warming. Combined with
the linear transition channel, this makes the combined GDP shock an upper bound rather
than a forecast.

**The level of damage is weakly identified.** The choice of $\kappa$ and of
temperature convention together span roughly ninety-fold. This is disclosed as a
sensitivity grid; no single point estimate should be quoted without it.

**World-level Proposition 1 is a modelling choice.** Damage is allocated across the
global grid, so per-region losses emerge from relative vulnerability rather than being
imposed. The within-region alternative is defensible and untested here.

**Vulnerability is separable by construction.** $VL(r,i) = \text{pattern}(i)\times
\text{scale}(r)$ assumes the sectoral shape of vulnerability is the same everywhere,
which is certainly false in detail — agriculture in Norway and agriculture in India
face different hazards — but no dataset supports the interaction term.

**Constant value-added shares.** Proposition 1 assumes $f_i$ fixed, consistent with
the static input–output table of the preceding chapter, and excludes structural change
over the horizon.

**Physical risk enters through output only.** Damage reduces value added and therefore
GDP, but does not enter the inflation channel of the following chapter. Supply-side
climate shocks — crop failures, disrupted logistics — are plausibly inflationary, and
their omission means the model understates the physical channel's effect on interest
rates.

---

### References

Barrage, L. and W. Nordhaus (2024). Policies, projections, and the social cost of
carbon: results from the DICE-2023 model. *PNAS* 121(13).

Berrahoui, M., C. Kenyon, A. Macrina and G. Nathanael (2025). *Simple climate stress
testing: an ensemble framework.* Working paper.

Notre Dame Global Adaptation Initiative (2024). *ND-GAIN Country Index.*

Swiss Re Institute (2024). *Changing climates: the heat is (still) on.*
