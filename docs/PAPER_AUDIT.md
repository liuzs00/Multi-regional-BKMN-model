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

> **RESOLVED (against the single-region reference).** The paper means the
> **level vs pre-industrial**. The reference implementation states it explicitly
> — *"Every consumer of Omega ... uses Ω(t) = 0.003467·ΔT(t)² computed from the
> temperature level vs pre-industrial"* — and validates it against the paper's
> printed rows (op-risk 3.62/3.02 against 3.6/3.0; 1-day rate −25.8 bp against
> −25). We now use the level; the earlier incremental-from-2022 reading
> understated Ω by 20.4×. See FX_REPORT §7b.

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

### C1. Cumulative short rate (Eq 15) — **resolved, now corroborated**

> Further evidence: the single-region reference *defines* `short_rate_shift`
> (the Σ policy·dt integral) in `rates.py` but **never calls it** anywhere in
> `pipeline.py`. Independent confirmation that the integral is not applied.

Eq 15 gives `Δr(t) = ∫ Δr^Policy(s) ds`. We use the Taylor output at *t* directly
as the short-rate shift. This was flagged for confirmation and is now settled on
three grounds.

**The reference implementation agrees.** The verified single-region reproduction
(commit `1760a2d`, the one that reproduces Table 4 to 0.04 pp) computes

```
dr    = markets.policy_rate_shock(infl, gdp_shock)      # phi_Pi*dPi + phi_Y*dY
rates = markets.rate_term_shift(dr, tau)                # Prop 2 applied to that dr
```

with no accumulation anywhere: the Taylor output *is* the short-rate shift fed to
Proposition 2.

**Dimensional analysis rules the literal reading out.** The paper defines
`Δr^Policy(t) = φΠ(Π(t⁺)−Π(t⁻)) + φY(Y(t⁺)−Y(t⁻))` — a difference of *levels*, so
already a rate deviation in basis points. Integrating a rate over time yields
basis-points × years, which is not a rate. The integral in Eq 15 is only
dimensionally coherent if `Δr^Policy` is read as a *rate of change* of the policy
rate, which is not what the equation above defines.

**The magnitudes confirm it.** Integrating our annual level deviations from 2022
would inflate the 2040 short-rate shift by roughly the horizon length — EU27
−132 bp → −1349 bp, India −522 bp → −5583 bp (≈ 10× in each case, i.e. −56 % on
the Indian policy rate). Those are not credible policy responses.

Conclusion: Eq 15 is best read as describing accumulation when the policy shock
arrives as a sequence of *increments*; where ΔΠ and ΔY are level deviations from
the no-climate baseline, as here and in the reference implementation, the Taylor
rule already returns the level shift and no integration is applied.

