# Audit of the implementation against the BKMN paper

Line-by-line check of every implemented channel against *Simple climate stress
testing: an ensemble framework* (Berrahoui, Kenyon, Macrina, Nathanael 2025).
One outright bug found and fixed; four places where the paper is ambiguous and
we had to choose, now made explicit; two paper features not implemented.

## A. Bug found and fixed

### A1. Damage function was 100× too large — **fixed**

Eq 11 reads `Ω_BN(ΔT) = 1.6768/(2.2×2.2) · ΔT²`. The `1.6768` is the GDP damage
at 2.2 °C **in per cent** — the paper's own Eq 13/14 write the fraction form as
`0.003467`. We had coded `1.6768/2.2²  = 0.3465`, i.e. Ω(2.2 °C) = **168 % of
GDP**.

Now `DAMAGE_COEF = 1.6768e-2/2.2² = 0.0034645` (SwissRe likewise
`8.5e-2/2.2² = 0.017562`). Two gates lock it: `Ω(2.2) = 1.6768 %` and
`coef ≈ 0.003467`.

**Effect** — physical damage at 2040 falls by 100×, e.g. EU27 under Current
Policies −5.15 % → **−0.05 %**. The transition/physical *ranking* flip survives
(under CP physical still exceeds transition, −0.05 % vs −0.02 %) but the
magnitudes are now small, and the earlier claim that physical damage rivals
transition cost was an artefact of this bug. All extension tables and figures
regenerated.

## B. Paper ambiguities — our choice, now explicit

### B1. Which ΔT feeds the damage function
Prop 1 says *"ΔT(t) is the temperature change, at t, relative to **pre-industrial**"*,
and Eq 13 telescopes consistently with that. But §2.1 argues the market curves we
start from already embed pre-damage expectations, so only warming **from today**
is a shock. The two readings differ by ~17× (ΔT 0.41 K vs 1.70 K at 2040).

`run_extensions.WARMING_BASELINE` selects; default `"incremental"`. Sensitivity:

| ΔT reading | damage fn | ΔT 2040 (CP) | EU27 | AFR |
|---|---|--:|--:|--:|
| incremental (default) | Barrage–Nordhaus | 0.41 K | −0.05 % | −0.08 % |
| incremental | SwissRe | 0.41 K | −0.26 % | −0.43 % |
| pre-industrial (Prop 1 literal) | Barrage–Nordhaus | 1.70 K | −0.87 % | −1.42 % |
| pre-industrial | SwissRe | 1.70 K | −4.40 % | −7.19 % |

The corner choice spans ~90×, so **state the convention in the write-up**; it is
the single largest discretionary lever in the physical channel.

### B2. Direct vs cascading physical effect
Prop 1 gives both: a direct allocation `ΔGVA_i/GVA_i = VL_i·α` **and** a cascading
form that adds `VL_i·α` to the sector tax rate so it propagates through the
Leontief. Both are implemented (`direct_shock`, `tax_addon`); the runner uses
**direct only** — applying both would double-count. Cascading is a natural
sensitivity to add.

### B3. Sign of Ω
Eq 11 defines Ω as a positive fraction while Prop 1 writes `ΔGVA/GVA = VL·α`
without a minus sign, which would read as a *gain*. We treat Ω as a damage
magnitude and return damage negative (`direct_shock = −VL·α`); the allocation
identity `Σ f·VL·α = Ω` is gate-checked.

### B4. Inflation: scope level or scope change
§2.6 writes `ΔΠ = (0.08%/10)·ΔXCE·ΔΩ_XCE` with ΔΩ the *change* in pricing scope —
a product of two changes, which would be second-order and is likely a typo. The
surrounding text ("inflation increases must be understood w.r.t. the scope")
supports scope as a **level**, which is what we use (`ΔΠ = 8e-5·ΔXCE·scope`),
matching the single-region reference implementation.

## C. Paper features not implemented (deliberate)

### C1. Cumulative short rate (Eq 15)
Eq 15 gives `Δr(t) = ∫ Δr^Policy(s) ds`. We use the Taylor output at *t* directly
as the short-rate shift, because our ΔΠ and ΔY are already **level deviations**
from the no-climate baseline at t, so the Taylor rule returns the policy-rate
deviation at t; integrating those would double-count. Flagged for confirmation
against the single-region reference code.

### C2. RCP transition matrix (Eq 1) — implemented as a **sensitivity**
See §E. Kept out of the headline because it needs two assumptions the static
mixture does not (λ, and a distance over narratives).