### C1b. §3.3 volatility — *we follow the paper's actual method*
An earlier draft of this audit listed the regime-switching Hull-White SDEs as
"not implemented". That was wrong: §3.3 is explicitly a sketch (*"We sketch how
to do so here"*), and the paper's own conclusion states what it did — *"In our
simplified approach, we **stressed the data by a factor of standard deviation**,
which depends on the chosen confidence level"*. That is exactly our Phase V.
Moreover the simplification is **exact**, not merely convenient: under §3.3's own
single-Brownian-motion assumption the whole chain is monotone in one shock, so
quantile-of-output = output-of-quantile-input (verified numerically across
z ∈ [−1.64, 1.64] for all 14 currencies). Simulating the SDEs would add value only
for distribution *shape* (expected shortfall) or if the single-BM assumption were
relaxed.

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
| §2.8 Prop 2 `ΔR = B(τ)/τ·Δr`, `a=0.04` | `rates.zero_rate_shift`, reported as a Table-11-style term structure (`out_ext_rate_term_structure.csv`, fig10) | 1D = short-rate shift; monotone decay; 20Y/1D = B(20)/20 = 0.688 exactly |
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


## F. Deviation register — everything we do not follow from the paper

Complete list of departures, for the dissertation's limitations section.
Reasons: **[data]** licensed/unavailable · **[scope]** out of the agreed scope ·
**[multi-R]** forced by the multi-region generalisation · **[ambiguous]** the
paper admits more than one reading · **[deferred]** planned, not yet built.

### F1. Paper features not implemented

| # | Paper | What it is | Why not | Consequence |
|---|---|---|---|---|
| 1 | §2.9 (CDS half) | CDS-spread shifts from GVA, per sector | [data] needs licensed CDS histories | credit channel absent; equity only |
| 2 | §2.10 | IFRS 9 expected credit loss, SICR | [data] hangs off CDS-implied PDs | no banking-book loss output |
| 3 | §3.1.3, Tables 7–8 | Government-sector ↔ CDS-sector mapping | [data] follows from 1 | equity is region-index level, not sector level |
| 4 | §4.2.1 | CCVA / Green KVA | [scope] | — |
| 5 | §4.2.2 | Green PD / Green RWA | [scope] | — |
| 6 | §4.2.3 | Green Return on Tangible Equity | [scope] | — |
| 7 | §3.2, Table 11 | Benchmarking against the ISDA short-term stresses | [scope] ISDA is UK/single-region | no external validation of magnitudes |
| 8 | §3.2, Table 12 | PFE(99.9 %) reporting | [deferred] machinery exists (Phase V) at 95 % | quantile level only |
| 9 | §2.1, §2.6, §2.8 | Anchoring on **observed market curves** — the paper starts from real yield/inflation curves and reports stressed *levels* | [scope] we report *shifts*, which need no curve data | cannot quote absolute stressed rates/inflation; FX is a shift, not a level |
| 10 | §2.6 (2nd eq.) | Inflation term-structure overlay `Π(t,T,T+1) = Π_market + ∫ΔΠ·f ds` | follows from 9 | annual deviation only, no forward-inflation curve |
| 11 | §3.3 | Volatility as **regime-switching Hull–White SDEs** for ΔT and ln XCE | [deferred] we stress inputs by z·σ instead (valid because the chain is monotone) | no simulated paths, no correlation structure |
| 12 | §2.6 | Carbon-pricing **scope** dynamics — Ω_XCE changing over time | implemented as a **sensitivity** (§G); headline keeps 2025 coverage | see §G |

### F2. Implemented differently

| # | Paper | Ours | Reason |
|---|---|---|---|
| 13 | SSP/RCP scenario set (5 RCP × 5 SSP = 25 paired states, some inadmissible) | 7 NGFS Phase-5 narratives, flat (no pair structure, no inadmissible combinations) | [multi-R] project brief mandates NGFS; only NGFS publishes *regional* carbon prices |
| 14 | Two independent Dirichlets (SSP ⟂ RCP) | one Dirichlet over the 7 narratives | follows from 13 |
| 15 | Prior = 90 % on SSP2/RCP4.5 (§3.1.4) | **`consensus`** prior built the same way but anchored on UNEP EGR 2025 / CAT COP30 2025 current-policy warming, plus `uniform` and two asserted bookends | method retained; anchor updated to the NGFS era (§H) |
| 16 | Eq 1 transition matrix, `d = \|j−k\|` on RCP labels | implemented as a **sensitivity**, `d` = standardised (T₂₁₀₀, XCE) distance | [multi-R] narratives have no numeric label — see §E |
| 16b | §2.7 output gap | **CORRECTED.** We fed transition + physical + tariff to the Taylor rule; the paper feeds Ω only (A.6 step 6: `dr = market + φΠ·ΔΠ − φY·Ω`; §2.7: output-gap change ≡ −Ω). A tax wedge is not an output gap — with quantities fixed it moves value to the tax authority rather than destroying it. Now physical-only; `TAYLOR_OUTPUT_GAP` in run_fx.py. |
| 17 | Eq 15 `Δr(t) = ∫Δr^Policy ds` | Taylor output at *t* used directly | [ambiguous] our ΔΠ/ΔY are already level deviations; integrating double-counts |
| 18 | §2.6 `ΔΠ ∝ ΔXCE · ΔΩ_XCE` (product of two *changes*) | `ΔΠ ∝ ΔXCE · scope` (scope as a level) | [ambiguous] the paper's literal form is second-order and reads as a typo |
| 19 | Prop 1 ΔT "relative to pre-industrial" | **Now followed exactly** — level vs pre-industrial, per the reference (§B1) | resolved |
| 20 | Prop 1 direct **and** cascading physical effect | direct only | [ambiguous] applying both double-counts |
| 21 | Prop 1 applied within one economy | applied across all 1000 region-sectors (world-level Ω) | [multi-R] our generalisation choice |
| 22 | Table 6 vulnerability, UK sectors | same sector *pattern* × ND-GAIN *region* scale | [multi-R] paper gives no cross-region vulnerability |
| 23 | Table 9 equity/CDS β (UK, FTSE) | β re-calibrated per region where free data exists (12/13); paper's β = 2.00 as proxy for JPN, CHL, KAZ | [data] |
| 24 | Table 10 op-risk β (UK/ORX) | used as-is for all 20 regions | [data] ORX is licensed |
| 25 | Okun κ = −0.182 (UK, Goto–Burgi) | UK value kept; literature-range defaults elsewhere | [data] κ is published for few countries |
| 26a | Static carbon intensities — the IO table's intensities apply at every horizon | Intensities scaled along the scenario's own emissions path, `CI_r(t) = CI_r(2022)·E_r(t)/E_r(2022)`, E from NGFS `Emissions|Kyoto Gases` | The paper applies a scenario carbon price to base-year intensities, i.e. charges for emissions the scenario says were abated — NGFS Net Zero cuts world emissions to 39.9% of 2020 by 2040. Static intensities put the Net Zero GDP shock 3–10× above NGFS's own NiGEM estimates; consistent ones land inside that range. Proportional within R5 zone, so it corrects the level not the composition of decarbonisation. `CONSISTENT_INTENSITY=False` restores the paper's treatment. |
| 26 | Table 15/16 σ by RCP | σ from the MAGICC p10/p90 fan and the NGFS cross-model spread | [multi-R] NGFS-native analogue |

### F3. Data substitutions (method unchanged)

| # | Paper | Ours |
|---|---|---|
| 27 | UK ONS input-output table, 20 SIC sectors, 2021 | OECD ICIO 2025, 20 regions × 50 ISIC industries, 2022 |
| 28 | ONS carbon intensity (Table 2) | OECD GHGFP 2025 Scope-1 ÷ ICIO gross output |
| 29 | IPCC AR6 SSP/RCP temperature | NGFS MAGICC v7.5.3 GSAT |

### F4. Followed exactly (for contrast)

Input-output core (Eqs. 2–4), the CO₂-as-tax cost-push with pass-through
(Eqs. 5–10), the damage-function form (Eq. 11), Prop 1's allocation identity,
Moessner's 0.08 %/$10, the Taylor rule with φΠ = φY = 0.5, Prop 2 with a = 0.04,
the log-linear GVA→market link (§2.9), Okun with β_Phillips = 0 (§2.11), the
Dirichlet-categorical conjugacy (§2.2), and the FX-from-yield-curve-differences
route (§4.3).


## G. Carbon-pricing scope: static vs dynamic (sensitivity)

§2.6 drives inflation with Δ**Ω**_XCE — a *change* in the fraction of emissions
priced — and notes that *"increases in scope of carbon pricing may have similar
effects and is included here"*. Our headline holds Ω at its observed **2025**
value for all horizons, which produces a visible artefact: India and Turkey price
nothing today, so with frozen coverage they contribute **zero** carbon inflation
even while paying $338/t in the transition channel under Net Zero. Their spot FX
then becomes purely the negative of EU27's inflation — identical to four decimals
(−2.2726 % each at 2040), regardless of how different the two economies are.

**Sensitivity** (`macro.scope_at`, `out_sens_fx_*_dynscope.csv`): coverage expands
with the scenario's own carbon price,

    Ω(t) = Ω₂₀₂₅ + (1 − Ω₂₀₂₅)·min(1, XCE(t)/XCE_full),   XCE_full = $100/t

The carbon price *is* the scenario's policy-stringency signal, so this is the
least assumption-heavy link available; `XCE_full` is the single asserted
parameter. Current Policies (~$3/t) leaves coverage essentially unchanged; Net
Zero (>$300/t by 2030) takes it to full.

**Effect** (spot FX vs EUR, 2040, Net Zero): the artefact resolves — IND and TUR
separate (−0.274 % vs −0.263 %) — and **all** spot moves collapse toward zero
(USA −1.95 % → −0.10 %, IND −2.27 % → −0.27 %). That is economically coherent: if
every region ends up with near-full coverage of the same carbon price, carbon
inflation is common and the PPP differential vanishes. It also shows the headline
spot channel is largely driven by **today's coverage disparities persisting for
two decades** — a strong assumption worth stating.

Note this does not touch the forward/CIP channel's driver (ΔY), which is where
most of the FX signal lives.


## H. The scenario prior: provenance

*Full method write-up (priors, transition matrix, worked transition probabilities):*
[`docs/MIXTURE_METHOD.md`](MIXTURE_METHOD.md).

`uniform` is the conventional uninformative prior. **`policy-sceptic` and
`ambition` are asserted bookends** — the directions are narrative logic, the
magnitudes arbitrary. There is no standard to borrow: NGFS deliberately publishes
no scenario probabilities.

**`consensus` is the citable one**, built by the paper's own method. §3.1.4 takes
an authoritative statement about where current policies lead (IPCC 2023: "a path
closer to SSP2 combined with RCP4.5 or RCP6.0") and puts 90 % on that pair. The
NGFS-era equivalents are the published current-policy warming estimates:

| Source | Current policies | NDCs | Optimistic |
|---|--:|--:|--:|
| UNEP Emissions Gap Report 2025 | **2.8 °C** | 2.3–2.5 °C | — |
| Climate Action Tracker, COP30 update (Nov 2025) | **~2.6 °C** | 2.6 °C | 1.6 °C |

Anchor μ = **2.7 °C** (midpoint), sd = **0.3 °C** (spread across the two
assessments). Weights are Gaussian in each scenario's own end-century warming,
`α_s ∝ exp(−½((T₂₁₀₀,s − μ)/sd)²)`, normalised to Σα = 14:

| scenario | T₂₁₀₀ | weight |
|---|--:|--:|
| Current Policies | 2.75 | **80.7 %** |
| Fragmented World | 2.11 | 11.8 % |
| NDCs | 2.03 | 6.7 % |
| Delayed transition | 1.75 | 0.5 % |
| Below 2 °C | 1.69 | 0.3 % |
| Low demand / Net Zero 2050 | 1.47 / 1.45 | ~0 % |

Current Policies lands within 0.05 K of the anchor, so the fit is tight. Like the
paper's 90 %, the result is concentrated — and that concentration is itself the
finding: **on the published trajectory the carbon price stays near zero, so
expected transition-FX moves collapse** (IND −6.20 % under `uniform` → **−0.54 %**
under `consensus` at 2040). Transition FX risk therefore lives in the *tail*, not
the expectation — which is an argument for reading the volatility band (§ Phase V)
and the ambitious scenarios as stress cases rather than central forecasts.

⚠️ One caveat on the mapping: NGFS's own "NDCs" scenario reaches 2.03 °C, while
UNEP and CAT put full NDC implementation at 2.3–2.6 °C. The NGFS NDC narrative is
therefore *more optimistic* than the external assessments, which is part of why
weight shifts onto Current Policies.


## I. CBAM as a carbon tariff (project stretch goal)

*Full method and results write-up:* [`docs/TARIFF_METHOD.md`](TARIFF_METHOD.md).

The brief's second objective is *"alternative shocks to CO2 prices, e.g. tariffs,
or changes in trade flows between regions"*. CBAM is the one carbon tariff that
exists, and it required **no new data**: the MRIO supplies bilateral trade by
sector, `CARBON_INTENSITY_20R` the embodied carbon by origin, and
`region_carbon_map.applied_price_usd` the price each origin already pays.

**Mechanism.** On covered imports the EU levies the price differential applied to
embodied carbon,

    tau(r,i) = max(0, XCE_EU − XCE_r) · CI(r,i) · 1e-6      [fraction of value]

which is dimensionless — the same units as the model's own `ct` — so it enters
the identical modified Leontief dual. Statutorily the EU importer pays, raising
EU costs in proportion to covered imports used; an incidence parameter θ shifts
the burden to the exporter (θ = 0) to bracket the elastic-demand case the model
cannot represent. Coverage follows CBAM Annex I mapped to ICIO: C23 cement,
C24A steel, C24B aluminium, D electricity, and 15 % of C20 for fertilisers and
hydrogen [ESTIMATE].

**Three findings.**

1. **Sector rates are enormous.** Kazakh electricity carries a **149 %**
   ad-valorem charge — its embodied carbon is worth more at \$80/t than the
   electricity itself. Indian electricity 73 %, Indonesian 59 %, Indonesian steel
   and aluminium 43 %.
2. **The macro effect is negligible.** Revenue is ~**\$9.4 bn/yr** (of which
   \$8.4 bn on intermediate imports and \$0.9 bn on imports going straight to final
   demand) and the EU GVA effect is **−0.010 %**. Covered sectors are a small share
   of EU imports, so a policy with extreme sectoral rates barely registers in
   aggregate — the coverage, not the rate, is binding.
3. **CBAM only exists where prices diverge.** Repricing at NGFS Net-Zero levels,
   where the scenario assumes near-uniform global carbon pricing, cuts revenue to
   **\$1.4 bn** — an 83 % fall. The instrument is a response to policy
   fragmentation and largely self-extinguishes under coordination.

**Incidence.** Under statutory incidence the EU bears −0.010 % and exporters
almost nothing; with full exporter absorption the burden inverts — Turkey
−0.020 %, Russia −0.019 %, Kazakhstan −0.013 %, EU27 only −0.001 %. Which holds
depends on elasticities the inelastic-demand assumption excludes, so both are
reported.

**Limitation.** With final demand fixed there is no trade diversion, which is
often a tariff's principal effect. What is measured is the cost-push incidence of
the charge, not the reallocation of trade away from carbon-intensive origins.

**Generalisation.** CBAM is now a special case of `bkmn/tariff.py`, which takes an
arbitrary schedule `TAU[k, d]` — an ad-valorem rate on good *k* entering region
*d* — and returns per-unit-output charges in the same units as `ct`. Any bilateral
or universal tariff is therefore a scenario, not a data problem: a shock is fully
specified by its *increment*, so no baseline tariff database is required. Two
illustrations at φ = 0.5:

| Scenario | Revenue | Importer pays (θ=1) | Exporter absorbs (θ=0) |
|---|--:|---|---|
| USA levies 25 % on Chinese manufactures | \$113 bn/yr | USA −0.017 % | CHN −0.051 % |
| Every region levies 10 % on all imports | \$2,252 bn/yr | CHN −0.387 %, EU27 −0.343 %, USA −0.124 % | — |

The universal case shows the openness ordering directly: the more a region relies
on imported inputs, the larger its cost-push loss. It also shows the framework's
limit — with final demand fixed nobody re-sources, so these are pure cost effects
and understate what a tariff does in practice.

### I.1 Tariffs carried through to FX

A tariff is the same object as the carbon charge — an ad-valorem cost wedge in the
same units — so it is **added to `ct` inside the main chain** and inherits the
entire downstream: Taylor, Hull-White, FX, equity and operational risk. (It was
initially computed as a side calculation that stopped at GVA, which meant the
tariff work produced no exchange-rate result — the project's actual deliverable.)

The one piece a tariff cannot inherit is the inflation route. §2.6's Moessner
relation is estimated on *carbon prices* and takes ΔXCE as its input, so it has
nothing to consume from a tariff. The tariff price effect is instead derived from
the model's own dual (`tariff.price_effect`): tariffed intermediate imports raise
producer prices through `L̃(φ)`, weighted to a consumer index by each region's
final-demand basket, plus the direct charge on tariffed final-demand imports.
That is arguably the cleaner route and leaves §2.6 untouched for carbon. A
permanent tariff is a price **level** shift, so it enters the cumulative term
(and hence spot/PPP FX) but not the inflation *rate* at later horizons — central
banks look through one-off level jumps.

Results are reported as the **increment** over the same scenario without the
tariff, so the carbon baseline cancels. At 2040, φ = 0.5, statutory incidence:

| Shock | Revenue | Headline FX effect |
|---|--:|---|
| CBAM (EU, applied prices) | \$9.4 bn/yr | all currencies within ±0.02 % |
| USA 25 % on Chinese manufactures | \$113 bn/yr | **USD +0.33 % vs EUR** (weakens) |
| Global 10 % on all imports | \$2,252 bn/yr | SGP +3.04 %, NOR +1.12 % … CHN −0.58 % |

Two findings.

**A tariff weakens the currency that levies it.** The US tariff raises US consumer
prices, and under relative PPP that depreciates the dollar 0.33 % against the
euro. The intuition that protection strengthens a currency does not survive in a
price-level channel.

**The cross-section is import dependence.** Under the universal tariff the spot
response correlates **0.926** with each region's imported share of intermediate
inputs: Singapore (50.8 % imported) depreciates 3.04 %, while China (7.7 %) and
the United States (8.2 %) *appreciate* because their price levels rise least. The
FX effect of a global trade war is, to a first approximation, a ranking of who
depends on imports.

Outputs: `out_sens_tariff_fx.csv`, `out_sens_tariff_gva.csv`,
`out_sens_cbam_gva.csv`, `out_sens_cbam_rates.csv`, `figures/fig11`.