## D. Checked and correct

| Paper | Implementation | Check |
|---|---|---|
| Eq 2 `A = Z x̂⁻¹`, `L = (I−A)⁻¹` | `transition.technical_matrix` | ρ(A)=0.587 < 1 |
| Eq 8 `L̃(φ) = (I−Aᵀφ̂)⁻¹φ̂` | `transition.gva_operator` | φ=0/1 endpoints exact |
| Eq 10 `Δv = [(I−Aᵀ)L̃(φ) −I +φ̂]ct` | same | reduction to committed CSV, 4e-16 |
| Eq 6 `ct = CI·XCE` (+1e-6 units) | `transition.ct_direct` | UK ∓0.851 % anchor |
| Prop 1 `α = Ω/Σ VL·f` | `physical.alpha` | identity `Σf·VL·α = Ω` to 1e-17 |
| §2.6 Moessner 0.08 %/$10 | `macro.inflation_dev` | scale checked |
| §2.7 Taylor `φΠ=φY=0.5` | `macro.taylor_rate_shift` | — |
| §2.8 Prop 2 `ΔR = B(τ)/τ·Δr`, `a=0.04` | `rates.zero_rate_shift` | τ→0 limit, decay |
| §2.9 `ΔS/S = β·ΔGVA/GVA` | `equity.equity_shift` | sign |
| §2.11 Okun `ΔU = κΔY`, β_Phillips = 0 | `oprisk` | sign chain |
| §2.2 Dirichlet-categorical | `mixture` | conjugacy, degenerate prior |
| §4.3 FX from yield-curve differences | `fx` | triangular consistency 2e-17 |

26 extension gates + 9 FX gates, all passing.


## E. Eq-1 transition matrix: the distance metric (sensitivity)

Eq 1 is `q(j,k) = exp(−λ·d(j,k))/Σ_h exp(−λ·d(j,h))`, with the paper's `d = |j−k|`
on **RCP concentration labels** — a physical number the scenario set supplies.
NGFS narratives have no such label, so `d` had to be defined.

**What we use:** Euclidean distance in **standardised (T₂₁₀₀, XCE₂₀₅₀) space** —
end-of-century warming and carbon price, the two characteristics that distinguish
the scenarios and that drive this model. Z-scoring each axis makes λ dimensionless
and stops $/t swamping K. Eq 1 explicitly allows this: the distance *"can be
generalized to include any function of RCP characteristics"*.

**Why not 1-D on warming** (the obvious first choice — it is the direct analogue of
an RCP level): it fails empirically. Correlation between pairwise distance and how
differently the model actually behaves (mean |ΔFX| across the 14 currencies, 2040):

| coordinate | correlation |
|---|--:|
| \|ΔT₂₁₀₀\| | 0.28 |
| \|ΔXCE\| | **0.98** |

The decisive case is Net Zero 2050 vs Low demand: **0.01 K apart** in end-warming —
so a warming metric calls them the same state — yet $306/t apart in carbon price and
3.2 pp apart in mean FX impact, the largest gap of any near-neighbour pair. They
reach the same temperature by different means, and the model cares. 2-D is also
robust if the physical channel is later scaled up (SwissRe / pre-industrial ΔT, §B1),
where warming *would* matter; a price-only metric would then be wrong.

*Method note:* the metric is defined on scenario **characteristics** (inputs). The
output correlation above is a diagnostic that it separates scenarios the model
treats differently — not the definition, which would be circular.

**On the non-uniform stationary distribution.** An exponential kernel on a bounded
set gives interior states more inflow than edge states. This is a property of Eq 1
as specified, not of our metric: the paper's own five RCP levels give a stationary
distribution of `[0.194, 0.222, 0.225, 0.204, 0.155]`. Under our 2-D metric the
isolated scenarios — Net Zero (0.089) and Current Policies (0.091) — get least
weight, which is the economically sensible reading.

**Result** (`out_sens_fx_drift_*.csv`, `figures/fig9`): drift erodes the prior
toward the stationary distribution, so the three priors converge — by 2045 at
λ = 0.5 they are indistinguishable, while the static mixture keeps them ~6 pp apart.
λ has no value in the paper (Table 17: *"the narrative users set the value of λ"*),
so it is swept over 5.0 / 2.0 / 0.5. Gate: λ → ∞ reproduces the static mixture
exactly.
